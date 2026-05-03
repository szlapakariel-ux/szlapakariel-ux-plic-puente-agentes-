# PUENTE-5A — Resultado: Contrato documental de integración Claude Haiku real

## 1. Estado

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-5A |
| Tipo | Documental — sin ejecución real |
| Fecha | 2026-05-03 |
| Rama | `docs/puente-5a-contrato-haiku-real-sin-ejecucion` |
| Commit base | `9aa3dc7` (main — PUENTE-4Z incluido) |
| Tests al iniciar | 173/173 OK |
| Estado | CONTRATO CREADO — pendiente revisión y cierre en main |

---

## 2. Qué se hizo en este microciclo

Se creó el contrato documental `docs/puente-5a-contrato-haiku-real.md` que define:

- El schema de input que se enviaría a Claude Haiku en un ciclo futuro real.
- El schema de output esperado de Haiku (9 campos — idéntico al contrato del Cerebro Mock).
- El mapeo de campos del Cerebro Mock al prompt de Haiku.
- El mapeo del output de Haiku hacia la Mano Local Simulada.
- Las reglas de seguridad obligatorias no delegables (R-01 a R-04).
- El protocolo de keys y secrets.
- El manejo de errores con principio de fail-safe.
- Los criterios para avanzar a PUENTE-5B.
- Los riesgos identificados y sus mitigaciones.
- Las condiciones de bloqueo para el ciclo real.

---

## 3. Schema de input definido

| Campo | Tipo | Descripción |
|---|---|---|
| `texto` | string | Instrucción recibida — campo principal de clasificación |
| `contexto` | string \| null | Contexto del sistema — enriquece la clasificación |
| `estado_del_ciclo` | string \| null | Estado actual del ciclo — condiciona continuidad |

Estos son exactamente los mismos 3 campos de entrada del Cerebro Mock actual.

---

## 4. Schema de output definido

| Campo | Tipo | Valores permitidos |
|---|---|---|
| `intencion` | string | Descripción breve de la intención clasificada |
| `confianza` | string | `"alta"` \| `"media"` \| `"baja"` |
| `riesgo` | string | `"bajo"` \| `"medio"` \| `"alto"` \| `"prohibido"` |
| `decision` | string | `"ejecutar"` \| `"continuar_documental"` \| `"pedir_autorizacion"` \| `"no_ejecutar"` |
| `requiere_ariel` | bool | `true` \| `false` |
| `requiere_torre` | bool | `true` \| `false` |
| `accion` | string \| null | Nombre de acción a ejecutar o `null` |
| `opciones` | list \| null | Lista de opciones o `null` |
| `motivo` | string | Explicación de la decisión |

Idéntico al contrato de 9 campos del Cerebro Mock — garantiza compatibilidad con la Mano Local sin cambios.

---

## 5. Reglas de seguridad no delegables

| Regla | Descripción |
|---|---|
| R-01 | Validar shape del output antes de pasarlo a Mano Local — campos presentes y valores en enum |
| R-02 | Post-proceso de seguridad: producción / secrets / repos prohibidos / output inválido → forzar `no_ejecutar / prohibido` |
| R-03 | Haiku no tiene acceso directo a la Mano Local — solo retorna JSON de decisión |
| R-04 | Logging obligatorio de cada llamada: input, output, correcciones R-02, decisión final |

**Principio de fail-safe:** ante cualquier error, output inválido o ambigüedad → `no_ejecutar / prohibido`.

---

## 6. Protocolo de secrets

| Elemento | Regla |
|---|---|
| `ANTHROPIC_API_KEY` | Variable de entorno local — fuera del repo |
| Archivos `.env` | En `.gitignore` — fuera del repo |
| Keys en código | PROHIBIDO — nunca |
| Keys en CI/CD públicos | PROHIBIDO |
| Logs de la key | PROHIBIDO |
| Acceso a keys reales | Solo Ariel |
| Revocación ante exposición | Inmediata en console.anthropic.com |

---

## 7. Manejo de errores — tabla resumen

| Error | Comportamiento |
|---|---|
| Timeout de red | `no_ejecutar / prohibido` + log |
| HTTP 401 | `no_ejecutar / prohibido` + log + alerta a Ariel |
| HTTP 429 (rate limit) | `no_ejecutar / prohibido` + log + espera |
| HTTP 5xx | `no_ejecutar / prohibido` + log + retry con backoff |
| JSON inválido en output | `no_ejecutar / prohibido` |
| Campo faltante en output | `no_ejecutar / prohibido` |
| Valor fuera de enum | `no_ejecutar / prohibido` |
| Output vacío | `no_ejecutar / prohibido` |

---

## 8. Condiciones para avanzar a PUENTE-5B

| Condición | Estado requerido |
|---|---|
| PUENTE-5A cerrado en main | Requerido |
| Autorización explícita de Ariel | Requerido |
| Tests 173/173 en main | Requerido |
| Alcance PUENTE-5B: solo cliente fake | Requerido — sin API real |
| Sin secrets reales en PUENTE-5B | Requerido |
| Sin modificar Mano Local en PUENTE-5B | Requerido |

**PUENTE-5B propuesto:** `cerebro_haiku_fake.py` — cliente que simula la interfaz de Haiku con respuestas hardcodeadas/fixtures, sin llamar a ningún endpoint real. Verifica integrabilidad del contrato antes de usar API real.

---

## 9. Riesgos — tabla resumen

| Riesgo | Nivel | Mitigación |
|---|---|---|
| Output no determinista | Alto | Validación R-01 + capa R-02 |
| Consumo inesperado de tokens | Medio | Rate limiting + monitoreo |
| Exposición de key | Alto | Key fuera del repo + .gitignore |
| Respuesta maliciosa / jailbreak | Alto | Capa R-02 no delegable |
| Latencia / timeout | Medio | Fail-safe → no_ejecutar |
| Costos acumulados en pruebas | Medio | Usar cliente fake primero (PUENTE-5B) |
| Haiku autoriza algo prohibido | Alto | R-02 forzada post-output — no evitable |

---

## 10. Qué NO se implementó en PUENTE-5A

| Ítem | Estado |
|---|---|
| Llamada real a `api.anthropic.com` | NO |
| `ANTHROPIC_API_KEY` real | NO |
| Archivo `.env` | NO |
| Modificación de `cerebro_mock.py` | NO |
| Modificación de `mano_local_simulada.py` | NO |
| Nuevos tests | NO |
| Instalación de dependencias | NO |
| Cliente Haiku fake (`cerebro_haiku_fake.py`) | NO — eso es PUENTE-5B |
| Workflows o CI | NO |
| Producción | NO — prohibición absoluta |
| Navegador / Playwright | NO — prohibición absoluta |
| Repos prohibidos | NO — prohibición absoluta |

---

## 11. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin imports nuevos en código existente | CONFIRMADO |
| `cerebro_mock.py` no modificado | CONFIRMADO |
| `mano_local_simulada.py` no modificado | CONFIRMADO |
| Tests no modificados | CONFIRMADO |
| Sin API real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin keys ni secrets | CONFIRMADO |
| Sin archivos `.env` | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin navegador ni Playwright | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin dependencias instaladas | CONFIRMADO |
| Sin repos prohibidos | CONFIRMADO |
| 173/173 tests pasan | CONFIRMADO |
| Solo documentos nuevos en este microciclo | CONFIRMADO |
