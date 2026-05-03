# PUENTE-3B — Resultado: Integración de contexto_actual, estado_del_ciclo y autorizaciones_disponibles en Cerebro Portero Mock

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-3B |
| Rama base | `main` |
| Commit base | `aacd001b0399085f2c30698f2291f119481fbfb3` |
| Rama de trabajo | `feat/puente-3b-contexto-estado-autorizaciones` |
| Estado de PUENTE-3A | Cerrado — contrato documental mergeado a main |
| Tests al iniciar | 56/56 OK |

---

## 2. Archivos modificados

| Archivo | Tipo de cambio | Descripción |
|---|---|---|
| `src/plic_puente_agentes/cerebro_mock.py` | Modificado | 17 reglas con evaluación de contexto, estado y autorizaciones |
| `tests/test_cerebro_mock.py` | Modificado | 30 tests nuevos agregados (total: 86 tests) |
| `docs/puente-3b-resultado-contexto-estado-autorizaciones.md` | Creado | Este archivo — evidencia de cierre del ciclo |

---

## 3. Qué se integró

| Capacidad | Descripción |
|---|---|
| Evaluación de `autorizaciones_disponibles` | 6 nuevas reglas que verifican autorización antes de decidir |
| Evaluación de `estado_del_ciclo` | 2 nuevas reglas que bloquean continuidad en estados incoherentes |
| Evaluación de `contexto_actual` | Subcampo `ultimo_output_portero.opciones_para_ariel` para interpretar "1" |
| Enriquecimiento de `motivo` | El campo `motivo` ahora referencia el campo de contexto que condicionó la decisión |
| Nuevas constantes | `_PALABRAS_API_REAL`, `_PALABRAS_ISSUE_COMENTAR`, `_PALABRAS_ISSUE_CERRAR`, `_AUTORIZACIONES_PROHIBIDAS` |
| Nueva decisión activa | `declarar_bloqueo` — ahora se emite cuando estado es `bloqueado` y se pide continuidad |

### Orden de evaluación (17 prioridades)

```
1.  Secrets / credenciales        → prohibido absoluto (o pedir_autorizacion si tiene autorizacion)
2.  Producción / deploy           → prohibido absoluto (o pedir_autorizacion si tiene autorizacion)
3.  Borrar / force push           → prohibido absoluto
4.  API real                      → no_ejecutar si sin autorización / pedir_autorizacion si autorizado
5.  estado pr_abierto + continuidad → pedir_autorizacion / medio
6.  estado bloqueado + continuidad  → declarar_bloqueo / alto
7.  Workflows / CI                → pedir_autorizacion / alto
8.  Navegador / Playwright        → pedir_autorizacion / alto
9.  Merge / PR                    → pedir_autorizacion / alto (motivo contextualizado)
10. Issue: comentar               → pedir_autorizacion / alto
11. Issue: cerrar                 → pedir_autorizacion / alto
12. Repos reales                  → pedir_autorizacion / alto (motivo con repo_autorizado_actual)
13. Suspensión                    → suspender / bajo
14. Anti-cartero                  → reformular / medio
15. "1" con/sin opciones (si contexto_actual presente) → continuar_documental o reformular
16. Continuidad segura            → continuar_documental / bajo
17. Default                       → reformular / medio
```

---

## 4. Cómo se usa `contexto_actual`

`contexto_actual` se usa en dos puntos:

**a) Subcampo `ultimo_output_portero.opciones_para_ariel` (Prioridad 15):**

Cuando `texto_original` es `"1"` y `contexto_actual` está explícitamente presente como dict:
- Si `ultimo_output_portero` es un dict con `opciones_para_ariel` no vacío → interpretar "1" como elección de la opción 1 → `continuar_documental`/`bajo`
- Si `ultimo_output_portero` es null o `opciones_para_ariel` está vacío → `reformular`/`medio`
- Si `contexto_actual` es null/ausente → "1" cae a la regla de continuidad segura (comportamiento anterior)

**b) Subcampo `repo_autorizado_actual` (Prioridad 12):**

Cuando el texto menciona un repo real externo (SOFSE, agente-saas, etc.), el `motivo` ahora incluye el nombre del repo actualmente autorizado, para que Ariel y Torre sepan exactamente cuál es el conflicto de scope.

---

## 5. Cómo se usa `estado_del_ciclo`

`estado_del_ciclo` se evalúa en Prioridades 5 y 6, antes de las reglas de workflow/merge/repos:

| Estado | Combinado con | Decisión | Riesgo |
|---|---|---|---|
| `pr_abierto` | continuidad (`seguí`, `1`, etc.) | `pedir_autorizacion` | `medio` |
| `bloqueado` | continuidad (`seguí`, `1`, etc.) | `declarar_bloqueo` | `alto` |
| `cerrado` | continuidad (sin bloqueo previo) | `continuar_documental` | `bajo` |
| cualquier otro / ausente | cualquier texto | sin efecto — cae a reglas siguientes | — |

**Regla clave:** Los checks de estado solo se disparan cuando el texto contiene keywords de continuidad. Otras acciones (workflow, merge, producción) no son afectadas por el estado.

---

## 6. Cómo se usa `autorizaciones_disponibles`

El campo es una lista de strings. Se extrae al inicio y se filtran `puede_tocar_produccion` y `puede_tocar_secrets` (son prohibiciones absolutas ignoradas incluso si están presentes).

