# PUENTE-4C-BACKLOG — Corrección de falsos positivos en mano_local_simulada

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-4C-BACKLOG |
| Rama base | `main` |
| Commit base | `47a405ec2e46d37c80cb4e74868610494c319e24` |
| Rama de trabajo | `fix/puente-4c-backlog-falsos-positivos-mano-local` |
| Estado de PUENTE-4B | Cerrado en main — 135 tests OK |
| Tests al iniciar | 135/135 OK |

---

## 2. Backlog abordado

### B-ML-01 — Keyword `"prod"`

**Problema detectado:** `"prod"` como substring dentro de `_PALABRAS_PELIGROSAS` bloqueaba instrucciones legítimas que contenían "prod" en posición interna.

| Texto | Comportamiento anterior | Comportamiento correcto |
|---|---|---|
| `"producir documentacion"` | `bloqueo: True` | `bloqueo: False` |
| `"reproducir el caso"` | `bloqueo: True` | `bloqueo: False` |
| `"revisar producto"` | `bloqueo: True` | `bloqueo: False` |
| `"mandalo a prod"` | `bloqueo: True` | `bloqueo: True` ✓ |
| `"entorno prod"` | `bloqueo: True` | `bloqueo: True` ✓ |
| `"deploy a prod"` | `bloqueo: True` | `bloqueo: True` ✓ |

**Corrección aplicada:** Se eliminó `"prod"` de `_PALABRAS_PELIGROSAS`. Se creó `_TOKENS_PELIGROSOS = ("prod",)` y el helper `_es_token()` que verifica límite de palabra. La Regla 9 ahora combina frases exactas y tokens con límite.

---

### B-ML-02 — Keyword `"pr"`

**Problema detectado:** `"pr"` como clave corta en `_MAPA_ACCION_SUGERIDA` mapeaba incorrectamente a `preparar_comentario_pr` cualquier palabra que contuviera "pr" como substring.

| Texto | Comportamiento anterior | Comportamiento correcto |
|---|---|---|
| `"preparar el documento"` | `accion: preparar_comentario_pr` | `accion: preparar_orden_documental` |
| `"comprimir archivos"` | `accion: preparar_comentario_pr` | `accion: preparar_orden_documental` |
| `"propuesta documental"` | `accion: preparar_comentario_pr` | `accion: preparar_orden_documental` |
| `"abrir pr de revision"` | `accion: preparar_comentario_pr` | `accion: preparar_comentario_pr` ✓ |
| `"comentar pr"` | `accion: preparar_comentario_pr` | `accion: preparar_comentario_pr` ✓ |
| `"pull request"` | `accion: preparar_comentario_pr` | `accion: preparar_comentario_pr` ✓ |

**Corrección aplicada:** Se eliminó `"pr"` del `_MAPA_ACCION_SUGERIDA`. Se creó `_FRASES_PR` con frases específicas y se agrega detección de `"pr"` como token aislado con `_es_token()`.

---

### B-ML-03 — Keyword `"issue"`

**Problema:** `"issue"` como clave de substring podía generar falsos positivos conceptuales para palabras que lo contengan internamente (ej: `"tissue"` en inglés).

**Corrección aplicada:** Se eliminó `"issue"` del `_MAPA_ACCION_SUGERIDA`. Se reemplazó con `_es_token(accion_lower, "issue")` para verificar límite de palabra. Los disparadores reales siguen funcionando: `"comentar issue"`, `"github issue"`, `"issue #5"`.

---

## 3. Problema detectado

Las tres keywords problemáticas usaban detección por substring simple sin verificar límites de palabra:

- `"prod"` en `_PALABRAS_PELIGROSAS` → bloqueaba palabras españolas con "prod" interno
- `"pr"` en `_MAPA_ACCION_SUGERIDA` → mapeaba incorrectamente verbos comunes ("preparar", "comprimir")
- `"issue"` en `_MAPA_ACCION_SUGERIDA` → potencial falso positivo por substring accidental

---

## 4. Corrección aplicada

### Helper `_es_token()`

Se añadió la misma función auxiliar pura que en `cerebro_mock.py` (B-02), sin imports:

