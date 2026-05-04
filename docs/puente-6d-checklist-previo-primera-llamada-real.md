# PUENTE-6D-CHECKLIST — Verificación operativa previa a primera llamada real

## 1. Nombre del checklist

**PUENTE-6D-CHECKLIST — Verificación operativa previa a primera llamada real a Anthropic/Haiku**

---

## 2. Objetivo del microciclo

Verificar documentalmente que todas las condiciones del checklist operativo PUENTE-6D-A están satisfechas antes de que Ariel inicie PUENTE-6D real (primera llamada efectiva a la API de Anthropic).

Este microciclo:
- Lee los documentos de PUENTE-6D-A y PUENTE-6D-B.
- Verifica el estado de cada condición del checklist.
- Produce un documento de verificación con dictamen.
- No ejecuta ninguna llamada real.

---

## 3. Autorización recibida de Ariel

> "Autorizo PUENTE-6D real: primera llamada real controlada a Anthropic/Haiku, completando antes el checklist operativo PUENTE-6D-A."

**Interpretación operativa**: La autorización permite avanzar hacia PUENTE-6D real, pero primero debe completarse el checklist operativo. Este microciclo solo verifica el checklist. El microciclo de llamada real es independiente y requiere instrucción explícita separada.

---

## 4. Aclaraciones explícitas

| Ítem | Estado |
|---|---|
| Esta verificación NO ejecuta llamada real | CONFIRMADO |
| Esta verificación NO pide ni lee API key | CONFIRMADO |
| Esta verificación NO habilita automáticamente la llamada real | CONFIRMADO |
| Esta verificación es solo documental | CONFIRMADO |
| El microciclo PUENTE-6D real es un paso separado | CONFIRMADO |

---

## 5. Estado de main

| Campo | Valor |
|---|---|
| Commit actual de main | `ed06736b4ed33bd9571c50f22b3bfd7c5ddfd904` |
| Tests en main | 416/416 OK |
| Working tree | Limpio |
| Rama de trabajo | `docs/puente-6d-checklist-previo-primera-llamada-real` |

---

## 6. Checklist operativo con estado verificado

### 6.1 Estado de microciclos en main

| Condición | Estado | Evidencia |
|---|---|---|
| PUENTE-6A cerrado en main | **OK** | Commit `9b9d82f` — `docs/puente-6a-contrato-prueba-api-real.md` en main |
| PUENTE-6B cerrado en main | **OK** | Commit `0adf9ab` — `src/plic_puente_agentes/cliente_api_real_preparado.py` en main |
| B-07 cerrado en main | **OK** | Commit `425b520` — validación de `request_id` activa en `cliente_api_real_preparado.py` |
| PUENTE-6D-A cerrado en main | **OK** | Commit `dae2f0f` — contrato operativo + checklist operativo en main |
| PUENTE-6D-B cerrado en main | **OK** | Commit `ed06736` — `cliente_api_real_bloqueado.py` en main |

### 6.2 Estado de tests

| Condición | Estado | Evidencia |
|---|---|---|
| Tests 416/416 OK | **OK** | `python -m unittest discover -s tests` → `Ran 416 tests in 0.015s — OK` |

### 6.3 Gate de llamada real

| Condición | Estado | Evidencia |
|---|---|---|
| Gate de llamada real incorporado en main | **OK** | `src/plic_puente_agentes/cliente_api_real_bloqueado.py` en main |
| `llamada_real_ejecutada` siempre `False` | **OK** | Invariante estructural — única asignación en L56, hardcodeada en `_salida()` |
| `llamada_real_bloqueada` siempre `True` | **OK** | Invariante estructural — hardcodeada en `_salida()` |
| `permitir_llamada_real=True` bloquea | **OK** | Regla de prioridad 5 — bloqueado incluso cuando viene `True` |
| Gate tiene cero imports | **OK** | Verificado en PUENTE-6D-C — 0 imports en módulo gate |
| Gate es función pura sin I/O ni red | **OK** | Verificado en PUENTE-6D-C — sin efectos secundarios |

