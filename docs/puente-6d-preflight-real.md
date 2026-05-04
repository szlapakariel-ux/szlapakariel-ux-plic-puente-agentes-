# PUENTE-6D-PREFLIGHT-REAL — Preflight previo a primera llamada real

## 1. Nombre del documento

**PUENTE-6D-PREFLIGHT-REAL — Verificación operativa completa previa a PUENTE-6D real**

---

## 2. Objetivo

Consolidar en un único documento todas las condiciones mínimas que deben estar satisfechas antes de que Ariel autorice y ejecute PUENTE-6D real (primera llamada efectiva a la API de Anthropic con el modelo `claude-haiku-4-5-20251001`).

Este documento:
- No ejecuta ninguna llamada real.
- No habilita automáticamente ninguna llamada real.
- Sirve como referencia operativa para el momento en que Ariel decida iniciar PUENTE-6D real.

---

## 3. Alcance permitido

Este documento es documental y de solo lectura. Solo se permite:
- Leer documentación existente.
- Leer código en modo read-only.
- Ejecutar tests sin llamada real.
- Crear este documento como evidencia del preflight.

---

## 4. Prohibiciones absolutas

| Prohibición | Estado |
|---|---|
| Ejecutar llamada real | PROHIBIDO — absoluto |
| Usar API real de Anthropic | PROHIBIDO — absoluto |
| Usar SDK de Anthropic | PROHIBIDO — absoluto |
| Pedir, leer o imprimir API key | PROHIBIDO — absoluto |
| Crear o modificar `.env` | PROHIBIDO — absoluto |
| Tocar producción | PROHIBIDO — absoluto |
| Tocar workflows CI/CD | PROHIBIDO — absoluto |
| Usar navegador real | PROHIBIDO — absoluto |
| Usar Playwright | PROHIBIDO — absoluto |
| Tocar otros repos | PROHIBIDO — absoluto |
| Modificar código Python fuera del preflight | PROHIBIDO — absoluto |
| Modificar tests | PROHIBIDO — absoluto |

---

## 5. Estado del repo verificado para este preflight

| Campo | Valor |
|---|---|
| Commit base | `1c14157ea07699926dd66ec0751b3fd87ff16233` |
| Rama principal | `main` |
| PR cerrado | #26 — PUENTE-6D-MODELO-FIX — mergeado por squash |
| Modelo autorizado | `claude-haiku-4-5-20251001` |
| Tests | 416/416 OK |
| Working tree | Limpio |

---

## 6. Checklist de condiciones mínimas para autorizar PUENTE-6D real

### 6.1 Microciclos cerrados en main

| Condición | Estado requerido |
|---|---|
| PUENTE-6A cerrado en main (contrato prueba API real) | REQUERIDO |
| PUENTE-6B cerrado en main (cliente API real preparado) | REQUERIDO |
| B-07 cerrado en main (validación request_id) | REQUERIDO |
| PUENTE-6D-A cerrado en main (contrato operativo + checklist) | REQUERIDO |
| PUENTE-6D-B cerrado en main (gate de llamada real bloqueado) | REQUERIDO |
| PUENTE-6D-C cerrado en main (auditoría técnica del gate) | REQUERIDO |
| PUENTE-6D-MODELO-FIX cerrado en main (modelo actualizado) | REQUERIDO |

### 6.2 Tests

| Condición | Estado requerido |
|---|---|
| `python -m unittest discover -s tests` → todos los tests pasan | REQUERIDO — mínimo 416/416 |
| Sin tests nuevos fallando | REQUERIDO |

### 6.3 Autorización de Ariel

| Condición | Estado requerido |
|---|---|
| Ariel otorga autorización explícita en sesión activa | REQUERIDO |
| La autorización menciona "primera llamada real" y "PUENTE-6D real" | REQUERIDO |
| No se asume autorización implícita por ningún merge previo | REQUERIDO |
| No se asume autorización implícita por este preflight | REQUERIDO |

### 6.4 Modelo

| Condición | Valor requerido |
|---|---|
| Modelo autorizado | `claude-haiku-4-5-20251001` |
| Ningún otro modelo | PROHIBIDO |
| Modelo verificado en `_MODELO_AUTORIZADO` | REQUERIDO |
| Modelo verificado en `_MODELOS_PERMITIDOS` | REQUERIDO |

### 6.5 Prompt

| Condición | Valor requerido |
|---|---|
| Prompt exacto | `Respondé exactamente: PLIC_OK` |
| Sin variaciones ni adiciones | REQUERIDO |
| Sin datos sensibles en prompt | REQUERIDO |
| Prompt verificado visualmente por Ariel antes de llamada | REQUERIDO |

### 6.6 Parámetros de la llamada

| Parámetro | Valor requerido |
|---|---|
| `timeout` | `<= 10` segundos |
| `max_tokens` | `<= 50` tokens |
| `request_id` | String no vacío, único, sin datos sensibles |
| `retry` | `0` — sin reintentos automáticos |
| `batch` | No — llamada única |
| `streaming` | No |

### 6.7 API key

