# PUENTE-4A — Resultado: Contrato de Mano Local Simulada

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-4A |
| Rama base | `main` |
| Commit base | `cb26fe99e68ed461ddd071b19b24f35b878a3e0d` |
| Rama de trabajo | `docs/puente-4a-contrato-mano-local-simulada` |
| Estado de PUENTE-3C-BACKLOG | Cerrado en main — 98 tests OK |
| Tests al iniciar | 98/98 OK |

---

## 2. Contrato creado

| Archivo | Tipo | Descripción |
|---|---|---|
| `docs/mano-local-simulada.md` | Creado | Contrato completo de la mano local simulada |
| `docs/puente-4a-resultado-contrato-mano-local-simulada.md` | Creado | Este archivo — evidencia de cierre del ciclo |

---

## 3. Qué queda habilitado

| Capacidad | Estado |
|---|---|
| Definición de la mano local como componente del sistema PLIC | HABILITADO |
| Diferenciación entre Cerebro, Torre, Mano local y Ejecutor externo | HABILITADO |
| Contrato de entrada (6 campos) | HABILITADO |
| Contrato de salida (8 campos) | HABILITADO |
| 6 acciones simulables definidas | HABILITADO |
| 8 casos mínimos documentados | HABILITADO |
| Criterios para iniciar PUENTE-4B | HABILITADO |

---

## 4. Qué NO queda habilitado

| Capacidad | Estado |
|---|---|
| Implementación de `mano_local_mock.py` | NO — deferred a PUENTE-4B |
| Tests para la mano local | NO — deferred a PUENTE-4B |
| Conexión con navegador real | NO — deferred a PUENTE-5+ |
| Uso de Playwright real | NO — deferred a PUENTE-5+ |
| Uso de API real | NO — requiere autorización explícita de Torre |
| Acciones sobre repos externos | NO — prohibición absoluta |
| Corrección de B-04 y B-05 del backlog | NO — deferred (ver sección 11) |

---

## 5. Tabla de entradas

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `decision_del_cerebro` | `str` | Sí | Decisión del `cerebro_mock`: `continuar_documental`, `reformular`, `pedir_autorizacion`, `no_ejecutar`, `declarar_bloqueo`, `suspender` |
| `accion_segura_sugerida` | `str` | Sí | Acción concreta sugerida por Cerebro o Torre |
| `contexto_actual` | `dict \| None` | No | Contexto del ciclo actual |
| `repo_autorizado` | `str \| None` | No | Repo en scope actual |
| `autorizaciones_disponibles` | `list[str]` | No | Autorizaciones activas para este ciclo |
| `modo_simulado` | `bool` | Sí | `True` en PUENTE-4. `False` habilitará ejecutores reales en el futuro |

---

## 6. Tabla de salidas

| Campo | Tipo | Descripción |
|---|---|---|
| `accion_simulada` | `str` | Nombre de la acción que se simularía |
| `destino_simulado` | `str` | Destino de la acción (`claude_api`, `github_issue`, etc.) |
| `payload_simulado` | `dict` | Contenido estructurado que se enviaría al destino |
| `resultado_simulado` | `str` | Descripción del resultado esperado |
| `requiere_autorizacion` | `bool` | `True` si se necesita confirmación antes de ejecutar en real |
| `bloqueo` | `bool` | `True` si la mano local no puede proceder |
| `motivo` | `str` | Explicación del resultado |
| `evidencia` | `dict` | Registro auditado de la operación |

---

## 7. Tabla de acciones simulables

| Acción | `accion_simulada` | `destino_simulado` |
|---|---|---|
| Preparar prompt para Claude | `preparar_prompt_claude` | `claude_api` |
| Preparar prompt para Codex | `preparar_prompt_codex` | `codex_api` |
| Preparar comentario de PR | `preparar_comentario_pr` | `github_pr` |
| Preparar comentario de issue | `preparar_comentario_issue` | `github_issue` |
| Preparar reporte de auditoría | `preparar_reporte_auditoria` | `registro_local` |
| Preparar orden para ejecutor | `preparar_orden_ejecutor` | `ejecutor_externo` |

