# PUENTE-3C-BACKLOG — Corrección de falsos positivos ci/prod/action en Cerebro Portero Mock

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-3C-BACKLOG |
| Rama base | `main` |
| Commit base | `b4a5aef5f3a1e56a109231c49c8aa43edd6fe834` |
| Rama de trabajo | `fix/puente-3c-backlog-falsos-positivos-keywords` |
| Estado de PUENTE-3B | Cerrado en main — 86 tests OK |
| Tests al iniciar | 86/86 OK |

---

## 2. Backlog abordado

### B-01 — Keyword `"ci"`

**Problema detectado:** `"ci"` como substring dentro de `_PALABRAS_WORKFLOW` disparaba la regla de workflow para palabras españolas que contienen "ci" como parte interna de la palabra:

| Texto | Comportamiento anterior | Comportamiento correcto |
|---|---|---|
| `"el microciclo avanza"` | `pedir_autorizacion`/`alto` | `reformular`/`medio` |
| `"la acción documental"` | `pedir_autorizacion`/`alto` | `reformular`/`medio` |
| `"servicio activo"` | `pedir_autorizacion`/`alto` | `reformular`/`medio` |
| `"activar CI"` | `pedir_autorizacion`/`alto` | `pedir_autorizacion`/`alto` ✓ |

**Corrección aplicada:** Se eliminó `"ci"` de `_PALABRAS_WORKFLOW`. Se creó la tupla `_TOKENS_WORKFLOW = ("ci",)` y el helper `_es_token()` que verifica límite de palabra usando `str.isalpha()` sin imports. La regla de Prioridad 7 ahora combina frases exactas y tokens con límite.

---

### B-02 — Keyword `"prod"`

**Problema detectado:** `"prod"` como substring dentro de `_PALABRAS_PRODUCCION` disparaba la regla de producción para palabras que contienen "prod" como parte interna:

| Texto | Comportamiento anterior | Comportamiento correcto |
|---|---|---|
| `"revisá el producto"` | `no_ejecutar`/`prohibido` | `reformular`/`medio` |
| `"vamos a producir documentación"` | `no_ejecutar`/`prohibido` | `reformular`/`medio` |
| `"reproducir el caso"` | `no_ejecutar`/`prohibido` | `reformular`/`medio` |
| `"mandalo a prod"` | `no_ejecutar`/`prohibido` | `no_ejecutar`/`prohibido` ✓ |
| `"entorno prod"` | `no_ejecutar`/`prohibido` | `no_ejecutar`/`prohibido` ✓ |

**Corrección aplicada:** Se eliminó `"prod"` de `_PALABRAS_PRODUCCION`. Se creó la tupla `_TOKENS_PRODUCCION = ("prod",)`. La regla de Prioridad 2 ahora combina frases exactas y tokens con límite.

---

### B-03 — Keyword `"action"`

**Problema:** `"action"` como substring podía generar falsos positivos conceptuales o por ruido.

**Corrección aplicada:** Se eliminó `"action"` como keyword standalone. Se reemplazó con frases específicas de GitHub Actions:
- `"github action"` (singular)
- `"action workflow"`
- `"actions workflow"`

`_PALABRAS_WORKFLOW` también se amplió con:
- `"github ci"`
- `"ci pipeline"`
- `"continuous integration"`
- `"integración continua"`

---

## 3. Problema detectado

Las keywords cortas (`"ci"`, `"prod"`, `"action"`) usaban detección por substring simple (`p in texto_lower`) sin verificar límites de palabra. En un sistema con texto en español, esto genera falsos positivos porque muchas palabras comunes contienen esas secuencias de letras en posición interna.

La severidad no era permisiva (ningún FP daba acceso indebido), pero sí producía rechazo incorrecto de instrucciones legítimas, lo que contradice el principio de que el Portero debe ser conservador pero no arbitrariamente restrictivo.

---

## 4. Corrección aplicada

### Helper `_es_token()`

Se añadió una función auxiliar pura (sin imports) que verifica si un token aparece como palabra completa:

```python
def _es_token(texto_lower, token):
    idx = texto_lower.find(token)
    while idx != -1:
        antes = idx == 0 or not texto_lower[idx - 1].isalpha()
        despues = (idx + len(token) == len(texto_lower) or
                   not texto_lower[idx + len(token)].isalpha())
        if antes and despues:
            return True
        idx = texto_lower.find(token, idx + 1)
    return False
```

**Propiedades:**
- Sin imports — usa solo `str.find()`, `str.isalpha()`, operadores básicos.
- Maneja Unicode correctamente — `"á"`, `"ó"`, `"é"` son `isalpha() = True` y actúan como límite interno.
- Maneja puntuación, números y espacios como límites de palabra.
- Funciona para inicio y fin de cadena.

