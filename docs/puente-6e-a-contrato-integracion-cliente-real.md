# PUENTE-6E-A — Contrato documental de integración mínima del cliente real

## 1. Identificación

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6E-A |
| Fecha/hora (UTC) | 2026-05-04 |
| Repo | `szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-` |
| Rama | `docs/puente-6e-a-contrato-integracion-cliente-real` |
| Commit base (main) | `21aae9622ecd43374a7764c70b107b3d31c19047` |
| Autorización de Ariel | "PUENTE-6E-A — contrato documental de integración mínima del cliente real segui" |

---

## 2. Estado

### **CONTRATO DOCUMENTAL — sin implementación**

Este documento define el contrato mínimo para integrar un cliente real de Anthropic en el sistema. **No implementa nada.** No ejecuta llamadas. No modifica código. No habilita PUENTE-6E-B automáticamente.

---

## 3. Objetivo

Definir el contrato mínimo para integrar un cliente real de Anthropic en una etapa futura (PUENTE-6E-B o posterior), sin ejecutar API real ni modificar código todavía.

### Por qué se necesita este contrato antes de la implementación

PUENTE-6D demostró que la llamada real funciona. Lo que no está definido todavía es:

| Pregunta | Estado |
|---|---|
| ¿Dónde vive el cliente real en el código? | Sin definir |
| ¿Cómo se inyecta el secret sin repo? | Sin definir |
| ¿Cuándo se permite llamar? | Sin definir |
| ¿Cuántos tokens máximos por sesión? | Sin definir |
| ¿Qué se loguea y qué se omite? | Sin definir |
| ¿Qué pasa ante error? | Sin definir |
| ¿Qué pasa ante rate limit? | Sin definir |
| ¿Qué pasa ante respuesta inesperada? | Sin definir |

Este contrato responde todas esas preguntas.

---

## 4. Alcance permitido en la futura etapa técnica

| Elemento | Descripción |
|---|---|
| Cliente real mínimo | Una función o clase controlada que encapsula la llamada real |
| Una función controlada | Un único punto de entrada, sin invocaciones dispersas |
| Modelo autorizado | `claude-haiku-4-5-20251001` — única opción permitida |
| Prompt mínimo | Texto fijo o parametrizado con validación previa |
| Respuesta esperada | Campo `content[].text` extraído y validado |
| Logging sanitizado | Solo campos seguros (ver sección 12) |
| Manejo de errores | Todos los errores esperados con body capturado (ver sección 10) |
| Corte por presupuesto | Verificación de presupuesto definido antes de cada llamada |
| No automatización por defecto | Sin scheduler, sin trigger automático, sin webhook |

---

## 5. Fuera de alcance

| Elemento | Estado |
|---|---|
| Producción | **FUERA DE ALCANCE** |
| Workflows CI/CD con secrets | **FUERA DE ALCANCE** |
| Agentes autónomos | **FUERA DE ALCANCE** |
| Retry automático | **FUERA DE ALCANCE** |
| Secrets en repo | **FUERA DE ALCANCE** |
| `.env` versionado | **FUERA DE ALCANCE** |
| Llamadas masivas o en lote | **FUERA DE ALCANCE** |
| Integración con UI | **FUERA DE ALCANCE** |
| Integración con WhatsApp | **FUERA DE ALCANCE** |
| Integración con navegador/Playwright | **FUERA DE ALCANCE** |
| Streaming de respuesta | **FUERA DE ALCANCE** |
| Múltiples modelos simultáneos | **FUERA DE ALCANCE** |
| Memoria o contexto persistente | **FUERA DE ALCANCE** |

---

## 6. Modelo autorizado

| Campo | Valor |
|---|---|
| Modelo único autorizado | `claude-haiku-4-5-20251001` |
| Fuente de autorización | `docs/puente-6d-preflight-real.md`, validado en PUENTE-6D |
| `max_tokens` máximo | 50 (según preflight) |
| `temperature` | `0.0` (float explícito — no entero) |
| Versión de API Anthropic | `2023-06-01` |

Cualquier intento de usar un modelo diferente debe ser bloqueado antes de la llamada, con error `modelo_no_autorizado`.

---

## 7. Reglas de secrets

| Regla | Estado |
|---|---|
| Ningún secret en repo | **OBLIGATORIO** |
| Ningún secret en documentación | **OBLIGATORIO** |
| Ningún secret en logs | **OBLIGATORIO** |
| Ningún `.env` versionado | **OBLIGATORIO** |
| Variable de entorno solo en entorno autorizado | **OBLIGATORIO** |
| Verificación booleana permitida | SÍ — `bool(os.environ.get('ANTHROPIC_API_KEY'))` |
| Imprimir valor real | **PROHIBIDO** |
| Imprimir prefijo de key | **PROHIBIDO** |
| Imprimir sufijo de key | **PROHIBIDO** |
| Imprimir longitud de key | **PROHIBIDO** |

### Método de inyección autorizado

La `ANTHROPIC_API_KEY` debe estar disponible como variable de entorno en el proceso que ejecuta el cliente, definida **antes** de iniciar el proceso. Las opciones autorizadas son:

