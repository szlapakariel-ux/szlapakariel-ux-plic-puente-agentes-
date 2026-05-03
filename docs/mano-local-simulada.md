# Contrato: Mano Local Simulada — PUENTE-4A

## 1. Nombre del contrato

**Mano Local Simulada** — componente de transporte de órdenes estructuradas en el sistema PLIC / Portero Local, operando en modo simulado sin navegador real ni acciones externas.

---

## 2. Objetivo de la mano local

La mano local es el componente que toma una decisión ya estructurada por el Cerebro Portero y la convierte en una acción concreta (o en la preparación de esa acción). En modo simulado, no ejecuta nada: produce la representación de lo que ejecutaría, de forma auditada y reversible.

---

## 3. Diferencia entre componentes

| Componente | Rol | Decide | Ejecuta |
|---|---|---|---|
| **Cerebro Portero** | Evalúa intención, riesgo y autorización | Sí — emite `decision` y `riesgo` | No |
| **Torre** | Coordina microciclos, valida scope y autoriza | Sí — autoriza o bloquea avance | No directamente |
| **Mano local** | Transporta la orden estructurada al destino | No — solo transporta | Sí (real) / Simula (mock) |
| **Ejecutor externo** | Herramienta real que recibe la orden | No | Sí — acción real (navegador, API, CLI) |

**Principio clave:** La mano local no decide, no inventa y no improvisa. Ejecuta o simula exactamente lo que el Cerebro ya autorizó.

---

## 4. Qué problema resuelve

### Problema: Ariel como cartero manual

En el estado actual, cuando el Cerebro Portero emite una decisión (`continuar_documental`, `pedir_autorizacion`, etc.), Ariel debe manualmente:

- copiar el output del Portero;
- pegarlo en la herramienta correcta (Claude, Codex, GitHub, etc.);
- ejecutar la acción;
- copiar el resultado;
- pegarlo de vuelta al flujo.

Este ciclo manual es la causa raíz del problema anti-cartero.

### Solución: la mano local como puente

La mano local resuelve tres puntos específicos:

| Problema | Solución |
|---|---|
| Copiar/pegar manual de outputs | La mano local transporta la orden directamente al destino |
| Pérdida de trazabilidad | Cada acción simulada o real queda registrada en `evidencia` |
| Preparación para herramientas futuras | El contrato simulado define la interfaz antes de conectar ejecutores reales |

---

## 5. Definición de mano local simulada

En PUENTE-4, la mano local opera **exclusivamente en modo simulado**:

- **No abre navegador.**
- **No usa Playwright real.**
- **No toca herramientas externas reales.**
- **No ejecuta acciones con efecto en sistemas externos.**
- **No comenta issues reales.**
- **No crea PRs reales.**
- **No escribe en repos externos.**

En cambio, **simula la intención, la acción y el resultado**:

- Recibe la decisión del Cerebro.
- Construye la representación de lo que haría.
- Devuelve un payload auditado con `resultado_simulado`.
- Marca `requiere_autorizacion` si la acción necesita confirmación antes de ejecutarse en real.

---

## 6. Entrada esperada

| Campo | Tipo | Descripción |
|---|---|---|
| `decision_del_cerebro` | `str` | Decisión emitida por `cerebro_mock`: `continuar_documental`, `reformular`, `pedir_autorizacion`, `no_ejecutar`, `declarar_bloqueo`, `suspender` |
| `accion_segura_sugerida` | `str` | Acción concreta sugerida por el Cerebro o por Torre (ej: `"preparar prompt para Claude"`) |
| `contexto_actual` | `dict \| None` | Contexto del ciclo actual: `ultimo_output_portero`, `estado_del_ciclo`, `repo_autorizado_actual`, etc. |
| `repo_autorizado` | `str \| None` | Repo en scope actual (ej: `"szlapakariel-ux-plic-puente-agentes-"`) |
| `autorizaciones_disponibles` | `list[str]` | Lista de autorizaciones activas para este ciclo |
| `modo_simulado` | `bool` | Siempre `True` en PUENTE-4. Cuando sea `False` en el futuro, se conectará a ejecutores reales |

---

## 7. Salida esperada

| Campo | Tipo | Descripción |
|---|---|---|
| `accion_simulada` | `str` | Nombre de la acción que se simularía (ej: `"preparar_prompt_claude"`) |
| `destino_simulado` | `str` | Destino de la acción (ej: `"claude_api"`, `"github_issue"`, `"github_pr"`) |
| `payload_simulado` | `dict` | Contenido estructurado que se enviaría al destino si fuera real |
| `resultado_simulado` | `str` | Descripción del resultado esperado si la acción se ejecutara (ej: `"Claude recibiría el prompt y respondería"`) |
| `requiere_autorizacion` | `bool` | `True` si la acción requiere confirmación de Ariel/Torre antes de ejecutarse en modo real |
| `bloqueo` | `bool` | `True` si la mano local no puede proceder por restricción de seguridad |
| `motivo` | `str` | Explicación del resultado: por qué se simula, por qué se bloquea, qué falta |
| `evidencia` | `dict` | Registro de la operación simulada: entrada recibida, acción tomada, timestamp lógico |

