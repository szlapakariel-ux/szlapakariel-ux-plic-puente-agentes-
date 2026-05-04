# PUENTE-6B — Resultado: Cliente API real preparado, sin llamada real

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6B |
| Rama base | `main` |
| Commit base | `9b9d82f4863b0dacb3d4d52aec0b9573b12a0bc7` (PUENTE-6A incluido) |
| Rama de trabajo | `feat/puente-6b-cliente-api-real-preparado-sin-llamada` |
| Tests al iniciar | 262/262 OK |
| Estado de PUENTE-6A | Cerrado en main — contrato documental disponible |

---

## 2. Archivos creados

| Archivo | Tipo | Descripción |
|---|---|---|
| `src/plic_puente_agentes/cliente_api_real_preparado.py` | Código Python | Función pura que valida y prepara una estructura de request futura sin ejecutar ninguna llamada real |
| `tests/test_cliente_api_real_preparado.py` | Tests unitarios | 64 tests cubriendo todos los casos del cliente preparado |
| `docs/puente-6b-resultado-cliente-api-real-preparado.md` | Documental | Este archivo — resultado del microciclo |

---

## 3. Qué implementa `cliente_api_real_preparado`

### Función principal

```python
cliente_api_real_preparado(entrada: dict) -> dict
```

### Input esperado (8 campos)

| Campo | Tipo | Descripción |
|---|---|---|
| `prompt` | string | Instrucción mínima a preparar — sin datos sensibles |
| `modo_seguro` | bool | Debe ser `True` (identidad estricta) |
| `proveedor` | string | Debe ser `"anthropic"` |
| `modelo` | string | Debe estar en la lista de modelos permitidos |
| `timeout` | int/float | Máximo 10 segundos |
| `max_tokens` | int | Máximo 300 |
| `request_id` | string | Identificador de trazabilidad |
| `permitir_llamada_real` | bool | Debe ser `False` o ausente — si es `True` bloquea |

### Output garantizado (13 campos)

