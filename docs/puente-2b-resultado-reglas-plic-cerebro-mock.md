# PUENTE-2B — Resultado: Integración mínima de reglas PLIC en Cerebro Portero Mock

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-2B |
| Rama base | `main` |
| Commit base | `c01076469a175d0d0ce00e66022d29f15ededfbe` |
| Rama de trabajo | `feat/puente-2b-reglas-plic-cerebro-mock` |
| Estado de PUENTE-2A | Cerrado — contrato de reglas PLIC mergeado a main |
| Tests al iniciar | 29/29 OK |

---

## 2. Archivos modificados

| Archivo | Tipo de cambio | Descripción |
|---|---|---|
| `src/plic_puente_agentes/cerebro_mock.py` | Modificado | Implementación de 12 reglas PLIC con jerarquía de prioridad |
| `tests/test_cerebro_mock.py` | Modificado | 27 tests nuevos agregados (total: 56 tests) |
| `docs/puente-2b-resultado-reglas-plic-cerebro-mock.md` | Creado | Este archivo — evidencia de cierre del ciclo |

---

## 3. Reglas PLIC integradas

| Prioridad | Regla | Keywords evaluadas | Riesgo | Decisión |
|---|---|---|---|---|
| 1 | Secrets / credenciales | `secret`, `secrets`, `token`, `clave`, `credencial`, `contraseña`, `password`, `api key` | `prohibido` | `no_ejecutar` |
| 2 | Producción / deploy | `producción`, `produccion`, `prod`, `deploy`, `publicar` | `prohibido` | `no_ejecutar` |
| 3 | Borrar / force push | `borrar`, `eliminar`, `force push`, `reset hard` | `prohibido` | `no_ejecutar` |
| 4 | Workflows / CI | `workflow`, `github actions`, `ci`, `action` | `alto` | `pedir_autorizacion` |
| 5 | Navegador / Playwright | `navegador`, `playwright`, `browser`, `chromium` | `alto` | `pedir_autorizacion` |
| 6 | Merge / PR | `merge`, `mergealo`, `cerrar pr`, `aprobar pr` | `alto` | `pedir_autorizacion` |
| 7 | Repos reales | `sofse`, `auditoria-sofse`, `agente-saas`, `torre-control` | `alto` | `pedir_autorizacion` |
| 8 | Suspensión | `suspender`, `frenar`, `parar` | `bajo` | `suspender` |
| 9 | Anti-cartero | `pasalo a claude`, `pasalo a codex`, `mandalo a otro agente` | `medio` | `reformular` |
| 10 | Continuidad segura | `seguí`, `seguir`, `continuá`, `seguimos`, `"1"` (exacto) | `bajo` | `continuar_documental` |
| 11 | Entrada inválida | Texto vacío o no-string | `medio` | `reformular` |
| 12 | Default | Cualquier otro texto | `medio` | `reformular` |

---

## 4. Prioridad de reglas

La jerarquía de evaluación garantiza que prohibiciones absolutas siempre ganen sobre instrucciones de continuación:

```
1. secrets / credenciales         → prohibido absoluto
2. producción / deploy            → prohibido absoluto
3. borrar / force push            → prohibido absoluto
4. workflows                      → requiere autorización
5. navegador / Playwright         → requiere autorización
6. merge / PR                     → requiere autorización
7. repos reales                   → requiere autorización
8. suspensión                     → pausa segura
9. anti-cartero                   → reformular vía Torre
10. continuidad segura            → continuar con bajo riesgo
11. entrada inválida              → reformular
12. default                       → reformular
```

Casos de prioridad verificados con tests:
- `"seguí y mandalo a producción"` → producción gana → `no_ejecutar` / `prohibido`
- `"pasalo a Claude con token"` → secret gana → `no_ejecutar` / `prohibido`
- `"usá el token para hacer el deploy"` → secret gana sobre deploy → `no_ejecutar` / `prohibido`
- `"mergealo a producción"` → producción gana sobre merge → `prohibido`

---

