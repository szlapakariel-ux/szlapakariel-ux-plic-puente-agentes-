# PUENTE-4Z — Cierre de fase mock: Cerebro + Mano Local Simulada

## 1. Nombre del cierre

**PUENTE-4Z — Cierre de fase mock**

Consolida el estado completo del Cerebro Portero Mock y la Mano Local Simulada antes de cualquier avance hacia PUENTE-5.

---

## 2. Objetivo del cierre

Documentar de forma verificable y auditable que:

- El Cerebro Portero Mock está completo, seguro y estable.
- La Mano Local Simulada está completa, segura y estable.
- Todos los backlogs conocidos de la fase mock fueron cerrados.
- El sistema de 173 tests cubre correctamente ambos módulos.
- No quedan decisiones pendientes que bloqueen el avance hacia PUENTE-5.
- Las prohibiciones absolutas siguen vigentes y no fueron violadas.

Este cierre NO habilita PUENTE-5 de forma automática. PUENTE-5 requiere autorización explícita de Ariel y contrato documental propio.

---

## 3. Estado de main usado como base

| Campo | Valor |
|---|---|
| Commit base | `3a3a4c4` |
| Mensaje del commit | `fix(puente): corregir estados suspendido y mergeado en cerebro mock` |
| Tests en ese commit | 173/173 OK |
| Microciclos cerrados previos | PUENTE-0 a PUENTE-4D-BACKLOG |

---

## 4. Lista de microciclos cerrados

| Microciclo | Descripción | Estado |
|---|---|---|
| PUENTE-0 | Bootstrap inicial del repo | CERRADO |
| PUENTE-1A | Contrato del Cerebro Portero Mock | CERRADO |
| PUENTE-1B | Implementación del Cerebro Mock (función pura) | CERRADO |
| PUENTE-1C | Auditoría técnica del Cerebro Mock | CERRADO |
| PUENTE-2A | Contrato de reglas PLIC | CERRADO |
| PUENTE-2B | Integración de reglas PLIC en Cerebro Mock | CERRADO |
| PUENTE-3A | Contrato de contexto, estado y autorizaciones | CERRADO |
| PUENTE-3B | Integración de contexto/estado/autorizaciones en Cerebro Mock | CERRADO |
| PUENTE-3C-BACKLOG | Corrección de falsos positivos ci/prod/action en Cerebro Mock | CERRADO |
| PUENTE-4A | Contrato de Mano Local Simulada | CERRADO |
| PUENTE-4B | Implementación de Mano Local Simulada (función pura) | CERRADO |
| PUENTE-4C | Auditoría técnica de Mano Local Simulada | CERRADO (APTO CON OBSERVACIONES → backlog generado) |
| PUENTE-4C-BACKLOG | Corrección de falsos positivos prod/pr/issue en Mano Local | CERRADO |
| PUENTE-4D | Auditoría técnica de estados suspendido/mergeado | CERRADO (APTO PARA PR) |
| PUENTE-4D-BACKLOG | Corrección de estados suspendido y mergeado en Cerebro Mock | CERRADO |
| PUENTE-4E | Auditoría técnica de B-04/B-05 | CERRADO (APTO PARA PR) |

---

## 5. Estado del Cerebro Portero Mock

### Qué evalúa

La función `cerebro_mock(entrada: dict) -> dict` recibe texto libre de Ariel y contexto estructurado, y lo evalúa contra 17 reglas de prioridad para producir una decisión estructurada y auditable.

### Decisiones soportadas

| Decisión | Cuándo |
|---|---|
| `no_ejecutar` | Texto contiene términos prohibidos (secrets, producción, borrado, API real sin autorización) |
| `pedir_autorizacion` | Texto requiere intervención explícita (workflows, navegador, merge, issue, repos externos, ciclo suspendido) |
| `reformular` | Texto vacío, anti-cartero, o texto no clasificable |
| `suspender` | Texto solicita pausa explícita del ciclo |
| `declarar_bloqueo` | Estado del ciclo es `bloqueado` + continuidad |
| `continuar_documental` | Continuidad segura (cerrado, mergeado, o sin estado sensible) |

### Riesgos soportados

| Riesgo | Significado |
|---|---|
| `prohibido` | Acción absolutamente vetada — no se ejecuta bajo ninguna circunstancia |
| `alto` | Requiere autorización explícita antes de proceder |
| `medio` | Requiere revisión y confirmación de contexto |
| `bajo` | Puede continuar documentalmente con supervisión de Torre |

### Reglas PLIC incorporadas (17 prioridades en orden)

