# PUENTE-6A — Resultado: Contrato para prueba mínima de API real

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6A |
| Rama base | `main` |
| Commit base | `da1af486250fc8d38909f1b47cc203510a43fddf` (PUENTE-5Z incluido) |
| Rama de trabajo | `docs/puente-6a-contrato-prueba-api-real-sin-ejecucion` |
| Tests al iniciar | 262/262 OK |
| Estado de PUENTE-5Z | Cerrado en main — fase cliente Haiku fake/local cerrada |

---

## 2. Contrato creado

| Archivo | Tipo | Descripción |
|---|---|---|
| `docs/puente-6a-contrato-prueba-api-real.md` | Documental | Contrato completo: objetivo, diferencias entre tipos de cliente, qué se prueba, qué no, entrada/salida futura, manejo de key, reglas de seguridad, condiciones de corte, riesgos, checklist, condiciones de bloqueo, dictamen esperado |
| `docs/puente-6a-resultado-contrato-prueba-api-real.md` | Documental | Este archivo — estado inicial, contrato creado, habilitaciones, prohibiciones, tablas de referencia, confirmaciones de seguridad, próximo microciclo |

---

## 3. Qué queda habilitado

| Capacidad | Estado |
|---|---|
| Referencia documental al endpoint `/v1/messages` | **HABILITADO** — solo en docs, sin llamada real |
| Definición del payload mínimo para futura prueba | **HABILITADO** — solo en docs, sin ejecución |
| Definición del protocolo de manejo seguro de `ANTHROPIC_API_KEY` | **HABILITADO** — solo nombre como referencia textual, nunca el valor |
| Inicio de PUENTE-6B (cliente preparado, sin llamada real) | **HABILITADO** — requiere autorización explícita de Ariel + PUENTE-6A en `main` |
| Uso del cliente fake como fallback en futura prueba | **HABILITADO** — `cliente_haiku_fake` sigue siendo el componente activo |
| Auditoría documental del contrato | **HABILITADO** — ver `docs/puente-6a-contrato-prueba-api-real.md` |

---

## 4. Qué NO queda habilitado

| Ítem | Estado |
|---|---|
| Llamada real a `api.anthropic.com` | **NO — requiere PUENTE-6C + autorización explícita de Ariel** |
| Instalación del SDK `anthropic` | **NO — requiere PUENTE-6B + autorización explícita de Ariel** |
| Uso de `ANTHROPIC_API_KEY` con valor real | **NO — prohibición absoluta en cualquier archivo del repo** |
| Archivo `.env` | **NO — prohibición absoluta** |
| Claude Haiku real | **NO — requiere PUENTE-6C mínimo** |
| Modificación de `cerebro_mock.py` | **NO — prohibición absoluta** |
| Modificación de `mano_local_simulada.py` | **NO — prohibición absoluta** |
| Modificación de `cliente_haiku_fake.py` | **NO — prohibición absoluta** |
| Modificación de tests existentes | **NO — prohibición absoluta** |
| Producción | **NO — prohibición absoluta** |
| Navegador real | **NO — requiere ciclo específico** |
| Playwright real | **NO — requiere ciclo específico** |
| Workflows de CI/CD | **NO — prohibición absoluta** |
| Ejecución real por Mano Local | **NO — requiere PUENTE-6C mínimo** |
| Reemplazo del Cerebro Mock por Haiku real | **NO — son componentes con roles distintos** |

---

## 5. Tabla de entrada futura

| Campo | Tipo | Valor permitido | Restricción |
|---|---|---|---|
| `prompt` | string | Instrucción mínima de clasificación | Máx 200 chars, sin datos sensibles, sin secrets |
| `modo_seguro` | bool | `True` (identidad estricta) | Rechaza `1`, `"true"`, `None` |
| `proveedor` | string | `"haiku_real"` | Inmutable — no configurable |
| `timeout_segundos` | int | `10` | Fijo en primera prueba — no configurable |
| `max_tokens` | int | `64` | Fijo en primera prueba — no configurable |
| `request_id` | string | UUID generado localmente | Trazabilidad — nunca contiene datos sensibles |

---

## 6. Tabla de salida futura

| Campo | Tipo | Valores posibles |
|---|---|---|
| `ok` | bool | `True` si llamada exitosa, `False` en cualquier error |
| `proveedor` | string | `"haiku_real"` o `"haiku_fake"` si se activó fallback |
| `modo` | string | `"api_real_prueba_minima"` o `"fake_local_sin_api"` |
| `response_text` | string \| null | Texto del modelo o `null` si falló |
| `error_tipo` | string \| null | `"auth"` \| `"timeout"` \| `"rate_limit"` \| `"red"` \| `"schema"` \| `"corte"` \| `"desconocido"` \| `null` |
| `fallback_usado` | bool | `True` si se usó `cliente_haiku_fake` |
| `tokens_estimados` | int \| null | `input + output tokens` o `null` |
| `costo_estimado` | float \| null | Estimación en USD o `null` |
| `evidencia` | dict \| null | Fragmento no sensible de la respuesta |
| `bloqueo` | bool | `True` si la prueba fue cortada por condición de corte |

---

## 7. Tabla de manejo de API key