### 6.4 Parámetros del futuro prompt

| Condición | Estado | Valor definido |
|---|---|---|
| Prompt futuro exacto definido | **OK** | `"Respondé exactamente: PLIC_OK"` — definido en PUENTE-6D-A sección 9 |
| Modelo futuro permitido definido | **OK** | `claude-3-5-haiku-latest` — único modelo autorizado |
| `request_id` obligatorio definido | **OK** | String no vacío, único, sin datos sensibles |
| `timeout` máximo futuro definido | **OK** | `<= 10` segundos |
| `max_tokens` máximo futuro definido | **OK** | `<= 50` tokens |

### 6.5 Prohibiciones de API key y secrets

| Condición | Estado | Evidencia |
|---|---|---|
| Variable permitida solo como nombre: `ANTHROPIC_API_KEY` | **OK** | Solo aparece como referencia textual en docs — nunca con valor real |
| Valor real de API key prohibido en repo | **OK** | `git grep -r "sk-ant" .` → sin resultados |
| Valor real de API key prohibido en prompt | **OK** | El único prompt autorizado es `"Respondé exactamente: PLIC_OK"` — sin keys |
| Valor real de API key prohibido en logs | **OK** | Ningún código en main imprime entorno ni headers |
| Headers prohibidos en evidencia | **OK** | Ningún test ni módulo loguea `Authorization` |
| `Authorization` prohibido en evidencia | **OK** | Verificado en PUENTE-6D-C: test `test_caso_valido_no_contiene_headers` activo |
| `.env` prohibido | **OK** | No existe ningún `.env` en el repo |
| Secrets en repo prohibidos | **OK** | Ningún archivo `.pem`, `.key`, `.p12`, `credentials.json` en repo |

### 6.6 Prohibiciones operativas

| Condición | Estado |
|---|---|
| Navegador prohibido | **OK** |
| Playwright prohibido | **OK** |
| Producción prohibida | **OK** |
| Workflows prohibidos | **OK** — no existe `.github/workflows/` |
| GitHub real como acción prohibido | **OK** |
| Mano Local real prohibida | **OK** — `mano_local_simulada.py` es el componente activo |

### 6.7 Controles operativos

| Condición | Estado | Evidencia |
|---|---|---|
| Fallback obligatorio definido | **OK** | `cliente_haiku_fake` disponible y pasando tests |
| Kill switch definido | **OK** | Bloque 13 del checklist PUENTE-6D-A — Ctrl+C en cualquier momento |
| Condiciones de corte definidas | **OK** | 12 condiciones de corte en PUENTE-6D-A sección 7 |
| Reporte final mínimo definido | **OK** | Bloque 19 del checklist PUENTE-6D-A — 8 ítems obligatorios |

---

## 7. Datos para el futuro microciclo de llamada real

**Estos datos son solo referencias documentales. No contienen valores secretos.**

| Campo | Valor documental |
|---|---|
| `request_id` propuesto | `PLIC-6D-REAL-001` (placeholder — generar UUID real en sesión de ejecución) |
| Prompt exacto | `Respondé exactamente: PLIC_OK` |
| Modelo exacto | `claude-3-5-haiku-latest` |
| `timeout` | `10` segundos (límite máximo) |
| `max_tokens` | `50` tokens (límite máximo) |
| Nombre de variable de entorno | `ANTHROPIC_API_KEY` (solo el nombre — nunca el valor en este documento) |
| Evidencia permitida | Texto de respuesta si es `PLIC_OK` o variante inocua; `error_tipo`; `fallback_usado`; timestamps UTC; `request_id` usado |
| Evidencia prohibida | Valor real de `ANTHROPIC_API_KEY`; header `Authorization` con valor real; dump de `os.environ`; cualquier string `sk-ant-*` |

---

## 8. Bloqueos antes de llamada real

Los siguientes escenarios bloquean automáticamente la ejecución de cualquier llamada real:

| Escenario | Acción |
|---|---|
| Falta `ANTHROPIC_API_KEY` en entorno real | Cortar antes de llamar — activar fallback |
| No hay autorización explícita separada para ejecutar | No avanzar — reportar a Ariel |
| Algún ítem del checklist no está en OK | No avanzar — resolver antes |
| Aparece cualquier valor real de key en texto | Cortar — no loguear — reportar |
| Se intenta usar navegador, Playwright, workflows o producción | Cortar — bloqueo absoluto |
| Se intenta ejecutar más de una llamada | Cortar — solo una llamada en PUENTE-6D real |
| Se intenta usar un prompt distinto de `"Respondé exactamente: PLIC_OK"` | Cortar — bloqueo absoluto |
| Respuesta del modelo sugiere acción real | Cortar — `error_tipo: "corte"` — reportar a Ariel |
| Error de autenticación (401/403) | Cortar — no reintentar |
| Rate limit | Cortar — esperar 60s mínimo antes de reintento en ciclo futuro |
| Timeout > 10s | Cortar — activar fallback |
| Red no disponible | Cortar — activar fallback |

---

## 9. Dictamen del checklist

### **APTO PARA PR DOCUMENTAL**

Todos los ítems del checklist operativo están en estado **OK**:

- Los 5 microciclos previos están cerrados en `main`.
- Los 416 tests pasan sin errores.
- El gate de llamada real está incorporado con invariantes verificadas.
- Los parámetros del futuro prompt están definidos.
- Las prohibiciones de API key y secrets están verificadas.
- Las prohibiciones operativas están activas.
- Los controles operativos (fallback, kill switch, condiciones de corte, reporte mínimo) están definidos.

No se detectó ninguna condición bloqueante.

> Este dictamen habilita abrir un PR documental de este checklist hacia `main`. No habilita la ejecución de PUENTE-6D real.

---

## 10. Próximo microciclo sugerido

**PUENTE-6D-CHECKLIST-AUDITORÍA — Auditoría read-only del checklist previo a primera llamada real**

Objetivo: revisar documentalmente este checklist de verificación, confirmar que todos los ítems son correctos, que no hay condiciones faltantes, y emitir dictamen de aprobación o bloqueo antes de considerar PUENTE-6D real.

Alcance:
- Solo lectura.
- Sin modificaciones al código.
- Sin modificaciones a tests.
- Auditar cada ítem del checklist.
- Verificar que los bloqueos son suficientes.
- Verificar que los datos documentales no contienen valores secretos.

Restricciones:
- Solo lectura.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.
- Sin secrets.
- Sin producción.
- Sin llamada real.

> No iniciar PUENTE-6D real hasta que la auditoría del checklist esté cerrada en `main` con evidencia verificable y autorización explícita separada de Ariel para ejecutar.

---

## 11. Verificaciones de seguridad del microciclo

| Verificación | Estado |
|---|---|
| Sin código ejecutable nuevo | CONFIRMADO — solo markdown |
| Sin imports nuevos | CONFIRMADO — cero archivos `.py` nuevos |
| `cerebro_mock.py` no modificado | CONFIRMADO |
| `mano_local_simulada.py` no modificada | CONFIRMADO |
| `cliente_haiku_fake.py` no modificado | CONFIRMADO |
| `cliente_api_real_preparado.py` no modificado | CONFIRMADO |
| `cliente_api_real_bloqueado.py` no modificado | CONFIRMADO |
| Tests no modificados | CONFIRMADO |
| Sin scripts `.sh` | CONFIRMADO |
| Sin workflows `.yml`/`.yaml` | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin `.env` | CONFIRMADO |
| Sin API keys reales | CONFIRMADO — solo nombre `ANTHROPIC_API_KEY` como texto |
| Sin llamada real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin SDK real instalado | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin repos prohibidos tocados | CONFIRMADO |
| Tests existentes pasan | CONFIRMADO — 416/416 OK |
