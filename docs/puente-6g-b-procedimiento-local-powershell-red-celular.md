# PUENTE-6G-B — Procedimiento local seguro PowerShell + red celular

## 1. Identificación

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6G-B |
| Fecha/hora (UTC) | 2026-05-05 |
| Repo | `szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-` |
| Rama | `docs/puente-6g-b-procedimiento-local-powershell-red-celular` |
| Commit base (main) | `a5b933097cf9ad8271ad5c752fde035c7db8abee` |
| Autorización de Ariel | "Crear procedimiento documental para futura llamada real desde entorno local seguro" |

---

## 2. Estado de base

| Elemento | Estado |
|---|---|
| main actual | `a5b933097cf9ad8271ad5c752fde035c7db8abee` |
| PUENTE-6G-A — diagnóstico entorno local | **CERRADO** en main (PR #38, commit `a5b9330`) |
| Diagnóstico de entorno | **APTO CON OBSERVACIONES** |
| Observación bloqueante documentada | `ANTHROPIC_API_KEY` ausente en Claude Code remoto |
| Conclusión operativa | Futura llamada real solo evaluable desde entorno local de Ariel |
| `docs/puente-6f-a-contrato-checklist-llamada-real.md` | Presente en main |
| `docs/puente-6f-b-preparacion-evidencia-llamada-real.md` | Presente en main |
| `docs/puente-6g-a-diagnostico-entorno-local-seguro.md` | Presente en main |
| `src/plic_puente_agentes/cliente_api_real_minimo.py` | Presente en main |
| Tests actuales | **507/507 OK** |
| Llamada real | **NO HABILITADA** — requiere microciclo propio y autorización explícita de Ariel |

---

## 3. Objetivo del procedimiento

Este documento no ejecuta ninguna llamada real. Su propósito es:

1. **Preparar el paso operativo local** que Ariel deberá seguir en el microciclo de ejecución real, para que ese microciclo no deba improvisar ni omitir pasos de seguridad.
2. **Evitar improvisación** en el momento de la ejecución — tener el procedimiento escrito reduce el riesgo de errores operativos, exposición accidental de secrets y llamadas no autorizadas.
3. **Separar preparación documental de ejecución real** — este microciclo es solo documental; la ejecución real es un evento separado con su propia autorización.

---

## 4. Entorno permitido para futura ejecución

La futura llamada real **solo puede ejecutarse** desde el siguiente entorno:

| Elemento | Valor requerido |
|---|---|
| Máquina | Local de Ariel — no remota, no compartida |
| Shell | PowerShell (Windows) |
| Red | Red celular / hotspot móvil — lección de PUENTE-6D |
| API key | Variable de entorno temporal en la sesión de PowerShell — nunca en archivo |
| Repo | Clonado localmente en la máquina de Ariel |
| Rama de ejecución | `main` actualizado — sin ramas de feature activas durante la llamada |
| Python | Disponible localmente — versión que corre los 507 tests |

### Forma correcta de setear la key en PowerShell (solo en terminal, sin pegar en chat)

```powershell
$env:ANTHROPIC_API_KEY = "..."   # completar en terminal local — nunca en chat ni en archivo
```

La variable existe solo en la sesión activa de PowerShell. No se guarda en archivo. No aparece en el repo. No se muestra en ningún log del repo.

---

## 5. Entornos NO permitidos

| Entorno | Motivo |
|---|---|
| Claude Code remoto | `ANTHROPIC_API_KEY` no disponible — bloqueante detectado en PUENTE-6G-A |
| GitHub Actions / CI/CD | Prohibido — podría ejecutar llamadas automáticas fuera de control |
| Producción | Prohibido sin excepción — por contrato PUENTE-6E-A |
| Navegador / Playwright | Prohibido por todos los microciclos de la fase PUENTE-6 |
| Entorno con logging automático de variables | Prohibido — riesgo de exponer `ANTHROPIC_API_KEY` en logs |
| Entorno con transcript activo que captura el valor | Prohibido — revisar que el transcript de PowerShell no capture el valor de la key |
| Cualquier entorno compartido con otros usuarios | Prohibido — entorno debe ser controlado exclusivamente por Ariel |

---

## 6. Checklist previo local (ejecutar en PowerShell de Ariel antes de cualquier llamada)

Verificar **cada ítem** antes de ejecutar la llamada. Registrar en el documento de evidencia del microciclo de ejecución.

| Ítem | Verificación requerida |
|---|---|
| Repo en main actualizado | `git pull origin main` → sin divergencias |
| Working tree limpio | `git status` → `nothing to commit, working tree clean` |
| Tests verdes | `python -m unittest discover -s tests` → `507/507 OK` o superior |
| Red celular activa | Hotspot móvil conectado — no red corporativa |
| Producción desconectada | No hay conexión a sistemas productivos durante la ejecución |
| Workflows ausentes / no usados | `.github/workflows/` no existe — confirmado en PUENTE-6G-A |
| `ANTHROPIC_API_KEY` presente | `[bool]$env:ANTHROPIC_API_KEY` → `True` (solo booleano — no imprimir valor) |
| Valor de key no mostrado | Confirmar que ningún comando imprimirá el valor de la key |
| `cliente_api_real_minimo` importable | `python -c "from plic_puente_agentes.cliente_api_real_minimo import cliente_api_real_minimo; print('OK')"` |
| Presupuesto declarado | Tokens máximos declarados antes de ejecutar — por contrato PUENTE-6E-A sección 11 |

---

## 7. Reglas de PowerShell seguro

Al ejecutar el microciclo de llamada real desde PowerShell, aplicar estrictamente:

| Regla | Detalle |
|---|---|
| No pegar API key en archivos | El valor de `ANTHROPIC_API_KEY` nunca debe aparecer en ningún archivo del repo |
| No imprimir la key | No usar `Write-Host $env:ANTHROPIC_API_KEY` ni equivalente — solo verificación booleana |
| Evitar historial visible | Si es posible, no escribir el valor en la línea de comandos del historial — preferir `Read-Host -AsSecureString` o asignación directa sin echo |
| No guardar transcript con secret | Si PowerShell tiene `Start-Transcript` activo, detenerlo antes de asignar la key o verificar que no captura el valor |
| No registrar headers completos | El header `x-api-key` contiene la key — no copiar headers de request en documentación ni en logs |
| Limpiar variable al terminar | `Remove-Item Env:\ANTHROPIC_API_KEY` al finalizar el microciclo si corresponde — evitar que persista en sesiones sucesivas |
| Documentar solo presencia booleana | Registrar `ANTHROPIC_API_KEY presente: True` — nunca el valor real |

---

## 8. Payload futuro permitido

La llamada real debe usar el payload mínimo definido en PUENTE-6F-A sección 7:

| Campo | Valor |
|---|---|
| `model` | `claude-haiku-4-5-20251001` — único modelo autorizado |
| `max_tokens` | ≤ 50 — por contrato PUENTE-6E-A sección 6 |
| `temperature` | `0.0` (float, no entero `0`) — lección de PUENTE-6D |
| `messages` | Un único mensaje de texto de prueba controlado — sin datos reales ni sensibles |
| Cantidad de mensajes | 1 — sin conversación multi-turn |
| Datos sensibles en el prompt | **NINGUNO** — texto de prueba genérico solamente |

### Ejemplo de invocación (Python, sin key visible)

```python
from plic_puente_agentes.cliente_api_real_minimo import cliente_api_real_minimo

resultado = cliente_api_real_minimo({
    "modo_seguro": True,
    "permitir_llamada_real": True,
    "prompt": "Responde solo: PLIC_OK",
    "modelo": "claude-haiku-4-5-20251001",
    "max_tokens": 10,
    "timeout": 10,
})
```

`ANTHROPIC_API_KEY` debe estar en el entorno del proceso (`$env:ANTHROPIC_API_KEY`) — nunca hardcodeada.

---

## 9. Límites de ejecución futura

| Límite | Valor |
|---|---|
| Máximo requests reales en el microciclo | **1** — sin excepción |
| Retry automático | **PROHIBIDO** — por contrato PUENTE-6E-A sección 9 |
| Loop o repetición | **PROHIBIDO** — ningún mecanismo de iteración |
| Automatización | **PROHIBIDA** — la llamada es manual, desde PowerShell de Ariel |
| Producción involucrada | **PROHIBIDA** — sin excepción |
| Workflows disparados | **PROHIBIDOS** — `.github/workflows/` no existe y no debe crearse |
| Merge durante la ejecución | **PROHIBIDO** — el microciclo de ejecución no modifica el repo |
| Llamadas a otros endpoints | **PROHIBIDAS** — solo `https://api.anthropic.com/v1/messages` |
| Múltiples modelos simultáneos | **PROHIBIDO** — por contrato PUENTE-6E-A |

---

## 10. Evidencia posterior esperada

Al completar la llamada real (en el microciclo de ejecución), Ariel debe registrar **todos** los siguientes campos usando la plantilla de PUENTE-6F-B:

| Campo | Descripción |
|---|---|
| Fecha/hora (UTC) | Timestamp del momento exacto de ejecución |
| Entorno usado | `PowerShell local` — especificar versión si es posible |
| Red usada | `Red celular / hotspot móvil` — confirmar que no fue red corporativa |
| Modelo | `claude-haiku-4-5-20251001` |
| Cantidad de requests realizados | Debe ser `1` |
| `status_code` obtenido | Valor numérico HTTP — esperado `200` |
| `respuesta_texto` resumida | Solo si no es sensible — sanitizada |
| `usage.input_tokens` | Entero |
| `usage.output_tokens` | Entero |
| `llamada_real_ejecutada` | Debe ser `True` |
| `secret_expuesto` | Debe ser `False` |
| Secrets expuestos | `0` — verificación explícita |
| Archivos modificados en el microciclo | Solo documentales — el código no se modifica |
| Tests pre-llamada | `507/507 OK` o superior |
| Tests post-llamada | `507/507 OK` o superior |
| Dictamen final | Registrado según criterios de PUENTE-6F-B |

---

## 11. Criterios de bloqueo

Si cualquiera de los siguientes criterios se cumple, la llamada real **no debe ejecutarse** y el microciclo debe frenarse inmediatamente:

| Criterio de bloqueo | Acción |
|---|---|
| Falta autorización explícita de Ariel para el microciclo de ejecución | **FRENAR** — no ejecutar sin autorización |
| No está en entorno local de Ariel | **FRENAR** — Claude Code remoto y CI/CD están prohibidos |
| Red celular no definida / no activa | **ADVERTENCIA** — preferir red celular; si se usa otra, documentar y evaluar riesgo |
| `ANTHROPIC_API_KEY` ausente en el entorno de ejecución | **FRENAR** — reportar `anthropic_api_key_ausente` |
| Riesgo de imprimir o exponer el valor de la key | **FRENAR** — revisar configuración antes de continuar |
| Tests rotos (`< 507/507 OK`) | **FRENAR** — corregir antes de cualquier llamada |
| Working tree sucio (cambios no commiteados) | **FRENAR** — limpiar o commitear antes |
| Intento de ejecutar más de una llamada en el microciclo | **FRENAR** — reducir a exactamente 1 |
| Intento de afectar sistema productivo | **FRENAR PERMANENTEMENTE** — prohibido sin excepción |
| `cliente_api_real_minimo` no importable o con error | **FRENAR** — corregir antes de continuar |
| Checklist PUENTE-6F-A no verificado | **FRENAR** — completar checklist antes |

---

## 12. Qué NO queda autorizado por este documento

Este documento define el procedimiento. No ejecuta nada. No autoriza nada todavía.

| Acción | Estado |
|---|---|
| Ejecutar llamada real a Anthropic | **NO AUTORIZADO** |
| Hacer request HTTP a cualquier endpoint | **NO AUTORIZADO** |
| Usar la API de Anthropic de forma efectiva | **NO AUTORIZADO** |
| Usar el SDK de Anthropic | **NO AUTORIZADO** |
| Usar `cliente_api_real_minimo` con `permitir_llamada_real=True` | **NO AUTORIZADO** |
| Leer, imprimir o exponer secrets | **NO AUTORIZADO** |
| Crear o modificar `.env` | **NO AUTORIZADO** |
| Modificar código fuente | **NO AUTORIZADO** |
| Modificar tests | **NO AUTORIZADO** |
| Tocar producción | **NO AUTORIZADO** |
| Crear workflows | **NO AUTORIZADO** |
| Usar navegador o Playwright | **NO AUTORIZADO** |
| Avanzar a ejecución real sin instrucción separada de Ariel | **NO AUTORIZADO** |

---

## 13. Confirmaciones de seguridad de este microciclo

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

## 14. Dictamen final

### **PUENTE-6G-B — PROCEDIMIENTO LOCAL SEGURO PREPARADO**

Este documento define el procedimiento operativo local (PowerShell + red celular) para una futura llamada real usando `cliente_api_real_minimo`. **No ejecuta ninguna llamada. No autoriza ninguna acción. No habilita producción.**

**La llamada real futura sigue NO habilitada.**

Para habilitarla se requieren: este documento mergeado en main, auditoría aprobada, y autorización explícita y separada de Ariel en un microciclo propio con nombre, alcance y presupuesto definidos.

> El próximo paso requiere instrucción explícita y separada de Ariel.
