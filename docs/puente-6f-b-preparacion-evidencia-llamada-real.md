# PUENTE-6F-B — Preparación de evidencia para futura llamada real

## 1. Identificación

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6F-B |
| Fecha/hora (UTC) | 2026-05-05 |
| Repo | `szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-` |
| Rama | `docs/puente-6f-b-preparacion-evidencia-llamada-real` |
| Commit base (main) | `e78cf936c0850e54b036f9f1b506258c35a1c72c` |
| Autorización de Ariel | "Crear preparación de evidencia para futura llamada real" |

---

## 2. Estado de base

| Elemento | Estado |
|---|---|
| main actual | `e78cf936c0850e54b036f9f1b506258c35a1c72c` |
| PUENTE-6F-A — contrato/checklist llamada real | **CERRADO** en main (PR #36, commit `e78cf93`) |
| Checklist disponible | `docs/puente-6f-a-contrato-checklist-llamada-real.md` |
| Cliente mínimo incorporado | `src/plic_puente_agentes/cliente_api_real_minimo.py` (PUENTE-6E-B, PR #34) |
| Tests actuales | **507/507 OK** |
| Llamada real | **NO HABILITADA** — requiere microciclo propio y autorización explícita de Ariel |

---

## 3. Objetivo del documento

Este documento no ejecuta ninguna llamada real. Su propósito es:

1. **Preparar el formato de evidencia** que deberá completarse en el microciclo de ejecución real, para que ese microciclo no deba improvisar ni olvidar campos obligatorios.
2. **Evitar improvisación** en el momento de la ejecución — tener el template listo reduce el riesgo de omitir datos auditables.
3. **Separar preparación documental de ejecución real** — este microciclo es solo documental; la ejecución real es un evento separado con su propia autorización.

---

## 4. Plantilla de evidencia futura

El microciclo de llamada real debe completar **todos** los campos de esta plantilla en su documento de resultado. Los campos con `___` deben ser llenados con datos reales en el momento de la ejecución.

```
# [NOMBRE-MICROCICLO] — Evidencia de llamada real

## Identificación

| Campo              | Valor |
|--------------------|-------|
| Microciclo         | ___ |
| Fecha/hora (UTC)   | ___ |
| Operador           | ___ (Ariel / Claude Code / otro — especificar) |
| Repo               | szlapakariel-ux/szlapakariel-ux-plic-puente-agentes- |
| Commit base (main) | ___ |

## Entorno de ejecución

| Campo              | Valor |
|--------------------|-------|
| Entorno usado      | ___ (PowerShell local / Claude Code remoto / otro) |
| Red usada          | ___ (celular / corporativa / otra — especificar) |
| Sistema operativo  | ___ |
| Método de ejecución | ___ (cliente_api_real_minimo / script directo / otro) |

## Parámetros de la llamada

| Campo                      | Valor |
|----------------------------|-------|
| Modelo                     | claude-haiku-4-5-20251001 |
| Payload resumido           | ___ (sin secrets — solo campos públicos) |
| max_tokens                 | ___ (≤ 50) |
| temperature                | 0.0 |
| timeout                    | ___ (≤ 10 segundos) |
| Cantidad máxima autorizada | 1 |

## Resultado de la ejecución

| Campo                        | Valor |
|------------------------------|-------|
| Cantidad real de requests    | ___ |
| status_code                  | ___ |
| ok                           | ___ |
| respuesta_texto (sanitizada) | ___ |
| llamada_real_ejecutada       | ___ |
| cantidad_llamadas            | ___ |
| secret_expuesto              | False |

## Usage

| Campo                        | Valor |
|------------------------------|-------|
| input_tokens                 | ___ |
| output_tokens                | ___ |
| cache_creation_input_tokens  | ___ |
| cache_read_input_tokens      | ___ |

## Errores (si aplica)

| Campo                  | Valor |
|------------------------|-------|
| error_tipo             | ___ (o N/A si no hubo error) |
| body_error_sanitizado  | ___ (máx 1000 chars, sin credenciales — o N/A) |

## Seguridad

| Verificación              | Estado |
|---------------------------|--------|
| Secrets expuestos         | 0 |
| ANTHROPIC_API_KEY impresa | NO |
| .env creado/modificado    | NO |
| Producción tocada         | NO |
| Archivos modificados      | Solo documentales |

## Tests

| Momento        | Resultado |
|----------------|-----------|
| Pre-llamada    | ___ /507 OK |
| Post-llamada   | ___ /507 OK |

## Dictamen final del microciclo

___
```

---

## 5. Reglas de sanitización

Al completar la plantilla en el microciclo de ejecución real, aplicar estrictamente:

| Regla | Detalle |
|---|---|
| No pegar API key | El valor de `ANTHROPIC_API_KEY` nunca debe aparecer en ningún campo |
| No pegar headers completos | El header `x-api-key` contiene la key — no documentar su valor |
| No pegar payload con secrets | El payload de `cliente_api_real_minimo` no contiene secrets, pero verificar antes de copiar |
| No pegar stack traces con datos sensibles | Si hay traceback, revisar que no incluya valores de variables con la key |
| No documentar variables de entorno completas | Solo registrar presencia booleana: `ANTHROPIC_API_KEY presente: True/False` |
| No pegar respuesta si contiene datos sensibles | Revisar `respuesta_texto` antes de copiar — truncar o resumir si es necesario |
| Limitar body de error a 1000 chars | Por diseño de `_sanitizar_body_error` — respetar ese límite en la documentación también |

---

## 6. Evidencia mínima obligatoria

Para que la evidencia sea aceptable como cierre del microciclo de ejecución real, debe incluir **todos** los siguientes elementos:

| Elemento | Requisito |
|---|---|
| Cantidad de requests | Exactamente 1 — no más |
| Timeout usado | Definido explícitamente (≤ 10 segundos) |
| Sin retry automático | Confirmado — ningún mecanismo de reintento activo |
| `status_code` | Registrado — valor numérico HTTP |
| Respuesta resumida | `respuesta_texto` o equivalente — sanitizada |
| `usage` si existe | `input_tokens` y `output_tokens` al menos |
| `secrets_expuestos` | `0` — verificación explícita |
| Producción tocada | `NO` — verificación explícita |
| Tests post-llamada | ≥ 507/507 OK |

---

## 7. Criterios para aceptar la evidencia

La evidencia del microciclo de ejecución real se acepta si:

| Criterio | Condición |
|---|---|
| Coincide con checklist PUENTE-6F-A | Todos los ítems del checklist fueron verificados y registrados |
| Sin secrets en el documento | Ningún campo contiene valores de API key, headers de auth, ni credenciales |
| Sin producción | Ningún sistema productivo fue afectado |
| Una sola llamada | `cantidad_llamadas = 1` confirmado |
| Evidencia suficiente para auditar | Un auditor puede verificar el resultado sin información adicional |
| Tests post-llamada verdes | ≥ 507/507 OK registrado |
| Operador identificado | Campo `Operador` completado con identidad real |
| Fecha/hora registrada | Campo `Fecha/hora (UTC)` completado |

---

## 8. Criterios para rechazar la evidencia

La evidencia del microciclo de ejecución real se rechaza si cualquiera de los siguientes criterios se cumple:

| Criterio de rechazo | Consecuencia |
|---|---|
| Falta autorización explícita de Ariel para el microciclo | **RECHAZO** — el microciclo no estaba autorizado |
| Falta `fecha/hora` | **RECHAZO** — no es auditable sin timestamp |
| No se puede confirmar cantidad de requests | **RECHAZO** — invariante central del protocolo |
| Aparece un valor de secret en el documento | **RECHAZO PERMANENTE** — violación de política de secrets |
| Se tocó producción | **RECHAZO PERMANENTE** — prohibido sin excepción |
| Hubo más de una llamada en el microciclo | **RECHAZO** — viola límite de PUENTE-6E-A sección 9 |
| Hubo retry automático | **RECHAZO** — prohibido por contrato PUENTE-6E-A sección 9 |
| Se modificó código sin autorización | **RECHAZO** — fuera del alcance del microciclo de llamada |
| Tests rotos post-llamada | **RECHAZO** — suite debe quedar en ≥ 507/507 OK |
| Falta `usage` cuando estuvo disponible | **RECHAZO** — obligatorio por PUENTE-6E-A sección 11 |

---

## 9. Qué NO queda autorizado por este documento

Este documento define la preparación. No ejecuta nada. No autoriza nada todavía.

| Acción | Estado |
|---|---|
| Ejecutar llamada real a Anthropic | **NO AUTORIZADO** |
| Hacer request HTTP a cualquier endpoint | **NO AUTORIZADO** |
| Usar la API de Anthropic de forma efectiva | **NO AUTORIZADO** |
| Usar el SDK de Anthropic | **NO AUTORIZADO** |
| Leer, imprimir o exponer secrets | **NO AUTORIZADO** |
| Crear o modificar `.env` | **NO AUTORIZADO** |
| Modificar código fuente | **NO AUTORIZADO** |
| Modificar tests | **NO AUTORIZADO** |
| Tocar producción | **NO AUTORIZADO** |
| Crear workflows | **NO AUTORIZADO** |
| Usar navegador o Playwright | **NO AUTORIZADO** |
| Avanzar a ejecución real sin instrucción separada de Ariel | **NO AUTORIZADO** |

---

## 10. Confirmaciones de seguridad de este microciclo

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

## 11. Dictamen final

### **PUENTE-6F-B — PREPARACIÓN DE EVIDENCIA LISTA**

Este documento prepara el formato y criterios de evidencia para una futura llamada real. **No ejecuta ninguna llamada. No autoriza ninguna acción. No habilita producción.**

**La llamada real futura sigue NO habilitada.**

Para habilitarla se requieren: este documento mergeado en main, auditoría aprobada, y autorización explícita y separada de Ariel en un microciclo propio con nombre, alcance y presupuesto definidos.

> El próximo paso requiere instrucción explícita y separada de Ariel.