| Regla | Estado |
|---|---|
| Valor de key en repo (cualquier archivo, cualquier rama) | **PROHIBIDO ABSOLUTO** |
| Valor de key en commits | **PROHIBIDO ABSOLUTO** |
| Valor de key en docs | **PROHIBIDO ABSOLUTO** |
| Valor de key en tests | **PROHIBIDO ABSOLUTO** |
| Valor de key en logs | **PROHIBIDO ABSOLUTO** |
| Valor de key en prompts enviados al modelo | **PROHIBIDO ABSOLUTO** |
| Nombre `ANTHROPIC_API_KEY` como referencia textual en docs | **PERMITIDO** |
| Variable de entorno local en sesión del operador | **PERMITIDO** — solo forma válida de cargar la key |
| Archivo `.env` en repo | **PROHIBIDO ABSOLUTO** |
| `print(api_key)` o equivalente | **PROHIBIDO ABSOLUTO** |

---

## 8. Tabla de riesgos

| Riesgo | Nivel | Mitigación |
|---|---|---|
| Filtrado accidental de API key en logs o docs | Alto | Nunca imprimir key; revisión manual de logs; `.env` en `.gitignore` |
| Logs con información sensible | Alto | Definir exactamente qué se registra antes de ejecutar |
| Costo inesperado por llamadas múltiples | Medio | `max_tokens: 64`, `retry: 0`, timeout: 10s, 1 llamada por prueba |
| Dependencia de red externa | Medio | Fallback al cliente fake siempre activo |
| Respuestas no determinísticas | Medio | Tests de prueba real solo verifican estructura, no contenido exacto |
| Confusión entre "modelo sugiere X" y "sistema ejecuta X" | Alto | La respuesta es solo texto — nunca se ejecuta directamente |
| Key comprometida por commit accidental | Alto | Pre-commit hook a implementar en PUENTE-6B |
| Escalada no autorizada a producción | Alto | Prohibición absoluta — entorno local aislado únicamente |

---

## 9. Tabla de condiciones de corte

| Condición | Acción inmediata |
|---|---|
| Error de autenticación (`authentication_error`) | Cortar — no reintentar — reportar sin mostrar la key |
| Rate limit (`rate_limit_error`) | Cortar — esperar mínimo 60s antes de reintento en ciclo futuro |
| Costo inesperado (tokens > 200) | Cortar — revisar prompt antes de continuar |
| Respuesta vacía o malformada | Cortar — `error_tipo: "schema"` |
| Respuesta que sugiere acción real | Cortar — `error_tipo: "corte"` — reportar a Ariel |
| Secret en entrada al modelo | Cortar antes de enviar — nunca enviar |
| Secret en respuesta del modelo | Cortar — no loguear respuesta completa |
| Timeout > 10 segundos | Cortar — activar fallback — reportar latencia |
| Pérdida de conectividad | Cortar — activar fallback |

---

## 10. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin código ejecutable nuevo | CONFIRMADO — solo markdown |
| Sin imports nuevos | CONFIRMADO — cero nuevos archivos `.py` |
| Sin modificación de `cerebro_mock.py` | CONFIRMADO |
| Sin modificación de `mano_local_simulada.py` | CONFIRMADO |
| Sin modificación de `cliente_haiku_fake.py` | CONFIRMADO |
| Sin modificación de tests | CONFIRMADO |
| Sin scripts (`.sh`) | CONFIRMADO |
| Sin workflows (`.yml`/`.yaml`) | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin `.env` | CONFIRMADO |
| Sin API keys reales | CONFIRMADO — solo nombre `ANTHROPIC_API_KEY` como texto de referencia |
| Sin llamada a API real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin SDK real instalado | CONFIRMADO |
| Sin navegador abierto | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin repos prohibidos tocados | CONFIRMADO — `torre-control`, `agente-saas`, `auditoria-sofse`, `plic-laboratorio-portero` no tocados |
| Tests existentes pasan | CONFIRMADO — 262/262 OK |

---

## 11. Próximo microciclo sugerido

**PUENTE-6B — Cliente API real mínimo preparado, sin llamada real**

### Objetivo

Crear el archivo `src/plic_puente_agentes/cliente_haiku_real.py` con:
- La firma de la función `cliente_haiku_real(entrada: dict) -> dict`.
- El manejo seguro de `ANTHROPIC_API_KEY` desde variable de entorno.
- La estructura del payload según el contrato definido en PUENTE-6A.
- El fallback automático a `cliente_haiku_fake` si la key no está disponible o si ocurre cualquier error.
- El manejo de todas las condiciones de corte definidas en PUENTE-6A.
- Sin ejecutar ninguna llamada real — la función queda preparada pero no llama a la API.

### Alcance

- Solo crear `cliente_haiku_real.py` (nuevo archivo, no modifica existentes).
- Solo crear tests unitarios del cliente real en modo sin-llamada (mock de red).
- Sin llamada real a `api.anthropic.com`.
- Sin instalar `anthropic` SDK en este ciclo.

### Restricciones

- Sin API real.
- Sin Claude Haiku real.
- Sin `.env`.
- Sin secrets.
- Sin producción.
- Sin workflows.
- Sin modificar los 3 módulos existentes.

### Condición de inicio

> No iniciar PUENTE-6B hasta que PUENTE-6A esté cerrado en `main` con evidencia verificable (commit hash) **y** autorización explícita de Ariel en la sesión activa.