1. Variable de entorno del sistema (permanente, sin versionar).
2. Variable definida en la terminal de lanzamiento (`export ANTHROPIC_API_KEY=...`) — sin pegar en chat.
3. Configuración de entorno de Claude Code (`settings.json` → `env`) — para entorno remoto.

En ningún caso la key debe aparecer en código, documentación, logs, commits ni chat.

---

## 8. Contrato mínimo del cliente real

### 8.1 Entrada mínima requerida

| Campo | Tipo | Descripción |
|---|---|---|
| `prompt` | `str` | Texto del mensaje del usuario — validado y no vacío |
| `modelo` | `str` | Debe ser `"claude-haiku-4-5-20251001"` — validado antes de llamar |
| `max_tokens` | `int` | Entre 1 y 50 — validado antes de llamar |

### 8.2 Campos prohibidos en la entrada

| Campo | Motivo |
|---|---|
| `api_key` como parámetro | Debe venir del entorno, nunca como argumento |
| `stream: true` | Fuera de alcance |
| `system` con datos sensibles | Requiere revisión antes de usar |
| `tools` / `tool_choice` | Fuera de alcance en esta etapa |

### 8.3 Salida mínima esperada

| Campo | Tipo | Descripción |
|---|---|---|
| `ok` | `bool` | `True` si la llamada fue exitosa |
| `respuesta_texto` | `str` o `None` | Texto extraído de `content[].text`, o `None` si no hubo respuesta válida |
| `modelo` | `str` | Modelo devuelto por la API |
| `status_code` | `int` | Código HTTP de la respuesta |
| `usage` | `dict` | Campos de usage (ver sección 11) |
| `llamada_real_ejecutada` | `bool` | Siempre `True` si llegó a ejecutar |
| `cantidad_llamadas` | `int` | Cantidad de llamadas en esta invocación — siempre `<= 1` |
| `secret_expuesto` | `bool` | Siempre `False` — hardcoded |

### 8.4 Estructura de respuesta segura

```python
{
    "ok": bool,
    "respuesta_texto": str | None,
    "modelo": str,
    "status_code": int,
    "usage": {
        "input_tokens": int,
        "output_tokens": int,
        "cache_creation_input_tokens": int,
        "cache_read_input_tokens": int
    },
    "error_tipo": str | None,
    "body_error_sanitizado": str | None,
    "llamada_real_ejecutada": bool,
    "cantidad_llamadas": int,
    "secret_expuesto": False
}
```

### 8.5 Metadata permitida en la respuesta

- `usage` completo (tokens)
- `modelo` devuelto
- `status_code`
- `id` presente (booleano) — no el valor completo si es sensible
- `service_tier`
- `inference_geo`

### 8.6 Metadata prohibida en la respuesta

- Valor de `ANTHROPIC_API_KEY`
- Headers completos de la request
- Valor de `x-api-key`
- Datos personales del usuario

---

## 9. Política de llamadas

| Regla | Valor |
|---|---|
| Llamadas automáticas | **PROHIBIDAS** |
| Cada llamada real requiere | Microciclo propio con autorización explícita |
| Máximo de llamadas por microciclo | **1** |
| Registro de `usage` | **OBLIGATORIO** en cada llamada |
| Registro de `modelo` | **OBLIGATORIO** en cada llamada |
| Registro de `status_code` | **OBLIGATORIO** en cada llamada |
| Corte ante error | **OBLIGATORIO** — no continuar si la llamada falla |
| Retry automático | **PROHIBIDO** |
| Acumulado de llamadas | Llevar conteo desde inicio del proyecto |

### Invariantes de la función cliente real

- `llamada_real_ejecutada` solo puede ser `True` si la función efectivamente envió una request HTTP.
- `cantidad_llamadas` solo puede ser `0` o `1` dentro de una invocación.
- `secret_expuesto` siempre es `False` — hardcoded en la salida.

---

## 10. Política de errores

| Tipo de error | Código HTTP | Acción |
|---|---|---|
| Error de autenticación | 401 | Frenar — reportar `auth_error` — no reintentar |
| Bad request | 400 | Frenar — capturar body sanitizado — reportar `bad_request` |
| Rate limit | 429 | Frenar — reportar `rate_limit` — no reintentar automáticamente |
| Timeout | — | Frenar — reportar `timeout` |
| Modelo no autorizado | — | Frenar antes de llamar — reportar `modelo_no_autorizado` |
| Respuesta inesperada | 200 con formato incorrecto | Reportar `respuesta_inesperada` — no considerar OK |
| Red/proxy | Conexión fallida | Reportar `error_red` |
| Servicio no disponible | 503 | Frenar — reportar `servicio_no_disponible` |

### Captura de body en errores HTTP

El body del error debe ser capturado siempre que sea posible, sanitizado y limitado:

```python
body_error = response_stream.read(1000)  # máximo 1000 caracteres
if len(body_error) == 1000:
    body_error += "...[truncado]"
```

