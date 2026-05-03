# PUENTE-1C — Decisión de Integración Mínima

## 1. Decisión final

## **A) APTO PARA INTEGRACIÓN MÍNIMA COMO BASE DEL PUENTE**

El Cerebro Portero Mock implementado en PUENTE-1B está aprobado para ser usado como base de la integración mínima del sistema Puente de Agentes / Portero Local.

---

## 2. Justificación

| Criterio | Estado | Detalle |
|---|---|---|
| Tests | ✓ PASA | 29/29 tests OK en 0.001s |
| Contrato de salida | ✓ COMPLETO | 9/9 campos presentes con nombres exactos |
| Reglas críticas de seguridad | ✓ ACTIVAS | Producción y secrets bloqueados con prioridad |
| Función pura | ✓ VERIFICADO | Zero imports, zero efectos secundarios |
| Sin API real | ✓ VERIFICADO | Sin conexiones externas de ningún tipo |
| Sin secrets | ✓ VERIFICADO | Sin lectura de entorno ni archivos de credenciales |
| Decisiones del contrato | ✓ 7/9 disponibles | `declarar_bloqueo` y `escalar_a_ariel` en set válido pero sin regla activa — no bloquea |
| Casos edge | ✓ DOCUMENTADOS | 6 casos edge identificados, ninguno es bug activo |

La decisión se basa en que el componente cumple su objetivo de PUENTE-1B: proveer una versión simulada del Cerebro Portero que permita probar el flujo de decisión de forma local y controlada, sin depender de ninguna API real, y respetando el contrato definido en PUENTE-1A.

---

## 3. Qué queda habilitado

Con esta decisión, el siguiente paso del sistema puede avanzar hacia:

- **Definición del contrato de reglas PLIC** (PUENTE-2A): el Cerebro Portero Mock es la base sobre la que se construirá el motor de reglas PLIC. El mock actual acepta todos los campos del contrato y puede ser extendido sin romper los tests existentes.
- **Uso del mock como fixture de prueba** en los microciclos siguientes: los tests actuales pueden reutilizarse como regresión al agregar nuevas reglas.
- **Referencia de interfaz** para la futura integración con Claude Haiku real (PUENTE-5): la firma `cerebro_mock(entrada: dict) -> dict` y la estructura de salida son el contrato que el cerebro real deberá respetar.

---

## 4. Qué NO queda habilitado

| Acción | Estado |
|---|---|
| Conectar Claude Haiku API real | NO — requiere PUENTE-5 y microciclo de secrets separado |
| Abrir navegador o usar Playwright | NO — requiere PUENTE-4 con autorización explícita |
| Modificar `cerebro_mock.py` sin nuevo microciclo | NO — cualquier cambio al código requiere PUENTE-2B o posterior |
| Agregar reglas nuevas sin contrato previo | NO — cada nuevo conjunto de reglas requiere contrato documental primero (PUENTE-2A) |
| Conectar el mock a sistemas reales externos | NO — el mock es estrictamente local |
| Usar el mock en producción | NO — prohibición absoluta según reglas PLIC |

---

## 5. Condiciones para avanzar al próximo microciclo

Para iniciar PUENTE-2A se deben cumplir todas estas condiciones:

1. PUENTE-1C mergeado a `main` con commit verificable.
2. Autorización explícita de Ariel para iniciar PUENTE-2A.
3. Sin PR abierto pendiente de merge en el repo.
4. Working tree limpio.
5. Tests existentes (29) siguen pasando en `main`.

---

## 6. Backlog de mejoras sugeridas

Los siguientes items son mejoras identificadas en la auditoría PUENTE-1C. No bloquean el avance pero deben incorporarse en microciclos futuros:

| # | Mejora | Prioridad | Microciclo sugerido |
|---|---|---|---|
| 1 | Evaluar `contexto_actual` y `estado_del_ciclo` en las reglas | Media | PUENTE-2B |
| 2 | Implementar regla para `escalar_a_ariel` | Media | PUENTE-2B |
| 3 | Implementar regla para `declarar_bloqueo` | Media | PUENTE-2B |
| 4 | Agregar guarda defensiva contra entrada no-dict | Baja | PUENTE-2B |
| 5 | Evaluar `autorizaciones_disponibles` para decisión | Media | PUENTE-2B |
| 6 | Agregar reglas para otros proyectos reales del ecosistema | Alta | PUENTE-2A (en contrato) |
| 7 | Tests para casos edge documentados (opción numérica sin contexto, dict vacío, entrada no-dict) | Baja | PUENTE-2B |

---

## 7. Próximo microciclo sugerido

**PUENTE-2A — Contrato documental de reglas PLIC para el Cerebro Portero Mock**

Objetivo: definir documentalmente el contrato de las reglas PLIC que el Cerebro Portero Mock debe evaluar. Incluye:

- Definición de los proyectos del ecosistema con riesgo conocido.
- Reglas para `escalar_a_ariel` y `declarar_bloqueo`.
- Uso de `contexto_actual`, `estado_del_ciclo` y `autorizaciones_disponibles` en las decisiones.
- Criterios de clasificación de riesgo basados en el estado del ciclo activo.

Este microciclo es **solo documental**. No implementa código. No usa API real. No abre navegador.

> No iniciar PUENTE-2A hasta que PUENTE-1C esté cerrado con evidencia verificable (commit + push) y autorización explícita de Ariel.
