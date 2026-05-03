# PUENTE-2A — Resultado: Contrato de Reglas PLIC para el Cerebro Portero Mock

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-2A |
| Rama base | `main` |
| Commit base | `4d9f24fb2c25799117357e1f37cfc13aa3daeec0` |
| Rama de trabajo | `docs/puente-2a-contrato-reglas-plic` |
| Estado de PUENTE-1C | Cerrado — auditoría técnica mergeada a main |
| Dictamen PUENTE-1C | A) APTO PARA INTEGRACIÓN MÍNIMA COMO BASE DEL PUENTE |
| Tests en main al iniciar | 29/29 OK |

---

## 2. Reglas PLIC documentadas

El contrato `docs/reglas-plic-cerebro-mock.md` define:

- **15 reglas base** (R-01 a R-15) que el Cerebro Portero Mock debe respetar al evaluar cualquier intención.
- **5 niveles de jerarquía** que resuelven conflictos entre reglas.
- **4 niveles de riesgo**: `bajo`, `medio`, `alto`, `prohibido`.
- **13 acciones prohibidas** por defecto con riesgo `prohibido`.
- **7 decisiones permitidas** alineadas con el contrato PUENTE-1A.
- **6 reglas anti-cartero** (AC-01 a AC-06).
- **10 casos mínimos** con decisión esperada y campos de salida completos.

---

## 3. Tabla de reglas

| # | Regla | Prioridad |
|---|---|---|
| R-01 | Un microciclo por vez | Alta |
| R-02 | Un objetivo por ciclo | Alta |
| R-03 | No subir de nivel sin cierre verificable | Alta |
| R-04 | No automatizar sin prueba documental previa | Alta |
| R-05 | No sumar agentes sin protocolo | Media |
| R-06 | No tocar código sin diagnóstico previo | Alta |
| R-07 | No tocar producción sin checklist aprobado | Crítica |
| R-08 | No tocar secrets | Crítica — prohibición absoluta |
| R-09 | No crear workflows sin autorización | Alta |
| R-10 | No abrir navegador/Playwright sin ciclo autorizado | Alta |
| R-11 | No usar API real sin ciclo autorizado | Alta |
| R-12 | No usar Claude Haiku real sin ciclo autorizado | Alta |
| R-13 | No modificar repos prohibidos | Crítica |
| R-14 | No convertir a Ariel en cartero | Media |
| R-15 | Si hay ambigüedad, reformular antes de ejecutar | Alta |

---

## 4. Tabla de acciones prohibidas

| Acción | Riesgo | Decisión |
|---|---|---|
| Producción | `prohibido` | `no_ejecutar` |
| Secrets | `prohibido` | `no_ejecutar` |
| Tokens | `prohibido` | `no_ejecutar` |
| Credenciales | `prohibido` | `no_ejecutar` |
| Workflows sin autorización | `prohibido` | `no_ejecutar` |
| Merge a main sin autorización | `prohibido` | `no_ejecutar` |
| Force push | `prohibido` | `no_ejecutar` |
| Borrar archivos | `prohibido` | `no_ejecutar` |
| Cerrar issues reales sin autorización | `prohibido` | `no_ejecutar` |
| Comentar issues reales sin autorización | `prohibido` | `no_ejecutar` |
| Usar APIs reales | `prohibido` | `no_ejecutar` |
| Abrir navegador automatizado | `prohibido` | `no_ejecutar` |
| Ejecutar Playwright real | `prohibido` | `no_ejecutar` |

---

## 5. Tabla de casos mínimos

| Entrada | Riesgo | Decisión | `requiere_ariel` | `requiere_torre` |
|---|---|---|---|---|
| `"seguí"` | `medio` | `reformular` | `true` | `false` |
| `"1"` | `bajo` | `continuar_documental` | `false` | `false` |
| `"pasalo a Claude"` | `medio` | `reformular` | `false` | `true` |
| `"mandalo a producción"` | `prohibido` | `no_ejecutar` | `true` | `false` |
| `"usa el token"` | `prohibido` | `no_ejecutar` | `true` | `false` |
| `"abrí navegador"` | `prohibido` | `no_ejecutar` | `true` | `false` |
| `"creá workflow"` | `prohibido` | `no_ejecutar` | `true` | `false` |
| `"mergealo"` | `prohibido` | `no_ejecutar` | `true` | `false` |
| `"diagnóstico SOFSE"` | `alto` | `pedir_autorizacion` | `true` | `false` |
| `"suspender"` | `bajo` | `suspender` | `false` | `false` |