---

## 8. Tabla de acciones prohibidas

| Acción prohibida | Razón |
|---|---|
| Abrir navegador | Fuera de scope hasta PUENTE-5+ |
| Usar Playwright real | Fuera de scope hasta PUENTE-5+ |
| Usar API real | Requiere autorización explícita de Torre |
| Comentar issue real | Acción externa irreversible |
| Cerrar issue real | Acción externa irreversible |
| Abrir PR real | Solo Torre autoriza |
| Mergear PR real | Solo Torre autoriza |
| Tocar producción | Prohibición absoluta |
| Tocar secrets | Prohibición absoluta |
| Escribir en repos prohibidos | torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero |
| Ejecutar comandos externos | Sin subprocess, sin shell, sin I/O |

---

## 9. Riesgos

| Riesgo | Mitigación |
|---|---|
| Confundir simulación con ejecución real | `modo_simulado: True` es obligatorio en PUENTE-4; la implementación de PUENTE-4B debe verificar este campo antes de cualquier acción |
| Acción simulada con efecto lateral no previsto | La mano local es función pura: sin I/O, sin red, sin subprocess; lo mismo que `cerebro_mock` |
| Scope creep hacia ejecución real | Prohibición absoluta documentada en sección 9; cualquier intento de acción real debe ser bloqueado y reportado |
| Falsa sensación de completitud | PUENTE-4B es necesario — este contrato es solo la especificación, no la implementación |

---

## 10. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin código modificado | CONFIRMADO — no se tocó `cerebro_mock.py` |
| Sin tests modificados | CONFIRMADO — no se tocó `test_cerebro_mock.py` |
| Sin imports nuevos | CONFIRMADO — este ciclo es solo documental |
| Sin API real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin dependencias instaladas | CONFIRMADO |
| Sin repos prohibidos tocados | CONFIRMADO — torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero no tocados |
| Tests existentes pasan | CONFIRMADO — 98/98 OK |
| Contrato de salida del Cerebro respetado | CONFIRMADO — este contrato extiende, no reemplaza |

---

## 11. Backlog pendiente

| Ítem | Estado |
|---|---|
| B-04: `estado suspendido` + continuidad — sin regla dedicada en `cerebro_mock` | Deferred — no abordado en PUENTE-4A |
| B-05: `estado mergeado` + continuidad — sin regla dedicada en `cerebro_mock` | Deferred — no abordado en PUENTE-4A |

Estos ítems pertenecen al backlog del Cerebro Portero, no de la Mano Local. Deberán abordarse en un microciclo específico (PUENTE-3D-B o equivalente) con autorización explícita de Ariel/Torre.

---

## 12. Próximo microciclo sugerido

**PUENTE-4B — Mock técnico de mano local simulada, sin navegador real**

Objetivo: implementar `mano_local_mock.py` como función pura (sin imports externos, sin I/O, sin efectos secundarios) que recibe la entrada definida en este contrato y produce la salida definida en este contrato. Agregar tests que cubran los 8 casos mínimos de la sección 10 de `mano-local-simulada.md`.

Alcance:
- Crear `src/plic_puente_agentes/mano_local_mock.py`.
- Crear tests en `tests/test_mano_local_mock.py`.
- Cubrir los 8 casos mínimos.
- Sin navegador real.
- Sin Playwright.
- Sin API real.
- Sin Claude Haiku real.
- Sin secrets.
- Sin producción.

Restricciones:
- No modificar `cerebro_mock.py`.
- No modificar `test_cerebro_mock.py`.
- Sin repos prohibidos.
- Sin dependencias externas.

> No iniciar PUENTE-4B hasta que PUENTE-4A esté cerrado con evidencia verificable (commit + push a main) y autorización explícita de Ariel.
