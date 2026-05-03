# PUENTE-3A — Resultado: Contrato de Contexto, Estado y Autorizaciones

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-3A |
| Rama base | `main` |
| Commit base | `7b3ed47838e575187d5cf72738f23ef27aeb0580` |
| Rama de trabajo | `docs/puente-3a-contrato-contexto-estado-autorizaciones` |
| Estado de PUENTE-2B | Cerrado — 56 tests OK, reglas PLIC integradas |
| Backlog abordado | B-04 de PUENTE-2C |
| Tests al iniciar | 56/56 OK |

---

## 2. Backlog B-04 abordado documentalmente

El ítem B-04 de la auditoría PUENTE-2C indicaba:

> *"Evaluar campos `contexto_actual`, `estado_del_ciclo` y `autorizaciones_disponibles` en al menos un caso."*

Este microciclo cierra ese ítem a nivel documental: los tres campos quedan definidos con significado operativo, reglas de uso, valores válidos y criterios de integración técnica.

La implementación en código queda para PUENTE-3B.

---

## 3. Campos definidos

| Campo | Tipo | Subcampos / valores |
|---|---|---|
| `contexto_actual` | dict o null | `proyecto_activo`, `ultimo_microciclo`, `ultimo_pr`, `ultima_decision`, `ultimo_bloqueo`, `ultimo_mensaje_ariel`, `ultimo_output_portero`, `repo_autorizado_actual` |
| `estado_del_ciclo` | string o null | 10 estados válidos (ver tabla siguiente) |
| `autorizaciones_disponibles` | lista de strings | 11 autorizaciones válidas (ver tabla siguiente) |

---

## 4. Tabla de estados del ciclo

| Estado | Descripción | Acciones seguras |
|---|---|---|
| `no_iniciado` | Sin ciclo activo | Documentar, diagnosticar |
| `en_diagnostico` | Analizando el sistema | Solo lectura, documentar hallazgos |
| `en_documentacion` | Redactando docs o contratos | Crear/modificar docs, sin código |
| `en_codigo` | Modificando código o tests | Modificar `src/`, `tests/` |
| `en_auditoria` | Auditando ciclo anterior | Solo lectura |
| `pr_abierto` | PR esperando merge | Solo revisar, sin código nuevo |
| `mergeado` | PR mergeado, cerrando ciclo | Documentación de cierre |
| `cerrado` | Ciclo cerrado con evidencia | Ninguna — iniciar nuevo ciclo |
| `bloqueado` | Condición bloqueante activa | Documentar bloqueo, escalar |
| `suspendido` | Pausado por Ariel | Ninguna hasta nueva instrucción |

---

## 5. Tabla de autorizaciones disponibles

| Autorización | Descripción | Disponible en producción/secrets |
|---|---|---|
| `puede_documentar` | Crear o modificar docs | Sí |
| `puede_diagnosticar` | Leer y analizar el sistema | Sí |
| `puede_modificar_codigo` | Modificar `src/` o `tests/` | Sí |
| `puede_abrir_pr` | Abrir PR hacia main | Sí |
| `puede_mergear` | Hacer merge de PR autorizado | Sí |
| `puede_comentar_issue` | Comentar en issues del repo | Sí |
| `puede_cerrar_issue` | Cerrar issues del repo | Sí |
| `puede_usar_api_real` | Usar APIs externas | Sí (requiere ciclo específico) |
| `puede_usar_navegador` | Usar Playwright o navegador | Sí (requiere ciclo específico) |
| `puede_tocar_produccion` | Actuar en producción | **NUNCA** — prohibición absoluta, se ignora |
| `puede_tocar_secrets` | Leer/escribir secrets | **NUNCA** — prohibición absoluta, se ignora |

---

## 6. Tabla de casos esperados

