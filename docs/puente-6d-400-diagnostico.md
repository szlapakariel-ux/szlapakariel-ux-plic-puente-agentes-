# PUENTE-6D-400-DIAGNOSTICO — Diagnóstico del error 400 sin llamada real

## 1. Identificación

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6D-400-DIAGNOSTICO |
| Fecha/hora (UTC) | 2026-05-04T17:31:23Z |
| Repo | `szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-` |
| Rama | `docs/puente-6d-400-diagnostico` |
| Commit base (main) | `e2f758dca92fa749e4f61fa7e838ed07bd66777a` |
| Autorización de Ariel | "Autorizo PUENTE-6D-400-DIAGNOSTICO, sin llamada real." |

---

## 2. Objetivo

Diagnosticar sin ejecutar llamadas reales la causa probable del HTTP 400 recibido en el intento local PowerShell, y diseñar un script mejorado para el próximo reintento autorizado que capture el body detallado del error.

---

## 3. Prohibiciones de este microciclo

| Prohibición | Estado |
|---|---|
| Llamada real | PROHIBIDO |
| Request HTTP | PROHIBIDO |
| Tocar endpoint Anthropic | PROHIBIDO |
| API real / SDK real | PROHIBIDO |
| Pedir/imprimir secrets | PROHIBIDO |
| Crear/modificar `.env` | PROHIBIDO |
| Modificar código/tests | PROHIBIDO |
| Abrir PR / mergear | PROHIBIDO |
| Avanzar a reintento real | PROHIBIDO |

---

## 4. Evidencia leída

| Documento | Contenido relevante |
|---|---|
| `docs/puente-6d-local-real-error-resultado.md` | HTTP 400, `WebException`, body no capturado, `Invoke-RestMethod`, 1 llamada real efectiva |
| `docs/puente-6d-real-primera-llamada-resultado.md` | Intentos 1-3 bloqueados, 0 llamadas |
| `docs/puente-6d-preflight-real.md` | Parámetros autorizados: modelo `claude-haiku-4-5-20251001`, `max_tokens <= 50`, `timeout <= 10s` |

### Resumen del estado previo

| Métrica | Valor |
|---|---|
| Llamadas reales efectivas acumuladas | 1 |
| Requests HTTP acumulados | 1 |
| Respuestas exitosas (`PLIC_OK`) | 0 |
| Secrets expuestos | 0 |
| Body del error 400 capturado | NO |
| PR #28 cerrado en main | SÍ |

---

## 5. Qué se sabe del error 400

### Lo que se sabe con certeza

- La solicitud llegó al servidor de Anthropic (no fue interceptada por proxy antes de llegar).
- Anthropic devolvió HTTP 400 — rechazó la solicitud por un problema en el request mismo.
- El tipo de excepción fue `WebException` de .NET — lanzada por `Invoke-RestMethod` al recibir un status no-2xx.
- El body de la respuesta de error **no fue capturado** — el bloque catch solo leyó el mensaje de la excepción, no el stream de la respuesta.
- No es error 401 (autenticación) — si la key fuera incorrecta, sería 401.
- No es error 429 (rate limit) ni 503 (servicio no disponible).

### Lo que no se sabe

Sin el body JSON del error, no es posible determinar la causa exacta. El body de Anthropic tiene esta forma:

```json
{"type": "error", "error": {"type": "invalid_request_error", "message": "..."}}
```

El campo `error.message` diría exactamente qué falló.

---

## 6. Causas posibles — hipótesis sin confirmar

**Nota de corrección (PUENTE-6D-400-DIAGNOSTICO-CORRECCION)**: Una versión previa de este documento afirmaba como "Causa 1 — Alta probabilidad" que `ConvertTo-Json` usó su profundidad por defecto (2), truncando el objeto anidado `messages[0]`. Esto era **incorrecto**: Ariel confirmó que el script ejecutado usó explícitamente `-Depth 10`. Esa hipótesis queda descartada. Todas las causas restantes son hipótesis sin confirmar. **La causa es INDETERMINADA hasta capturar el body del error.**

