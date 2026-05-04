# PUENTE-6D-MODELO-FIX — Resultado: Actualización de modelo autorizado

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6D-MODELO-FIX |
| Rama base | `main` |
| Commit base | `f5ce60b` (PUENTE-6D-MODELO diagnóstico incluido) |
| Rama de trabajo | `feat/puente-6d-modelo-fix` |
| Tests al iniciar | 416/416 OK |
| Autorización de Ariel | "Autorizo PUENTE-6D-MODELO-FIX, sin llamada real." |

---

## 2. Bloqueo resuelto

| Campo | Valor |
|---|---|
| Modelo anterior (retirado) | `claude-3-5-haiku-latest` |
| Modelo alternativo anterior (retirado) | `claude-3-haiku-20240307` |
| Modelo nuevo autorizado | `claude-haiku-4-5-20251001` |
| Fuente | Documentación pública de Anthropic — Model Deprecations |
| Tipo de cambio | Solo constante de modelo — sin cambio de lógica |

---

## 3. Archivos modificados

| Archivo | Tipo | Cambio |
|---|---|---|
| `src/plic_puente_agentes/cliente_api_real_bloqueado.py` | Código Python | `_MODELO_AUTORIZADO` actualizado |
| `src/plic_puente_agentes/cliente_api_real_preparado.py` | Código Python | `_MODELOS_PERMITIDOS` actualizado |
| `tests/test_cliente_api_real_bloqueado.py` | Tests | 3 referencias al modelo actualizadas |
| `tests/test_cliente_api_real_preparado.py` | Tests | 3 referencias y 1 test semántico actualizado |
| `docs/puente-6d-a-contrato-operativo-primera-llamada-real.md` | Documental | Tabla de modelos actualizada |
| `docs/puente-6d-a-checklist-ejecucion-primera-llamada-real.md` | Documental | Bloque 5.1 actualizado |
| `docs/puente-6d-checklist-previo-primera-llamada-real.md` | Documental | Sección 6.4 y sección 7 actualizadas |
| `docs/puente-6d-modelo-previo-llamada-real.md` | Documental | Encabezado de estado actualizado (RESUELTO) |
| `docs/puente-6d-modelo-fix-resultado.md` | Documental | Este archivo — resultado del microciclo |

**Total: 9 archivos — 8 modificados + 1 creado.**

---

## 4. Detalle de cambios en código

### `cliente_api_real_bloqueado.py`

```python
# Antes:
_MODELO_AUTORIZADO = "claude-3-5-haiku-latest"

# Después:
_MODELO_AUTORIZADO = "claude-haiku-4-5-20251001"
```

Sin cambio en lógica. El gate sigue bloqueando llamada real estructuralmente. `llamada_real_ejecutada=False` y `llamada_real_bloqueada=True` son invariantes no afectadas.

### `cliente_api_real_preparado.py`

```python
# Antes:
_MODELOS_PERMITIDOS = (
    "claude-3-5-haiku-latest",
    "claude-3-haiku-20240307",
)

# Después:
_MODELOS_PERMITIDOS = (
    "claude-haiku-4-5-20251001",
)
```

Los dos modelos anteriores fueron retirados por Anthropic. Solo el modelo activo queda autorizado.

---

## 5. Detalle de cambios en tests

### `test_cliente_api_real_bloqueado.py`

| Línea | Cambio |
|---|---|
| `_ENTRADA_BASE["modelo"]` | `claude-3-5-haiku-latest` → `claude-haiku-4-5-20251001` |
| `test_caso_valido_modelo_en_salida` | assertEqual con `claude-haiku-4-5-20251001` |
| `test_no_modifica_cliente_api_real_preparado` | modelo en llamada de aislamiento actualizado |
| `test_modelo_haiku_3_bloquea` | Sin cambio — `claude-3-haiku-20240307` sigue siendo rechazado |

### `test_cliente_api_real_preparado.py`

| Línea | Cambio |
|---|---|
| `_ENTRADA_BASE["modelo"]` | `claude-3-5-haiku-latest` → `claude-haiku-4-5-20251001` |
| `test_modelo_haiku_latest_pasa` → `test_modelo_haiku_4_5_pasa` | Renombrado; modelo actualizado |
| `test_modelo_haiku_fecha_pasa` → `test_modelo_haiku_3_fecha_bloquea` | Semántica invertida: `claude-3-haiku-20240307` ahora es rechazado |
| `test_caso_valido_modelo_en_salida` | assertEqual con `claude-haiku-4-5-20251001` |

---

## 6. Resultado de tests

```
python -m unittest discover -s tests
Ran 416 tests in 0.019s
OK
```

| Tests originales antes del fix | Tests después del fix | Total |
|---|---|---|
| 416 | 416 | **416/416 OK** |

Sin tests eliminados. Sin tests nuevos. Mismo conteo — solo actualizadas las aserciones de modelo.

---

## 7. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin llamada real | CONFIRMADO |
| Sin API real | CONFIRMADO |
| Sin SDK real | CONFIRMADO |
| Sin API keys pedidas ni leídas | CONFIRMADO |
| Sin `.env` | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin dependencias instaladas | CONFIRMADO |
| Sin repos prohibidos tocados | CONFIRMADO |
| Sin cambio de lógica | CONFIRMADO — solo constante de modelo |
| `llamada_real_ejecutada` invariante preservada | CONFIRMADO — siempre `False` |
| `llamada_real_bloqueada` invariante preservada | CONFIRMADO — siempre `True` |
| `cerebro_mock.py` no modificado | CONFIRMADO |
| `mano_local_simulada.py` no modificada | CONFIRMADO |
| `cliente_haiku_fake.py` no modificado | CONFIRMADO |

---

## 8. Estado post-fix

| Ítem | Estado |
|---|---|
| Bloqueo PUENTE-6D-MODELO | RESUELTO |
| Modelo autorizado para PUENTE-6D real | `claude-haiku-4-5-20251001` |
| Gate de llamada real | Activo — bloqueo estructural preservado |
| Checklist PUENTE-6D-A | Actualizado — modelo corregido |
| Primera llamada real | Suspendida hasta nueva instrucción explícita de Ariel |

---

## 9. Próximo microciclo sugerido

**Auditoría read-only de PUENTE-6D-MODELO-FIX** — verificar que los cambios son mínimos, que no se modificó lógica fuera del modelo, que los tests siguen pasando, y emitir dictamen A) APTO antes de PR.

> No iniciar PUENTE-6D real hasta que PUENTE-6D-MODELO-FIX esté cerrado en `main` con evidencia verificable y nueva instrucción explícita de Ariel para ejecutar la primera llamada real con el modelo `claude-haiku-4-5-20251001`.
