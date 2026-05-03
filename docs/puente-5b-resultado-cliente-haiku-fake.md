# PUENTE-5B — Resultado: Cliente Haiku fake/local

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-5B |
| Rama base | `main` |
| Commit base | `12ec0e448c006c2840b909528aaaab9534dbee4e` (PUENTE-5A incluido) |
| Rama de trabajo | `feat/puente-5b-cliente-haiku-fake-local` |
| Tests al iniciar | 173/173 OK |
| Estado de PUENTE-5A | Cerrado en main — contrato documental disponible |

---

## 2. Archivos creados

| Archivo | Tipo | Descripción |
|---|---|---|
| `src/plic_puente_agentes/cliente_haiku_fake.py` | Código Python | Cliente fake/local que simula la interfaz futura de Haiku |
| `tests/test_cliente_haiku_fake.py` | Tests unitarios | 66 tests cubriendo todos los casos del cliente fake |
| `docs/puente-5b-resultado-cliente-haiku-fake.md` | Documental | Este archivo — resultado del microciclo |

---

## 3. Qué implementa `cliente_haiku_fake`

### Función principal

```python
cliente_haiku_fake(entrada: dict) -> dict
```

### Input esperado (7 campos)

| Campo | Tipo | Descripción |
|---|---|---|
| `texto_original` | string | Instrucción a clasificar |
| `contexto_actual` | string \| null | Contexto del sistema |
| `estado_del_ciclo` | string \| null | Estado actual del ciclo |
| `autorizaciones_disponibles` | list | Autorizaciones disponibles |
| `reglas_plic` | list | Reglas PLIC activas |
| `historial_resumido` | string | Resumen del historial |
| `modo_seguro` | bool | Debe ser `True` para procesar |

### Output garantizado (11 campos)

| Campo | Tipo | Descripción |
|---|---|---|
| `decision` | string | `"continuar_documental"` \| `"pedir_autorizacion"` \| `"no_ejecutar"` \| `"reformular"` |
| `riesgo` | string | `"bajo"` \| `"medio"` \| `"alto"` \| `"prohibido"` |
| `requiere_ariel` | bool | Si requiere autorización de Ariel |
| `requiere_torre` | bool | Si requiere confirmación de Torre |
| `motivo` | string | Explicación de la decisión |
| `accion_segura_sugerida` | string \| null | Acción sugerida (si aplica) |
| `opciones_para_ariel` | list \| null | Opciones para revisión de Ariel |
| `bloqueo` | bool | Si la instrucción está bloqueada |
| `evidencia` | any \| null | Evidencia adicional |
| `proveedor` | string | Siempre `"haiku_fake"` |
| `modo` | string | Siempre `"fake_local_sin_api"` |

### Reglas implementadas (por prioridad)

| Prioridad | Condición | Decision | Riesgo |
|---|---|---|---|
| 1 | `entrada` no es dict | `reformular` | `medio` |
| 2 | `modo_seguro` no es `True` | `no_ejecutar` | `prohibido` |
| 3 | `texto_original` vacío | `reformular` | `medio` |
| 4 | Texto menciona API real / key / secret / token / .env / producción / navegador / Playwright | `no_ejecutar` | `prohibido` |
| 5 | Texto menciona continuidad (seguí, continuá, siguiente) | `continuar_documental` | `bajo` |
| 6 | Texto menciona merge / PR / issue | `pedir_autorizacion` | `alto` |
| 7 | Texto solicita delegación a otro agente | `reformular` | `medio` |
| 8 | Default | `reformular` | `medio` |

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

---

## 4. Qué NO implementa

| Ítem | Estado |
|---|---|
| Llamada real a `api.anthropic.com` | NO — función pura local |
| Uso de `ANTHROPIC_API_KEY` | NO |
| Integración con Cerebro Mock | NO — es independiente |
| Integración con Mano Local Simulada | NO — es independiente |
| Decisiones de ejecución real | NO — solo clasifica y devuelve decision |
| Navegador / Playwright | NO |
| Secrets / `.env` | NO |
| Producción | NO |
| Dependencias externas | NO — cero imports |
| Workflows o CI | NO |
| Reemplazo del Cerebro Mock | NO — son componentes separados |
| Conexión entre cliente fake y Mano Local | NO — eso es un ciclo posterior |

