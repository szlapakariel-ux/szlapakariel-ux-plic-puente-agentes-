# PUENTE-4D-BACKLOG — Corrección de estados suspendido y mergeado en Cerebro Portero Mock

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-4D-BACKLOG |
| Rama base | `main` |
| Commit base | `8a6aeca2e3662b4d01b845601c8dbb847b81bca1` |
| Rama de trabajo | `fix/puente-4d-backlog-estados-cerebro` |
| Estado de PUENTE-4C-BACKLOG | Cerrado en main — 150 tests OK |
| Tests al iniciar | 150/150 OK |

---

## 2. Backlog abordado

### B-04 — estado `suspendido` + continuidad

**Problema detectado:** Cuando `estado_del_ciclo` era `"suspendido"` y el texto indicaba continuidad (`"seguí"`, `"continuá"`, `"seguimos"`, `"1"`), el Cerebro caía en la regla genérica de Prioridad 16 y devolvía `continuar_documental / bajo`, como si el ciclo pudiera retomarse automáticamente.

| Texto | Estado | Comportamiento anterior | Comportamiento correcto |
|---|---|---|---|
| `"seguí"` | `suspendido` | `continuar_documental / bajo` | `pedir_autorizacion / medio` |
| `"continuá"` | `suspendido` | `continuar_documental / bajo` | `pedir_autorizacion / medio` |
| `"1"` | `suspendido` | `continuar_documental / bajo` | `pedir_autorizacion / medio` |

**Corrección aplicada:** Se añadió una nueva regla de prioridad (después de Prioridad 14 — anti-cartero y antes de Prioridad 15 — "1" con contexto) que detecta `estado == "suspendido"` + continuidad y devuelve `pedir_autorizacion / medio`, con `requiere_ariel: True` y motivo que menciona explícitamente "suspendido".

---

### B-05 — estado `mergeado` + continuidad

**Problema detectado:** Cuando `estado_del_ciclo` era `"mergeado"` y el texto indicaba continuidad, el Cerebro devolvía el motivo genérico sin reconocer que el ciclo anterior fue mergeado correctamente. No había motivo específico.

| Texto | Estado | Comportamiento anterior | Comportamiento correcto |
|---|---|---|---|
| `"seguí"` | `mergeado` | `continuar_documental / bajo` (motivo genérico) | `continuar_documental / bajo` (motivo menciona "mergeado") |
| `"continuá"` | `mergeado` | `continuar_documental / bajo` (motivo genérico) | `continuar_documental / bajo` (motivo menciona "mergeado") |
| `"1"` | `mergeado` | `continuar_documental / bajo` (motivo genérico) | `continuar_documental / bajo` (motivo menciona "mergeado") |

**Corrección aplicada:** Se añadió `elif estado == "mergeado"` en la Prioridad 16 (continuidad segura) con motivo específico que menciona "mergeado" y que el ciclo anterior fue completado por merge.

---

## 3. Problema detectado

Dos keywords de estado (`suspendido` y `mergeado`) no tenían reglas dedicadas en el Cerebro Portero Mock:

- `"suspendido"`: caía en la regla genérica de continuidad → devolvía `continuar_documental` incorrectamente. Un ciclo suspendido NO debe retomarse automáticamente.
- `"mergeado"`: caía en la regla genérica de continuidad → devolvía `continuar_documental` con motivo genérico. Correcto en decisión, pero sin contexto específico del estado.

---

## 4. Corrección aplicada

### Nueva regla — B-04 (entre Prioridad 14 y 15)

```python
# B-04 — estado_del_ciclo: suspendido + continuidad
if estado == "suspendido" and (
    texto.strip() == "1" or any(p in texto_lower for p in _PALABRAS_CONTINUIDAD)
):
    return _respuesta(
        intencion="Continuación solicitada con ciclo suspendido",
        confianza="alta",
        riesgo="medio",
        decision="pedir_autorizacion",
        requiere_ariel=True,
        requiere_torre=True,
        accion=None,
        opciones=[
            "1) Revisar el estado del ciclo suspendido con Ariel antes de continuar",
            "2) Cerrar el ciclo suspendido y abrir uno nuevo",
            "3) Mantener suspensión hasta nueva instrucción",
        ],
        motivo="estado_del_ciclo es 'suspendido'. Un ciclo suspendido no puede retomarse automáticamente — requiere revisión y autorización explícita de Ariel y Torre antes de continuar.",
    )
```

### Modificación de Prioridad 16 — B-05

```python
# Prioridad 16 — continuidad segura
if texto.strip() == "1" or any(p in texto_lower for p in _PALABRAS_CONTINUIDAD):
    if estado == "cerrado":
        motivo_cont = "... ciclo anterior está completo ..."
    elif estado == "mergeado":
        motivo_cont = "Intención de continuación reconocida. estado_del_ciclo es 'mergeado' — el ciclo anterior fue mergeado correctamente. Torre confirma contexto del próximo paso documental antes de ejecutar."
    else:
        motivo_cont = "Intención de continuación reconocida. Riesgo bajo. Torre confirma contexto antes de ejecutar."
```

### Comportamiento de prioridad — garantizado

Las reglas restrictivas existentes (secrets, producción, merge, API real) verifican ANTES que la nueva regla B-04, por lo tanto:

| Texto mixto | Estado | Resultado |
|---|---|---|
| `"seguí y mandalo a producción"` | `suspendido` | `no_ejecutar / prohibido` (Prioridad 2 gana) |
| `"seguí y usá API real"` | `mergeado` | `no_ejecutar / prohibido` (Prioridad 4 gana) |
| `"seguí y mergealo"` | `suspendido` | `pedir_autorizacion / alto` (Prioridad 9 gana) |

---

## 5. Tests agregados o ajustados

### Tests nuevos (23 nuevos, total 173)

Clase `TestCerebroMockEstadosSuspendidoMergeado`:

| Test | Verifica |
|---|---|
| `test_segui_estado_suspendido_decision` | `"seguí"` + suspendido → `pedir_autorizacion` |
| `test_segui_estado_suspendido_riesgo` | `"seguí"` + suspendido → `medio` |
| `test_continua_estado_suspendido_decision` | `"continuá"` + suspendido → `pedir_autorizacion` |
| `test_continua_estado_suspendido_riesgo` | `"continuá"` + suspendido → `medio` |
| `test_uno_estado_suspendido_decision` | `"1"` + suspendido → `pedir_autorizacion` |
| `test_uno_estado_suspendido_riesgo` | `"1"` + suspendido → `medio` |
| `test_suspendido_motivo_menciona_suspendido` | motivo contiene "suspendido" |
| `test_suspendido_requiere_ariel` | `requiere_ariel: True` |
| `test_suspendido_requiere_torre` | `requiere_torre: True` |
| `test_segui_estado_mergeado_decision` | `"seguí"` + mergeado → `continuar_documental` |
| `test_segui_estado_mergeado_riesgo` | `"seguí"` + mergeado → `bajo` |
| `test_continua_estado_mergeado_decision` | `"continuá"` + mergeado → `continuar_documental` |
| `test_continua_estado_mergeado_riesgo` | `"continuá"` + mergeado → `bajo` |
| `test_uno_estado_mergeado_decision` | `"1"` + mergeado → `continuar_documental` |
| `test_uno_estado_mergeado_riesgo` | `"1"` + mergeado → `bajo` |
| `test_mergeado_motivo_menciona_mergeado` | motivo contiene "mergeado" |
| `test_mergeado_no_requiere_ariel` | `requiere_ariel: False` |
| `test_mergeado_requiere_torre` | `requiere_torre: True` |
| `test_produccion_gana_sobre_suspendido` | `"seguí y mandalo a producción"` + suspendido → `no_ejecutar / prohibido` |
| `test_api_real_gana_sobre_mergeado` | `"seguí y usá API real"` + mergeado → `no_ejecutar / prohibido` |
| `test_merge_gana_sobre_suspendido` | `"seguí y mergealo"` + suspendido → `pedir_autorizacion / alto` |
| `test_segui_estado_cerrado_regresion_decision` | estado cerrado sigue → `continuar_documental` |
| `test_segui_estado_cerrado_regresion_riesgo` | estado cerrado sigue → `bajo` |

### Tests originales conservados (150)

Los 150 tests de PUENTE-4C-BACKLOG y anteriores siguen pasando sin modificación.

---

## 6. Resultado de tests

```
python -m unittest discover -s tests

Ran 173 tests in 0.004s

OK
```

**173/173 tests pasan.** Sin errores. Sin warnings.

---

## 7. Qué NO se implementó

| Ítem | Estado |
|---|---|
| Conexión a API real | NO — prohibición absoluta |
| Navegador real / Playwright | NO — prohibición absoluta |
| Nuevas capacidades de mano local | NO — no modificado |
| Modificación de `mano_local_simulada.py` | NO — no tocado |
| Nuevas acciones externas | NO — función pura |
| Workflows o CI | NO — prohibición absoluta |
| Dependencias instaladas | NO — cero dependencias |

---

## 8. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin imports nuevos | CONFIRMADO — `cerebro_mock.py` sigue sin ningún `import` |
| Función pura preservada | CONFIRMADO — sin I/O, sin red, sin subprocess |
| `mano_local_simulada.py` no modificado | CONFIRMADO |
| Sin API real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin dependencias instaladas | CONFIRMADO |
| Sin repos prohibidos | CONFIRMADO — torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero no tocados |
| Contrato de salida 9 campos respetado | CONFIRMADO |
| Tests originales pasan | CONFIRMADO — 150/150 originales + 23 nuevos = 173/173 OK |

---

## 9. Próximo microciclo sugerido

**PUENTE-4E — Auditoría técnica de corrección de estados suspendido/mergeado en Cerebro Portero Mock**

Objetivo: revisar la implementación de PUENTE-4D-BACKLOG, validar que los estados `suspendido` y `mergeado` se manejan correctamente, confirmar que las reglas restrictivas siguen ganando en textos mixtos, y evaluar si quedan casos edge no cubiertos.

Alcance:
- Solo lectura.
- Sin modificaciones al código.
- Sin modificaciones a tests.
- Auditar la nueva regla B-04 con casos edge adicionales.
- Auditar el motivo de B-05 con variantes de texto.

Restricciones:
- Solo lectura.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.
- Sin secrets.
- Sin producción.

> No iniciar PUENTE-4E hasta que PUENTE-4D-BACKLOG esté cerrado con evidencia verificable (commit + push) y autorización explícita de Ariel.