| Caso | `texto_original` | Campo condicionante | Decisión | Riesgo |
|---|---|---|---|---|
| Seguí con ciclo cerrado | `"seguí"` | `estado_del_ciclo: "cerrado"` | `reformular` | `medio` |
| Seguí con PR abierto | `"seguí"` | `estado_del_ciclo: "pr_abierto"` | `reformular` | `medio` |
| Merge sin autorización | `"mergealo"` | `autorizaciones_disponibles` sin `puede_mergear` | `pedir_autorizacion` | `alto` |
| Merge con autorización | `"mergealo"` | `autorizaciones_disponibles: ["puede_mergear"]` + `estado: "pr_abierto"` | `continuar_documental` | `bajo` |
| "1" con opciones previas | `"1"` | `contexto_actual.ultimo_output_portero` con opciones | `continuar_documental` | `bajo` |
| "1" sin opciones previas | `"1"` | `contexto_actual.ultimo_output_portero: null` | `reformular` | `medio` |
| Pasalo a Claude sin protocolo | `"pasalo a Claude"` | `contexto_actual: null` | `reformular` | `medio` |
| SOFSE sin repo autorizado | `"diagnóstico SOFSE"` | `contexto_actual.repo_autorizado_actual` ≠ SOFSE | `pedir_autorizacion` | `alto` |
| Suspender en cualquier estado | `"suspender"` | — | `suspender` | `bajo` |

---

## 7. Reglas de prioridad

| Prioridad | Principio |
|---|---|
| 1 | Prohibiciones explícitas ganan siempre — incluso sobre `autorizaciones_disponibles` |
| 2 | `autorizaciones_disponibles` condiciona: sin autorización → `pedir_autorizacion` |
| 3 | `estado_del_ciclo` evita saltos de fase — estado incoherente → `reformular` |
| 4 | `contexto_actual` evita Ariel-cartero — sin contexto suficiente → `reformular` |
| 5 | `texto_original` solo no alcanza para acciones sensibles |

---

## 8. Qué queda habilitado

Con este contrato cerrado, el siguiente microciclo puede:

- **Extender `cerebro_mock.py`** para evaluar `contexto_actual`, `estado_del_ciclo` y `autorizaciones_disponibles` en las reglas existentes.
- **Agregar tests** para los 9 casos documentados en la sección 6.
- **Implementar el orden de evaluación** definido en la regla central (sección 7 del contrato).
- **Usar las constantes de valores válidos** definidas en este contrato como sets de referencia en el código.
- **Agregar `motivo` contextualizado** que referencie el campo que condicionó la decisión.

---

## 9. Qué NO queda habilitado

| Acción | Estado |
|---|---|
| Modificar `cerebro_mock.py` | NO — requiere PUENTE-3B |
| Modificar `test_cerebro_mock.py` | NO — requiere PUENTE-3B |
| Usar API real | NO — requiere PUENTE-5 |
| Usar navegador o Playwright | NO — requiere PUENTE-4 |
| Habilitar `puede_tocar_produccion` | NO — prohibición absoluta |
| Habilitar `puede_tocar_secrets` | NO — prohibición absoluta |
| Merge automático sin revisión de Torre | NO |
| Cierre automático de issues | NO |

---

## 10. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin modificaciones al código | CONFIRMADO |
| Sin modificaciones a tests | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin API real | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin dependencias instaladas | CONFIRMADO |
| Sin repos prohibidos | CONFIRMADO — torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero no tocados |
| Tests existentes pasan | CONFIRMADO — 56/56 OK |

---

## 11. Próximo microciclo sugerido

**PUENTE-3B — Integración mínima de `contexto_actual`, `estado_del_ciclo` y `autorizaciones_disponibles` en Cerebro Portero Mock, sin API real**

Objetivo: implementar en `cerebro_mock.py` la evaluación de los tres campos de contexto según el contrato de PUENTE-3A, agregar tests para los 9 casos documentados, y verificar que los 56 tests originales siguen pasando.

Alcance esperado:
- Implementar evaluación de `estado_del_ciclo` antes de las reglas PLIC.
- Implementar evaluación de `autorizaciones_disponibles` para acciones que la requieran.
- Implementar evaluación de `contexto_actual` para casos de continuidad y anti-cartero.
- Agregar 9+ tests nuevos para los casos documentados.
- Actualizar `motivo` para referenciar el campo condicionante.
- Mantener función pura — sin imports, sin I/O.

Restricciones:
- Solo código local.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.
- Sin secrets.
- Sin producción.
- Los 56 tests existentes deben seguir pasando.

> No iniciar PUENTE-3B hasta que PUENTE-3A esté cerrado con evidencia verificable (commit + push a main) y autorización explícita de Ariel.