---

## 5. Casos cubiertos por tests

### Clases de tests y cobertura

| Clase | Tests | Cubre |
|---|---|---|
| `TestClienteHaikuFakeIdentidad` | 2 | proveedor y modo constantes |
| `TestClienteHaikuFakeModoSeguro` | 7 | modo_seguro False/None/ausente bloquea |
| `TestClienteHaikuFakeEntradaInvalida` | 5 | entrada no dict bloquea con campos correctos |
| `TestClienteHaikuFakeTextoVacio` | 5 | texto vacío y solo espacios reformula |
| `TestClienteHaikuFakeProhibidos` | 11 | API real, API key, token, .env, producción (con/sin tilde), navegador, Playwright, secret |
| `TestClienteHaikuFakeContinuidad` | 8 | seguí, segui, continuá, siguiente — riesgo bajo, sin ariel, con torre, sin bloqueo |
| `TestClienteHaikuFakeMerge` | 7 | merge, PR, issue — riesgo alto, requiere ariel y torre, sin bloqueo |
| `TestClienteHaikuFakeDelegacion` | 6 | pasalo a Claude/Codex, mandalo a otro agente |
| `TestClienteHaikuFakeDefault` | 5 | instrucción no reconocida → reformular/medio |
| `TestClienteHaikuFakeCampos` | 4 | 11 campos presentes en todos los paths |
| `TestClienteHaikuFakeAislamiento` | 6 | no importa cerebro_mock, mano_local, requests, anthropic, os, subprocess |

**Total: 66 tests nuevos.**

---

## 6. Resultado de tests

```
python -m unittest discover -s tests

Ran 239 tests in 0.006s

OK
```

| Tests originales | Tests nuevos | Total |
|---|---|---|
| 173 | 66 | **239** |

**239/239 tests pasan.** Sin errores. Sin warnings.

---

## 7. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin imports en `cliente_haiku_fake.py` | CONFIRMADO — cero imports |
| Función pura preservada | CONFIRMADO — sin I/O, sin red, sin subprocess |
| `cerebro_mock.py` no modificado | CONFIRMADO |
| `mano_local_simulada.py` no modificado | CONFIRMADO |
| Tests originales conservados (173) | CONFIRMADO — siguen pasando |
| Sin API real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin dependencias instaladas | CONFIRMADO |
| Sin repos prohibidos | CONFIRMADO — torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero no tocados |
| Contrato de salida 11 campos respetado | CONFIRMADO |

---

## 8. Riesgos

| Riesgo | Nivel | Mitigación |
|---|---|---|
| Confundir cliente fake con cliente real | Bajo | `proveedor: "haiku_fake"` y `modo: "fake_local_sin_api"` siempre presentes en output |
| Usar cliente fake para bypass de seguridad | Bajo | Reglas de prioridad siguen el mismo orden que el contrato PUENTE-5A |
| Reglas incompletas vs API real futura | Medio | Cliente fake no reemplaza al Cerebro Mock — es un componente separado de prueba |
| Tests no deterministicos | Cero | Función pura — 100% determinista |

---

## 9. Próximo microciclo sugerido

**PUENTE-5C — Auditoría técnica de cliente Haiku fake/local**

Objetivo: revisar la implementación de PUENTE-5B, validar que el cliente fake es una función pura sin imports, que las reglas de prioridad son correctas, que los 66 tests nuevos cubren los casos críticos, y evaluar si quedan casos edge no cubiertos.

Alcance:
- Solo lectura.
- Sin modificaciones al código.
- Sin modificaciones a tests.
- Auditar reglas de prioridad con casos edge adicionales.
- Auditar aislamiento del cliente fake respecto al Cerebro Mock y Mano Local.

Restricciones:
- Solo lectura.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.
- Sin secrets.
- Sin producción.

> No iniciar PUENTE-5C hasta que PUENTE-5B esté cerrado con evidencia verificable (commit + push) y autorización explícita de Ariel.
