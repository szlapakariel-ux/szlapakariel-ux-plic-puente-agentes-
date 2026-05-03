# PUENTE-5D-BACKLOG — Corrección de falsos positivos B-06 en cliente Haiku fake/local

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-5D |
| Rama base | `main` |
| Commit base | `4888c4916bf72904cb862c6ddecde2d0211dc34b` (PUENTE-5B incluido) |
| Rama de trabajo | `fix/puente-5d-backlog-falsos-positivos-cliente-haiku-fake` |
| Estado de PUENTE-5B | Cerrado en main — cliente fake disponible |
| Tests al iniciar | 239/239 OK |

---

## 2. Backlog abordado

### B-06 — "tissue" dispara "issue"

**Problema:** La detección de `"issue"` en `_PALABRAS_MERGE` usaba `in` (substring), por lo que textos como `"no hay tissue aquí"` disparaban `pedir_autorizacion / alto` incorrectamente.

| Texto | Comportamiento anterior | Comportamiento correcto |
|---|---|---|
| `"no hay tissue aquí"` | `pedir_autorizacion / alto` | `reformular / medio` |
| `"comentar issue"` | `pedir_autorizacion / alto` | `pedir_autorizacion / alto` ✓ |
| `"cerrar issue #5"` | `pedir_autorizacion / alto` | `pedir_autorizacion / alto` ✓ |

---

### B-06 — "tokenización" dispara "token"

**Problema:** La detección de `"token"` usaba `in` (substring), por lo que textos como `"tokenización del texto"` o `"tokenizar"` disparaban `no_ejecutar / prohibido` incorrectamente.

| Texto | Comportamiento anterior | Comportamiento correcto |
|---|---|---|
| `"tokenización del texto"` | `no_ejecutar / prohibido` | `reformular / medio` |
| `"tokenizar texto"` | `no_ejecutar / prohibido` | `reformular / medio` |
| `"usar token"` | `no_ejecutar / prohibido` | `no_ejecutar / prohibido` ✓ |
| `"api token"` | `no_ejecutar / prohibido` | `no_ejecutar / prohibido` ✓ |

---

### B-06 — "continuamente" dispara "continua"

**Problema:** La detección de `"continua"` en `_PALABRAS_CONTINUIDAD` usaba `in` (substring), por lo que `"revisar continuamente"` disparaba `continuar_documental / bajo` incorrectamente.

| Texto | Comportamiento anterior | Comportamiento correcto |
|---|---|---|
| `"revisar continuamente"` | `continuar_documental / bajo` | `reformular / medio` |
| `"continua con el ciclo"` | `continuar_documental / bajo` | `continuar_documental / bajo` ✓ |
| `"continuá"` | `continuar_documental / bajo` | `continuar_documental / bajo` ✓ |

---

### B-06 — "secretaría" dispara "secret"

**Problema:** La detección de `"secret"` usaba `in` (substring), por lo que `"reunión de secretaría"` o `"secretario"` disparaban `no_ejecutar / prohibido` incorrectamente.

| Texto | Comportamiento anterior | Comportamiento correcto |
|---|---|---|
| `"reunión de secretaría"` | `no_ejecutar / prohibido` | `reformular / medio` |
| `"preguntá al secretario"` | `no_ejecutar / prohibido` | `reformular / medio` |
| `"secret"` | `no_ejecutar / prohibido` | `no_ejecutar / prohibido` ✓ |
| `"secrets del vault"` | `no_ejecutar / prohibido` | `no_ejecutar / prohibido` ✓ |

---

## 3. Problema detectado

Cuatro keywords de detección en `cliente_haiku_fake.py` usaban comparación por substring (`palabra in texto_lower`) sin verificar límites de palabra:

- `"issue"` en `_PALABRAS_MERGE`
- `"token"` en `_PROHIBIDAS_TOKEN` / lista anterior
- `"continua"` en `_PALABRAS_CONTINUIDAD`
- `"secret"` en lista de prohibidas

Esto provocaba falsos positivos conservadores: textos inocuos eran clasificados como peligrosos o como continuaciones, generando ruido en el sistema.

---

## 4. Corrección aplicada

### Helper `_es_token(texto, token)`

```python
def _es_token(texto, token):
    pos = texto.find(token)
    while pos != -1:
        antes = pos == 0 or not texto[pos - 1].isalpha()
        despues = pos + len(token) >= len(texto) or not texto[pos + len(token)].isalpha()
        if antes and despues:
            return True
        pos = texto.find(token, pos + 1)
    return False
```

Sin imports. Sin regex. Usa `str.find()` y `str.isalpha()` para verificar que el carácter inmediatamente anterior y posterior al token no sea alfabético — idéntico al patrón `_es_token()` de `cerebro_mock.py` y `mano_local_simulada.py`.

### Separación de listas de prohibidas

Las palabras prohibidas se dividieron en dos grupos:

| Grupo | Detección | Palabras |
|---|---|---|
| `_PROHIBIDAS_FRASE` | Substring exacto (`in`) | Frases que no tienen problema de substring: `"api real"`, `"api key"`, `".env"`, `"produccion"`, `"navegador"`, `"playwright"`, `"credencial"`, `"clave"`, `"contraseña"`, `"secreto"`, `"secrets"` |
| `_PROHIBIDAS_TOKEN` | Límite de palabra (`_es_token`) | Palabras cortas con riesgo de substring: `"secret"`, `"token"` |

