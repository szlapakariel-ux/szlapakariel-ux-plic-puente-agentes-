# PUENTE-6B — Backlog B-07: Validar request_id vacío en cliente API preparado

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6B-BACKLOG (B-07) |
| Rama base | `main` |
| Commit base | `0adf9ab` (PUENTE-6B mergeado) |
| Rama de trabajo | `fix/puente-6b-backlog-validar-request-id` |
| Tests al iniciar | 326/326 OK |
| Origen del backlog | PUENTE-6C — Auditoría técnica de PUENTE-6B |

---

## 2. Origen del ítem B-07

Durante la auditoría PUENTE-6C se detectó que `cliente_api_real_preparado` aceptaba `request_id=""` (string vacío) y `request_id` ausente sin bloquear. El campo `request_id` es el único mecanismo de trazabilidad disponible antes de una futura llamada real (PUENTE-6D). Sin este campo válido, no sería posible correlacionar una solicitud preparada con su respuesta real.

| Caso | Comportamiento antes del fix | Comportamiento esperado |
|---|---|---|
| `request_id=""` | `ok=True`, `request_id` en output como `""` | `ok=False`, `bloqueo=True`, `error_tipo="request_id_invalido"` |
| `request_id` ausente | `ok=True`, `request_id="sin_request_id"` en output | `ok=False`, `bloqueo=True`, `error_tipo="request_id_invalido"` |
| `request_id="   "` | `ok=True` | `ok=False`, `bloqueo=True` |
| `request_id=None` | `ok=True` | `ok=False`, `bloqueo=True` |
| `request_id=123` | `ok=True` | `ok=False`, `bloqueo=True` |

---

## 3. Archivos modificados

| Archivo | Tipo | Cambio |
|---|---|---|
| `src/plic_puente_agentes/cliente_api_real_preparado.py` | Código Python | Agrega validación de `request_id` (prioridad 11) |
| `tests/test_cliente_api_real_preparado.py` | Tests unitarios | Agrega 13 tests en clase `TestClienteApiRealPreparadoRequestId` |
| `docs/puente-6b-backlog-validar-request-id.md` | Documental | Este archivo |

---

## 4. Cambio implementado en `cliente_api_real_preparado.py`

### Antes

```python
request_id = entrada.get("request_id", "sin_request_id")
prompt_resumido = prompt_lower[:50] + "..." if len(prompt_lower) > 50 else prompt_lower
```

### Después

```python
request_id = entrada.get("request_id", None)
if not isinstance(request_id, str) or not request_id.strip():
    return _bloqueo(
        error_tipo="request_id_invalido",
        motivo="request_id es obligatorio para trazabilidad antes de cualquier futura llamada real. Debe ser un string no vacío.",
        modelo=modelo,
    )

prompt_resumido = prompt_lower[:50] + "..." if len(prompt_lower) > 50 else prompt_lower
```

### Prioridad de la nueva regla en la cadena

| Prioridad | Condición | error_tipo |
|---|---|---|
| 1 | `entrada` no es dict | `entrada_invalida` |
| 2 | `modo_seguro` no es `True` | `modo_seguro_requerido` |
| 3 | `permitir_llamada_real` es `True` | `llamada_real_no_autorizada` |
| 4 | `prompt` vacío | `prompt_vacio` |
| 5 | `prompt` contiene término sensible (frase) | `entrada_sensible` |
| 6 | `prompt` contiene término sensible (token) | `entrada_sensible` |
| 7 | `proveedor` no es `"anthropic"` | `proveedor_no_autorizado` |
| 8 | `modelo` no está en lista permitida | `modelo_no_autorizado` |
| 9 | `timeout` > 10 | `timeout_excesivo` |
| 10 | `max_tokens` > 300 | `max_tokens_excesivo` |
| **11** | **`request_id` ausente, vacío, solo espacios o no-string** | **`request_id_invalido`** |
| 12 | Default válido | preparación exitosa |

---

## 5. Tests agregados

### Clase `TestClienteApiRealPreparadoRequestId` (13 tests nuevos)

| Test | Cubre |
|---|---|
| `test_request_id_ausente_bloquea` | `request_id` no presente en el dict de entrada |
| `test_request_id_vacio_bloquea` | `request_id=""` |
| `test_request_id_solo_espacios_bloquea` | `request_id="   "` |
| `test_request_id_none_bloquea` | `request_id=None` |
| `test_request_id_int_bloquea` | `request_id=123` (no-string) |
| `test_request_id_bool_bloquea` | `request_id=True` (no-string) |
| `test_request_id_valido_no_bloquea_por_este_motivo` | `request_id="req-001"` → no produce `request_id_invalido` |
| `test_request_id_valido_ok_true` | `request_id="req-001"` → `ok=True` |
| `test_request_id_valido_bloqueo_false` | `request_id="req-001"` → `bloqueo=False` |
| `test_request_id_invalido_bloqueo_true` | `request_id=""` → `bloqueo=True` |
| `test_request_id_invalido_ok_false` | `request_id=""` → `ok=False` |
| `test_request_id_valido_aparece_en_request_preparado` | `request_id` válido se refleja en `request_preparado["request_id"]` |
| `test_request_id_invalido_motivo_menciona_trazabilidad` | El motivo del bloqueo menciona "trazabilidad" |

---

## 6. Resultado de tests

```
python -m unittest discover -s tests

Ran 339 tests in 0.008s

OK
```

| Tests originales (PUENTE-6B) | Tests nuevos (B-07) | Total |
|---|---|---|
| 326 | 13 | **339** |

**339/339 tests pasan.** Sin errores. Sin warnings.

---

## 7. Propiedades preservadas

| Propiedad | Estado |
|---|---|
| Función pura | SÍ — sin efectos secundarios |
| Sin imports externos | SÍ — cero imports |
| Sin I/O | SÍ |
| Sin red | SÍ |
| Sin subprocess | SÍ |
| Sin lectura de entorno | SÍ |
| Sin API real | SÍ |
| Sin SDK de Anthropic | SÍ |
| Contrato de 13 campos en salida | SÍ — preservado |
| `cerebro_mock.py` no modificado | CONFIRMADO |
| `mano_local_simulada.py` no modificado | CONFIRMADO |
| `cliente_haiku_fake.py` no modificado | CONFIRMADO |
| Tests originales conservados (326) | CONFIRMADO |

---

## 8. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin imports nuevos en `cliente_api_real_preparado.py` | CONFIRMADO — cero imports |
| Sin API real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin SDK real | CONFIRMADO |
| Sin lectura de entorno | CONFIRMADO |
| Sin `ANTHROPIC_API_KEY` leída | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin repos prohibidos | CONFIRMADO |

---

## 9. Impacto en PUENTE-6D

Con B-07 corregido, `request_id` es un campo obligatorio validado antes de construir `request_preparado`. Esto garantiza que cualquier solicitud que llegue a PUENTE-6D (primera llamada real) tendrá un identificador de trazabilidad no vacío, permitiendo correlacionar request y response sin depender del campo `sin_request_id` como fallback silencioso.

---

## 10. Cierre del backlog

| Ítem | Estado |
|---|---|
| B-07 detectado en PUENTE-6C | CONFIRMADO |
| Fix implementado en `cliente_api_real_preparado.py` | CONFIRMADO |
| 13 tests nuevos agregados | CONFIRMADO |
| 339/339 tests pasan | CONFIRMADO |
| Función pura preservada | CONFIRMADO |
| Rama de trabajo | `fix/puente-6b-backlog-validar-request-id` |
| PR abierto | NO — no requerido en este ciclo |
