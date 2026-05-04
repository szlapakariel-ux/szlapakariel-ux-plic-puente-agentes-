# PUENTE-6D-B — Resultado: Cliente API real bloqueado por defecto

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6D-B |
| Rama base | `main` |
| Commit base | `dae2f0fabb4af55d815c73a606deaaaecc3b5315` (PUENTE-6D-A incluido) |
| Rama de trabajo | `feat/puente-6d-b-cliente-api-real-bloqueado` |
| Tests al iniciar | 339/339 OK |
| Estado de PUENTE-6D-A | Cerrado en main — contrato operativo disponible |
| Estado de B-07 | Cerrado en main — validación de `request_id` activa |

---

## 2. Archivos creados

| Archivo | Tipo | Descripción |
|---|---|---|
| `src/plic_puente_agentes/cliente_api_real_bloqueado.py` | Código Python | Gate de control: valida todas las condiciones de una futura llamada real sin ejecutarla — llamada real bloqueada por diseño |
| `tests/test_cliente_api_real_bloqueado.py` | Tests unitarios | 77 tests cubriendo todos los casos del gate |
| `docs/puente-6d-b-resultado-cliente-api-real-bloqueado.md` | Documental | Este archivo — resultado del microciclo |

---

## 3. Qué implementa `cliente_api_real_bloqueado`

### Función principal

```python
cliente_api_real_bloqueado(entrada: dict) -> dict
```

### Input esperado (11 campos)

| Campo | Tipo | Descripción |
|---|---|---|
| `prompt` | string | Debe ser exactamente `"Respondé exactamente: PLIC_OK"` |
| `modo_seguro` | bool | Debe ser `True` (identidad estricta) |
| `proveedor` | string | Debe ser `"anthropic"` |
| `modelo` | string | Debe ser `"claude-3-5-haiku-latest"` |
| `timeout` | int/float | Máximo 10 segundos |
| `max_tokens` | int | Máximo 50 |
| `request_id` | string | Obligatorio no vacío |
| `permitir_llamada_real` | bool | `True` bloquea — PUENTE-6D-B no ejecuta llamadas reales |
| `autorizacion_ariel` | string | Debe ser exactamente `"PUENTE-6D-B-SIN-LLAMADA-REAL"` |
| `contrato_puente_6d_a_confirmado` | bool | Debe ser `True` |
| `dry_run` | bool | Debe ser `True` — PUENTE-6D-B solo opera en modo dry_run |

### Output garantizado (14 campos)

| Campo | Tipo | Descripción |
|---|---|---|
| `ok` | bool | `True` si el gate validó correctamente, `False` en cualquier bloqueo |
| `proveedor` | string | Siempre `"anthropic_gate"` |
| `modo` | string | Siempre `"llamada_real_bloqueada_por_defecto"` |
| `modelo` | string | Modelo validado o `""` si bloqueó antes |
| `llamada_real_ejecutada` | bool | Siempre `False` — invariante absoluta de PUENTE-6D-B |
| `llamada_real_bloqueada` | bool | Siempre `True` — la llamada real nunca se ejecuta en este ciclo |
| `request_id` | string | Identificador de trazabilidad o `""` si bloqueó antes |
| `prompt_validado` | bool | `True` solo si el prompt exacto fue aceptado |
| `error_tipo` | string | Tipo de error o `""` si ok |
| `fallback_usado` | bool | Siempre `False` en PUENTE-6D-B |
| `evidencia` | string \| null | Indica que no se ejecutó llamada real |
| `bloqueo` | bool | `True` si alguna regla bloqueó la validación |
| `motivo` | string | Explicación de la decisión |
| `proximo_paso_seguro` | string | Siempre apunta a PUENTE-6D-C si el gate es válido |

### Reglas implementadas (por prioridad)