```python
def _es_token(texto_lower, token):
    """Verifica si token aparece como palabra completa en texto_lower."""
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

### Cambios en constantes

| Constante | Antes | Después |
|---|---|---|
| `_PALABRAS_PELIGROSAS` | Incluía `"prod"` | Sin `"prod"` |
| `_TOKENS_PELIGROSOS` | (no existía) | `("prod",)` |
| `_MAPA_ACCION_SUGERIDA` | Incluía `"issue"` y `"pr"` | Solo `"claude"` y `"codex"` |
| `_FRASES_PR` | (no existía) | Tupla con 5 frases específicas de PR |

### Cambios en reglas

- Regla 9 (peligrosas): `any(frases) or any(_es_token(...) for tokens)`
- Regla 8 (acciones): separada en mapeo de frases (claude/codex), luego frases de PR o token "pr", luego token "issue"

---

## 5. Tests agregados o ajustados

### Tests nuevos (15 nuevos, total 150)

Clase `TestManoLocalFalsoPositivos`:

| Test | Verifica |
|---|---|
| `test_producir_documentacion_no_bloquea` | `"producir documentacion"` → `bloqueo: False` |
| `test_reproducir_el_caso_no_bloquea` | `"reproducir el caso"` → `bloqueo: False` |
| `test_revisar_producto_no_bloquea` | `"revisar producto"` → `bloqueo: False` |
| `test_mandalo_a_prod_bloquea` | `"mandalo a prod"` → `bloqueo: True` |
| `test_entorno_prod_bloquea` | `"entorno prod"` → `bloqueo: True` |
| `test_deploy_a_prod_bloquea` | `"deploy a prod"` → `bloqueo: True` |
| `test_preparar_documento_no_mapea_pr` | `"preparar el documento"` → `preparar_orden_documental` |
| `test_comprimir_archivos_no_mapea_pr` | `"comprimir archivos"` → no PR |
| `test_propuesta_documental_no_mapea_pr` | `"propuesta documental"` → no PR |
| `test_abrir_pr_mapea_pr` | `"abrir pr de revision"` → `preparar_comentario_pr` |
| `test_comentar_pr_mapea_pr` | `"comentar pr"` → `preparar_comentario_pr` |
| `test_pull_request_mapea_pr` | `"pull request"` → `preparar_comentario_pr` |
| `test_pr_aislado_mapea_pr` | `"revisá el pr"` → `preparar_comentario_pr` |
| `test_comentar_issue_mapea_issue` | `"comentar issue"` → `preparar_comentario_issue` |
| `test_github_issue_mapea_issue` | `"github issue #5"` → `preparar_comentario_issue` |

### Tests originales conservados (135)

Los 135 tests de PUENTE-4B siguen pasando sin modificación.

---

## 6. Resultado de tests

```
python -m unittest discover -s tests

Ran 150 tests in 0.004s

OK
```

**150/150 tests pasan.** Sin errores. Sin warnings.

---

## 7. Qué NO se implementó

| Ítem | Estado |
|---|---|
| B-04: `estado suspendido` + continuidad en cerebro_mock | No implementado — deferred |
| B-05: `estado mergeado` + continuidad en cerebro_mock | No implementado — deferred |
| Conexión a API real | NO — prohibición absoluta |
| Navegador real / Playwright | NO — prohibición absoluta |
| Nuevas capacidades de mano local | NO — solo corrección de falsos positivos |

---

## 8. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin imports nuevos | CONFIRMADO — `mano_local_simulada.py` sigue sin ningún `import` |
| `_es_token()` es función pura | CONFIRMADO — sin efectos secundarios |
| `cerebro_mock.py` no modificado | CONFIRMADO |
| Sin API real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin dependencias instaladas | CONFIRMADO |
| Sin repos prohibidos | CONFIRMADO |
| Contrato de salida respetado (8 campos) | CONFIRMADO |
| Tests originales pasan | CONFIRMADO — 135/135 originales + 15 nuevos = 150/150 OK |

---

## 9. Próximo microciclo sugerido

**PUENTE-4D — Auditoría técnica de corrección de falsos positivos en mano local simulada**

Objetivo: revisar la implementación de PUENTE-4C-BACKLOG, validar que los falsos positivos fueron corregidos correctamente, confirmar que los disparadores reales siguen funcionando, y evaluar si quedan casos edge no cubiertos.

Alcance:
- Solo lectura.
- Sin modificaciones al código.
- Sin modificaciones a tests.
- Auditar `_es_token()` con casos edge adicionales.
- Auditar `_FRASES_PR` y `_TOKENS_PELIGROSOS`.

Restricciones:
- Solo lectura.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.
- Sin secrets.
- Sin producción.

> No iniciar PUENTE-4D hasta que PUENTE-4C-BACKLOG esté cerrado con evidencia verificable (commit + push a main) y autorización explícita de Ariel.