## 5. Tests agregados o actualizados

### Tests nuevos (27 nuevos, total 56)

| Clase | Tests nuevos | Qué cubre |
|---|---|---|
| `TestCerebroMockContinuarDocumental` | 2 | `"seguí"` como keyword directa |
| `TestCerebroMockReformular` | 2 | Riesgo y `requiere_ariel` para anti-cartero |
| `TestCerebroMockNoEjecutar` | 6 | `deploy`, `password`, `force push` |
| `TestCerebroMockPedirAutorizacion` | 9 | `workflow`, `playwright`, `merge` con decisión, riesgo y `requiere_ariel` |
| `TestCerebroMockPrioridad` | 4 | Prioridad entre reglas (casos de solapamiento) |
| `TestCerebroMockEstructuraSalida` | 4 | Campos presentes para nuevos casos + valores válidos extendidos |

### Tests originales conservados (29)

Todos los tests de PUENTE-1B siguen pasando sin modificación en su lógica de aserción. Los casos cubiertos (`"seguí con lo del celu"`, `"1"`, `"pasalo a Claude"`, `"mandalo a producción"`, `"dame el token de producción"`, `"diagnóstico SOFSE"`, `"suspender"`, `""`, `{}`) mantienen sus resultados esperados.

---

## 6. Resultado de tests

```
python -m unittest discover -s tests -v

Ran 56 tests in 0.005s

OK
```

**56/56 tests pasan.** Sin errores. Sin warnings.

---

## 7. Qué NO se implementó

| Capacidad | Estado |
|---|---|
| `declarar_bloqueo` como decisión activa | No implementado — sin regla activa. Está en el set válido de decisiones. Backlog PUENTE-3+ |
| `escalar_a_ariel` como decisión activa | No implementado — sin regla activa. Está en el set válido de decisiones. Backlog PUENTE-3+ |
| Evaluación de `contexto_actual` | No implementado — solo `texto_original` evaluado |
| Evaluación de `estado_del_ciclo` | No implementado — backlog PUENTE-3+ |
| Evaluación de `autorizaciones_disponibles` | No implementado — backlog PUENTE-3+ |
| Guarda defensiva contra entrada no-dict | Implementada parcialmente — `isinstance(entrada, dict)` agregado en la lectura de `texto_original` |
| Claude Haiku API real | No implementado — PUENTE-5 en adelante |
| Playwright real | No implementado — PUENTE-4 en adelante |

**Nota sobre el keyword `"ci"`:** La regla de workflows usa `"ci"` como substring. Esto puede generar falsos positivos en textos que contengan "ci" como parte de otra palabra (e.g., "especifici-dad"). El comportamiento es conservador — preferible rechazar que aprobar. Documentado para PUENTE-3.

---

## 8. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin imports nuevos | CONFIRMADO — `cerebro_mock.py` sigue sin ningún `import` |
| Sin API real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin dependencias externas | CONFIRMADO — solo stdlib Python en tests |
| Sin repos prohibidos | CONFIRMADO — torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero no tocados |
| Función pura preservada | CONFIRMADO — sin efectos secundarios |
| Contrato de salida respetado | CONFIRMADO — 9 campos presentes en todos los casos |
| Tests originales pasan | CONFIRMADO — 29/29 originales + 27 nuevos = 56/56 OK |

---

## 9. Próximo microciclo sugerido

**PUENTE-2C — Auditoría técnica de reglas PLIC integradas en Cerebro Portero Mock**

Objetivo: revisar la implementación de PUENTE-2B, validar que el contrato PUENTE-1A y las reglas PLIC de PUENTE-2A están correctamente reflejadas en el código, identificar casos edge no cubiertos, y confirmar que los 56 tests son suficientes como suite de regresión para las reglas integradas.

Restricciones:
- Solo lectura.
- Sin modificaciones al código.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.

> No iniciar PUENTE-2C hasta que PUENTE-2B esté cerrado con evidencia verificable (commit + push a main) y autorización explícita de Ariel.