---

## 6. Relación con el contrato PUENTE-1A

| Elemento PUENTE-1A | Cubierto en PUENTE-2A |
|---|---|
| 7 campos de entrada | Todos aceptados. `texto_original` es el campo evaluado. Los demás quedan en backlog PUENTE-2B. |
| 9 campos de salida | Todos incluidos en la especificación de salida esperada. |
| 7 decisiones | Todas presentes en la tabla de decisiones permitidas con criterio de uso. |
| 4 niveles de riesgo | Todos definidos con semántica y acción por defecto. |
| Firma `cerebro_mock(entrada: dict) -> dict` | Respetada. No se modifica en este ciclo. |

Nuevos casos incorporados en PUENTE-2A que no estaban en PUENTE-1B:

| Entrada nueva | Decisión esperada | Estado en PUENTE-1B |
|---|---|---|
| `"usa el token"` | `no_ejecutar` / `prohibido` | Cubierto por `_PALABRAS_SECRETS` (palabra `"token"`) |
| `"abrí navegador"` | `no_ejecutar` / `prohibido` | Sin regla activa — requiere PUENTE-2B |
| `"creá workflow"` | `no_ejecutar` / `prohibido` | Sin regla activa — requiere PUENTE-2B |
| `"mergealo"` | `no_ejecutar` / `prohibido` | Sin regla activa — requiere PUENTE-2B |
| `"seguí"` | `reformular` / `medio` | Cubierto por regla default |

---

## 7. Qué queda habilitado

Con este contrato cerrado, el siguiente microciclo puede:

- **Extender `cerebro_mock.py`** con nuevas reglas basadas en este contrato, sin romper los 29 tests existentes.
- **Agregar tests** para los 4 nuevos casos no cubiertos: `"abrí navegador"`, `"creá workflow"`, `"mergealo"`, y variantes ambiguas de `"seguí"`.
- **Implementar `declarar_bloqueo` y `escalar_a_ariel`** como decisiones activas, según el criterio definido aquí.
- **Usar `contexto_actual`, `estado_del_ciclo` y `autorizaciones_disponibles`** como campos evaluables en las reglas, una vez que se defina la lógica en PUENTE-2B.

---

## 8. Qué NO queda habilitado

| Acción | Estado |
|---|---|
| Modificar `cerebro_mock.py` | NO — requiere PUENTE-2B con microciclo de implementación |
| Modificar `test_cerebro_mock.py` | NO — requiere PUENTE-2B |
| Conectar Claude Haiku API real | NO — requiere PUENTE-5 |
| Abrir navegador o Playwright | NO — requiere PUENTE-4 con autorización |
| Usar API real de ningún tipo | NO — prohibición activa |
| Agregar reglas sin contrato previo | NO — toda regla nueva requiere contrato documental primero |
| Avanzar a PUENTE-2B sin autorización explícita | NO |

---

## 9. Confirmaciones de seguridad

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
| Tests existentes pasan | CONFIRMADO — 29/29 OK |

---

## 10. Próximo microciclo sugerido

**PUENTE-2B — Integración mínima de reglas PLIC en Cerebro Portero Mock, sin API real**

Objetivo: implementar en `cerebro_mock.py` las nuevas reglas definidas en este contrato (PUENTE-2A), agregar tests para los casos nuevos, y verificar que los 29 tests originales siguen pasando.

Alcance esperado:
- Agregar reglas para: `"abrí navegador"`, `"creá workflow"`, `"mergealo"` → `no_ejecutar` / `prohibido`.
- Implementar decisiones activas para `declarar_bloqueo` y `escalar_a_ariel`.
- Agregar guarda defensiva contra entrada no-dict.
- Evaluar campos `contexto_actual`, `estado_del_ciclo`, `autorizaciones_disponibles` en al menos un caso.

Restricciones:
- Solo código local.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.
- Sin secrets.
- Sin producción.

> No iniciar PUENTE-2B hasta que PUENTE-2A esté cerrado con evidencia verificable (commit + push a main) y autorización explícita de Ariel.