| Prioridad | Condición | error_tipo |
|---|---|---|
| 1 | `entrada` no es dict | `entrada_invalida` |
| 2 | `modo_seguro` no es `True` | `modo_seguro_requerido` |
| 3 | `contrato_puente_6d_a_confirmado` no es `True` | `contrato_no_confirmado` |
| 4 | `dry_run` no es `True` | `dry_run_requerido` |
| 5 | `permitir_llamada_real` es `True` | `llamada_real_bloqueada_por_defecto` |
| 6 | `autorizacion_ariel` no es `"PUENTE-6D-B-SIN-LLAMADA-REAL"` | `autorizacion_invalida` |
| 7 | `prompt` contiene término sensible | `entrada_sensible` |
| 8 | `prompt` no es exactamente el prompt autorizado | `prompt_no_autorizado` |
| 9 | `request_id` ausente, vacío, solo espacios o no-string | `request_id_invalido` |
| 10 | `proveedor` no es `"anthropic"` | `proveedor_no_autorizado` |
| 11 | `modelo` no es `"claude-3-5-haiku-latest"` | `modelo_no_autorizado` |
| 12 | `timeout` > 10 o no numérico | `timeout_invalido` |
| 13 | `max_tokens` > 50 o no int | `max_tokens_invalido` |
| 14 | Default válido | gate validado, llamada bloqueada por diseño |

### Invariantes absolutas

| Invariante | Valor siempre |
|---|---|
| `llamada_real_ejecutada` | `False` — sin excepción |
| `llamada_real_bloqueada` | `True` — sin excepción |
| `proveedor` | `"anthropic_gate"` |
| `modo` | `"llamada_real_bloqueada_por_defecto"` |

### Propiedades de la función

| Propiedad | Estado |
|---|---|
| Función pura | SÍ — sin efectos secundarios |
| Sin imports externos | SÍ — cero imports |
| Sin I/O | SÍ |
| Sin red | SÍ |
| Sin subprocess | SÍ |
| Sin lectura de entorno | SÍ |
| Sin lectura de archivos | SÍ |
| Sin API real | SÍ |
| Sin SDK de Anthropic | SÍ |
| Sin llamada real | SÍ — `permitir_llamada_real=True` es condición de bloqueo |

---

## 4. Qué NO implementa

| Ítem | Estado |
|---|---|
| Llamada real a `api.anthropic.com` | NO — prohibición absoluta en este ciclo |
| Lectura de `ANTHROPIC_API_KEY` | NO — ni desde entorno ni desde archivo |
| Uso del SDK `anthropic` | NO — no instalado ni importado |
| Archivo `.env` | NO |
| Integración con Cerebro Mock | NO — componente independiente |
| Integración con Mano Local | NO — componente independiente |
| Fallback automático al cliente fake | NO — gate solo valida, no ejecuta |
| Retry | NO — cero reintentos |
| Streaming | NO |
| Cálculo de costo | NO |
| Tokenización real | NO |

---

## 5. Casos cubiertos por tests

### Clases de tests y cobertura

| Clase | Tests | Cubre |
|---|---|---|
| `TestClienteApiRealBloqueadoIdentidad` | 5 | proveedor, modo, `llamada_real_ejecutada` siempre `False` |
| `TestClienteApiRealBloqueadoEntradaInvalida` | 3 | no dict, lista, None |
| `TestClienteApiRealBloqueadoModoSeguro` | 4 | False, None, int, string |
| `TestClienteApiRealBloqueadoContrato` | 3 | False, ausente, None |
| `TestClienteApiRealBloqueadoDryRun` | 3 | False, ausente, None |
| `TestClienteApiRealBloqueadoPermitirLlamadaReal` | 3 | True bloquea, motivo menciona PUENTE-6D-B y PUENTE-6D-C |
| `TestClienteApiRealBloqueadoAutorizacion` | 4 | incorrecta, ausente, vacía, exacta |
| `TestClienteApiRealBloqueadoPrompt` | 7 | distinto, vacío, secret, token, api key, exacto, validado |
| `TestClienteApiRealBloqueadoRequestId` | 6 | ausente, vacío, espacios, no-string, None, válido en salida |
| `TestClienteApiRealBloqueadoProveedor` | 2 | no autorizado, vacío |
| `TestClienteApiRealBloqueadoModelo` | 4 | gpt-4, vacío, haiku-3, autorizado |
| `TestClienteApiRealBloqueadoTimeout` | 4 | >10, no numérico, None, 10 pasa |
| `TestClienteApiRealBloqueadoMaxTokens` | 4 | >50, no int (float), None, 50 pasa |
| `TestClienteApiRealBloqueadoCasoValido` | 15 | ok, bloqueo, ejecutada, bloqueada, validado, error, fallback, evidencia, proximo_paso, sin headers, sin api_key, proveedor, modo, modelo, request_id |
| `TestClienteApiRealBloqueadoCampos` | 2 | 14 campos en salida válida y bloqueada |
| `TestClienteApiRealBloqueadoAislamiento` | 8 | no imports SDK/requests/urllib/http; cerebro_mock, mano_local, cliente_haiku_fake, cliente_api_real_preparado no modificados |