| Campo | Tipo | Descripción |
|---|---|---|
| `ok` | bool | `True` si la preparación fue exitosa, `False` en cualquier bloqueo |
| `proveedor` | string | Siempre `"anthropic_preparado"` |
| `modo` | string | Siempre `"api_real_preparada_sin_llamada"` |
| `modelo` | string | Modelo solicitado o `""` si bloqueó antes |
| `request_preparado` | dict \| null | Estructura del request futuro (sin headers, sin key) o `null` si bloqueó |
| `response_text` | string | Siempre `""` — no hay llamada real |
| `error_tipo` | string | Tipo de error o `""` si ok |
| `fallback_usado` | bool | Siempre `False` en este ciclo |
| `tokens_estimados` | int \| null | Estimación local (len(prompt)//4 + max_tokens) |
| `costo_estimado` | string | Siempre `"no_calculado_sin_llamada"` |
| `evidencia` | string \| null | Indica que no se ejecutó llamada real |
| `bloqueo` | bool | `True` si alguna regla bloqueó la preparación |
| `motivo` | string | Explicación de la decisión |

### Reglas implementadas (por prioridad)

| Prioridad | Condición | error_tipo |
|---|---|---|
| 1 | `entrada` no es dict | `entrada_invalida` |
| 2 | `modo_seguro` no es `True` | `modo_seguro_requerido` |
| 3 | `permitir_llamada_real` es `True` | `llamada_real_no_autorizada` |
| 4 | `prompt` vacío | `prompt_vacio` |
| 5 | `prompt` contiene término sensible (frase) | `entrada_sensible` |
| 6 | `prompt` contiene término sensible (token con límite de palabra) | `entrada_sensible` |
| 7 | `proveedor` no es `"anthropic"` | `proveedor_no_autorizado` |
| 8 | `modelo` no está en lista permitida | `modelo_no_autorizado` |
| 9 | `timeout` > 10 | `timeout_excesivo` |
| 10 | `max_tokens` > 300 | `max_tokens_excesivo` |
| 11 | Default válido | preparación exitosa |

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

### Modelos permitidos (lista documental)

| Modelo |
|---|
| `claude-3-5-haiku-latest` |
| `claude-3-haiku-20240307` |

### Helper `_es_token`

Mismo patrón que `cerebro_mock.py`, `mano_local_simulada.py` y `cliente_haiku_fake.py` — word-boundary sin regex, sin imports.

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
| Integración con Cliente Haiku Fake | NO — componente independiente |
| Fallback automático al cliente fake | NO — en este ciclo siempre devuelve `fallback_usado: False` |
| Retry | NO — cero reintentos |
| Streaming | NO |
| Cálculo real de costo | NO — siempre `"no_calculado_sin_llamada"` |
| Tokenización real | NO — estimación local simplificada |

---

## 5. Casos cubiertos por tests

### Clases de tests y cobertura

| Clase | Tests | Cubre |
|---|---|---|
| `TestClienteApiRealPreparadoIdentidad` | 2 | proveedor y modo constantes en toda salida |
| `TestClienteApiRealPreparadoEntradaInvalida` | 5 | no dict, lista, None, int, proveedor en bloqueo |
| `TestClienteApiRealPreparadoModoSeguro` | 5 | False, None, int 1, string "true", ausente |
| `TestClienteApiRealPreparadoLlamadaReal` | 5 | True bloquea, motivo menciona PUENTE-6B y PUENTE-6C, False y ausente no bloquean |
| `TestClienteApiRealPreparadoPrompt` | 10 | vacío, solo espacios, secret, token, api key, .env, clave, contraseña + falsos positivos (tokenización, secretaría) |
| `TestClienteApiRealPreparadoProveedor` | 3 | openai bloquea, vacío bloquea, anthropic pasa |
| `TestClienteApiRealPreparadoModelo` | 4 | gpt-4 bloquea, vacío bloquea, haiku-latest pasa, haiku-fecha pasa |
| `TestClienteApiRealPreparadoTimeout` | 3 | 11 bloquea, 10 pasa, 5 pasa |
| `TestClienteApiRealPreparadoMaxTokens` | 3 | 301 bloquea, 300 pasa, 1 pasa |
| `TestClienteApiRealPreparadoCasoValido` | 16 | ok, bloqueo, response_text, fallback, evidencia, request_preparado, sin api_key, sin headers, sin Authorization, tokens_estimados local, costo, proveedor, modo, error_tipo, modelo |
| `TestClienteApiRealPreparadoCampos` | 2 | 13 campos en salida válida y en salida bloqueada |
| `TestClienteApiRealPreparadoAislamiento` | 7 | no importa anthropic/requests/urllib/http.client; cerebro_mock, mano_local_simulada, cliente_haiku_fake no modificados |

**Total: 65 tests nuevos.**

---

## 6. Resultado de tests

```
python -m unittest discover -s tests

Ran 326 tests in 0.008s

OK
```

| Tests originales | Tests nuevos | Total |
|---|---|---|
| 262 | 64 | **326** |

**326/326 tests pasan.** Sin errores. Sin warnings.

---

## 7. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin imports en `cliente_api_real_preparado.py` | CONFIRMADO — cero imports |
| Función pura preservada | CONFIRMADO — sin I/O, sin red, sin subprocess |
| `cerebro_mock.py` no modificado | CONFIRMADO |
| `mano_local_simulada.py` no modificado | CONFIRMADO |
| `cliente_haiku_fake.py` no modificado | CONFIRMADO |
| Tests originales conservados (262) | CONFIRMADO — siguen pasando |
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
| Sin repos prohibidos | CONFIRMADO — torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero no tocados |
| `permitir_llamada_real=True` es condición de bloqueo | CONFIRMADO — test 5 lo verifica |
| Contrato de salida 13 campos respetado | CONFIRMADO |

---

## 8. Riesgos

| Riesgo | Nivel | Mitigación |
|---|---|---|
| Confundir `modo: "api_real_preparada_sin_llamada"` como autorización real | Bajo | El campo es inmutable y siempre visible en el output |
| Usar el cliente preparado como bypass de las reglas de seguridad | Bajo | `permitir_llamada_real=True` es condición de bloqueo explícita |
| Escalar prematuramente a llamada real sin PUENTE-6C | Alto | Función no tiene código de red — imposible ejecutar llamada desde esta función |
| Estimación de tokens imprecisa | Bajo | Es solo documental/local — no afecta funcionalidad; la llamada real requiere PUENTE-6C |
| Tests no deterministas | Cero | Función pura — 100% determinista |

---

## 9. Próximo microciclo sugerido

**PUENTE-6C — Auditoría técnica del cliente API real preparado, sin llamada real**

Objetivo: revisar la implementación de PUENTE-6B, validar que el cliente preparado es una función pura sin imports, que las reglas de prioridad son correctas, que los 64 tests cubren los casos críticos, que `permitir_llamada_real=True` bloquea correctamente, que no hay código de red, y evaluar si quedan casos edge no cubiertos.

Alcance:
- Solo lectura.
- Sin modificaciones al código.
- Sin modificaciones a tests.
- Auditar reglas de prioridad con casos edge adicionales.
- Verificar que la función es segura para ser el punto de entrada de PUENTE-6D (primera llamada real).

Restricciones:
- Solo lectura.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.
- Sin secrets.
- Sin producción.

> No iniciar PUENTE-6C hasta que PUENTE-6B esté cerrado con evidencia verificable (commit + push) y autorización explícita de Ariel.