### Separación de listas de merge

| Grupo | Detección | Palabras |
|---|---|---|
| `_MERGE_FRASE` | Substring exacto (`in`) | `"merge"`, `" pr "`, `"pull request"` |
| `_MERGE_TOKEN` | Límite de palabra (`_es_token`) | `"issue"` (para evitar "tissue") |

### Continuidad con `_es_token`

La detección de `_PALABRAS_CONTINUIDAD` se migró a `_es_token` para evitar `"continuamente"` → `"continua"`.

---

## 5. Tests agregados o ajustados

### Tests nuevos (23 nuevos, total 262)

Clase `TestClienteHaikuFakeB06FalsosPositivos`:

| Test | Verifica |
|---|---|
| `test_tissue_no_pide_autorizacion` | "tissue" no dispara pedir_autorizacion |
| `test_tissue_no_es_alto` | "tissue" no da riesgo alto |
| `test_issue_real_pide_autorizacion` | "comentar issue" → pedir_autorizacion / alto |
| `test_github_issue_pide_autorizacion` | "github issue" → pedir_autorizacion / alto |
| `test_issue_numero_pide_autorizacion` | "issue #5" → pedir_autorizacion / alto |
| `test_tokenizacion_no_bloquea` | "tokenización" → no bloquea |
| `test_tokenizar_no_bloquea` | "tokenizar texto" → no bloquea |
| `test_usar_token_bloquea` | "usar token" → no_ejecutar / prohibido |
| `test_api_token_bloquea` | "api token" → no_ejecutar / prohibido |
| `test_bearer_token_bloquea` | "bearer token" → no_ejecutar / prohibido |
| `test_token_solo_bloquea` | "token" solo → no_ejecutar / prohibido |
| `test_continuamente_no_continua_documental` | "continuamente" → no continuar_documental |
| `test_continua_real_continua_documental` | "continua con el ciclo" → continuar_documental / bajo |
| `test_continuar_real_continua_documental` | "continuar con el paso" → continuar_documental / bajo |
| `test_continua_solo_continua_documental` | "continuá" → continuar_documental |
| `test_secretaria_no_bloquea` | "secretaría" → no bloquea |
| `test_secretario_no_bloquea` | "secretario" → no bloquea |
| `test_secret_solo_bloquea` | "secret" solo → no_ejecutar / prohibido |
| `test_secrets_bloquea` | "secrets del vault" → no_ejecutar / prohibido |
| `test_credencial_bloquea` | "credencial" → no_ejecutar / prohibido |
| `test_clave_bloquea` | "clave" → no_ejecutar / prohibido |
| `test_segui_con_token_prohibido_gana` | "seguí y usar token" → prohibido gana |
| `test_continua_con_api_key_prohibido_gana` | "continuá y api key" → prohibido gana |

### Tests originales conservados (239)

Los 239 tests de PUENTE-5B y anteriores siguen pasando sin modificación.

---

## 6. Resultado de tests

```
python -m unittest discover -s tests

Ran 262 tests in 0.006s

OK
```

**262/262 tests pasan.** Sin errores. Sin warnings.

---

## 7. Qué NO se implementó

| Ítem | Estado |
|---|---|
| Conexión a API real | NO — prohibición absoluta |
| Claude Haiku real | NO — prohibición absoluta |
| Nuevas capacidades del cliente fake | NO — solo corrección de falsos positivos |
| Modificación de `cerebro_mock.py` | NO — no tocado |
| Modificación de `mano_local_simulada.py` | NO — no tocado |
| Nuevas acciones externas | NO — función pura |
| Workflows o CI | NO — prohibición absoluta |
| Dependencias instaladas | NO — cero dependencias |

---

## 8. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin imports nuevos | CONFIRMADO — `cliente_haiku_fake.py` sigue sin ningún `import` |
| Función pura preservada | CONFIRMADO — sin I/O, sin red, sin subprocess |
| `cerebro_mock.py` no modificado | CONFIRMADO |
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
| Contrato de salida 11 campos respetado | CONFIRMADO |
| Tests originales pasan | CONFIRMADO — 239/239 originales + 23 nuevos = 262/262 OK |

---

## 9. Próximo microciclo sugerido

**PUENTE-5E — Auditoría técnica de corrección B-06 en cliente Haiku fake/local**

Objetivo: revisar la corrección de falsos positivos B-06 en `cliente_haiku_fake.py`, validar que el helper `_es_token()` funciona correctamente para todos los casos reportados, confirmar que los disparadores reales siguen funcionando, y evaluar si quedan casos edge no cubiertos.

Alcance:
- Solo lectura.
- Sin modificaciones al código.
- Sin modificaciones a tests.
- Auditar el helper `_es_token()` con casos edge adicionales.
- Verificar que las 4 correcciones B-06 son completas.

Restricciones:
- Solo lectura.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.
- Sin secrets.
- Sin producción.

> No iniciar PUENTE-5E hasta que PUENTE-5D esté cerrado con evidencia verificable (commit + push) y autorización explícita de Ariel.