**Total: 77 tests nuevos.**

---

## 6. Resultado de tests

```
python -m unittest discover -s tests

Ran 416 tests in 0.009s

OK
```

| Tests originales | Tests nuevos | Total |
|---|---|---|
| 339 | 77 | **416** |

**416/416 tests pasan.** Sin errores. Sin warnings.

---

## 7. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin imports en `cliente_api_real_bloqueado.py` | CONFIRMADO — cero imports |
| Función pura preservada | CONFIRMADO — sin I/O, sin red, sin subprocess |
| `llamada_real_ejecutada` siempre `False` | CONFIRMADO — invariante en toda rama del código |
| `llamada_real_bloqueada` siempre `True` | CONFIRMADO — invariante en toda rama del código |
| `cerebro_mock.py` no modificado | CONFIRMADO |
| `mano_local_simulada.py` no modificada | CONFIRMADO |
| `cliente_haiku_fake.py` no modificado | CONFIRMADO |
| `cliente_api_real_preparado.py` no modificado | CONFIRMADO |
| Tests originales conservados (339) | CONFIRMADO — siguen pasando |
| Sin API real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin SDK real | CONFIRMADO |
| Sin lectura de entorno | CONFIRMADO |
| Sin `ANTHROPIC_API_KEY` leída | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin dependencias instaladas | CONFIRMADO |
| Sin repos prohibidos | CONFIRMADO |

---

## 8. Riesgos

| Riesgo | Nivel | Mitigación |
|---|---|---|
| Confundir el gate validado como autorización de llamada real | Bajo | `llamada_real_bloqueada: True` y `llamada_real_ejecutada: False` siempre visibles en output |
| Usar el gate como bypass eliminando el chequeo de `permitir_llamada_real` | Bajo | El módulo es de solo lectura en producción; cualquier cambio requiere nuevo ciclo de auditoría |
| Escalar prematuramente a llamada real sin PUENTE-6D-C | Alto | El gate no tiene código de red — imposible ejecutar llamada desde esta función |
| `autorizacion_ariel` hardcodeada como string | Bajo | Es intencional — el valor exacto debe venir del operador, no de config externa |
| Tests no deterministas | Cero | Función pura — 100% determinista |

---

## 9. Próximo microciclo sugerido

**PUENTE-6D-C — Auditoría técnica del cliente API real bloqueado por defecto**

Objetivo: revisar la implementación de PUENTE-6D-B, validar que el gate es una función pura sin imports, que las reglas de prioridad son correctas, que los 77 tests cubren los casos críticos, que `llamada_real_ejecutada` es siempre `False`, que no hay código de red, y evaluar si quedan casos edge no cubiertos antes de considerar PUENTE-6D real.

Alcance:
- Solo lectura.
- Sin modificaciones al código.
- Sin modificaciones a tests.
- Auditar reglas de prioridad con casos edge adicionales.
- Verificar que la función es segura como gate previo a PUENTE-6D real.

Restricciones:
- Solo lectura.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.
- Sin secrets.
- Sin producción.

> No iniciar PUENTE-6D-C hasta que PUENTE-6D-B esté cerrado con evidencia verificable (commit + push) y autorización explícita de Ariel.