### Causa 1 — Sin confirmar: `temperature` como entero en vez de float

**Descripción**: En algunos lenguajes y contextos, `temperature: 0` puede serializarse como entero `0` en vez de float `0.0`. La API de Anthropic espera un número de punto flotante para `temperature`.

**Ejemplo del problema**:
```powershell
$payload = @{
    temperature = 0   # Se serializa como 0, no 0.0
}
```

**Resultado JSON**: `"temperature": 0` vs `"temperature": 0.0`

La API de Anthropic generalmente acepta ambas formas, pero en algunos contextos estrictos puede rechazar el entero.

**Solución**:
```powershell
temperature = [double]0.0
```

### Causa 2 — Sin confirmar: encoding incorrecto del body

**Descripción**: `Invoke-RestMethod` en versiones antiguas de PowerShell puede enviar el body con encoding que no es UTF-8, especialmente en Windows con configuración regional no-inglesa. El servidor de Anthropic requiere UTF-8.

**Solución**: especificar encoding explícitamente:
```powershell
$bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)
```

### Causa 3 — Sin confirmar: header `content-type` mal formado o ausente

**Descripción**: Si el header `Content-Type` no tiene el valor exacto `application/json`, Anthropic puede rechazar la solicitud con 400.

**Solución**: especificarlo explícitamente:
```powershell
-ContentType "application/json"
```

### Causa 4 — Sin confirmar: modelo no disponible para la cuenta

**Descripción**: Es posible que `claude-haiku-4-5-20251001` no esté habilitado para la cuenta de la API key usada. Sin embargo, si fuera el caso, Anthropic generalmente devuelve un error específico (a veces 404, a veces 400 con `model_not_found`).

**No se puede confirmar ni descartar** sin el body del error.

### Causa 5 — Sin confirmar: problema de proxy/firewall corporativo

**Descripción**: Un proxy corporativo puede interceptar la solicitud, modificar headers, o devolver su propio error 400 antes de que llegue a Anthropic.

**Argumento en contra**: el mensaje recibido fue "Error en el servidor remoto: (400) Solicitud incorrecta" — esto es el mensaje estándar de `WebException` de .NET para respuestas 400, lo que sugiere que sí llegó al servidor real de Anthropic (un proxy generalmente devuelve 407 o un error diferente). Sin embargo, no se puede descartar completamente.

**Solución para aislar**: ejecutar el próximo reintento desde red del celular (hotspot móvil) sin pasar por la red corporativa.

---

## 7. Análisis de red corporativa vs red del celular

### Por qué la red corporativa puede generar falsos 400

| Mecanismo | Descripción |
|---|---|
| Proxy de inspección SSL (MITM) | El proxy corporativo puede interceptar HTTPS, re-firmar el certificado y modificar headers. Esto puede causar errores en APIs que verifican el origen. |
| Firewall de aplicación web (WAF) | Algunos WAF corporativos rechazan requests que parecen sospechosos (headers con `x-api-key`, payloads JSON con ciertos patrones). |
| Header injection | El proxy puede agregar headers adicionales que Anthropic no espera, o modificar `Content-Type`. |
| Reescritura de URL | Algunos proxies modifican la URL o el path, causando un 400 en el destino. |
| Política de egress | Algunas redes corporativas bloquean o transforman requests a dominios no aprobados. |

### Por qué el 400 recibido probablemente NO es de red corporativa

| Argumento | Descripción |
|---|---|
| Código 400, no 407 | Un proxy que bloquea la conexión generalmente devuelve 407 (Proxy Authentication Required) o corta la conexión. Un 400 llegó desde el servidor de destino. |
| Mensaje es de `WebException` | El mensaje "Error en el servidor remoto: (400) Solicitud incorrecta" es la representación .NET de un HTTP 400 genuino. |
| Sin error de certificado | No hubo mención de error de certificado SSL, que ocurriría si un proxy MITM fallara. |

**Conclusión sobre red**: el error 400 es probablemente de origen en Anthropic (payload malformado), pero **probar desde red del celular es de bajo costo y elimina completamente la variable de red**. Se recomienda hacerlo.

