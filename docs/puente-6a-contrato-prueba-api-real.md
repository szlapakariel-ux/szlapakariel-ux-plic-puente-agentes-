# PUENTE-6A — Contrato para prueba mínima de API real

## 1. Nombre del contrato

| Campo | Valor |
|---|---|
| Contrato | PUENTE-6A |
| Tipo | Documental — sin ejecución real |
| Fecha | 2026-05-04 |
| Rama base | `main` |
| Commit base | `da1af486250fc8d38909f1b47cc203510a43fddf` |
| Fase previa cerrada | PUENTE-5Z — Cliente Haiku fake/local |
| Tests al abrir | 262/262 OK |

**Este contrato no ejecuta ninguna llamada real.** No usa API real, no usa SDK real, no usa keys reales, no modifica código, no modifica tests.

---

## 2. Objetivo de PUENTE-6A

Definir de forma verificable y sin ejecutar ninguna acción real:

- Qué es una primera prueba mínima con API real.
- Qué entraría, qué saldría y qué se espera verificar.
- Cómo se manejaría la API key de forma segura.
- Qué condiciones deben cumplirse antes de intentar cualquier llamada real.
- Qué reglas de corte se aplicarían si algo sale mal.
- Qué riesgos existen y cómo mitigarlos.

PUENTE-6A no autoriza ninguna llamada real. Solo define el piso documental para que PUENTE-6B (preparación del cliente) sea responsable.

---

## 3. Diferencias entre tipos de cliente y ejecución

| Tipo | Descripción | Llama API | Usa key | Código existente | Determinista |
|---|---|---|---|---|---|
| **Cliente fake/local** | `cliente_haiku_fake.py` — función pura, 0 imports, reglas locales | NO | NO | SÍ | SÍ — siempre |
| **Cliente API real (SDK)** | Función que usa `anthropic` SDK para llamar a `api.anthropic.com` | SÍ | SÍ | NO — no existe aún | NO — varía por modelo |
| **Cliente API real (HTTP directo)** | Función que usa `requests` o `httpx` para llamar directamente al endpoint | SÍ | SÍ | NO — no existe aún | NO |
| **SDK real** | Librería `anthropic` de Python instalada como dependencia | SÍ | SÍ | NO — no instalado | NO aplica |
| **Llamada real** | Invocación efectiva de `POST /v1/messages` con key válida | SÍ | SÍ | NO | NO |
| **Ejecución real** | Mano Local Simulada + instrucción ejecutada en sistema operativo real | SÍ + acciones | SÍ | NO — no existe aún | NO |
| **Producción** | Cualquier sistema con usuarios reales, datos reales o consecuencias irreversibles | SÍ | SÍ | NO aplica | NO aplica |

### Qué tiene el cliente fake que el real no puede garantizar

| Propiedad | Cliente fake | Cliente API real |
|---|---|---|
| Output idéntico en cada llamada | SÍ | NO — el modelo varía |
| Costo cero | SÍ | NO — cada token tiene costo |
| Sin latencia de red | SÍ | NO — depende de conectividad |
| Sin credenciales | SÍ | NO — requiere key válida |
| Tests deterministas sin mocks | SÍ | NO — requiere fixtures o mocks de red |
| Función pura sin efectos | SÍ | NO — tiene I/O y red |

---

## 4. Qué se busca probar en el futuro (PUENTE-6B en adelante)

### 4.1 Conectividad mínima

Verificar que desde el entorno local se puede establecer una conexión TCP con `api.anthropic.com:443` y recibir una respuesta HTTP válida (200 o error estructurado de la API) sin timeout.

### 4.2 Formato de request

Verificar que un payload mínimo de `POST /v1/messages` con `model`, `max_tokens`, `messages` y `system` es aceptado por la API sin error de validación de schema.

Payload mínimo de referencia (sin valor de key):
```
{
  "model": "claude-haiku-4-5-20251001",
  "max_tokens": 64,
  "system": "Sos un clasificador de instrucciones del sistema PLIC. Respondé solo con JSON válido.",
  "messages": [{"role": "user", "content": "Clasificá esta instrucción: revisar el documento."}]
}
```

