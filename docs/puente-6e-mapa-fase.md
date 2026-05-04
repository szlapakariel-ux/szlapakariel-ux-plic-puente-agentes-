# PUENTE-6E-MAPA — Mapa de fase previo a implementación técnica

## 1. Identificación

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6E-MAPA |
| Fecha/hora (UTC) | 2026-05-04 |
| Repo | `szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-` |
| Commit base (main) | `00a74d6386173c513ac8575927bf1ffa03af9f18` |
| Estado de main | PUENTE-6D cerrado + PUENTE-6E-A cerrado |

---

## 2. Estado cerrado

| Hito | Estado | PR | Commit en main |
|---|---|---|---|
| PUENTE-6D — primera llamada real mínima exitosa | **CERRADO** | #31 | `21aae96` |
| PUENTE-6E-A — contrato documental de integración mínima | **CERRADO** | #32 | `00a74d6` |
| PUENTE-6E-B — implementación técnica | **NO HABILITADO** | — | — |

No hay PR abierto. No hay llamada real autorizada. No hay código autorizado. Estamos frenados para revisar el mapa.

---

## 3. Qué está probado

| Elemento probado | Evidencia |
|---|---|
| La API de Anthropic responde con HTTP 200 a un payload mínimo bien formado | `docs/puente-6d-real-reintento-celular-resultado.md` |
| El modelo `claude-haiku-4-5-20251001` está disponible para la cuenta | Mismo documento — `"modelo": "claude-haiku-4-5-20251001"` devuelto por la API |
| El modelo devuelve exactamente `"PLIC_OK"` con el prompt `"Respondé exactamente: PLIC_OK"` | `"respuesta_texto": "PLIC_OK"` confirmado |
| La llamada puede ejecutarse desde PowerShell local de Ariel sin exponer secrets | `secret_expuesto: false`, `repo_tocado: false` |
| La red celular funciona para llamadas a Anthropic | Intento 5 exitoso desde hotspot móvil |
| `HttpWebRequest` con UTF-8 explícito, `-Depth 10`, `temperature [double]0.0` produce respuesta válida | Script del intento 5 |
| 416 tests pasan sin modificar código | Verificado en cada microciclo |
| El protocolo de microciclos (inspect → branch → doc → commit → push → auditoría → PR → merge) funciona end-to-end | PRs #26 al #32 mergeados |

---

## 4. Qué falta antes de cualquier integración técnica

| Pendiente | Descripción |
|---|---|
| Cliente real en código | No existe ninguna función en Python que llame a la API real |
| Inyección de secret en entorno remoto | Claude Code remoto no hereda `ANTHROPIC_API_KEY` — sin resolver |
| Tests del cliente real (sin API real) | No existen tests para la futura función cliente |
| Logging sanitizado implementado | Definido en contrato (PUENTE-6E-A) pero no implementado |
| Manejo de errores implementado | Definido en contrato pero no implementado |
| Política de presupuesto/tokens implementada | Definida en contrato pero no implementada |
| Decisión: dónde vive el cliente real en el código | ¿En `cliente_api_real_preparado.py`? ¿Nuevo módulo? Sin definir |
| Decisión: cómo se inyecta el secret | Variables del sistema, Claude Code settings, otro método — sin decidir |
| Decisión: cuándo se permite llamar desde código | Solo local, solo con env var verificada, solo en microciclo — sin decidir |

---

## 5. Riesgos vigentes

| Riesgo | Probabilidad | Impacto | Mitigación disponible |
|---|---|---|---|
| Fuga de secret en código/logs/commit | Media | Alto | Reglas de secrets de PUENTE-6E-A — no implementadas todavía |
| Llamada involuntaria desde código de producción | Media | Alto | Política de llamadas de PUENTE-6E-A — no implementada todavía |
| Costos no controlados | Media | Medio | Política de presupuesto de PUENTE-6E-A — no implementada todavía |
| Red corporativa bloquea llamada | Posible | Medio | Usar red celular — demostrado en PUENTE-6D |
| Error 400 por payload mal formado | Posible | Bajo | Script mejorado documentado — no implementado en código |
| Claude Code remoto sin key | Alta | Medio | Sección 7 de PUENTE-6E-A — sin implementar |
| Respuesta inesperada tratada como éxito | Baja | Medio | Validación de `content[].text` — no implementada |
| Tests con API real en suite existente | Alta (si se agrega sin cuidado) | Alto | Suite actual es 0 imports, 0 I/O — proteger esta invariante |

