# PUENTE-6E-C — Cierre documental del cliente real mínimo

## 1. Identificación

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6E-C |
| Fecha/hora (UTC) | 2026-05-05 |
| Repo | `szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-` |
| Rama | `docs/puente-6e-c-cierre-cliente-real-minimo` |
| Commit base (main) | `31964964b668480c78c7e4f4ec2d983d070598f9` |
| Autorización de Ariel | "Crear cierre documental corto del cliente real mínimo incorporado en PUENTE-6E-B" |

---

## 2. Estado cerrado

| Hito | Estado | PR | Commit en main |
|---|---|---|---|
| PUENTE-6E-MAPA — mapa de fase | **CERRADO** | #33 | `6b23853` |
| PUENTE-6E-B — cliente real mínimo | **CERRADO** | #34 | `3196496` |
| PUENTE-6E-C — este cierre documental | En curso | — | — |

**No hubo llamada real en ningún microciclo de PUENTE-6E.**

---

## 3. Qué quedó incorporado en main

Commit `3196496` (squash del PR #34) incorporó exactamente 3 archivos:

| Archivo | Descripción |
|---|---|
| `src/plic_puente_agentes/cliente_api_real_minimo.py` | Función cliente real mínima — bloqueada por defecto |
| `tests/test_cliente_api_real_minimo.py` | 91 tests — sin red real, con `_http_ejecutor` mock |
| `docs/puente-6e-b-resultado-cliente-real-minimo.md` | Documento de resultado de PUENTE-6E-B |

Ningún módulo preexistente fue modificado. Ningún test preexistente fue modificado.

---

## 4. Qué quedó probado

| Elemento probado | Evidencia |
|---|---|
| `cliente_api_real_minimo` bloquea por defecto (`permitir_llamada_real=False`) | `TestPermitirLlamadaReal::test_false_bloquea` — `llamada_real_no_autorizada` |
| `modo_seguro` debe ser `True` exacto para continuar | `TestModoSeguro` — 4 casos |
| Solo `claude-haiku-4-5-20251001` es aceptado | `TestModelo` — 4 casos |
| `max_tokens` limitado a rango 1–50 | `TestMaxTokens` — 7 casos |
| `timeout` limitado a rango (0, 10] | `TestTimeout` — 7 casos |
| Sin `ANTHROPIC_API_KEY` bloquea antes de ejecutar | `TestApiKeyAusente` — 2 casos |
| `secret_expuesto: False` en todo camino posible | `TestSecretInvariante` — 3 casos |
| `_http_ejecutor` permite testear sin red | `TestCasoValido`, `TestErroresHTTP` — 23 casos combinados |
| `urllib.request` no importado en nivel de módulo | `TestAislamiento::test_sin_urllib_request_en_nivel_modulo` |
| Todos los campos del contrato PUENTE-6E-A presentes | `TestCamposRespuesta` — 8 casos |
| Errores HTTP 401, 400, 429, 503 clasificados correctamente | `TestErroresHTTP` — 10 casos |
| Body de error sanitizado (max 1000 chars, patrones de secret omitidos) | `TestSanitizarBodyError` — 8 casos |
| 416 tests preexistentes siguen pasando | `test_cliente_api_real_preparado`, `test_cliente_haiku_fake`, `test_mano_local_simulada` |
| Suite total post-merge | **507/507 OK** |

### Lo que los tests NO prueban (por diseño)

- Que la key `"sk-test-fake-key-para-tests-no-real"` sea válida para Anthropic — es deliberadamente inválida.
- Que `_ejecutar_http` funcione contra la API real — nunca se invocó en ningún test.
- Que el modelo responda `PLIC_OK` en entorno real — eso fue probado en PUENTE-6D (Ariel, PowerShell, red celular).

---

## 5. Qué sigue bloqueado

| Elemento | Estado |
|---|---|
| Llamadas reales desde código | **BLOQUEADO** — requiere `permitir_llamada_real=True` + `ANTHROPIC_API_KEY` en entorno + microciclo propio |
| `ANTHROPIC_API_KEY` en Claude Code remoto | **NO RESUELTA** — Claude Code corre en entorno Linux aislado; la key no se propaga automáticamente desde PowerShell de Ariel |
| Llamada real desde `cliente_api_real_minimo` | **NO AUTORIZADA** — ningún microciclo la ha habilitado |
| Retry automático | **PROHIBIDO** — por contrato PUENTE-6E-A sección 9 |
| Integración en producción | **FUERA DE ALCANCE** |
| Agentes autónomos llamando a API real | **FUERA DE ALCANCE** |
| Scheduler o trigger automático | **FUERA DE ALCANCE** |

---

## 6. Riesgos residuales

| Riesgo | Nivel | Descripción | Mitigación |
|---|---|---|---|
| Llamada accidental desde código | **BAJO** | Requiere `permitir_llamada_real=True` + key presente + 7 validaciones más simultáneamente | 8 guardas en cascada; ningún camino accidental |
| `_ejecutar_http` invocada por reflexión | **MUY BAJO** | Solo accesible via `from cliente_api_real_minimo import _ejecutar_http` + key real en entorno | Requiere acción deliberada explícita |
| `ANTHROPIC_API_KEY` en entorno remoto inadvertida | **BAJO** | Si alguien inyecta la key en Claude Code settings y también pasa `permitir_llamada_real=True` | La combinación de guardas hace imposible el accidente puro |
| Confusión entre entorno local y remoto | **MEDIO** | Claude Code remoto no hereda la key del entorno local de Ariel | Documentado en PUENTE-6D-CIERRE-OPERATIVO y PUENTE-6E-A sección 7 |
| Costos no controlados | **BAJO** (hoy) | No hay mecanismo de llamada automática activo | Política de presupuesto de PUENTE-6E-A sección 11 — obligatoria en cualquier microciclo futuro con llamada real |

---

## 7. Qué NO queda autorizado por PUENTE-6E-B ni por este cierre

| Acción | Estado |
|---|---|
| Ejecutar llamada real a Anthropic desde código | **NO AUTORIZADO** |
| Pasar `permitir_llamada_real=True` en producción | **NO AUTORIZADO** |
| Usar `_ejecutar_http` directamente | **NO AUTORIZADO** |
| Automatizar llamadas sin microciclo propio | **NO AUTORIZADO** |
| Considerar que `claude-haiku-4-5-20251001` responderá igual que en PUENTE-6D | **NO GARANTIZADO** sin nueva verificación |
| Inyectar `ANTHROPIC_API_KEY` en Claude Code remoto sin microciclo documental | **NO AUTORIZADO** |
| Iniciar siguiente microciclo sin instrucción explícita de Ariel | **NO AUTORIZADO** |

---

## 8. Condiciones mínimas antes de una futura llamada real

Para autorizar una llamada real desde `cliente_api_real_minimo` se requieren **todas** las siguientes condiciones:

| Condición | Estado |
|---|---|
| Este cierre (PUENTE-6E-C) mergeado en main | Pendiente — PR de este microciclo |
| Auditoría de PUENTE-6E-C aprobada | Pendiente |
| Decisión sobre propagación de `ANTHROPIC_API_KEY` en entorno de ejecución | Pendiente — PUENTE-6E-ENV (opción B del mapa) o equivalente |
| Microciclo separado con nombre propio para la llamada real | Obligatorio |
| Presupuesto declarado explícitamente en ese microciclo | Obligatorio — por contrato PUENTE-6E-A sección 11 |
| Autorización explícita de Ariel para ese microciclo | **BLOQUEANTE** |
| Máximo 1 llamada real en ese microciclo | Obligatorio — por contrato PUENTE-6E-A sección 9 |
| No retry automático | Obligatorio |
| Evidencia documentada y auditada antes de PR | Obligatorio |

---

## 9. Confirmaciones de seguridad de este microciclo

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

## 10. Dictamen final

### **PUENTE-6E-C — CLIENTE MÍNIMO CERRADO DOCUMENTALMENTE**

`cliente_api_real_minimo` quedó incorporado en main, probado con 507 tests, bloqueado por defecto y sin ninguna llamada real ejecutada en ningún punto del ciclo PUENTE-6E.

**La llamada real futura sigue NO habilitada.**

Para habilitarla se requieren: este documento mergeado, auditoría aprobada, resolución del entorno de key, y autorización explícita y separada de Ariel en un microciclo propio.

> El próximo paso requiere instrucción explícita y separada de Ariel.