### 4.3 Formato de response

Verificar que la respuesta contiene al menos:
- `id` (string)
- `type` == `"message"`
- `role` == `"assistant"`
- `content` (lista con al menos un elemento de tipo `"text"`)
- `model` (string que contiene "haiku" o el modelo solicitado)
- `stop_reason` (string)
- `usage.input_tokens` (int)
- `usage.output_tokens` (int)

### 4.4 Manejo de errores

Verificar que ante un error de auth (key inválida o ausente) la API devuelve un error estructurado con `type: "error"` y `error.type: "authentication_error"`, sin filtrar la key en la respuesta.

### 4.5 Fallback al fake

Verificar que si la llamada real falla por cualquier motivo (error de auth, timeout, rate limit, red no disponible), el sistema puede continuar usando `cliente_haiku_fake` sin modificar el código base.

### 4.6 Logs seguros

Verificar que ningún log de la prueba contiene el valor de la API key, headers de autorización ni datos sensibles del entorno.

---

## 5. Qué NO se prueba todavía

| Ítem | Razón |
|---|---|
| Producción | Prohibición absoluta — requiere ciclo dedicado con alcance y rollback definidos |
| Navegador real | Requiere ciclo específico — PLIC no tiene UI por ahora |
| Playwright real | Requiere ciclo específico — no hay interfaz de usuario a automatizar |
| Workflows de CI/CD | Prohibición absoluta — ninguna key debe existir en pipelines automáticos |
| Automatización externa (bots, webhooks, triggers) | Requiere diseño previo y prueba controlada |
| Acciones sobre GitHub (push, PR, merge por Haiku) | Prohibición absoluta — ninguna acción real delegada a modelo |
| Ejecución real por Mano Local | Requiere PUENTE-6C mínimo — fuera del alcance de 6A/6B |
| Integración Cerebro Mock + Haiku real | Requiere diseño de orquestación — fuera del alcance actual |
| Streaming de tokens | No necesario en primera prueba — respuesta completa es suficiente |
| Batches / Files API | Fuera del alcance de prueba mínima |
| Prompt caching | Fuera del alcance de prueba mínima |
| Tool use / function calling | Fuera del alcance de prueba mínima |

---

## 6. Entrada futura permitida para una primera prueba

| Campo | Tipo | Descripción | Restricción |
|---|---|---|---|
| `prompt` | string | Instrucción mínima a clasificar — sin datos sensibles | Máximo 200 caracteres. Sin nombres propios, sin datos personales, sin secrets |
| `modo_seguro` | bool | Debe ser `True` — sin esto no se llama | Identidad estricta: `True`, no `1`, no `"true"` |
| `proveedor` | string | Siempre `"haiku_real"` para distinguir del fake | Inmutable en el contrato |
| `timeout_segundos` | int | Máximo de espera para la respuesta | Valor fijo: `10` — no configurable en primera prueba |
| `max_tokens` | int | Límite de tokens en la respuesta | Valor fijo: `64` — mínimo viable |
| `request_id` | string | Identificador único de la prueba para trazabilidad | UUID generado localmente antes de la llamada |

### Lo que nunca puede estar en la entrada

| Prohibición |
|---|
| Valor real de `ANTHROPIC_API_KEY` |
| Datos de usuario o datos personales |
| Paths del sistema de archivos local |
| Nombres de otras personas |
| Tokens o credenciales de cualquier tipo |
| Instrucciones que soliciten ejecutar acciones reales |

---

## 7. Salida futura esperada

