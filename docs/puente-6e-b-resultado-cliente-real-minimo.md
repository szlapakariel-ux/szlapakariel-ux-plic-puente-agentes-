# PUENTE-6E-B — Resultado: cliente real mínimo implementado

## 1. Identificación

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6E-B |
| Fecha/hora (UTC) | 2026-05-05 |
| Repo | `szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-` |
| Rama | `feat/puente-6e-b-cliente-real-minimo` |
| Commit base (main) | `6b23853` (PUENTE-6E-MAPA) |

---

## 2. Estado

### **IMPLEMENTACIÓN TÉCNICA MÍNIMA COMPLETADA — SIN LLAMADA REAL**

La función `cliente_api_real_minimo` fue implementada siguiendo el contrato de PUENTE-6E-A. No se ejecutó ninguna llamada real. No se tocaron secrets. No se modificaron tests existentes.

---

## 3. Archivos creados

| Archivo | Descripción |
|---|---|
| `src/plic_puente_agentes/cliente_api_real_minimo.py` | Función cliente real mínima — sin red a nivel de módulo |
| `tests/test_cliente_api_real_minimo.py` | 91 tests — sin llamada real, con `_http_ejecutor` mock |
| `docs/puente-6e-b-resultado-cliente-real-minimo.md` | Este documento |

---

## 4. Diseño del cliente real mínimo

### 4.1 Constantes

| Constante | Valor |
|---|---|
| `_MODELO_AUTORIZADO` | `"claude-haiku-4-5-20251001"` |
| `_MAX_TOKENS_MAXIMO` | `50` |
| `_TIMEOUT_MAXIMO` | `10` |
| `_API_VERSION` | `"2023-06-01"` |
| `_ENDPOINT` | `"https://api.anthropic.com/v1/messages"` |
| `_BODY_ERROR_LIMITE` | `1000` |

### 4.2 Firma de la función principal

```python
def cliente_api_real_minimo(entrada: dict, _http_ejecutor=None) -> dict
```

`_http_ejecutor` es el hook de testeo: si se provee, reemplaza la función `_ejecutar_http` interna. En uso real nunca se pasa — la llamada HTTP ocurre dentro de `_ejecutar_http` usando `urllib.request`, que solo se importa dentro de esa función (no en nivel de módulo).

### 4.3 Validaciones en orden

1. `entrada` debe ser `dict` → `entrada_invalida`
2. `modo_seguro` debe ser `True` exacto → `modo_seguro_requerido`
3. `permitir_llamada_real` debe ser `True` o `False` exacto → `permitir_llamada_real_invalido`
4. `prompt` debe ser `str` no vacío → `prompt_invalido`
5. `modelo` debe ser `"claude-haiku-4-5-20251001"` → `modelo_no_autorizado`
6. `max_tokens` debe ser `int` (no `bool`) entre 1 y 50 → `max_tokens_invalido` / `max_tokens_fuera_de_rango`
7. `timeout` debe ser `int` o `float` (no `bool`) entre 0 y 10 exclusive → `timeout_invalido` / `timeout_fuera_de_rango`
8. Si `permitir_llamada_real=False` → bloquea con `llamada_real_no_autorizada`
9. Verifica `ANTHROPIC_API_KEY` en entorno (booleano — nunca imprime el valor) → `anthropic_api_key_ausente`