| Condición | Estado requerido |
|---|---|
| `ANTHROPIC_API_KEY` definida en entorno local de Ariel | REQUERIDO (solo en sesión de ejecución) |
| `ANTHROPIC_API_KEY` nunca en el repo | REQUERIDO — verificar con `git grep -r "sk-ant" .` → sin resultados |
| `ANTHROPIC_API_KEY` nunca en `.env` | REQUERIDO — no existe `.env` |
| Valor real de la key nunca impreso ni logueado | REQUERIDO |
| Header `Authorization` nunca impreso ni logueado | REQUERIDO |

### 6.8 Seguridad operativa

| Condición | Estado requerido |
|---|---|
| Sin producción | REQUERIDO |
| Sin CI/CD automático | REQUERIDO — no existe `.github/workflows/` |
| Sin navegador real | REQUERIDO |
| Sin Playwright | REQUERIDO |
| Sin otros repos | REQUERIDO |
| Fallback activo y verificado | REQUERIDO — `cliente_haiku_fake` disponible |
| Kill switch activo | REQUERIDO — Ctrl+C en cualquier momento |

---

## 7. Condiciones de corte durante PUENTE-6D real

Si cualquiera de estas condiciones se activa, la prueba debe cortarse inmediatamente:

| Condición | Acción |
|---|---|
| Falta `ANTHROPIC_API_KEY` en entorno | Cortar — activar fallback |
| Error 401 o 403 (autenticación) | Cortar — no reintentar |
| Error de modelo no disponible | Cortar — reportar a Ariel |
| Rate limit | Cortar — esperar mínimo 60s en ciclo futuro |
| Timeout > 10s | Cortar — activar fallback |
| Red no disponible | Cortar — activar fallback |
| Respuesta del modelo sugiere acción real | Cortar — `error_tipo: "corte"` — reportar a Ariel |
| Cualquier valor `sk-ant-*` aparece en output | Cortar — no loguear — reportar a Ariel |
| Se activa más de una llamada | Cortar — bloqueo absoluto |
| Prompt difiere de `"Respondé exactamente: PLIC_OK"` | Cortar — bloqueo absoluto |

---

## 8. Criterios de éxito de PUENTE-6D real

| Criterio | Descripción |
|---|---|
| `ok=True` | La llamada fue procesada sin error |
| `response_text` contiene `PLIC_OK` | La respuesta del modelo es la esperada |
| `llamada_real_ejecutada=True` | La llamada fue ejecutada (único caso donde se permite) |
| `fallback_usado=False` | No fue necesario activar fallback |
| `error_tipo=""` | Sin error en la llamada |
| Key no aparece en ningún log | Verificado después de la prueba |

---

## 9. Reporte mínimo requerido después de PUENTE-6D real

Al terminar PUENTE-6D real (con éxito o con corte), debe quedar registrado como mínimo:

| Campo | Descripción |
|---|---|
| Timestamp inicio y fin (UTC) | Obligatorio |
| `request_id` usado | Obligatorio |
| Modelo usado | `claude-haiku-4-5-20251001` |
| `ok=True` o `ok=False` | Obligatorio |
| `response_text` si es `PLIC_OK` | Solo si es inocuo — nunca si contiene secreto |
| `error_tipo` si hubo error | Obligatorio si `ok=False` |
| `fallback_usado` | Obligatorio |
| Confirmación de que key no aparece en logs | Obligatorio |

---

## 10. Criterios de bloqueo automático

Si cualquiera de estos ítems falla, la prueba queda bloqueada:

| Ítem | Bloquea si |
|---|---|
| Autorización explícita de Ariel | No está en sesión activa |
| Tests 416/416 OK | Algún test falla |
| Prompt exacto | Difiere de `"Respondé exactamente: PLIC_OK"` |
| `request_id` no vacío | Está vacío, ausente o no es string |
| `timeout <= 10` | Es mayor a 10 |
| `max_tokens <= 50` | Es mayor a 50 |
| Key no en repo | `git grep "sk-ant"` tiene resultados |
| No producción | Prueba en servidor remoto |
| No workflow | Push dispara CI automático |
| Fallback disponible | `cliente_haiku_fake` no responde |
| Modelo correcto | Difiere de `claude-haiku-4-5-20251001` |

---

## 11. Restricciones post-preflight

- Este documento **no habilita** PUENTE-6D real.
- PUENTE-6D real requiere instrucción explícita separada de Ariel.
- El merge de este documento hacia `main` **no autoriza** la primera llamada real.
- La primera llamada real es un microciclo independiente con su propia autorización.

---

## 12. Evidencia requerida antes de cualquier llamada real

Antes de ejecutar PUENTE-6D real, deben estar disponibles como evidencia verificable:

1. Commit de main con PUENTE-6D-MODELO-FIX mergeado (`1c14157` o posterior).
2. Output de `python -m unittest discover -s tests` → todos los tests OK.
3. Output de `git grep -r "sk-ant" .` → sin resultados.
4. Confirmación de que no existe `.env` en el repo.
5. Confirmación de que no existe `.github/workflows/` en el repo.
6. Autorización explícita de Ariel en sesión activa.
7. `request_id` generado (UUID local) registrado antes de la llamada.
8. Prompt verificado visualmente por Ariel: `"Respondé exactamente: PLIC_OK"`.
9. Modelo verificado en código: `claude-haiku-4-5-20251001`.
10. `ANTHROPIC_API_KEY` presente en entorno local de Ariel (sin imprimir ni loguear).
