# PUENTE-6D-MODELO — Diagnóstico de modelo previo a primera llamada real

> **ESTADO: RESUELTO** — Bloqueo resuelto en PUENTE-6D-MODELO-FIX. Modelo actualizado a `claude-haiku-4-5-20251001`.

## 1. Nombre del diagnóstico

**PUENTE-6D-MODELO — Verificación del modelo permitido antes de primera llamada real a Anthropic**

---

## 2. Objetivo

Diagnosticar documentalmente si el modelo registrado en el contrato PUENTE-6D-A para la primera llamada real sigue siendo válido según la documentación pública actual de Anthropic, antes de ejecutar cualquier llamada real.

Este diagnóstico:
- Compara el modelo documentado en PUENTE-6D-A con el estado actual de modelos de Anthropic.
- Registra el bloqueo detectado.
- Recomienda el camino de corrección.
- No ejecuta ninguna llamada real.

---

## 3. Autorización recibida de Ariel para PUENTE-6D real

> "Autorizo PUENTE-6D real: primera llamada real controlada a Anthropic/Haiku, completando antes el checklist operativo PUENTE-6D-A."

**Interpretación operativa**: La autorización fue recibida, pero el presente diagnóstico detecta un bloqueo controlado previo a la ejecución — modelo potencialmente retirado. La llamada real no puede ejecutarse hasta resolver el bloqueo.

---

## 4. Aclaraciones explícitas

| Ítem | Estado |
|---|---|
| No se ejecutó llamada real | CONFIRMADO |
| No se pidió API key | CONFIRMADO |
| No se leyó API key | CONFIRMADO |
| No se usó API real | CONFIRMADO |
| No se usó SDK real | CONFIRMADO |
| No se usó Claude Haiku real | CONFIRMADO |
| No se creó `.env` | CONFIRMADO |
| No se tocaron secrets | CONFIRMADO |
| No se abrió navegador | CONFIRMADO |
| No se usó Playwright | CONFIRMADO |
| No se tocó producción | CONFIRMADO |
| No se modificó código | CONFIRMADO |
| No se modificaron tests | CONFIRMADO |

---

## 5. Modelo documentado previamente

En los siguientes documentos en `main`, el modelo previsto para la primera llamada real es:

| Documento | Referencia al modelo |
|---|---|
| `docs/puente-6d-a-contrato-operativo-primera-llamada-real.md` | `claude-3-5-haiku-latest` — sección 5 (modelo) |
| `docs/puente-6d-a-checklist-ejecucion-primera-llamada-real.md` | `claude-3-5-haiku-latest` o `claude-3-haiku-20240307` — bloque 5 |
| `docs/puente-6d-checklist-previo-primera-llamada-real.md` | `claude-3-5-haiku-latest` — sección 6.4 |
| `src/plic_puente_agentes/cliente_api_real_bloqueado.py` | `_MODELO_AUTORIZADO = "claude-3-5-haiku-latest"` |
| `src/plic_puente_agentes/cliente_api_real_preparado.py` | `"claude-3-5-haiku-latest"` como modelo autorizado |

---

## 6. Riesgo detectado

### Descripción del bloqueo

**Torre detectó** que la documentación pública de Anthropic indica que `claude-3-5-haiku-latest` fue **retirado** y que el modelo de reemplazo recomendado es `claude-haiku-4-5-20251001`.

| Campo | Valor |
|---|---|
| Modelo en contrato | `claude-3-5-haiku-latest` |
| Estado según Anthropic | Retirado — deprecated |
| Modelo de reemplazo recomendado | `claude-haiku-4-5-20251001` |
| Fuente | Documentación pública de Anthropic — Model Deprecations |

### Por qué es un bloqueo controlado y no un bloqueo de seguridad

Este bloqueo **no** es de seguridad interna (no hay riesgo de fuga de datos, ejecución de código, ni escalada no autorizada). Es un bloqueo **operativo**:

- Si se ejecuta la primera llamada real con `claude-3-5-haiku-latest` y ese modelo ya está retirado, la llamada podría fallar con error de modelo no disponible.
- El resultado de la primera llamada real podría quedar contaminado por un error de modelo en lugar de producir una respuesta limpia de `PLIC_OK`.
- Sería ineficiente gastar la primera llamada real autorizada en un modelo potencialmente inválido.
- El contrato PUENTE-6D-A define condiciones de corte precisas — si la primera llamada falla por modelo incorrecto, los logs de diagnóstico serían confusos.

### Alcance del bloqueo

| Ítem | Estado |
|---|---|
| ¿Bloquea llamada real? | SÍ — hasta actualizar modelo permitido |
| ¿Bloquea PR documental de este diagnóstico? | NO — este diagnóstico puede mergearse |
| ¿Requiere modificar código? | SÍ — en microciclo PUENTE-6D-MODELO-FIX separado con autorización de Ariel |
| ¿Requiere modificar documentos? | SÍ — en microciclo PUENTE-6D-MODELO-FIX separado |
| ¿Requiere nueva auditoría? | SÍ — antes de PUENTE-6D real |

---

## 7. Modelo recomendado para corregir el contrato

| Campo | Valor |
|---|---|
| Modelo recomendado | `claude-haiku-4-5-20251001` |
| Familia | Claude Haiku 4.5 |
| Tipo | Modelo de producción activo |
| Fuente | Documentación pública de Anthropic — Model Deprecations |