### 4.4 Estructura de salida — contrato PUENTE-6E-A cumplido

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
        "cache_read_input_tokens": int,
    },
    "error_tipo": str | None,
    "body_error_sanitizado": str | None,
    "llamada_real_ejecutada": bool,
    "cantidad_llamadas": int,
    "secret_expuesto": False,  # hardcoded
}
```

---

## 5. Invariantes verificadas

| Invariante | Verificación |
|---|---|
| `secret_expuesto` siempre `False` | Hardcoded en `_salida()` — no puede ser `True` |
| `llamada_real_ejecutada` solo `True` si ejecutor corrió | Solo se pone `True` después de llamar al ejecutor |
| `cantidad_llamadas` máximo `1` por invocación | Nunca hay loop, máximo una llamada |
| `urllib.request` solo dentro de `_ejecutar_http` | Import local, no en nivel de módulo |
| Sin `anthropic` SDK | Solo `json` y `os` en nivel de módulo |
| Sin `.env`, sin secrets en código | Key solo via `os.environ.get()` booleano |

---

## 6. Manejo de errores implementado

| Código HTTP | `error_tipo` devuelto |
|---|---|
| 401 | `auth_error` |
| 400 | `bad_request` |
| 429 | `rate_limit` |
| 503 | `servicio_no_disponible` |
| 0 con "timeout" | `timeout` |
| 0 sin timeout | `error_red` |
| 200 con JSON inválido | `respuesta_inesperada` |
| 200 con `content` vacío o ausente | `respuesta_inesperada` |
| Excepción del ejecutor | `error_ejecutor` |

Body de error capturado, sanitizado a máx 1000 chars. Si contiene patrones `sk-ant`, `api_key`, `authorization`, `x-api-key` → se omite completamente.

---

## 7. Tests implementados — 91 tests

| Clase | Tests | Qué verifica |
|---|---|---|
| `TestIdentidad` | 3 | Módulo importable, funciones existen |
| `TestAislamiento` | 4 | Sin anthropic SDK, sin requests, urllib.request solo en _ejecutar_http |
| `TestSecretInvariante` | 3 | `secret_expuesto` siempre `False` en todos los caminos |
| `TestLlamadaRealInvariante` | 6 | `llamada_real_ejecutada` y `cantidad_llamadas` correctos |
| `TestEntradaInvalida` | 3 | No-dict rechazado |
| `TestModoSeguro` | 4 | `modo_seguro` debe ser `True` exacto |
| `TestPermitirLlamadaReal` | 4 | `permitir_llamada_real` validado |
| `TestPrompt` | 5 | Prompt vacío, None, no-string rechazados |
| `TestModelo` | 4 | Solo modelo autorizado acepta |
| `TestMaxTokens` | 7 | Rango 1-50, tipos, bool rechazado |
| `TestTimeout` | 7 | Rango 0-10, tipos, bool rechazado |
| `TestApiKeyAusente` | 2 | Sin key o key vacía bloquea |
| `TestCasoValido` | 13 | Todos los campos del contrato en caso exitoso |
| `TestCamposRespuesta` | 8 | Todos los campos presentes, tipos correctos |
| `TestErroresHTTP` | 10 | 401, 400, 429, 503, red caída, JSON inválido, content vacío |
| `TestSanitizarBodyError` | 8 | Sanitización: None, vacío, truncado, patrones secret |

---

## 8. Tests totales en la suite

| Estado | Cantidad |
|---|---|
| Tests antes de PUENTE-6E-B | 416 |
| Tests nuevos (PUENTE-6E-B) | 91 |
| **Total** | **507** |
| Tests fallidos | **0** |

---

## 9. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Llamada real ejecutada | **NO** |
| Request HTTP ejecutado | **NO** |
| Secret expuesto | **NO** |
| `ANTHROPIC_API_KEY` leída o impresa | **NO** — solo verificación booleana en tests |
| `.env` creado o modificado | **NO** |
| Tests existentes modificados | **NO** |
| Tests existentes rotos | **NO** — 416/416 siguen pasando |
| Workflows tocados | **NO** |
| Producción tocada | **NO** |
| Navegador usado | **NO** |
| Playwright usado | **NO** |
| Otros repos tocados | **NO** |
| SDK `anthropic` importado | **NO** |
| `requests` importado | **NO** |

---

## 10. Qué falta para una llamada real desde código

Este microciclo NO habilita llamadas reales. Para ejecutar `cliente_api_real_minimo` con `permitir_llamada_real=True` en un contexto real se requiere:

| Requisito | Estado |
|---|---|
| `ANTHROPIC_API_KEY` disponible en entorno del proceso | Pendiente — no resuelta para Claude Code remoto |
| Microciclo separado con autorización explícita de Ariel | Obligatorio |
| Presupuesto declarado antes de la llamada | Obligatorio |
| Máximo 1 llamada por microciclo | Obligatorio |
| No retry automático | Obligatorio |

---

## 11. Dictamen

### **PUENTE-6E-B COMPLETADO — implementación técnica mínima lista**

`cliente_api_real_minimo` implementa el contrato de PUENTE-6E-A. Bloquea toda llamada real por defecto. Es testeable sin red via `_http_ejecutor`. 507 tests pasan. 0 secrets expuestos. 0 llamadas reales ejecutadas.

**Este resultado NO autoriza:**
- Llamadas reales a la API.
- Retry automático.
- Integración en producción.
- Automatización de ningún tipo.
- Inicio de cualquier siguiente microciclo sin autorización explícita de Ariel.

> El próximo paso requiere instrucción explícita y separada de Ariel.
