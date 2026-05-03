# PUENTE-1C — Auditoría Técnica del Cerebro Portero Mock

## 1. Nombre del microciclo

**PUENTE-1C — Auditoría técnica del Cerebro Portero Mock y decisión de integración mínima**

Rama de trabajo: `docs/puente-1c-auditoria-cerebro-mock`
Sin modificaciones al código. Sin API real. Solo auditoría y documentación.

---

## 2. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-1C |
| Rama base | `main` |
| Commit base | `0c86a7325ccfa421497fb5f28e8deb7dfd2db581` |
| Estado de PUENTE-1B | Cerrado — Cerebro Portero Mock mergeado a main |
| Tests en main | 29/29 OK al iniciar este ciclo |

---

## 3. Archivos auditados

| Archivo | Rol |
|---|---|
| `docs/contrato-cerebro-mock.md` | Contrato de referencia (PUENTE-1A) |
| `src/plic_puente_agentes/cerebro_mock.py` | Implementación auditada (PUENTE-1B) |
| `tests/test_cerebro_mock.py` | Suite de tests (PUENTE-1B) |

---

## 4. Resultado de tests

```
python -m unittest discover -s tests -v

Ran 29 tests in 0.001s

OK
```

**29/29 tests pasan.** Sin errores. Sin warnings. Tiempo: 0.001s.

---

## 5. Verificación de contrato

### 5.1 Campos de entrada

El contrato PUENTE-1A define 7 campos de entrada:

| Campo del contrato | Presente en cerebro_mock | Observación |
|---|---|---|
| `texto_original` | ✓ — `entrada.get("texto_original", "")` | Usado como base de todas las reglas |
| `contexto_actual` | Aceptado pero no evaluado | No hay reglas que usen este campo todavía |
| `proyecto_detectado` | Aceptado pero no evaluado | No hay reglas que usen este campo todavía |
| `estado_del_ciclo` | Aceptado pero no evaluado | No hay reglas que usen este campo todavía |
| `riesgo_inicial` | Aceptado pero no evaluado | No hay reglas que usen este campo todavía |
| `ultima_respuesta_portero` | Aceptado pero no evaluado | No hay reglas que usen este campo todavía |
| `autorizaciones_disponibles` | Aceptado pero no evaluado | No hay reglas que usen este campo todavía |

**Evaluación:** Correcto para un mock mínimo. El contrato establece que estos campos son "mínimos esperados", no que todos deban ser evaluados en la primera implementación. `texto_original` es el campo central y es el único evaluado, lo cual es consistente con el alcance de PUENTE-1B.

### 5.2 Campos de salida

El contrato PUENTE-1A define 9 campos de salida. Verificados contra `_respuesta()`:

| Campo del contrato | Presente en salida | Nombre exacto |
|---|---|---|
| `intencion_detectada` | ✓ | `"intencion_detectada"` |
| `confianza` | ✓ | `"confianza"` |
| `riesgo` | ✓ | `"riesgo"` |
| `decision` | ✓ | `"decision"` |
| `requiere_ariel` | ✓ | `"requiere_ariel"` |
| `requiere_torre` | ✓ | `"requiere_torre"` |
| `accion_segura_sugerida` | ✓ | `"accion_segura_sugerida"` |
| `opciones_para_ariel` | ✓ | `"opciones_para_ariel"` |
| `motivo` | ✓ | `"motivo"` |

**Evaluación:** Contrato de salida 100% respetado. Todos los campos están presentes con los nombres exactos definidos en PUENTE-1A.

### 5.3 Decisiones permitidas

El contrato define 7 decisiones. Verificadas contra el código:

| Decisión del contrato | Implementada | Regla |
|---|---|---|
| `continuar_documental` | ✓ | Reglas 4 y 5 |
| `pedir_autorizacion` | ✓ | Regla 6 |
| `reformular` | ✓ | Reglas 3, 8 y 9 (default) |
| `suspender` | ✓ | Regla 7 |
| `declarar_bloqueo` | No implementada | Sin regla activa |
| `escalar_a_ariel` | No implementada | Sin regla activa |
| `no_ejecutar` | ✓ | Reglas 1 y 2 |

**Evaluación:** `declarar_bloqueo` y `escalar_a_ariel` no tienen reglas activas en el mock, pero están definidas como valores válidos en el test `test_decision_valores_validos`. No es una violación del contrato — son decisiones disponibles pero aún no activadas por ninguna regla en esta versión mínima. El set de valores válidos está correcto.

### 5.4 Riesgos permitidos

| Riesgo del contrato | Implementado | Regla |
|---|---|---|
| `bajo` | ✓ | Reglas 4, 5, 7 |
| `medio` | ✓ | Reglas 3, 8, 9 |
| `alto` | ✓ | Regla 6 |
| `prohibido` | ✓ | Reglas 1, 2 |