1. Secrets y credenciales → `no_ejecutar / prohibido`
2. Producción y deploy → `no_ejecutar / prohibido` (con excepción si autorización disponible → `pedir_autorizacion / alto`)
3. Borrar / force push / reset hard → `no_ejecutar / prohibido`
4. API real → `no_ejecutar / prohibido` (con excepción si autorización disponible → `pedir_autorizacion / alto`)
5. Estado `pr_abierto` + continuidad → `pedir_autorizacion / medio`
6. Estado `bloqueado` + continuidad → `declarar_bloqueo / alto`
7. Workflows y CI → `pedir_autorizacion / alto`
8. Navegador / Playwright → `pedir_autorizacion / alto`
9. Merge / PR → `pedir_autorizacion / alto`
10. Issue: comentar → `pedir_autorizacion / alto`
11. Issue: cerrar → `pedir_autorizacion / alto`
12. Repos externos (sofse, agente-saas, torre-control) → `pedir_autorizacion / alto`
13. Suspensión → `suspender / bajo`
14. Anti-cartero → `reformular / medio`
15. Estado `suspendido` + continuidad → `pedir_autorizacion / medio` *(B-04)*
16. "1" con contexto y opciones previas → `continuar_documental / bajo`
17. Continuidad segura (incluye `cerrado` y `mergeado`) → `continuar_documental / bajo` *(B-05)*
18. Default → `reformular / medio`

### Cómo usa `contexto_actual`

- Extrae `contexto_actual.ultimo_output_portero.opciones_para_ariel` para interpretar "1" como selección de opción previa.
- Extrae `contexto_actual.repo_autorizado_actual` para personalizar el motivo en repos externos.

### Cómo usa `estado_del_ciclo`

| Estado | Efecto |
|---|---|
| `pr_abierto` | Bloquea continuidad hasta resolver el PR (Prioridad 5) |
| `bloqueado` | Fuerza declarar_bloqueo (Prioridad 6) |
| `suspendido` | Bloquea continuidad automática — pide autorización (Prioridad 15 / B-04) |
| `mergeado` | Permite continuar con motivo específico (Prioridad 17 / B-05) |
| `cerrado` | Permite continuar con motivo de ciclo completo (Prioridad 17) |
| Ninguno / otro | Reglas genéricas aplicables |

### Cómo usa `autorizaciones_disponibles`

- `puede_tocar_secrets` → eleva `no_ejecutar` a `pedir_autorizacion/alto` para secrets (prohibición no superable automáticamente).
- `puede_tocar_produccion` → eleva `no_ejecutar` a `pedir_autorizacion/alto` para producción.
- `puede_usar_api_real` → eleva `no_ejecutar` a `pedir_autorizacion/alto` para API real.
- `puede_mergear` → personaliza motivo de merge.
- `puede_comentar_issue` → personaliza motivo de comentar issue.
- `puede_cerrar_issue` → personaliza motivo de cerrar issue.
- `puede_usar_navegador` → personaliza motivo de navegador.
- `puede_tocar_produccion` y `puede_tocar_secrets` están en `_AUTORIZACIONES_PROHIBIDAS` — se filtran de la lista efectiva y no pueden eludir las reglas 1 y 2.

---

## 6. Estado de la Mano Local Simulada

### Qué recibe

La función `mano_local_simulada(entrada: dict) -> dict` recibe 6 campos:

| Campo | Tipo | Obligatorio |
|---|---|---|
| `decision_del_cerebro` | `str` | Sí |
| `accion_segura_sugerida` | `str` | Sí |
| `contexto_actual` | `dict \| None` | No |
| `repo_autorizado` | `str \| None` | No |
| `autorizaciones_disponibles` | `list[str]` | No |
| `modo_simulado` | `bool` | Sí — debe ser `True` |

### Qué devuelve

8 campos de salida:

| Campo | Tipo |
|---|---|
| `accion_simulada` | `str` |
| `destino_simulado` | `str` |
| `payload_simulado` | `dict` |
| `resultado_simulado` | `str` |
| `requiere_autorizacion` | `bool` |
| `bloqueo` | `bool` |
| `motivo` | `str` |
| `evidencia` | `dict` |

### Qué acciones simula

| Acción simulada | Destino | Cuándo |
|---|---|---|
| `preparar_prompt_claude` | `claude_api` | `accion_sugerida` menciona "claude" |
| `preparar_prompt_codex` | `codex_api` | `accion_sugerida` menciona "codex" |
| `preparar_comentario_pr` | `github_pr` | `accion_sugerida` tiene frase PR o token "pr" aislado |
| `preparar_comentario_issue` | `github_issue` | `accion_sugerida` tiene token "issue" aislado |
| `preparar_orden_documental` | `ejecutor_simulado` | `decision: continuar_documental` sin acción específica |
| `preparar_prompt_reformulado` | `torre` | `decision: reformular` |
| `preparar_solicitud_autorizacion` | `torre` | `decision: pedir_autorizacion` |
| `suspender_ciclo` | `registro_local` | `decision: suspender` |
| `registrar_bloqueo` | `registro_local` | `decision: declarar_bloqueo` |
| `no_accion` | `ninguno` | `decision: no_ejecutar` |