### Archivos que deben actualizarse en PUENTE-6D-MODELO-FIX

| Archivo | Cambio necesario |
|---|---|
| `docs/puente-6d-a-contrato-operativo-primera-llamada-real.md` | Actualizar modelo de `claude-3-5-haiku-latest` a `claude-haiku-4-5-20251001` |
| `docs/puente-6d-a-checklist-ejecucion-primera-llamada-real.md` | Actualizar bloque 5 — modelo autorizado |
| `docs/puente-6d-checklist-previo-primera-llamada-real.md` | Actualizar sección 6.4 y sección 7 |
| `src/plic_puente_agentes/cliente_api_real_bloqueado.py` | Actualizar `_MODELO_AUTORIZADO` |
| `src/plic_puente_agentes/cliente_api_real_preparado.py` | Actualizar modelo autorizado |
| Tests afectados | Actualizar referencias a `claude-3-5-haiku-latest` en tests del gate y del cliente preparado |

---

## 8. Impacto

| Ítem | Estado |
|---|---|
| Primera llamada real con modelo retirado | NO RECOMENDADO — riesgo de error de modelo no disponible |
| Checklist completo para PUENTE-6D real | INCOMPLETO hasta actualizar modelo permitido |
| Uso de API real antes de corrección | NO autorizado — bloqueo controlado activo |
| Tests actuales (416/416) | Siguen pasando — el gate bloquea llamada real estructuralmente |
| Seguridad interna del repo | No afectada — el bloqueo es solo operativo |
| Continuidad de desarrollo | Puede continuar con PUENTE-6D-MODELO-FIX sin afectar componentes existentes |

---

## 9. Decisión recomendada

**Abrir microciclo documental/técnico mínimo PUENTE-6D-MODELO-FIX** para:

1. Actualizar el modelo permitido de `claude-3-5-haiku-latest` a `claude-haiku-4-5-20251001` en todos los documentos y módulos afectados.
2. Actualizar los tests que referencian el modelo anterior.
3. Verificar que los 416 tests (más los nuevos del fix) siguen pasando.
4. Emitir nuevo dictamen antes de PUENTE-6D real.

Este microciclo requiere autorización explícita de Ariel porque modifica código Python (`cliente_api_real_bloqueado.py`, `cliente_api_real_preparado.py`) y tests.

---

## 10. Qué NO se hizo en este ciclo

| Ítem | Estado |
|---|---|
| Llamada real | NO — prohibición absoluta |
| API real | NO — prohibición absoluta |
| SDK de Anthropic | NO — no instalado ni importado |
| API key pedida o leída | NO |
| `.env` | NO |
| Navegador | NO |
| Playwright | NO |
| Producción | NO |
| Modificación de código | NO — solo documentación |
| Modificación de tests | NO |
| Scripts ejecutables | NO |
| Workflows | NO |
| Secrets | NO |

---

## 11. Resultado de tests

```
python -m unittest discover -s tests
Ran 416 tests in 0.019s
OK
```

**416/416 OK** — sin regresiones. El gate de llamada real sigue activo: `llamada_real_ejecutada=False` y `llamada_real_bloqueada=True` en toda rama de código.

---

## 12. Dictamen

### **BLOQUEO CONTROLADO — LLAMADA REAL SUSPENDIDA HASTA ACTUALIZAR MODELO PERMITIDO**

La autorización de Ariel para PUENTE-6D real fue recibida y registrada. Sin embargo, el modelo documentado en el contrato (`claude-3-5-haiku-latest`) fue retirado por Anthropic según documentación pública. El modelo de reemplazo recomendado es `claude-haiku-4-5-20251001`.

Por este motivo, **la primera llamada real queda suspendida** hasta que:

1. PUENTE-6D-MODELO-FIX actualice el modelo en documentos y código.
2. Los tests del fix pasen.
3. La auditoría del fix emita dictamen A) APTO.
4. Se reciba instrucción explícita separada de Ariel para ejecutar PUENTE-6D real con el modelo corregido.

Este diagnóstico no cancela la autorización de Ariel — la extiende al modelo correcto.

---

## 13. Próximo microciclo sugerido

**PUENTE-6D-MODELO-FIX — Actualizar modelo permitido a `claude-haiku-4-5-20251001`**

Objetivo: actualizar en una única rama el modelo permitido en todos los documentos, módulos Python y tests afectados, sin ejecutar ninguna llamada real.

Alcance:
- Actualizar `_MODELO_AUTORIZADO` en `cliente_api_real_bloqueado.py`.
- Actualizar modelo autorizado en `cliente_api_real_preparado.py`.
- Actualizar referencias en 3 documentos PUENTE-6D.
- Actualizar tests que referencian `claude-3-5-haiku-latest`.
- Verificar que todos los tests pasan.
- Emitir nuevo dictamen técnico antes de PUENTE-6D real.

Restricciones:
- Sin llamada real.
- Sin API real.
- Sin SDK real.
- Sin API keys.
- Sin navegador.
- Sin Playwright.
- Sin producción.
- Sin `.env`.
- Sin secrets.

> No iniciar PUENTE-6D real hasta que PUENTE-6D-MODELO-FIX esté cerrado en `main` con evidencia verificable y dictamen A) APTO.