### Cambios en constantes

| Constante | Antes | Después |
|---|---|---|
| `_PALABRAS_WORKFLOW` | `("workflow", "github actions", "ci", "action")` | 9 frases específicas, sin "ci" ni "action" standalone |
| `_TOKENS_WORKFLOW` | (no existía) | `("ci",)` |
| `_PALABRAS_PRODUCCION` | `("producción", "produccion", "prod", "deploy", "publicar")` | Sin "prod" |
| `_TOKENS_PRODUCCION` | (no existía) | `("prod",)` |

### Cambios en reglas

- Prioridad 2 (producción): `any(frases) or any(_es_token(...) for tokens)`
- Prioridad 7 (workflow): `any(frases) or any(_es_token(...) for tokens)`

---

## 5. Tests agregados o ajustados

### Tests nuevos (12 nuevos, total 98)

Clase `TestCerebroMockFalsoPositivos`:

| Test | Verifica |
|---|---|
| `test_microciclo_no_dispara_workflow` | `"el microciclo avanza"` → `reformular` |
| `test_accion_documental_no_dispara_workflow` | `"la acción documental está lista"` → `reformular` |
| `test_servicio_activo_no_dispara_workflow` | `"servicio activo"` → `reformular` |
| `test_producto_no_dispara_produccion` | `"revisá el producto"` → `reformular` |
| `test_producir_documentacion_no_dispara_produccion` | `"vamos a producir documentación"` → `reformular` |
| `test_reproducir_no_dispara_produccion` | `"reproducir el caso"` → `reformular` |
| `test_activar_ci_dispara_workflow` | `"activar CI"` → `pedir_autorizacion`/`alto` |
| `test_github_actions_dispara_workflow` | `"github actions"` → `pedir_autorizacion`/`alto` |
| `test_crear_workflow_dispara_workflow` | `"crear workflow"` → `pedir_autorizacion`/`alto` |
| `test_mandalo_a_prod_dispara_produccion` | `"mandalo a prod"` → `no_ejecutar`/`prohibido` |
| `test_deploy_a_produccion_dispara_produccion` | `"deploy a producción"` → `no_ejecutar`/`prohibido` |
| `test_entorno_prod_dispara_produccion` | `"entorno prod"` → `no_ejecutar`/`prohibido` |

### Tests originales conservados (86)

Los 86 tests de PUENTE-3B siguen pasando sin modificación.

---

## 6. Resultado de tests

```
python -m unittest discover -s tests

Ran 98 tests in 0.006s

OK
```

**98/98 tests pasan.** Sin errores. Sin warnings.

---

## 7. Qué NO se implementó

| Ítem | Estado |
|---|---|
| B-04: Regla para `estado suspendido` + continuidad | No implementado — deferred |
| B-05: Evaluación de `estado mergeado` + continuidad | No implementado — deferred |
| Corrección de `"action"` como falso positivo exacto en español | No aplica — se demostró que `"acción"` no contiene `"action"` como substring (ó ≠ o). El FP era B-01 (`"ci"`). Se eliminó `"action"` standalone por precaución y se reemplazó con frases específicas. |
| Uso de regex | NO — `_es_token()` usa solo stdlib básico sin imports |

---

## 8. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin imports nuevos | CONFIRMADO — `cerebro_mock.py` sigue sin ningún `import` |
| Función pura preservada | CONFIRMADO — `_es_token()` es pura, sin efectos secundarios |
| Sin API real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin dependencias externas | CONFIRMADO |
| Sin repos prohibidos | CONFIRMADO |
| Contrato de salida respetado | CONFIRMADO — 9 campos en todas las respuestas |
| Tests originales pasan | CONFIRMADO — 86/86 originales + 12 nuevos = 98/98 OK |

---

## 9. Próximo microciclo sugerido

**PUENTE-3D — Auditoría técnica de corrección de falsos positivos ci/prod/action**

Objetivo: revisar la implementación de PUENTE-3C-BACKLOG, validar que los falsos positivos fueron corregidos correctamente, confirmar que los disparadores reales siguen funcionando, y evaluar si quedan casos edge no cubiertos.

Alcance:
- Solo lectura.
- Sin modificaciones al código.
- Sin modificaciones a tests.
- Auditar `_es_token()` con casos edge adicionales.
- Auditar B-04 y B-05 del backlog restante.

Restricciones:
- Solo lectura.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.
- Sin secrets.
- Sin producción.

> No iniciar PUENTE-3D hasta que PUENTE-3C-BACKLOG esté cerrado con evidencia verificable (commit + push a main) y autorización explícita de Ariel.
