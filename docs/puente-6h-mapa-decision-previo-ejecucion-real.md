# PUENTE-6H-MAPA — Mapa de decisión previo a ejecución real

## 1. Identificación

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6H-MAPA |
| Fecha/hora (UTC) | 2026-05-05 |
| Repo | `szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-` |
| Rama | `docs/puente-6h-mapa-decision-previo-ejecucion-real` |
| Commit base (main) | `6c4971bce0efad648b95e5b4a949076e1f49e3ae` |
| Autorización de Ariel | "Crear mapa de decisión previo a ejecución real" |

---

## 2. Estado de base

| Elemento | Estado |
|---|---|
| main actual | `6c4971bce0efad648b95e5b4a949076e1f49e3ae` |
| PUENTE-6G-A — diagnóstico entorno local | **CERRADO** en main (PR #38) |
| PUENTE-6G-B — procedimiento local seguro | **CERRADO** en main (PR #39) |
| PUENTE-6G-C — cierre documental fase 6G | **CERRADO** en main (PR #40) |
| Fase 6G completa | **CERRADA DOCUMENTALMENTE** |
| Tests actuales | **507/507 OK** |
| Llamada real futura | **NO HABILITADA** — requiere microciclo propio y autorización explícita de Ariel |

---

## 3. Objetivo del mapa

Este documento NO es un checklist de ejecución. Es un mapa de decisión que:

- **Evita el salto por inercia**: tener el procedimiento listo no habilita su ejecución automáticamente.
- **Separa la decisión de la ejecución**: elegir si conviene avanzar es una decisión distinta y previa a ejecutar.
- **Ordena los caminos posibles**: identifica opciones, riesgos y condiciones antes de cualquier llamada real.

> El hecho de que el procedimiento esté documentado y listo **no autoriza** ejecutar la llamada real.

---

## 4. Qué ya está cerrado

| Elemento cerrado | PR | Ubicación en main |
|---|---|---|
| `cliente_api_real_minimo.py` — cliente bloqueado por defecto | #34 | `src/plic_puente_agentes/cliente_api_real_minimo.py` |
| PUENTE-6E-A — contrato de integración mínima | #32 | `docs/puente-6e-a-contrato-cliente-real.md` |
| PUENTE-6E-C — cierre documental cliente real | #35 | `docs/puente-6e-c-cierre-cliente-real-minimo.md` |
| PUENTE-6F-A — checklist previo a llamada real | #36 | `docs/puente-6f-a-contrato-checklist-llamada-real.md` |
| PUENTE-6F-B — plantilla de evidencia | #37 | `docs/puente-6f-b-preparacion-evidencia-llamada-real.md` |
| PUENTE-6G-A — diagnóstico de entorno local | #38 | `docs/puente-6g-a-diagnostico-entorno-local-seguro.md` |
| PUENTE-6G-B — procedimiento local PowerShell + red celular | #39 | `docs/puente-6g-b-procedimiento-local-powershell-red-celular.md` |
| PUENTE-6G-C — cierre documental fase 6G | #40 | `docs/puente-6g-c-cierre-fase-entorno-local.md` |

---

## 5. Qué todavía NO está habilitado

| Acción | Estado |
|---|---|
| Llamada real a Anthropic | **NO HABILITADA** |
| Request HTTP real a cualquier endpoint | **NO HABILITADO** |
| API real efectiva | **NO HABILITADA** |
| SDK real efectivo | **NO HABILITADO** |
| `cliente_api_real_minimo` con `permitir_llamada_real=True` | **NO HABILITADO** |
| Producción | **NO HABILITADA** |
| Automatización / scheduler | **NO HABILITADOS** |
| Uso operativo de ningún cliente | **NO HABILITADO** |
| Ejecución desde Claude Code remoto | **NO HABILITADA** — `ANTHROPIC_API_KEY` ausente en ese entorno |

---

## 6. Opciones posibles para el próximo ciclo

### Opción A — PUENTE-6H-A: checklist final previo a una única llamada real local

- **Qué es**: completar y ejecutar el checklist de PUENTE-6F-A adaptado al entorno local de PUENTE-6G-B, confirmando condición a condición antes de autorizar una única llamada real.
- **Prerrequisitos**: autorización explícita de Ariel, entorno local activo, red celular, variable temporal lista (sin exponer valor).
- **Resultado esperado**: checklist aprobado o bloqueado con evidencia; si aprobado, habilitación explícita de una única llamada real en microciclo separado.
- **Riesgo principal**: precipitarse si alguna condición no está confirmada.

### Opción B — PUENTE-ENV-A: mapa de variables/entorno sin exponer secrets

- **Qué es**: documentar las variables necesarias, su origen, su ciclo de vida y cómo manejarlas sin exponerlas, antes de llegar al checklist.
- **Prerrequisitos**: ninguno — es documental puro.
- **Resultado esperado**: documento que reduce riesgo de exposición accidental en el momento de ejecución.
- **Riesgo principal**: ninguno operativo; solo costo de tiempo.

### Opción C — PUENTE-COSTOS-A: estimación documental de costo/riesgo antes de llamar API

- **Qué es**: estimar el costo esperado de 1 request real (tokens, precio por modelo, impacto si hay retries accidentales) sin ejecutar ninguna llamada.
- **Prerrequisitos**: ninguno — es documental puro.
- **Resultado esperado**: documento con estimación de costo máximo controlado y criterios de corte.
- **Riesgo principal**: ninguno operativo; solo costo de tiempo.

### Opción D — Pausa estratégica: no avanzar a ejecución real todavía

- **Qué es**: cerrar PUENTE-6H-MAPA y no avanzar a ningún microciclo de ejecución real hasta que Ariel lo decida conscientemente en otro momento.
- **Prerrequisitos**: ninguno.
- **Resultado esperado**: todo lo documentado sigue disponible; no hay regresión; la llamada real sigue disponible para cuando sea el momento correcto.
- **Riesgo principal**: ninguno — es la opción de menor riesgo.

---

## 7. Riesgos de avanzar a llamada real

| Riesgo | Nivel | Descripción |
|---|---|---|
| Secret expuesto | **ALTO** | Si el valor de `ANTHROPIC_API_KEY` se copia en el chat, en un archivo o en un log |
| Entorno equivocado | **ALTO** | Si se intenta ejecutar desde Claude Code remoto donde la key no está disponible |
| Más de un request | **MEDIO** | Si el flujo no está controlado y se ejecutan requests adicionales |
| Retry accidental | **MEDIO** | Si hay un error y el código reintenta automáticamente (el cliente lo prohíbe, pero el riesgo existe si se bypasea) |
| Evidencia incompleta | **MEDIO** | Si no se documenta el resultado antes de cerrar la sesión |
| Confusión entre prueba y producción | **MEDIO** | Si se usa un endpoint productivo creyendo que es de prueba |
| Costo no controlado | **MEDIO** | Si se desconoce el costo por request y se ejecutan más llamadas de las previstas |
| Salto de nivel sin cierre | **BAJO** | Avanzar a ejecución real sin haber cerrado documentalmente el checklist previo |

---

## 8. Señales de que NO conviene avanzar

Si alguna de las siguientes condiciones está presente, **no avanzar a ejecución real**:

| Señal | Descripción |
|---|---|
| Ariel no está en entorno local controlado | Si está usando Claude Code remoto o un entorno sin la key disponible como variable temporal |
| No hay red celular definida | Si va a usar red corporativa o doméstica con proxy desconocido (lección de PUENTE-6D) |
| No está claro el costo | Si no se sabe cuánto costará el request ni cuál es el techo aceptable |
| No está lista la evidencia | Si no hay plantilla disponible o no se sabe dónde se va a registrar el resultado |
| Hay cansancio o apuro | Si se intenta avanzar rápido para "terminar" — el error de exposición de secret es irreversible |
| Falta autorización explícita | Si Ariel no ha dado instrucción separada y explícita para el microciclo de ejecución real |
| Se intenta resolver desde Claude Code remoto | Ese entorno no tiene `ANTHROPIC_API_KEY` disponible — bloqueante confirmado en PUENTE-6G-A |

---

## 9. Condiciones mínimas para habilitar un próximo checklist final

Para autorizar el avance a un checklist final (que a su vez puede habilitar una única llamada real) se requieren **todas** las siguientes:

| Condición | Estado actual |
|---|---|
| Autorización explícita de Ariel para el microciclo de checklist | **PENDIENTE — bloqueante** |
| Decisión consciente de ir hacia prueba real (no por inercia) | **PENDIENTE** |
| Entorno local de Ariel confirmado (PowerShell, no Claude Code remoto) | A confirmar en el momento |
| Red celular activa (hotspot móvil) | A confirmar en el momento |
| `ANTHROPIC_API_KEY` lista como variable temporal en sesión local, sin exponer valor | A confirmar — nunca en archivo ni en chat |
| Payload mínimo definido previamente | A definir en el checklist |
| Límite de 1 request confirmado | Obligatorio — contrato PUENTE-6E-A |
| Sin retry automático | Obligatorio — cliente bloqueado por diseño |
| Plantilla de evidencia PUENTE-6F-B lista para completar post-llamada | **PRESENTE** en main |
| Criterio de éxito y bloqueo definido | A definir en el checklist |
| Tests ≥ 507/507 OK en commit base | **PRESENTE** — 507/507 OK confirmado |
| Este mapa (PUENTE-6H-MAPA) mergeado en main | Pendiente — PR de este microciclo |

---

## 10. Qué NO queda autorizado por este mapa

| Acción | Estado |
|---|---|
| Ejecutar llamada real a Anthropic | **NO AUTORIZADO** |
| Hacer request HTTP a cualquier endpoint | **NO AUTORIZADO** |
| Usar la API de Anthropic de forma efectiva | **NO AUTORIZADO** |
| Usar el SDK de Anthropic | **NO AUTORIZADO** |
| Usar `cliente_api_real_minimo` con `permitir_llamada_real=True` | **NO AUTORIZADO** |
| Leer, imprimir o exponer secrets | **NO AUTORIZADO** |
| Crear o modificar `.env` | **NO AUTORIZADO** |
| Modificar código fuente | **NO AUTORIZADO** |
| Modificar tests | **NO AUTORIZADO** |
| Tocar producción | **NO AUTORIZADO** |
| Crear workflows | **NO AUTORIZADO** |
| Usar navegador o Playwright | **NO AUTORIZADO** |
| Avanzar a ejecución real sin instrucción separada de Ariel | **NO AUTORIZADO** |

---

## 11. Confirmaciones de seguridad de este microciclo

| Verificación | Estado |
|---|---|
| Llamada real ejecutada | NO |
| Request HTTP ejecutado | NO |
| Secret expuesto | NO |
| `ANTHROPIC_API_KEY` leída o impresa | NO |
| `.env` creado o modificado | NO |
| Código fuente modificado | NO |
| Tests modificados | NO |
| Workflows tocados | NO |
| Producción tocada | NO |
| Navegador usado | NO |
| Playwright usado | NO |
| Otros repos tocados | NO |
| PR abierto | NO |
| Merge ejecutado | NO |

---

## 12. Dictamen final

### **PUENTE-6H-MAPA — SOLO ORDENA LA DECISIÓN PREVIA**

Este documento mapea opciones, riesgos y condiciones antes de cualquier llamada real. No habilita ninguna acción efectiva. No autoriza ningún request. No permite ejecución desde ningún entorno.

**La llamada real futura sigue NO habilitada.**

> El próximo paso requiere instrucción explícita y separada de Ariel.