El body nunca debe contener la API key ni datos sensibles. Si el body contiene patrones que parecen credenciales, omitirlo por completo.

---

## 11. Política de costos/tokens

| Regla | Descripción |
|---|---|
| Registrar `input_tokens` | Obligatorio en cada llamada |
| Registrar `output_tokens` | Obligatorio en cada llamada |
| Registrar `cache_creation_input_tokens` | Obligatorio si existe |
| Registrar `cache_read_input_tokens` | Obligatorio si existe |
| Definir presupuesto antes de llamar | El microciclo debe declarar el presupuesto máximo antes de autorizar |
| Cortar si no hay presupuesto definido | Sin presupuesto declarado → no llamar |
| Acumular totales entre microciclos | Mantener conteo histórico en documentación |

### Referencia de uso conocido

El intento exitoso de PUENTE-6D (prompt `"Respondé exactamente: PLIC_OK"`, modelo `claude-haiku-4-5-20251001`, `max_tokens: 16`) consumió:

| Métrica | Valor |
|---|---|
| `input_tokens` | 18 |
| `output_tokens` | 8 |
| `cache_creation_input_tokens` | 0 |
| `cache_read_input_tokens` | 0 |
| `service_tier` | `standard` |

Este dato sirve como referencia base para estimar el costo de llamadas similares.

---

## 12. Logging sanitizado

### Campos permitidos en logs

| Campo | Ejemplo |
|---|---|
| `status_code` | `200` |
| `modelo` | `"claude-haiku-4-5-20251001"` |
| `respuesta_texto` (si no es sensible) | `"PLIC_OK"` |
| `usage.input_tokens` | `18` |
| `usage.output_tokens` | `8` |
| `error_tipo` | `"bad_request"` |
| `body_error_sanitizado` | `"invalid_request_error: ..."` (máx 1000 chars) |
| `llamada_real_ejecutada` | `True` / `False` |
| `cantidad_llamadas` | `1` |

### Campos prohibidos en logs

| Campo | Motivo |
|---|---|
| `ANTHROPIC_API_KEY` | Secret — prohibido siempre |
| Headers completos de la request | Contienen `x-api-key` |
| `Authorization` / `x-api-key` | Secret directo |
| Prompts con datos personales | Privacidad |
| Datos de usuarios | Privacidad |
| Cualquier valor que parezca una clave `sk-ant-...` | Secret |

---

## 13. Criterios mínimos para PUENTE-6E-B

PUENTE-6E-B **no queda habilitado automáticamente** por este contrato.

Para avanzar a PUENTE-6E-B debe existir:

| Criterio | Estado requerido |
|---|---|
| Este contrato (`puente-6e-a-contrato-integracion-cliente-real.md`) mergeado en main | Pendiente — PR de este microciclo |
| Auditoría read-only de este contrato aprobada | Pendiente |
| Autorización explícita de Ariel para PUENTE-6E-B | Pendiente |
| Alcance técnico acotado definido en PUENTE-6E-B | Pendiente |
| Tests sin API real actualizados si se agregan funciones | Pendiente |
| Sin producción | Obligatorio |
| Sin workflows con secrets | Obligatorio |
| Diff de PUENTE-6E-B exacto y auditado | Obligatorio |

---

## 14. Riesgos identificados

| Riesgo | Descripción | Mitigación |
|---|---|---|
| Fuga de secrets | La key podría exponerse en logs, commits o chat | Reglas de secrets (sección 7) — verificación booleana única |
| Llamadas involuntarias | Una función mal diseñada puede llamar sin que el operador lo sepa | Invariante `llamada_real_ejecutada` + conteo obligatorio |
| Costos no controlados | Llamadas en bucle o sin presupuesto pueden incurrir en cargos | Política de presupuesto (sección 11) — corte sin presupuesto |
| Dependencia de red | La red corporativa causó un error 400 en PUENTE-6D | Recomendación de red celular para pruebas (documentado) |
| Errores sin body capturado | Sin body, el diagnóstico es imposible (PUENTE-6D lo aprendió) | Captura obligatoria de body sanitizado (sección 10) |
| Automatización prematura | Un trigger automático podría llamar sin autorización | Política de llamadas (sección 9) — no retry, no scheduler |
| Confusión entre entorno local y remoto | Claude Code remoto no hereda la key del entorno local | Sección 7 — inyección de entorno explícita |
| Respuesta inesperada tratada como éxito | El código puede creer que `200` siempre es válido | Validar `content[].text` además del status code |

---

## 15. Confirmaciones de seguridad de este microciclo

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
| PR abierto | NO |
| Merge ejecutado | NO |

---

## 16. Dictamen

### **CONTRATO DOCUMENTAL PUENTE-6E-A CREADO**

Este documento define el contrato de integración mínima del cliente real. **No implementa nada. No autoriza llamada real. No autoriza código. No autoriza producción. No habilita PUENTE-6E-B automáticamente.**

> El próximo paso requiere: este contrato mergeado en main, auditoría aprobada, y autorización explícita separada de Ariel para PUENTE-6E-B.