| Autorización evaluada | Sin autorización | Con autorización |
|---|---|---|
| `puede_tocar_secrets` | `no_ejecutar`/`prohibido` | `pedir_autorizacion`/`alto` |
| `puede_tocar_produccion` | `no_ejecutar`/`prohibido` | `pedir_autorizacion`/`alto` |
| `puede_usar_api_real` | `no_ejecutar`/`prohibido` | `pedir_autorizacion`/`alto` |
| `puede_usar_navegador` | `pedir_autorizacion`/`alto` (motivo sin auth) | `pedir_autorizacion`/`alto` (motivo con auth) |
| `puede_mergear` | `pedir_autorizacion`/`alto` (motivo sin auth) | `pedir_autorizacion`/`alto` (motivo con auth) |
| `puede_comentar_issue` | `pedir_autorizacion`/`alto` (motivo sin auth) | `pedir_autorizacion`/`alto` (motivo con auth) |
| `puede_cerrar_issue` | `pedir_autorizacion`/`alto` (motivo sin auth) | `pedir_autorizacion`/`alto` (motivo con auth) |

**Nota importante:** `puede_tocar_produccion` y `puede_tocar_secrets` son verificados desde `entrada.get("autorizaciones_disponibles")` directamente (antes del filtrado), para poder distinguir entre "sin autorización" y "con autorización pero aún así restringida".

---

## 7. Tests agregados o actualizados

### Tests nuevos (30 nuevos, total 86)

| Clase | Tests nuevos | Qué cubre |
|---|---|---|
| `TestCerebroMockContextoEstado` | 8 | `seguí` + `cerrado`, `pr_abierto`, `bloqueado` — decisión, riesgo, `requiere_ariel` |
| `TestCerebroMockContextoActual` | 5 | `"1"` con/sin `opciones_para_ariel` en `ultimo_output_portero` |
| `TestCerebroMockAutorizaciones` | 17 | merge, issue comentar/cerrar, API real, producción, secrets, SOFSE con repo, prioridad API vs continuidad |

### Tests originales conservados (56)

Los 56 tests de PUENTE-2B siguen pasando sin modificación. Los casos base (`"seguí"`, `"1"`, `"pasalo a Claude"`, `"producción"`, `"SOFSE"`, `"suspender"`, etc.) mantienen sus resultados esperados cuando no hay campos de contexto presentes.

---

## 8. Resultado de tests

```
python -m unittest discover -s tests

Ran 86 tests in 0.003s

OK
```

**86/86 tests pasan.** Sin errores. Sin warnings.

---

## 9. Qué NO se implementó

| Capacidad | Estado |
|---|---|
| `escalar_a_ariel` como decisión activa | No implementado — sin regla activa todavía |
| Evaluación de `ultimo_microciclo` | No implementado — sin regla que lo use |
| Evaluación de `ultimo_pr` | No implementado — sin regla que lo use |
| Evaluación de `ultima_decision` | No implementado — sin regla que lo use |
| Evaluación de `ultimo_bloqueo` | No implementado — sin regla activa |
| Evaluación de `ultimo_mensaje_ariel` | No implementado — sin regla activa |
| Corrección del falso positivo de `"ci"` (backlog B-01) | No implementado — deferred a PUENTE-3C o posterior |
| Corrección del falso positivo de `"prod"` (backlog B-02) | No implementado — deferred a PUENTE-3C o posterior |
| Claude Haiku API real | No implementado — PUENTE-5 en adelante |
| Playwright real | No implementado — PUENTE-4 en adelante |

---

## 10. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin imports nuevos | CONFIRMADO — `cerebro_mock.py` sigue sin ningún `import` |
| Función pura preservada | CONFIRMADO — sin efectos secundarios, sin I/O, sin red |
| Sin API real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin dependencias externas | CONFIRMADO — solo stdlib Python en tests |
| Sin repos prohibidos | CONFIRMADO — torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero no tocados |
| Contrato de salida respetado | CONFIRMADO — 9 campos presentes en todos los casos |
| Tests originales pasan | CONFIRMADO — 56/56 originales + 30 nuevos = 86/86 OK |
| `puede_tocar_produccion` y `puede_tocar_secrets` ignorados | CONFIRMADO — filtrados de `autorizaciones` incluso si aparecen |

---

## 11. Próximo microciclo sugerido

**PUENTE-3C — Auditoría técnica de contexto, estado y autorizaciones integradas en Cerebro Portero Mock**

Objetivo: revisar la implementación de PUENTE-3B, validar que el contrato PUENTE-3A está correctamente reflejado en el código, identificar casos edge no cubiertos, y confirmar que los 86 tests son suficientes como suite de regresión para las reglas de contexto integradas.

Alcance esperado:
- Solo lectura.
- Sin modificaciones al código.
- Sin modificaciones a tests.
- Auditar el orden de evaluación de las 17 reglas.
- Auditar los casos edge de `contexto_actual`, `estado_del_ciclo` y `autorizaciones_disponibles`.
- Identificar backlog para PUENTE-4 y posteriores.

Restricciones:
- Solo lectura.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.
- Sin secrets.
- Sin producción.

> No iniciar PUENTE-3C hasta que PUENTE-3B esté cerrado con evidencia verificable (commit + push a main) y autorización explícita de Ariel.