| Campo | Tipo | Descripción |
|---|---|---|
| `ok` | bool | `True` si la llamada fue exitosa, `False` en cualquier error |
| `proveedor` | string | Siempre `"haiku_real"` si llegó a la API; `"haiku_fake"` si se activó el fallback |
| `modo` | string | `"api_real_prueba_minima"` o `"fake_local_sin_api"` si hubo fallback |
| `response_text` | string \| null | Texto de la respuesta del modelo (campo `content[0].text`) o `null` si falló |
| `error_tipo` | string \| null | Tipo de error si `ok == False`: `"auth"`, `"timeout"`, `"rate_limit"`, `"red"`, `"schema"`, `"corte"`, `"desconocido"` |
| `fallback_usado` | bool | `True` si se usó `cliente_haiku_fake` como fallback |
| `tokens_estimados` | int \| null | `usage.input_tokens + usage.output_tokens` si la llamada fue exitosa |
| `costo_estimado` | float \| null | Estimación en USD basada en tokens y tarifa pública del modelo, o `null` si no aplica |
| `evidencia` | dict \| null | Fragmento no sensible de la respuesta para trazabilidad — sin headers, sin key |
| `bloqueo` | bool | `True` si la prueba fue cortada por condición de corte obligatoria |

---

## 8. Manejo de API key

| Regla | Descripción |
|---|---|
| Nunca en repo | `ANTHROPIC_API_KEY` no puede existir en ningún archivo del repo en ninguna rama |
| Nunca en prompt | El valor de la key no puede aparecer en ningún mensaje enviado al modelo |
| Nunca en logs | El valor de la key no puede ser impreso, escrito en archivo ni enviado a ningún destino |
| Nunca en docs con valor real | Los documentos solo pueden referenciar el nombre `ANTHROPIC_API_KEY`, nunca su valor |
| Solo variable de entorno controlada | La key solo puede existir como variable de entorno en la sesión local del operador |
| Nombre permitido como referencia textual | `ANTHROPIC_API_KEY` — solo el nombre, nunca el valor |
| Valor real prohibido en cualquier artefacto | Commits, docs, tests, logs, prompts, PR bodies, comentarios de código |

### Protocolo de carga segura de la key (referencia para PUENTE-6B)

```python
# Referencia documental — no ejecutar en este ciclo
import os
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("ANTHROPIC_API_KEY no está definida en el entorno")
# NUNCA imprimir api_key ni incluirla en logs
```

---

## 9. Reglas de seguridad

| Regla | Descripción |
|---|---|
| No loguear headers de Authorization | El header `Authorization: Bearer <key>` nunca debe aparecer en logs |
| No loguear el valor de la key | Ni completo ni parcial (ni los primeros 8 caracteres) |
| No imprimir variables de entorno | Ningún `print(os.environ)` ni equivalente |
| No subir `.env` | `.env` debe estar en `.gitignore` y nunca debe existir en el repo |
| No hacer retry infinito | Máximo 1 intento en la primera prueba — sin retry automático |
| Timeout corto y fijo | 10 segundos — si no hay respuesta en ese tiempo, se activa el fallback |
| Fallback al fake siempre disponible | Si cualquier condición falla, `cliente_haiku_fake` debe poder responder sin cambios |
| Kill switch manual | El operador puede interrumpir la prueba en cualquier momento — la prueba no es autónoma |

---

## 10. Condiciones de corte

Si alguna de estas condiciones ocurre durante una futura prueba real, la prueba debe detenerse inmediatamente y activar el fallback:

| Condición | Acción |
|---|---|
| Error de autenticación (`authentication_error`) | Cortar — no reintentar — reportar sin mostrar la key |
| Rate limit (`rate_limit_error`) | Cortar — esperar mínimo 60 segundos antes de cualquier reintento en ciclo futuro |
| Costo inesperado (tokens > 200 en una sola prueba) | Cortar — revisar el prompt antes de continuar |
| Respuesta vacía o malformada (sin `content[0].text`) | Cortar — clasificar como `error_tipo: "schema"` |
| Respuesta que sugiere ejecutar una acción real | Cortar — clasificar como `error_tipo: "corte"` — reportar a Ariel |
| Aparición de cualquier secret en la entrada al modelo | Cortar antes de enviar — nunca enviar |
| Aparición de cualquier secret en la respuesta del modelo | Cortar — no loguear la respuesta completa |
| Timeout superado (> 10 segundos) | Cortar — activar fallback — reportar latencia |
| Pérdida de conectividad de red | Cortar — activar fallback |

---

## 11. Riesgos