### Qué bloquea (`bloqueo: True`)

- `modo_simulado` no es `True` (Regla 1)
- Texto contiene palabras peligrosas: produccion, producción, secret, secrets, token, workflow, navegador, playwright, api real (Regla 9, por substring)
- Texto contiene "prod" como token aislado (Regla 9, con `_es_token()`)
- `decision: no_ejecutar` (Regla 2)
- `decision: declarar_bloqueo` (Regla 6)
- Decisión desconocida (default)

### Qué nunca ejecuta

- Llamadas HTTP o de red (cero imports, cero I/O)
- Comandos externos (sin subprocess)
- Lectura de archivos o variables de entorno
- Comentarios reales en issues
- PRs reales
- Merges reales
- Acciones en producción
- Uso de secrets o tokens reales

---

## 7. Backlogs cerrados

| Backlog | Descripción | Estado |
|---|---|---|
| B-01 (Cerebro) | `"ci"` disparaba workflows para palabras como "microciclo", "acción", "servicio activo" | CERRADO — `_es_token()` verifica límite de palabra |
| B-02 (Cerebro) | `"prod"` disparaba producción para palabras como "producto", "producir", "reproducir" | CERRADO — `_TOKENS_PRODUCCION` + `_es_token()` |
| B-03 (Cerebro) | `"action"` disparaba workflows para palabras con "action" interno | CERRADO — eliminado de keywords; `"github action"` detectado como frase completa |
| B-ML-01 (Mano) | `"prod"` bloqueaba "producir", "reproducir", "producto" | CERRADO — `_TOKENS_PELIGROSOS` + `_es_token()` |
| B-ML-02 (Mano) | `"pr"` mapeaba "preparar", "comprimir", "propuesta" a PR | CERRADO — `_FRASES_PR` + `_es_token(accion_lower, "pr")` |
| B-ML-03 (Mano) | `"issue"` como substring podía mapear "tissue" a issue | CERRADO — `_es_token(accion_lower, "issue")` |
| B-04 (Cerebro) | `estado suspendido` + continuidad → `continuar_documental` incorrecto | CERRADO — nueva regla Prioridad 15: `pedir_autorizacion / medio` |
| B-05 (Cerebro) | `estado mergeado` + continuidad → motivo genérico sin contexto | CERRADO — `elif estado == "mergeado"` en Prioridad 17 con motivo específico |

---

## 8. Tests

| Métricas | Valor |
|---|---|
| Total de tests | 173 |
| Resultado | **173/173 OK** |
| Tiempo de ejecución | ~0.004s |
| Framework | `unittest` (stdlib, sin dependencias externas) |

### Qué cubren

| Clase de tests | Tests | Qué cubre |
|---|---|---|
| `TestCerebroMockContinuarDocumental` | 7 | Continuidad básica: seguí, 1, celu |
| `TestCerebroMockReformular` | 7 | Texto vacío, anti-cartero, entrada inválida |
| `TestCerebroMockNoEjecutar` | 11 | Producción, secrets, deploy, force push |
| `TestCerebroMockPedirAutorizacion` | 12 | SOFSE, workflow, Playwright, merge |
| `TestCerebroMockSuspender` | 3 | Suspensión explícita |
| `TestCerebroMockPrioridad` | 4 | Prioridades entre reglas |
| `TestCerebroMockEstructuraSalida` | 14 | Campos requeridos, decisiones y riesgos válidos |
| `TestCerebroMockContextoEstado` | 8 | pr_abierto, bloqueado, cerrado con continuidad |
| `TestCerebroMockContextoActual` | 5 | "1" con/sin opciones previas |
| `TestCerebroMockAutorizaciones` | 16 | Autorizaciones disponibles para merge, issue, api, producción, secrets |
| `TestCerebroMockFalsoPositivos` | 12 | B-01/B-02/B-03 — ci/prod/action |
| `TestCerebroMockEstadosSuspendidoMergeado` | 23 | B-04/B-05 — suspendido/mergeado |
| `TestManoLocalSimuladaModoSimulado` | 3 | modo_simulado False/None/ausente |
| `TestManoLocalSimuladaNoEjecutar` | 2 | no_ejecutar |
| `TestManoLocalSimuladaPedirAutorizacion` | 2 | pedir_autorizacion |
| `TestManoLocalSimuladaReformular` | 1 | reformular |
| `TestManoLocalSimuladaContinuarDocumental` | 1 | continuar_documental |
| `TestManoLocalSimuladaDeclararBloqueo` | 1 | declarar_bloqueo |
| `TestManoLocalSimuladaSuspender` | 1 | suspender |
| `TestManoLocalSimuladaAccionesExternas` | 4 | Claude/Codex/issue/PR como payload simulado |
| `TestManoLocalSimuladaTerminosRestringidos` | 6 | producción/secrets/token/playwright/navegador |
| `TestManoLocalSimuladaEstructura` | 9 | 8 campos requeridos |
| `TestManoLocalSimuladaAislamientoYRegresion` | 7 | Sin red, sin subprocess, sin efectos en cerebro_mock |
| `TestManoLocalFalsoPositivos` | 15 | B-ML-01/B-ML-02/B-ML-03 |

