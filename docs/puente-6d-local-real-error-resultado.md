# PUENTE-6D-LOCAL-REAL — Primera llamada real efectiva — Error 400

## 1. Identificación

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6D-LOCAL-REAL-ERROR-DOC |
| Fecha/hora (UTC) | 2026-05-04T15:50:50Z |
| Repo | `szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-` |
| Rama | `feat/puente-6d-real-primera-llamada` |
| Commit base (main) | `544fce3a8e21655286185557f1513f479f5c168c` |
| Ejecutor de la llamada | Ariel — desde PowerShell local |
| Autorización previa | "Autorizo PUENTE-6D-LOCAL-REAL desde PowerShell local, una sola llamada real, sin exponer secrets." |

---

## 2. Historial de intentos acumulado

| Intento | Commit | Ejecutor | Causa | Llamadas HTTP | Secrets |
|---|---|---|---|---|---|
| 1 | `90e74a0` | Claude Code remoto | `anthropic_api_key_ausente` | 0 | 0 |
| 2 | `2d84988` | Claude Code remoto | `anthropic_api_key_ausente` | 0 | 0 |
| 3 | `dcfb2b2` | Claude Code remoto | `anthropic_api_key_ausente` | 0 | 0 |
| **4 (este)** | — | **Ariel, PowerShell local** | **Error 400 Bad Request** | **1** | 0 |

**Acumulado tras este intento: 1 llamada real efectiva, 1 request HTTP, 0 secrets expuestos.**

---

## 3. Primera llamada real efectivamente ejecutada

Este es el primer intento en el que la llamada llegó a la API de Anthropic y recibió una respuesta.

| Campo | Valor |
|---|---|
| Endpoint | `https://api.anthropic.com/v1/messages` |
| Método | POST |
| Modelo solicitado | `claude-haiku-4-5-20251001` |
| Ejecutado desde | PowerShell local de Ariel |
| Llamada real ejecutada | **SÍ — primera vez** |
| Cantidad de llamadas en este intento | **1** |
| Respuesta recibida | **Sí — HTTP 400 Bad Request** |

---

## 4. Resultado de la llamada

| Campo | Valor reportado por Ariel |
|---|---|
| `ok` | `false` |
| `error_tipo` | `WebException` |
| `mensaje_sanitizado` | `"Error en el servidor remoto: (400) Solicitud incorrecta."` |
| `llamada_real_ejecutada` | `true` |
| `cantidad_llamadas_reales` | `1` |
| `secret_expuesto` | `false` |
| `env_modificado` | `false` |
| `repo_tocado` | `false` |
| Body detallado del error | **No capturado** |

### Interpretación del error 400

HTTP 400 Bad Request indica que el servidor de Anthropic recibió la solicitud pero la rechazó por un problema en el formato o contenido del payload. No es un error de autenticación (eso sería 401) ni de modelo no disponible (eso sería 404 o un error específico en el body). Las causas posibles de un 400 en la API de Anthropic son:

| Causa posible | Descripción |
|---|---|
| Formato de payload incorrecto | El JSON enviado no cumple el schema esperado |
| Campo requerido ausente o mal tipado | Por ejemplo `messages` mal formado o `max_tokens` fuera de rango |
| Versión de API incorrecta | Header `anthropic-version` con valor no soportado |
| Encoding incorrecto | El body no fue enviado como UTF-8 o no fue serializado correctamente en PowerShell |
| `temperature: 0` como integer vs float | Algunos endpoints requieren `0.0` |
| Nombre de parámetro incorrecto | Por ejemplo `content` en vez de `messages` |

Sin el body detallado del error 400, no es posible determinar la causa exacta.

---

## 5. Información no capturada — limitación del script PowerShell

El script de PowerShell capturó el mensaje de excepción de .NET (`WebException`) pero no leyó el body de la respuesta HTTP 400. La API de Anthropic devuelve un JSON en el body del error con el campo `error.type` y `error.message` que indica exactamente qué falló.

Para el próximo reintento autorizado, el script debe capturar el body de la respuesta en el bloque `catch`:

```powershell
# Ejemplo de captura correcta del body en PowerShell
catch [System.Net.WebException] {
    $errorResponse = $_.Exception.Response
    $reader = New-Object System.IO.StreamReader($errorResponse.GetResponseStream())
    $body = $reader.ReadToEnd()
    Write-Host "Body del error:", $body
}
```

Esto permitiría ver el JSON de error completo de Anthropic, por ejemplo:
```json
{"type": "error", "error": {"type": "invalid_request_error", "message": "..."}}
```

---

## 6. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Secret expuesto | NO — `ANTHROPIC_API_KEY` no impresa ni logueada |
| `.env` creado o modificado | NO |
| `.env` existente en repo | NO |
| Código fuente modificado | NO |
| Tests modificados | NO |
| Workflows tocados | NO |
| Producción tocada | NO |
| Navegador usado | NO |
| Playwright usado | NO |
| Otros repos tocados | NO |
| Repo tocado durante la llamada local | NO — la llamada fue directa desde PowerShell |
| Más de 1 llamada real en este intento | NO — exactamente 1 |

---

## 7. Estado del acumulado

| Métrica | Antes de este intento | Después de este intento |
|---|---|---|
| Llamadas reales efectivas | 0 | **1** |
| Requests HTTP a Anthropic | 0 | **1** |
| Respuestas recibidas | 0 | **1 (HTTP 400)** |
| Respuestas exitosas (`PLIC_OK`) | 0 | 0 |
| Secrets expuestos | 0 | 0 |

---

## 8. Reintento

**No se autoriza reintento automático en este microciclo.** Cualquier nuevo intento requiere:

1. Diagnóstico del error 400 — determinar la causa exacta (preferiblemente con body del error).
2. Diseño de script corregido si el payload tenía un problema.
3. Autorización explícita separada de Ariel para el nuevo intento.

---

## 9. Dictamen

### **C) LLAMADA REAL EJECUTADA CON ERROR 400 — no reintentar sin nuevo microciclo**

Primera llamada real efectivamente ejecutada — desde PowerShell local de Ariel. La API de Anthropic recibió la solicitud y devolvió HTTP 400 Bad Request. El body del error no fue capturado. Sin secrets expuestos. Sin modificación de código, tests, repo ni `.env`.

El próximo microciclo recomendado es **diagnóstico del error 400**: reproducir el payload en modo dry-run para verificar su estructura, y si corresponde, diseñar un script mejorado que capture el body de error antes del próximo reintento autorizado.

> No ejecutar nuevo reintento hasta recibir instrucción explícita separada de Ariel después del diagnóstico.