| Riesgo | Nivel | Mitigación |
|---|---|---|
| Filtrado accidental de API key en logs o docs | Alto | Nunca imprimir key; revisión manual de logs antes de guardar; `.env` en `.gitignore` |
| Logs con información sensible de la sesión | Alto | Definir exactamente qué se registra antes de ejecutar la prueba |
| Costo inesperado por llamadas múltiples o tokens altos | Medio | `max_tokens: 64`, `retry: 0`, timeout: 10s, 1 sola llamada por prueba |
| Dependencia de red externa (API no disponible) | Medio | Fallback al cliente fake siempre activo sin modificar código |
| Respuestas no determinísticas del modelo | Medio | Los tests de prueba real no pueden afirmar contenido exacto — solo verificar estructura |
| Confusión entre "el modelo sugiere X" y "el sistema ejecuta X" | Alto | La respuesta del modelo es solo texto — nunca se ejecuta directamente — requiere validación humana |
| Key comprometida por un commit accidental | Alto | Pre-commit hook que detecte patrones de key en staged files (a implementar en PUENTE-6B) |
| Escalada no autorizada a producción | Alto | Prohibición absoluta — cualquier llamada futura es en entorno local aislado |

---

## 12. Checklist previo a PUENTE-6B

Antes de iniciar PUENTE-6B (cliente API real preparado, sin llamada real), se deben verificar **todos** estos ítems:

- [ ] PUENTE-6A mergeado en `main` con evidencia verificable (commit hash)
- [ ] `python -m unittest discover -s tests` → 262/262 OK en `main`
- [ ] Autorización explícita de Ariel en la sesión activa para iniciar PUENTE-6B
- [ ] Confirmar que `ANTHROPIC_API_KEY` no está en ningún archivo del repo
- [ ] Confirmar que `.env` no existe en el repo ni en `.gitignore` sin estar ignorado
- [ ] Confirmar que `anthropic` SDK no está instalado (o si lo está, que no hay código que lo importe)
- [ ] Confirmar que no hay workflows que se activarían con el push de PUENTE-6B
- [ ] Rama de trabajo dedicada para PUENTE-6B (no trabajar en `main`)
- [ ] Definir exactamente qué función nueva se creará en PUENTE-6B (solo la firma y el contrato, no la llamada)
- [ ] Confirmar que los 3 módulos existentes no se modificarán en PUENTE-6B

---

## 13. Condiciones de bloqueo

Las siguientes condiciones bloquean el inicio de cualquier ciclo que involucre código de API real:

| Condición de bloqueo | Nivel |
|---|---|
| No hay autorización explícita de Ariel en la sesión activa | ABSOLUTO |
| PUENTE-6A no está en `main` | ABSOLUTO |
| Algún test falla en `main` | ABSOLUTO |
| La API key estaría en un archivo del repo en cualquier formato | ABSOLUTO |
| No existe rollback definido al cliente fake | ABSOLUTO |
| La prueba se ejecutaría en producción | ABSOLUTO |
| La prueba se ejecutaría en un workflow de CI/CD automático | ABSOLUTO |
| El alcance excede una sola función aislada | ABSOLUTO |
| Los 3 módulos existentes serían modificados | ABSOLUTO |
| No se definió `timeout`, `max_tokens` ni `retry` antes de la llamada | ABSOLUTO |
| No se auditó el código nuevo antes de la primera llamada real | ABSOLUTO |

---

## 14. Dictamen esperado del contrato

Una vez que este documento sea auditado y mergeado en `main`, el dictamen esperado es:

**CONTRATO APTO PARA PUENTE-6B — con las siguientes condiciones obligatorias:**

1. PUENTE-6B solo prepara el cliente (firma, estructura, manejo de errores) — no ejecuta ninguna llamada real.
2. La primera llamada real solo ocurre en PUENTE-6C, con autorización explícita de Ariel.
3. Los 3 módulos existentes (`cerebro_mock`, `mano_local_simulada`, `cliente_haiku_fake`) no se modifican en ningún ciclo de PUENTE-6.
4. El fallback al cliente fake debe estar activo y verificado antes de la primera llamada real.
5. La API key nunca toca ningún archivo del repo — solo variable de entorno en sesión local del operador.