**Evaluación:** Los 4 niveles de riesgo están implementados. Contrato 100% respetado.

---

## 6. Verificación de implementación

| Aspecto | Estado | Evidencia |
|---|---|---|
| Función pura | ✓ | Sin efectos secundarios. Mismo input → mismo output siempre. |
| Sin imports | ✓ | `cerebro_mock.py` no contiene ninguna línea `import`. Verificado con grep: sin resultados. |
| Sin llamadas a API | ✓ | No hay `requests`, `httpx`, `anthropic`, `openai`, ni similares. |
| Sin lectura de entorno | ✓ | No hay `os.environ`, `os.getenv`, ni lectura de variables de entorno. |
| Sin apertura de archivos | ✓ | No hay `open()`, `pathlib`, ni acceso a filesystem. |
| Sin comandos del sistema | ✓ | No hay `subprocess`, `os.system`, ni similares. |
| Sin apertura de navegador | ✓ | No hay `playwright`, `selenium`, ni `webbrowser`. |
| Función auxiliar `_respuesta` | ✓ | Helper interno que construye el dict de salida. Convención de nombre con `_` indica uso interno. |
| Constantes de módulo | ✓ | `_PALABRAS_PROHIBIDAS` y `_PALABRAS_SECRETS` son tuplas inmutables a nivel de módulo. Correcto. |

---

## 7. Verificación de reglas

| Regla | Condición | Decisión | Riesgo | Resultado | Observación |
|---|---|---|---|---|---|
| 1 | `"producción"` o `"produccion"` en texto | `no_ejecutar` | `prohibido` | ✓ | Cubre variante sin tilde |
| 2 | `"secrets"`, `"token"`, `"clave"`, `"credencial"` | `no_ejecutar` | `prohibido` | ✓ | Prioridad sobre reglas 3-9 |
| 3 | `"pasalo a claude"` | `reformular` | `medio` | ✓ | Normalizado a minúsculas |
| 4 | Texto exacto `"1"` | `continuar_documental` | `bajo` | ✓ | Usa `texto.strip()` — tolera espacios |
| 5 | `"seguí con lo del celu"` o `"segui con lo del celu"` | `continuar_documental` | `bajo` | ✓ | Cubre variante sin tilde |
| 6 | `"sofse"` | `pedir_autorizacion` | `alto` | ✓ | Case-insensitive vía `lower()` |
| 7 | `"suspender"` | `suspender` | `bajo` | ✓ | — |
| 8 | Texto vacío o no-string | `reformular` | `medio` | ✓ | Primer guard del flujo |
| 9 | Default (cualquier otro) | `reformular` | `medio` | ✓ | Camino seguro por defecto |

**Prioridad de reglas:** Reglas 1 y 2 (riesgo `prohibido`) están evaluadas ANTES que las demás. Un texto que contenga tanto "producción" como otro término siempre resultará en `no_ejecutar`. El orden es correcto desde el punto de vista de seguridad.

---

## 8. Verificación de seguridad

| Verificación | Estado |
|---|---|
| Sin Claude Haiku real | CONFIRMADO |
| Sin API real | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin secrets en código | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin dependencias externas | CONFIRMADO — solo stdlib Python |
| Sin repos prohibidos | CONFIRMADO — torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero no referenciados operativamente |

---

## 9. Casos edge detectados

Los siguientes casos edge no tienen cobertura de tests actualmente. No son bugs ni violaciones del contrato — son áreas de mejora para versiones futuras.

### 9.1 Ambigüedad de mayúsculas/minúsculas en regla 4

La regla 4 verifica `texto.strip() == "1"`. Si el texto es `"  1  "` (con espacios), `strip()` lo maneja. Sin embargo, `"1."` o `"(1)"` no serían reconocidos como opciones numéricas. Comportamiento actual: caen al default (`reformular`). Comportamiento esperado a futuro: podría necesitar normalización más robusta.

### 9.2 Frases con riesgo mezclado

Ejemplo: `"pasalo a Claude pero no a producción"`. Bajo las reglas actuales, la regla 1 (`producción`) tiene prioridad y devuelve `no_ejecutar`. Este es el comportamiento CORRECTO y SEGURO — cualquier mención de "producción" activa el bloqueo independientemente del contexto. No es un bug, pero conviene documentarlo explícitamente.

### 9.3 Opciones numéricas fuera de contexto

`"1"` siempre produce `continuar_documental` aunque no haya un contexto previo con opciones. La función no tiene estado ni memoria entre llamadas. Comportamiento actual: correcto para el mock mínimo. A futuro: el campo `ultima_respuesta_portero` podría usarse para validar que efectivamente se presentaron opciones antes.

### 9.4 Proyectos reales distintos de SOFSE