---

## 6. Qué NO está autorizado

| Acción | Estado |
|---|---|
| Modificar código fuente | **NO AUTORIZADO** |
| Crear función cliente real | **NO AUTORIZADO** |
| Modificar tests | **NO AUTORIZADO** |
| Ejecutar llamada real | **NO AUTORIZADO** |
| Hacer request HTTP | **NO AUTORIZADO** |
| Usar API real o SDK real | **NO AUTORIZADO** |
| Leer, crear o modificar secrets | **NO AUTORIZADO** |
| Crear o modificar `.env` | **NO AUTORIZADO** |
| Tocar producción | **NO AUTORIZADO** |
| Crear workflows | **NO AUTORIZADO** |
| Usar navegador o Playwright | **NO AUTORIZADO** |
| Instalar dependencias nuevas | **NO AUTORIZADO** |
| Iniciar PUENTE-6E-B | **NO AUTORIZADO** |
| Automatizar cualquier llamada | **NO AUTORIZADO** |

---

## 7. Opciones posibles para el próximo ciclo

Estas son opciones — ninguna está autorizada todavía. Cada una requiere instrucción explícita separada de Ariel.

### Opción A — PUENTE-6E-B: Implementación técnica mínima del cliente real

Implementar en Python la función cliente real siguiendo el contrato de PUENTE-6E-A, con:
- Tests sin API real que cubran la función
- Logging sanitizado
- Manejo de errores con body capturado
- Validación de modelo antes de llamar
- Sin llamada real en este microciclo

**Costo**: alto — requiere diseño, implementación, tests y auditoría.

### Opción B — PUENTE-6E-ENV: Resolver propagación de ANTHROPIC_API_KEY en Claude Code remoto

Definir y documentar el método para que Claude Code remoto tenga acceso a `ANTHROPIC_API_KEY` sin exponer el valor. Opciones:
- Claude Code `settings.json` → `env`
- Variable de sistema permanente antes de lanzar Claude Code
- Verificación booleana previa al intent de llamada

**Costo**: bajo — solo documental o configuración de entorno.

### Opción C — PUENTE-6E-C: Segunda llamada real mínima controlada desde entorno mejorado

Autorizar una segunda llamada real desde PowerShell o desde Claude Code (si el entorno está resuelto), con el script mejorado de PUENTE-6D, para confirmar reproducibilidad.

**Costo**: medio — requiere resolución de entorno (Opción B) si se quiere desde Claude Code.

### Opción D — Pausa estratégica

Frenar aquí y revisar si PUENTE-6E tiene sentido en este momento, antes de invertir en implementación técnica.

**Costo**: ninguno.

---

## 8. Condiciones mínimas para habilitar PUENTE-6E-B

| Condición | Estado |
|---|---|
| PUENTE-6E-A mergeado en main | **CUMPLIDO** — PR #32 @ `00a74d6` |
| Auditoría de PUENTE-6E-A aprobada | **CUMPLIDO** — dictamen A |
| Este mapa (PUENTE-6E-MAPA) mergeado en main | Pendiente — PR de este microciclo |
| Auditoría de PUENTE-6E-MAPA aprobada | Pendiente |
| Autorización explícita de Ariel para PUENTE-6E-B | **PENDIENTE — bloqueante** |
| Alcance técnico acotado de PUENTE-6E-B definido | Pendiente |
| Tests sin API real diseñados para la función cliente | Pendiente |
| Sin producción, sin workflows, sin automatización | Obligatorio |

---

## 9. Dictamen

### **PUENTE-6E-B sigue NO habilitado**

Este documento es solo un mapa orientativo. No implementa nada. No autoriza código. No autoriza llamada real. No habilita PUENTE-6E-B.

**Para habilitar PUENTE-6E-B** se requiere:
1. Este documento mergeado en main.
2. Auditoría aprobada.
3. Instrucción explícita y separada de Ariel eligiendo una opción del mapa (sección 7).
4. Contrato técnico acotado de PUENTE-6E-B.

> El próximo paso es decidir cuál opción de la sección 7 perseguir — o pausar. Esa decisión es de Ariel.