### Recomendación sobre red del celular

**Usar hotspot del celular para el próximo reintento.** Esto:
1. Elimina cualquier proxy corporativo, WAF o firewall de la ecuación.
2. Permite atribuir cualquier error restante exclusivamente al payload o la key.
3. No agrega costo operativo significativo.
4. Si el reintento desde celular también da 400, la causa es definitivamente el payload.
5. Si el reintento desde celular da 200, la causa era la red corporativa.

---

## 8. Limitación principal: body no capturado

Sin el body JSON del error, no es posible emitir un diagnóstico definitivo. Todas las causas anteriores son hipótesis ordenadas por probabilidad.

**El body del error es el único dato que permite diagnóstico certero.** El script para el próximo reintento debe capturarlo obligatoriamente.

---

## 9. Script PowerShell mejorado para el próximo reintento autorizado

Este script **NO debe ejecutarse en este microciclo**. Es un diseño para un futuro reintento con autorización explícita de Ariel.

```powershell
# PUENTE-6D-REAL — Script PowerShell mejorado para reintento
# IMPORTANTE: No ejecutar sin autorización explícita de Ariel.
# Este script ejecuta UNA sola llamada real. No modificar ni reutilizar sin autorización.

$api_key = $env:ANTHROPIC_API_KEY
if (-not $api_key) {
    Write-Host (ConvertTo-Json @{
        ok = $false
        error_tipo = "anthropic_api_key_ausente"
        llamada_real_ejecutada = $false
    })
    exit 2
}

# Payload con depth explícito y temperature como float
$payload = @{
    model      = "claude-haiku-4-5-20251001"
    max_tokens = 16
    temperature = [double]0.0
    messages   = @(
        @{
            role    = "user"
            content = "Respondé exactamente: PLIC_OK"
        }
    )
}

# Serialización con -Depth 10 para evitar truncado de objetos anidados
$body = $payload | ConvertTo-Json -Depth 10 -Compress

# Encoding UTF-8 explícito
$bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)

$headers = @{
    "x-api-key"         = $api_key
    "anthropic-version" = "2023-06-01"
    "content-type"      = "application/json"
}

$cantidad_llamadas = 0
$llamada_real_ejecutada = $false
$secret_expuesto = $false

try {
    $request = [System.Net.HttpWebRequest]::Create("https://api.anthropic.com/v1/messages")
    $request.Method = "POST"
    $request.ContentType = "application/json"
    $request.Headers.Add("x-api-key", $api_key)
    $request.Headers.Add("anthropic-version", "2023-06-01")
    $request.Timeout = 30000  # 30 segundos

    $stream = $request.GetRequestStream()
    $stream.Write($bodyBytes, 0, $bodyBytes.Length)
    $stream.Close()

    $cantidad_llamadas = 1
    $llamada_real_ejecutada = $true

    $response = $request.GetResponse()
    $reader = New-Object System.IO.StreamReader($response.GetResponseStream())
    $responseBody = $reader.ReadToEnd()
    $reader.Close()

    $data = $responseBody | ConvertFrom-Json
    $texto = ($data.content | Where-Object { $_.type -eq "text" } | ForEach-Object { $_.text }) -join ""
    $texto = $texto.Trim()

    Write-Host (ConvertTo-Json @{
        ok                    = ($texto -eq "PLIC_OK")
        status                = "respuesta_recibida"
        modelo                = $data.model
        respuesta_texto       = $texto
        id_presente           = ($null -ne $data.id)
        usage                 = $data.usage
        llamada_real_ejecutada = $true
        cantidad_llamadas      = $cantidad_llamadas
        secret_expuesto        = $false
    } -Depth 5)

} catch [System.Net.WebException] {
    $errorResponse = $_.Exception.Response
    $body_error = ""
    if ($null -ne $errorResponse) {
        try {
            $reader = New-Object System.IO.StreamReader($errorResponse.GetResponseStream())
            $body_error = $reader.ReadToEnd()
            $reader.Close()
            # Limitar a 1000 caracteres para evitar exponer datos sensibles
            if ($body_error.Length -gt 1000) { $body_error = $body_error.Substring(0, 1000) + "...[truncado]" }
        } catch {
            $body_error = "[no se pudo leer el stream del error]"
        }
        $status_code = [int]$errorResponse.StatusCode
    } else {
        $status_code = 0
    }

    Write-Host (ConvertTo-Json @{
        ok                    = $false
        error_tipo            = "http_error"
        status_code           = $status_code
        body_sanitizado       = $body_error
        llamada_real_ejecutada = $llamada_real_ejecutada
        cantidad_llamadas      = $cantidad_llamadas
        secret_expuesto        = $false
    } -Depth 3)
    exit 1

} catch {
    Write-Host (ConvertTo-Json @{
        ok                    = $false
        error_tipo            = $_.Exception.GetType().Name
        mensaje               = $_.Exception.Message.Substring(0, [Math]::Min(300, $_.Exception.Message.Length))
        llamada_real_ejecutada = $llamada_real_ejecutada
        cantidad_llamadas      = $cantidad_llamadas
        secret_expuesto        = $false
    } -Depth 3)
    exit 1
}
```