---

## 8. Acciones simulables

La mano local simulada puede representar las siguientes acciones:

| Acción simulada | `accion_simulada` | `destino_simulado` |
|---|---|---|
| Preparar prompt para Claude | `preparar_prompt_claude` | `claude_api` |
| Preparar prompt para Codex | `preparar_prompt_codex` | `codex_api` |
| Preparar comentario de PR | `preparar_comentario_pr` | `github_pr` |
| Preparar comentario de issue | `preparar_comentario_issue` | `github_issue` |
| Preparar reporte de auditoría | `preparar_reporte_auditoria` | `registro_local` |
| Preparar orden para ejecutor | `preparar_orden_ejecutor` | `ejecutor_externo` |

**Todas estas acciones son solo preparación.** En modo simulado, ninguna llega a un sistema externo.

---

## 9. Acciones prohibidas

La mano local simulada **nunca** puede ejecutar las siguientes acciones, ni en modo simulado ni en modo real durante PUENTE-4:

| Acción prohibida | Razón |
|---|---|
| Abrir navegador | Fuera de scope hasta PUENTE-5+ |
| Usar Playwright real | Fuera de scope hasta PUENTE-5+ |
| Usar API real (Claude, GitHub) | Requiere autorizacion explícita de Torre |
| Comentar issue real | Acción externa irreversible |
| Cerrar issue real | Acción externa irreversible |
| Abrir PR real | Acción externa — solo Torre autoriza |
| Mergear PR real | Acción externa — solo Torre autoriza |
| Tocar producción | Prohibición absoluta |
| Tocar secrets | Prohibición absoluta |
| Escribir en repos prohibidos | torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero |
| Ejecutar comandos externos | Sin subprocess, sin shell, sin I/O |

---

## 10. Casos mínimos

Los siguientes casos deben tener comportamiento definido en la implementación de PUENTE-4B:

| Situación | Entrada clave | Salida esperada |
|---|---|---|
| Cerebro dice `continuar_documental` | `decision_del_cerebro: "continuar_documental"` | Simular preparación del siguiente paso documental; `requiere_autorizacion: False` |
| Cerebro dice `reformular` | `decision_del_cerebro: "reformular"` | Simular devolución a Ariel con sugerencia de reformulación; `requiere_autorizacion: False` |
| Cerebro dice `pedir_autorizacion` | `decision_del_cerebro: "pedir_autorizacion"` | Preparar pregunta estructurada para Ariel; `requiere_autorizacion: True` |
| Cerebro dice `no_ejecutar` | `decision_del_cerebro: "no_ejecutar"` | Bloquear acción; `bloqueo: True`; no simular nada |
| Cerebro dice `declarar_bloqueo` | `decision_del_cerebro: "declarar_bloqueo"` | Emitir declaración de bloqueo; `bloqueo: True`; no simular acción |
| Ariel responde `"1"` con opciones previas | `accion_segura_sugerida` apunta a opción 1 del contexto | Simular ejecución de la opción 1; `requiere_autorizacion: False` |
| Ariel pide `"pasalo a Claude"` | `accion_simulada: "preparar_prompt_claude"` | Simular preparación del prompt; `destino_simulado: "claude_api"` |
| Ariel pide `"comentá el issue"` sin autorización | `"puede_comentar_issue"` ausente en `autorizaciones_disponibles` | `bloqueo: True`; `motivo`: falta `puede_comentar_issue` |

---

## 11. Relación con anti-cartero

| Principio | Aplicación |
|---|---|
| La mano local no decide | Solo ejecuta lo que el Cerebro ya autorizó |
| La mano local no inventa | No genera acciones fuera del `accion_segura_sugerida` |
| La mano local transporta una orden estructurada | Convierte `decision_del_cerebro` en `payload_simulado` |
| Si Ariel debe copiar/pegar, se registra causa raíz | En `evidencia` queda consignado si la acción no pudo completarse automáticamente y por qué |

**Objetivo anti-cartero:** eliminar el ciclo manual copiar/pegar. Cada paso que la mano local puede completar sin intervención de Ariel reduce la carga del cartero. Cada paso que sigue requiriendo intervención manual debe quedar documentado como deuda técnica.

---

## 12. Criterios para pasar a PUENTE-4B

El contrato de PUENTE-4A habilita el inicio de PUENTE-4B si y solo si:

| Criterio | Estado requerido |
|---|---|
| Este contrato está cerrado | Sí — commit en rama, PR mergeado a main |
| Casos mínimos definidos (sección 10) | Sí — 8 casos documentados |
| Riesgos definidos | Sí — acciones prohibidas documentadas (sección 9) |
| Pruebas mock diseñadas conceptualmente | Sí — los 8 casos mínimos son la base de los tests de PUENTE-4B |
| Sin navegador real todavía | Confirmado — PUENTE-4B sigue en modo simulado |
| Autorización explícita de Ariel/Torre | Requerida antes de iniciar PUENTE-4B |
