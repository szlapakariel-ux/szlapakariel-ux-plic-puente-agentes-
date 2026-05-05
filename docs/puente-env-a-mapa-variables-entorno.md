# PUENTE-ENV-A — Mapa de variables y entorno sin exponer secrets

## 1. Identificación

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-ENV-A |
| Fecha/hora (UTC) | 2026-05-05 |
| Repo | `szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-` |
| Rama | `docs/puente-env-a-mapa-variables-entorno` |
| Commit base (main) | `a5d6549caca0baba222364508596d3be3aa9bc32` |
| Autorización de Ariel | "Crear mapa de variables y entorno sin exponer secrets" |

---

## 2. Estado de base

| Elemento | Estado |
|---|---|
| main actual | `a5d6549caca0baba222364508596d3be3aa9bc32` |
| PUENTE-6H-MAPA | **CERRADO** en main (PR #41) |
| Fase 6G completa | **CERRADA DOCUMENTALMENTE** |
| Tests actuales | **507/507 OK** |
| Checklist final (PUENTE-6H-A) | **NO INICIADO** |
| Llamada real futura | **NO HABILITADA** — requiere checklist final aprobado + autorización explícita de Ariel |

---

## 3. Objetivo del mapa

Este documento ordena el conocimiento sobre variables y entorno **antes** de llegar a cualquier checklist final o ejecución real. No verifica valores. No ejecuta nada. Su propósito es:

- **Ordenar las variables necesarias**: nombrar qué existe, qué se necesita, qué está prohibido.
- **Separar presencia de valor**: registrar solo si una variable existe (True/False), nunca su contenido.
- **Evitar exposición de secrets**: establecer reglas claras antes de que haya presión de ejecución.
- **Preparar condiciones para un futuro checklist final**: que el momento de ejecución no sea el momento de aprender las reglas.

> Saber que una variable existe no autoriza usarla. Tenerla disponible no habilita la llamada real.

---

## 4. Variables conocidas o esperadas

### 4.1 Variables de autenticación

| Variable | Tipo | Descripción | Obligatoria para llamada real |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | **SECRET** | Clave de autenticación para la API de Anthropic | **SÍ — bloqueante** |

### 4.2 Variables de configuración técnica

| Variable / Parámetro | Tipo | Descripción | Valor documentado |
|---|---|---|---|
| Modelo autorizado | Configuración técnica | Modelo a usar en el request | `claude-haiku-4-5-20251001` (documentado en PUENTE-6D-MODELO-FIX, PR #26) |
| `permitir_llamada_real` | Flag de bloqueo | Flag interno de `cliente_api_real_minimo.py` | `False` por defecto — bloqueante sin flag explícito |
| `max_tokens` | Configuración técnica | Límite de tokens por request | Mínimo posible; a definir en checklist |
| Endpoint API | Configuración técnica | URL del endpoint de Anthropic | Estándar de la librería; no configurar manualmente |

### 4.3 Variables de entorno de ejecución

| Variable / Condición | Tipo | Descripción |
|---|---|---|
| Tipo de red | Configuración de entorno | Red celular (hotspot móvil) — obligatoria por PUENTE-6G-B |
| Tipo de entorno | Configuración de entorno | Máquina local de Ariel (PowerShell) — obligatorio por PUENTE-6G-B |
| `ANTHROPIC_API_KEY` presente en sesión | Presencia booleana | Solo registrar True/False — nunca el valor |

### 4.4 Variables prohibidas en repo

| Variable | Motivo de prohibición |
|---|---|
| Valor de `ANTHROPIC_API_KEY` | Secret — nunca en repo, nunca en documento, nunca en chat |
| Cualquier token de API | Secret — misma regla |
| Headers de autenticación completos | Secret — pueden contener el valor de la key |
| Transcripts con valor de key expuesto | Secret — no commitear si contienen valor real |

---

## 5. Clasificación de variables

| Variable / Elemento | Clasificación | ¿Va al repo? | ¿Se imprime? | ¿Se verifica? |
|---|---|---|---|---|
| `ANTHROPIC_API_KEY` (nombre) | Secret | NO el valor — solo el nombre | NO el valor | Solo presencia booleana |
| `ANTHROPIC_API_KEY` (valor) | Secret | **NUNCA** | **NUNCA** | Solo True/False |
| Modelo (`claude-haiku-4-5-20251001`) | Configuración técnica | SÍ — ya documentado | SÍ | SÍ |
| `permitir_llamada_real` | Flag de bloqueo | SÍ — en código | SÍ | SÍ |
| `max_tokens` | Configuración técnica | SÍ — en código/checklist | SÍ | SÍ |
| Tipo de red (celular) | Configuración de entorno | SÍ — en procedimiento | SÍ | SÍ — pre-ejecución |
| Tipo de entorno (local/remoto) | Configuración de entorno | SÍ — en procedimiento | SÍ | SÍ — pre-ejecución |
| Headers HTTP de autenticación | Secret | **NUNCA** | **NUNCA** | **NUNCA** |
| Evidencia sanitizada | Documentación | SÍ — solo campos seguros | SÍ | SÍ |

---

## 6. Reglas para secrets

Las siguientes reglas aplican **siempre**, sin excepción, en cualquier entorno y en cualquier microciclo:

| Regla | Descripción |
|---|---|
| No guardar en repo | `ANTHROPIC_API_KEY` nunca en ningún archivo del repo, incluido `.env`, `.env.example`, scripts, docs o tests |
| No crear `.env` | Prohibido crear archivos `.env` de ningún tipo — ni de ejemplo |
| No imprimir valor | Ningún `print`, `echo`, `log` ni output puede mostrar el valor de la key |
| No pegar en documentos | No copiar el valor en ningún documento de evidencia, PR, commit ni issue |
| No registrar headers completos | Los headers HTTP de autenticación no se loguean ni documentan completos |
| No guardar transcripts con secret | Si un transcript de PowerShell contiene el valor, no se commitea |
| Solo presencia booleana | Lo único permitido es registrar `ANTHROPIC_API_KEY presente: True` o `False` — nunca el valor |
| Variable temporal en sesión | La key se asigna como variable de entorno temporal en la sesión de PowerShell; se elimina al terminar con `Remove-Item Env:\ANTHROPIC_API_KEY` |
| No hardcodear | El valor nunca se escribe directamente en código, scripts ni configuración |

---

## 7. Entornos posibles

| Entorno | Descripción |
|---|---|
| **Claude Code remoto** | Entorno de ejecución de este agente — sin `ANTHROPIC_API_KEY` disponible |
| **Máquina local de Ariel** | Entorno candidato para futura llamada real — PowerShell, Windows |
| **PowerShell** | Shell de ejecución en entorno local de Ariel |
| **Red celular (hotspot móvil)** | Red preferida para ejecución real — evita proxy corporativo |
| **Red corporativa / doméstica** | Red con riesgo de proxy — no recomendada (lección de PUENTE-6D) |
| **GitHub (remoto)** | Plataforma de versionado — solo documentación y código; nunca secrets |
| **Producción** | Cualquier sistema productivo — prohibido sin excepción |
| **CI / GitHub Actions / workflows** | Automatización — prohibida para llamada real |

---

## 8. Estado permitido por entorno

| Entorno | ¿Puede diagnosticar? | ¿Puede ejecutar llamada real? | ¿Candidato futuro? | ¿Prohibido? |
|---|---|---|---|---|
| Claude Code remoto | **SÍ** — read-only, presencia booleana | **NO** — `ANTHROPIC_API_KEY` ausente (bloqueante confirmado en PUENTE-6G-A) | **NO** — excluido por ausencia de key | NO (para diagnóstico) |
| Máquina local de Ariel (PowerShell) | **SÍ** | **SÍ** — candidato para futuro microciclo de ejecución | **SÍ** — cumple todos los requisitos de PUENTE-6G-B | NO |
| Red celular | Aplica al entorno local | **SÍ** — obligatoria con entorno local | **SÍ** — requerida | NO |
| Red corporativa / doméstica | Solo lectura | **NO** — riesgo de proxy (lección PUENTE-6D) | Evitar | NO (para lectura) |
| GitHub | **SÍ** — lectura de repo | **NO** | NO | NO (para lectura) |
| Producción | **NO** | **NO** | **NO** | **SÍ — prohibido siempre** |
| CI / GitHub Actions | **NO** para llamada real | **NO** | **NO** | **SÍ — prohibido para llamada real** |

---

## 9. Riesgos

| Riesgo | Nivel | Descripción | Mitigación |
|---|---|---|---|
| Secret expuesto en chat o documento | **ALTO** | Si el valor de `ANTHROPIC_API_KEY` se copia en el chat, en un archivo o en un PR | Regla absoluta: solo presencia booleana — ver §6 |
| `.env` accidental | **ALTO** | Si se crea un archivo `.env` con la key "para mayor comodidad" | Prohibición explícita — ver §6 |
| Variable persistida en sesión | **MEDIO** | Si la key queda asignada en la sesión de PowerShell después de ejecutar | `Remove-Item Env:\ANTHROPIC_API_KEY` al terminar — documentado en PUENTE-6G-B §7 |
| Historial de PowerShell | **MEDIO** | PowerShell puede guardar el comando de asignación con el valor en el historial | Evitar pegar el valor directamente en la línea de comando; usar método seguro de asignación |
| Logs con headers de autenticación | **MEDIO** | Si el cliente loguea los headers HTTP completos, la key puede quedar expuesta | `cliente_api_real_minimo.py` no loguea headers — verificar antes de ejecutar |
| Confusión entre entorno remoto y local | **MEDIO** | Intentar ejecutar desde Claude Code remoto creyendo que funcionará | PUENTE-6G-A confirma que `ANTHROPIC_API_KEY` no está en ese entorno — siempre verificar presencia antes |
| Ejecución desde CI / workflow | **MEDIO** | Si se configura un workflow que llame a la API con secrets de GitHub | Prohibido explícitamente — workflows de llamada real quedan fuera de alcance |
| Evidencia incompleta o sin sanitizar | **BAJO** | Si la evidencia post-llamada incluye campos sensibles sin sanitizar | Usar plantilla PUENTE-6F-B con reglas de sanitización antes de commitear |
| Retry accidental | **BAJO** | Si el código reintenta al recibir un error | `cliente_api_real_minimo.py` prohíbe retry por diseño — 8 guardas en cascada |

---

## 10. Controles mínimos

Los siguientes controles deben estar activos **en el momento de cualquier futura ejecución real**, no antes. Este documento los registra para que estén definidos cuando llegue ese momento:

| Control | Descripción | Estado actual |
|---|---|---|
| Working tree limpio | `git status` → `nothing to commit` antes de cualquier acción | A verificar en microciclo de ejecución |
| Tests verdes | `507/507 OK` en el commit base de ejecución | **PRESENTE** — 507/507 OK confirmado |
| Variable temporal en sesión | `ANTHROPIC_API_KEY` asignada solo como variable de sesión, nunca en archivo | A aplicar en entorno local de Ariel |
| Presencia booleana solamente | Solo registrar True/False — nunca el valor de la key | Regla activa desde PUENTE-6G-A |
| Limpieza posterior | `Remove-Item Env:\ANTHROPIC_API_KEY` al terminar la sesión | A ejecutar en entorno local de Ariel |
| 1 request máximo | Solo 1 request real en el microciclo de ejecución — sin retry | Obligatorio — contrato PUENTE-6E-A |
| Evidencia sanitizada | Completar plantilla PUENTE-6F-B con campos seguros únicamente | A ejecutar post-llamada, antes de commitear |
| Criterio de éxito/bloqueo definido | Definir qué constituye éxito y qué constituye bloqueo antes de ejecutar | A definir en checklist final (PUENTE-6H-A) |

---

## 11. Qué NO queda autorizado por este mapa

| Acción | Estado |
|---|---|
| Ejecutar llamada real a Anthropic | **NO AUTORIZADO** |
| Hacer request HTTP a cualquier endpoint | **NO AUTORIZADO** |
| Usar la API de Anthropic de forma efectiva | **NO AUTORIZADO** |
| Usar el SDK de Anthropic | **NO AUTORIZADO** |
| Usar `cliente_api_real_minimo` con `permitir_llamada_real=True` | **NO AUTORIZADO** |
| Leer, imprimir o exponer secrets | **NO AUTORIZADO** |
| Mostrar valores de variables de entorno | **NO AUTORIZADO** |
| Crear o modificar `.env` | **NO AUTORIZADO** |
| Modificar código fuente | **NO AUTORIZADO** |
| Modificar tests | **NO AUTORIZADO** |
| Tocar producción | **NO AUTORIZADO** |
| Crear workflows | **NO AUTORIZADO** |
| Usar navegador o Playwright | **NO AUTORIZADO** |
| Avanzar a ejecución real sin checklist final aprobado | **NO AUTORIZADO** |
| Avanzar a ejecución real sin autorización explícita separada de Ariel | **NO AUTORIZADO** |

---

## 12. Confirmaciones de seguridad de este microciclo

| Verificación | Estado |
|---|---|
| Llamada real ejecutada | NO |
| Request HTTP ejecutado | NO |
| Secret expuesto | NO |
| `ANTHROPIC_API_KEY` leída o impresa | NO |
| Valor de variable de entorno mostrado | NO |
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

### **PUENTE-ENV-A — SOLO ORDENA VARIABLES Y ENTORNO**

Este documento mapea variables, clasificaciones, reglas de manejo de secrets y estado por entorno. No verifica valores. No ejecuta nada. No habilita ninguna acción efectiva.

**La llamada real futura sigue NO habilitada.**

El checklist final (PUENTE-6H-A) o cualquier ejecución real requieren autorización explícita y separada de Ariel en un microciclo propio.

> El próximo paso requiere instrucción explícita y separada de Ariel.
