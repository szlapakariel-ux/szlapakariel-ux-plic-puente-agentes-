# PUENTE-1A — Resultado: Contrato Cerebro Portero Mock

## Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-1A |
| Rama base | `main` |
| Commit base | `4b8ed74b478637caf13f52c0b55ad63f6df409d3` |
| Rama de trabajo | `docs/puente-1a-contrato-cerebro-mock` |
| Estado de PUENTE-0 | Cerrado — mergeado a main el 2026-05-03 |
| Código ejecutable | Ninguno en este ciclo |

---

## Contrato definido

El microciclo PUENTE-1A produjo el archivo `docs/contrato-cerebro-mock.md`, que define:

- El nombre y objetivo del Cerebro Portero Mock.
- Los campos de entrada que el sistema espera recibir.
- Los campos de salida que el sistema debe devolver.
- Las 7 decisiones posibles.
- Los 4 niveles de riesgo.
- Las 5 reglas anti-cartero.
- Los 5 casos de ejemplo con entradas y salidas completas.
- Los 10 límites explícitos del sistema.

---

## Ejemplos de entrada/salida definidos

| Caso | Texto original | Decisión | Riesgo |
|---|---|---|---|
| 1 | `"seguí con lo del celu"` | `pedir_autorizacion` | `medio` |
| 2 | `"1"` | `continuar_documental` | `bajo` |
| 3 | `"pasalo a Claude"` | `reformular` | `medio` |
| 4 | `"mandalo a producción"` | `no_ejecutar` | `prohibido` |
| 5 | `"diagnóstico SOFSE"` | `escalar_a_ariel` | `alto` |

---

## Decisiones permitidas

El Cerebro Portero Mock puede devolver las siguientes decisiones:

| Decisión | Cuándo aplica |
|---|---|
| `continuar_documental` | Acción segura, sin ambigüedad, dentro del microciclo activo |
| `pedir_autorizacion` | Acción reconocible pero con riesgo medio o contexto incompleto |
| `reformular` | Intención ambigua que requiere que Torre estructure antes de ejecutar |
| `suspender` | Contexto insuficiente, microciclo mal definido, o sesión sin continuidad |
| `declarar_bloqueo` | Estado inesperado que impide continuar — se registra y escala |
| `escalar_a_ariel` | Riesgo alto que requiere autorización explícita del operador |
| `no_ejecutar` | Riesgo prohibido — viola regla PLIC absoluta |

---

## Decisiones prohibidas

El Cerebro Portero Mock no puede producir las siguientes decisiones ni acciones:

| Acción prohibida | Razón |
|---|---|
| Autorizar producción directamente | Riesgo `prohibido` — regla PLIC absoluta |
| Exponer o validar secrets | Prohibición absoluta en todos los microciclos |
| Hacer merge o cerrar issues | Fuera del alcance del Portero en todos los ciclos |
| Llamar API real sin microciclo dedicado | PUENTE-5 o posterior, con autorización explícita |
| Iniciar PUENTE-1B sin cierre verificable de PUENTE-1A | Regla de un microciclo por vez |
| Ejecutar herramientas (Playwright, CLI) | Solo desde PUENTE-4 en adelante, con autorización |

---

## Validación anti-cartero

| Regla | Validada |
|---|---|
| Ariel puede responder con una palabra o número | SÍ — `opciones_para_ariel` es lista seleccionable |
| El Portero estructura la intención | SÍ — `intencion_detectada` y `accion_segura_sugerida` son responsabilidad del Portero |
| Torre reformula si hay ambigüedad | SÍ — `requiere_torre: true` activa el flujo de reformulación |
| El ejecutor no recibe texto crudo | SÍ — el ejecutor solo recibe `accion_segura_sugerida` o la reformulación de Torre |
| Ariel no redacta prompts largos | SÍ — el contrato acepta frases de una palabra como `"1"` o `"seguí"` |

---

## Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin código ejecutable | CONFIRMADO |
| Sin scripts | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin API real | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright real | CONFIRMADO |
| Sin toque a torre-control | CONFIRMADO |
| Sin toque a agente-saas | CONFIRMADO |
| Sin toque a auditoria-sofse | CONFIRMADO |
| Sin toque a plic-laboratorio-portero | CONFIRMADO |
| Sin PR abierto | CONFIRMADO |
| Sin merge | CONFIRMADO |

---

## Próximo microciclo sugerido

**PUENTE-1B — Implementación mínima del Cerebro Portero Mock sin API real**

Objetivo: implementar en Python una función `cerebro_mock(entrada: dict) -> dict` que, usando el contrato definido en PUENTE-1A, evalúe la entrada con reglas hardcodeadas y devuelva la salida estructurada. Sin llamadas a Claude Haiku. Sin API real. Con tests unitarios mínimos.

> Este microciclo no debe iniciarse hasta que PUENTE-1A esté cerrado con evidencia verificable (commit + push).