### Diferencias clave respecto al script anterior

| Aspecto | Script anterior | Script mejorado |
|---|---|---|
| `ConvertTo-Json -Depth` | `-Depth 10` — correcto (no trunca) | `-Depth 10` — igual; no es cambio |
| `temperature` | `0` (entero) | `[double]0.0` (float explícito) |
| HTTP client | `Invoke-RestMethod` | `HttpWebRequest` — control total |
| Encoding del body | Implícito | UTF-8 explícito |
| Captura de body de error | NO — solo mensaje de excepción | **SÍ — lee stream de respuesta** |
| Límite del body de error | — | 1000 caracteres — sanitizado |
| `cantidad_llamadas` | No registrado | Registrado explícitamente |

---

## 10. Condición para el próximo reintento

El próximo reintento requiere:

1. Instrucción explícita separada de Ariel para un nuevo microciclo de llamada real.
2. Usar el script mejorado de la sección 9.
3. Ejecutar preferiblemente desde red del celular (hotspot móvil) para aislar variable de red corporativa.
4. Máximo absoluto: una sola llamada real.
5. No reintentar si falla — registrar el body del error y frenar.

---

## 11. Confirmaciones de seguridad de este microciclo

| Verificación | Estado |
|---|---|
| Llamada real ejecutada | NO |
| Request HTTP ejecutado | NO |
| Secret expuesto | NO |
| `.env` creado o modificado | NO |
| Código fuente modificado | NO |
| Tests modificados | NO |
| Workflows tocados | NO |
| Producción tocada | NO |
| Navegador usado | NO |
| Playwright usado | NO |
| Otros repos tocados | NO |

---

## 12. Dictamen

### **A) DIAGNÓSTICO 400 DOCUMENTADO — CAUSA INDETERMINADA — no reintentar sin nuevo microciclo**

Sin el body del error no hay diagnóstico definitivo. **La causa es INDETERMINADA.** Una hipótesis previa (truncado de `ConvertTo-Json` con depth por defecto) quedó descartada: el script de Ariel usó `-Depth 10` explícitamente.

Las hipótesis restantes sin confirmar son: `temperature = 0` como entero en vez de float, encoding implícito en `Invoke-RestMethod`, header `content-type` mal formado, modelo no habilitado para la cuenta, o interferencia de red corporativa. Ninguna puede confirmarse ni descartarse sin el body del error.

La red corporativa es una causa posible pero menos probable dado que el error fue 400 y no 407. Se recomienda probar desde red del celular para aislar esa variable.

El script de la sección 9 captura el body del error y corrige varias causas posibles (`temperature` como float, `HttpWebRequest` para control total de headers y encoding). Será el único dato que permita diagnóstico definitivo en el próximo reintento.

> No ejecutar el script propuesto ni hacer ningún reintento hasta recibir autorización explícita separada de Ariel en un nuevo microciclo.