Solo SOFSE tiene regla explícita de `pedir_autorizacion`. Otros proyectos reales (ej. `"torre-control"`, `"agente-saas"`) no tienen regla dedicada y caerían al default (`reformular`). El default es seguro pero no específico. A futuro: PUENTE-2 podría incorporar reglas para proyectos conocidos del ecosistema.

### 9.5 Entradas no-dict

Si se llama `cerebro_mock("texto")` (pasando un string en lugar de dict), `entrada.get()` fallaría con `AttributeError`. El contrato define la firma como `entrada: dict` — la responsabilidad de pasar un dict es del caller. No es un bug del mock pero podría añadirse una guarda defensiva en versiones futuras.

### 9.6 Variantes de "token"

La palabra `"token"` en `_PALABRAS_SECRETS` produciría `no_ejecutar` para frases como `"dame el token de git"`, `"renovar token"`, o incluso `"token de seguridad expirado"`. Es el comportamiento CORRECTO y CONSERVADOR — cualquier referencia a tokens activa el bloqueo.

---

## 10. Riesgos

| Riesgo | Nivel | Mitigación actual |
|---|---|---|
| Texto ambiguo que evade reglas de keywords | Bajo | Default a `reformular` — comportamiento seguro |
| Intención válida bloqueada por keyword (false positive) | Bajo-medio | Aceptable en fase mock — Torre puede reformular |
| Llamada con dict vacío `{}` | Bajo | Manejado — `texto_original` ausente → `reformular` |
| Llamada con `texto_original: None` | Bajo | Manejado — `not isinstance(texto, str)` devuelve `reformular` |
| Llamada con dict que no es dict | Bajo | No manejado — falla en `AttributeError`. Documentado en backlog. |
| Evasión de regla de producción por ortografía alternativa | Bajo | Regla cubre `"producción"` y `"produccion"`. Otras variantes (ej. inglés "production") no cubiertas. |

---

## 11. Hallazgos

### Hallazgos positivos

1. **Función pura verificada:** `cerebro_mock.py` sin imports, sin efectos secundarios, sin conexiones externas.
2. **Contrato de salida 100% respetado:** Los 9 campos están presentes con nombres exactos.
3. **Reglas de prohibición con prioridad correcta:** Producción y secrets evaluados primero.
4. **Cobertura de variantes con/sin tilde:** Reglas 1 y 5 cubren variantes `"produccion"/"producción"` y `"segui/seguí"`.
5. **29 tests pasan en 0.001s:** Sin dependencias externas, sin flakiness.
6. **Decisiones y riesgos válidos verificados en tests:** La clase `TestCerebroMockEstructuraSalida` valida los valores contra los sets permitidos por el contrato.

### Hallazgos de mejora (no bloquean integración)

1. **6 campos de entrada no evaluados:** `contexto_actual`, `proyecto_detectado`, `estado_del_ciclo`, `riesgo_inicial`, `ultima_respuesta_portero`, `autorizaciones_disponibles` son aceptados pero ignorados. Esperado para mock mínimo.
2. **2 decisiones sin regla activa:** `declarar_bloqueo` y `escalar_a_ariel` están en el set válido pero sin casos que las disparen. Backlog para PUENTE-2+.
3. **Sin guarda contra entrada no-dict:** `cerebro_mock(42)` produciría error. Mejora menor para versión siguiente.
4. **Sin cobertura de variantes de "production" en inglés:** El sistema opera en español por diseño. No es un gap real en el contexto actual.

### Hallazgos de seguridad

Ninguno. El código es estrictamente local, sin imports, sin conexiones, sin acceso a filesystem ni entorno.

---

## 12. Dictamen técnico

**Contrato:** 100% respetado en campos de salida. Campos de entrada opcionales aceptados pero no evaluados — correcto para mock mínimo.

**Implementación:** Función pura sin imports. Zero riesgo de ejecución externa. Correcto.

**Reglas:** 9 reglas activas. 7/9 decisiones del contrato disponibles (2 sin activar: `declarar_bloqueo`, `escalar_a_ariel`). 4/4 niveles de riesgo cubiertos. Correcto.

**Tests:** 29/29 OK. Cobertura de los 7 casos críticos del contrato más validaciones de estructura y valores. Sin dependencias externas.

**Casos edge:** 6 identificados, ninguno es un bug activo. Todos son mejoras para versiones posteriores.

**Seguridad:** Sin vectores de riesgo. Zero conexiones externas. Zero acceso a entorno.

### DICTAMEN FINAL: **A) APTO PARA INTEGRACIÓN MÍNIMA COMO BASE DEL PUENTE**

El Cerebro Portero Mock en su estado actual es apto para ser usado como base de la integración mínima del Puente. Los hallazgos de mejora identificados son menores y no bloquean el avance al siguiente microciclo.