---

## 9. Qué queda habilitado

| Capacidad | Estado |
|---|---|
| Uso del Cerebro Portero Mock | HABILITADO — función pura, sin imports |
| Uso de la Mano Local Simulada | HABILITADO — función pura, sin imports |
| Simulación de decisiones PLIC | HABILITADO |
| Preparación de payloads simulados (Claude, Codex, PR, issue, documental) | HABILITADO |
| Auditoría documental | HABILITADO |
| Tests de regresión | HABILITADO — 173 tests |
| Iteración documental y corrección de backlogs | HABILITADO |
| Planificación de PUENTE-5 (contrato previo) | HABILITADO — solo si Ariel autoriza |

---

## 10. Qué NO queda habilitado

| Capacidad | Estado |
|---|---|
| API real (Claude Haiku, Codex, cualquier endpoint) | NO HABILITADO — prohibición absoluta hasta PUENTE-5+ con contrato |
| Claude Haiku real | NO HABILITADO |
| Navegador real | NO HABILITADO — requiere ciclo específico PUENTE-5+ |
| Playwright real | NO HABILITADO — requiere ciclo específico PUENTE-5+ |
| Secrets o API keys reales | NO HABILITADO — prohibición absoluta |
| Producción | NO HABILITADO — prohibición absoluta |
| Workflows de CI/CD | NO HABILITADO — requiere autorización explícita |
| Automatización externa sin supervisión | NO HABILITADO |
| Comentarios reales en issues de GitHub | NO HABILITADO — solo payload simulado |
| PRs automáticos sin autorización | NO HABILITADO |
| Merges automáticos sin autorización | NO HABILITADO |
| Ejecución autónoma sin ciclo documental | NO HABILITADO |
| Tocar torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero | NO HABILITADO — prohibición absoluta |

---

## 11. Riesgos residuales

| Riesgo | Descripción | Mitigación |
|---|---|---|
| Confusión simulación/real | Alguien podría asumir que los payloads simulados se ejecutan realmente | `modo_simulado: True` es obligatorio; la función bloquea si es False |
| Scope creep hacia PUENTE-5 prematuro | Avanzar a API real sin contrato propio | PUENTE-5 requiere contrato documental previo y autorización de Ariel |
| Keyword no cubierta en Cerebro | Un texto nuevo podría caer en default en lugar de regla específica | 173 tests de regresión; auditoría por microciclo |
| Estado del ciclo no reconocido | Un estado nuevo (ej. "en_revision") cae en continuidad genérica | Documentado en contrato; requiere backlog específico si aparece |
| `"seguimos"` con estado suspendido | No testeado explícitamente (cubierto por lógica pero no por test dedicado) | Pendiente como backlog menor para PUENTE-5 o posterior |

---

## 12. Dictamen de cierre de fase

**FASE MOCK — CERRADA**

El Cerebro Portero Mock y la Mano Local Simulada están completos, auditados, sin backlogs pendientes conocidos, y con 173 tests que pasan. Ambos son funciones puras sin imports, sin I/O, sin red, sin subprocess. Las prohibiciones absolutas (API real, Haiku real, navegador, Playwright, secrets, producción) fueron respetadas en todos los microciclos.

El sistema está en condición de avanzar hacia PUENTE-5, sujeto a:
- Autorización explícita de Ariel.
- Contrato documental propio (PUENTE-5A).
- Sin saltear la fase de contrato.
- Sin mezclar en el primer ciclo de PUENTE-5: Haiku real + navegador + automatización externa.

> No iniciar PUENTE-5 hasta que PUENTE-4Z esté cerrado en main y Ariel haya dado autorización explícita.
