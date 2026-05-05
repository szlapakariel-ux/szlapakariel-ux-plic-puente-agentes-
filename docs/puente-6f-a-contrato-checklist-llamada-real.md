# PUENTE-6F-A — Contrato/checklist previo a futura llamada real

## 1. Identificación

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6F-A |
| Fecha/hora (UTC) | 2026-05-05 |
| Repo | `szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-` |
| Rama | `docs/puente-6f-a-contrato-checklist-llamada-real` |
| Commit base (main) | `3ac37e855b3a36a2c47c3c4be2ab892b7607f506` |
| Autorización de Ariel | "Crear contrato/checklist documental para futura llamada real" |

---

## 2. Estado de base

| Elemento | Estado |
|---|---|
| main actual | `3ac37e855b3a36a2c47c3c4be2ab892b7607f506` |
| PUENTE-6D — primera llamada real exitosa | **CERRADO** en main |
| PUENTE-6E-A — contrato de integración mínima | **CERRADO** en main |
| PUENTE-6E-MAPA — mapa de fase | **CERRADO** en main |
| PUENTE-6E-B — cliente real mínimo | **CERRADO** en main (PR #34, commit `3196496`) |
| PUENTE-6E-C — cierre documental | **CERRADO** en main (PR #35, commit `3ac37e8`) |
| Cliente mínimo incorporado | `src/plic_puente_agentes/cliente_api_real_minimo.py` |
| Tests actuales | **507/507 OK** |
| Llamada real futura | **NO HABILITADA** — requiere microciclo propio y autorización explícita |

---

## 3. Objetivo de una futura llamada real

### Qué se buscaría validar

| Objetivo | Descripción |
|---|---|
| Que `cliente_api_real_minimo` ejecuta correctamente una llamada real | Verificar que la ruta de código en `_ejecutar_http` funciona con la API de Anthropic en el entorno actual |
| Que el modelo `claude-haiku-4-5-20251001` sigue disponible para la cuenta | Confirmar disponibilidad desde el entorno de ejecución autorizado |
| Que la respuesta llega correctamente y se parsea | Verificar extracción de `content[].text` en condición real |
| Que el payload construido por `cliente_api_real_minimo` es válido | Confirmar que `temperature: 0.0`, `max_tokens`, modelo y mensaje son aceptados |
| Que `llamada_real_ejecutada: True` y `cantidad_llamadas: 1` en resultado real | Verificar invariantes en condición real |

### Qué NO se buscaría validar

| Elemento | Motivo |
|---|---|
| Capacidad de respuesta creativa del modelo | Fuera de alcance — solo verificación estructural |
| Integración con otras partes del sistema | Fuera de alcance — cliente aislado |
| Rendimiento o latencia | Fuera de alcance en este microciclo |
| Múltiples modelos simultáneos | Prohibido por contrato PUENTE-6E-A |
| Streaming | Prohibido por contrato PUENTE-6E-A |
| Memoria o contexto persistente | Prohibido por contrato PUENTE-6E-A |

### Por qué no debe mezclarse con producción

- El entorno de producción no está definido ni autorizado.
- Una llamada real en producción podría generar costos no controlados.
- Los logs de producción podrían capturar datos sensibles si no están correctamente sanitizados.
- El protocolo exige aislamiento: una llamada real es un evento de microciclo, no una operación rutinaria.

---

## 4. Condiciones previas obligatorias

Todas las siguientes condiciones deben estar cumplidas **antes** de autorizar cualquier llamada real. Ninguna es opcional.

| Condición | Obligatoriedad |
|---|---|
| Autorización explícita de Ariel para el microciclo de llamada real | **BLOQUEANTE** — sin esto no se avanza |
| Este contrato/checklist (PUENTE-6F-A) mergeado en main | **BLOQUEANTE** |
| Auditoría de PUENTE-6F-A aprobada | **BLOQUEANTE** |
| Red definida — se recomienda red celular (hotspot móvil) para aislar proxy corporativo | Obligatorio — lección de PUENTE-6D |
| Modelo definido — `claude-haiku-4-5-20251001` único autorizado | Obligatorio — por contrato PUENTE-6E-A sección 6 |
| Payload definido explícitamente en el microciclo de ejecución | Obligatorio |
| Presupuesto de tokens declarado antes de la llamada | Obligatorio — por contrato PUENTE-6E-A sección 11 |
| Límite de una llamada máxima en el microciclo | Obligatorio — por contrato PUENTE-6E-A sección 9 |
| Evidencia esperada definida antes de ejecutar | Obligatorio |
| Rollback documental definido si la llamada falla | Obligatorio |
| `ANTHROPIC_API_KEY` disponible en entorno local seguro (no en repo, no en chat) | Obligatorio — por contrato PUENTE-6E-A sección 7 |
| Tests 507/507 verdes en el commit base | Obligatorio |
| Prohibición de producción activa | Siempre vigente |

---

## 5. Checklist técnico previo

Verificar cada ítem antes de ejecutar la llamada. Registrar el resultado en el documento de evidencia del microciclo de ejecución.

| Ítem | Verificación requerida |
|---|---|
| Rama limpia | `git status` → `nothing to commit, working tree clean` |
| main actualizado | `git pull origin main` — sin divergencias |
| Tests verdes | `python -m unittest discover -s tests` → `507/507 OK` o superior |
| `cliente_api_real_minimo` bloqueado por defecto | Confirmar que sin `permitir_llamada_real=True` la función devuelve `llamada_real_no_autorizada` |
| Llamada aislada de otros módulos | Ningún otro módulo llama a la función durante el microciclo |
| Sin workflows activos | No hay trigger de CI/CD que pueda ejecutar la llamada automáticamente |
| Sin producción involucrada | El entorno de ejecución es local o remoto aislado — no productivo |
| Sin logs sensibles | Confirmar que ningún logger captura `ANTHROPIC_API_KEY` ni headers de request |

---

## 6. Checklist de secrets

| Regla | Verificación |
|---|---|
| No guardar secret en repo | `git grep -r "sk-ant"` → sin resultados |
| No imprimir secret en terminal ni en salida de función | Revisar que `_salida()` no incluye la key |
| No documentar valor de secret en ningún archivo | Ningún `.md`, `.txt` ni log contiene el valor |
| No crear `.env` | Confirmar que `.env` no existe y no se creará |
| Usar variable disponible solo en entorno local seguro | `export ANTHROPIC_API_KEY=...` en terminal local — sin pegar en chat |
| Confirmar presencia sin mostrar valor | `bool(os.environ.get("ANTHROPIC_API_KEY"))` → `True` (verificación booleana únicamente) |
| Key va solo al header `x-api-key` | Confirmado por diseño de `_ejecutar_http` — no aparece en payload ni en salida |

---

## 7. Checklist de ejecución

| Regla | Valor / Verificación |
|---|---|
| Máximo 1 request real en el microciclo | Contar `cantidad_llamadas` en el resultado — debe ser `1` |
| Payload mínimo | `{"model": "claude-haiku-4-5-20251001", "max_tokens": ≤50, "temperature": 0.0, "messages": [...]}` |
| Timeout definido | `timeout ≤ 10` segundos |
| Captura sanitizada de status HTTP | Registrar `status_code` — esperado `200` |
| Captura sanitizada de respuesta | Registrar `respuesta_texto` — sin datos sensibles |
| No repetir automáticamente | Si falla → frenar, documentar, no reintentar en el mismo microciclo |
| No retry automático | Prohibido por contrato PUENTE-6E-A sección 9 |
| Captura sanitizada de body de error (si falla) | `body_error_sanitizado` — máx 1000 chars, sin patrones de credencial |

---

## 8. Checklist de evidencia

El documento de evidencia del microciclo de llamada real debe contener todos los siguientes campos:

| Campo | Descripción |
|---|---|
| Fecha/hora (UTC) | Timestamp del momento de ejecución |
| Entorno usado | Local PowerShell / Claude Code remoto / otro — especificar |
| Red usada | Celular / corporativa / otra — especificar |
| Modelo | `claude-haiku-4-5-20251001` |
| Cantidad de requests realizados | Debe ser `1` |
| `status_code` obtenido | Valor numérico HTTP |
| `respuesta_texto` resumida | Solo si no es sensible — sanitizada |
| `usage.input_tokens` | Entero |
| `usage.output_tokens` | Entero |
| `llamada_real_ejecutada` | Debe ser `True` |
| `secret_expuesto` | Debe ser `False` |
| Secrets expuestos | `0` — verificación explícita |
| Archivos modificados en el microciclo | Solo documentales |
| Tests post-llamada | `507/507 OK` o superior |

---

## 9. Criterios de éxito

| Criterio | Valor esperado |
|---|---|
| `status_code` | `200` |
| `ok` | `True` |
| `respuesta_texto` | No vacío y no `None` |
| `llamada_real_ejecutada` | `True` |
| `cantidad_llamadas` | `1` |
| `secret_expuesto` | `False` |
| Producción tocada | `0` — ningún sistema productivo involucrado |
| Evidencia documentada | Sí — en documento propio del microciclo de ejecución |
| Tests post-llamada | `507/507 OK` o superior |

---

## 10. Criterios de bloqueo

Si cualquiera de los siguientes criterios se cumple, la llamada real **no debe ejecutarse** y el microciclo debe frenarse inmediatamente:

| Criterio de bloqueo | Acción |
|---|---|
| Falta autorización explícita de Ariel | **FRENAR** — no ejecutar |
| `ANTHROPIC_API_KEY` no disponible en entorno de ejecución | **FRENAR** — reportar `anthropic_api_key_ausente` |
| Riesgo de que el valor de la key aparezca en logs, output o chat | **FRENAR** — revisar antes de continuar |
| Tests rotos (`< 507/507`) | **FRENAR** — corregir antes de cualquier llamada |
| Cambios no documentales sin auditar en el diff | **FRENAR** — auditar antes de continuar |
| Intento de ejecutar en producción o afectar sistema productivo | **FRENAR PERMANENTEMENTE** — prohibido sin excepción |
| Más de una llamada planificada en el microciclo | **FRENAR** — reducir a exactamente 1 |
| Red corporativa sin aislar (si hay proxy activo) | **ADVERTENCIA** — preferir red celular (lección de PUENTE-6D) |
| `cliente_api_real_minimo` no importable o con error | **FRENAR** — corregir antes de continuar |

---

## 11. Qué NO queda autorizado por este contrato

Este documento define el contrato. No ejecuta nada. No autoriza nada todavía.

| Acción | Estado |
|---|---|
| Ejecutar llamada real a Anthropic | **NO AUTORIZADO** |
| Hacer request HTTP a cualquier endpoint | **NO AUTORIZADO** |
| Usar la API de Anthropic de forma efectiva | **NO AUTORIZADO** |
| Usar el SDK de Anthropic | **NO AUTORIZADO** |
| Modificar código fuente | **NO AUTORIZADO** |
| Modificar tests | **NO AUTORIZADO** |
| Leer, imprimir o exponer secrets | **NO AUTORIZADO** |
| Crear o modificar `.env` | **NO AUTORIZADO** |
| Tocar producción | **NO AUTORIZADO** |
| Crear workflows | **NO AUTORIZADO** |
| Usar navegador o Playwright | **NO AUTORIZADO** |
| Avanzar a ejecución real sin instrucción separada de Ariel | **NO AUTORIZADO** |

---

## 12. Confirmaciones de seguridad de este microciclo

| Verificación | Estado |
|---|---|
| Llamada real ejecutada | NO |
| Request HTTP ejecutado | NO |
| Secret expuesto | NO |
| `ANTHROPIC_API_KEY` leída o impresa | NO |
| `.env` creado o modificado | NO |
| Código fuente modificado | NO |
| Tests modificados | NO |
| Workflows tocados | NO |
| Producción tocada | NO |
| Navegador usado | NO |
| Playwright usado | NO |
| Otros repos tocados | NO |
| PR abierto | NO |
| Merge ejecutado | NO |

---

## 13. Dictamen final

### **PUENTE-6F-A — CONTRATO/CHECKLIST PREPARADO**

Este documento define el contrato completo y el checklist obligatorio para una futura llamada real usando `cliente_api_real_minimo`. **No ejecuta ninguna llamada. No autoriza ninguna acción. No habilita producción.**

**La llamada real futura sigue NO habilitada.**

Para habilitarla se requieren: este contrato mergeado en main, auditoría aprobada, y autorización explícita y separada de Ariel en un microciclo propio con nombre y alcance definidos.

> El próximo paso requiere instrucción explícita y separada de Ariel.
