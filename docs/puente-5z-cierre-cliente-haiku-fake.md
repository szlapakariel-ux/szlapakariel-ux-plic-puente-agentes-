# PUENTE-5Z — Cierre de fase cliente Haiku fake/local

## 1. Nombre del cierre

| Campo | Valor |
|---|---|
| Cierre | PUENTE-5Z |
| Tipo | Documental — sin ejecución real |
| Fecha | 2026-05-04 |
| Commit base | `169468ef37eba391d987a1f3e4230e8f34bc9eaf` |
| Rama base | `main` |
| Fase cerrada | PUENTE-5 — Cliente Haiku fake/local |
| Tests al cerrar | 262/262 OK |

---

## 2. Objetivo del cierre

Consolidar de forma verificable el estado final de la fase PUENTE-5 (cliente Haiku fake/local), establecer qué quedó cerrado, qué sigue prohibido y cuáles son las condiciones mínimas para pensar en una prueba futura con API real (PUENTE-6).

**Este documento no habilita ninguna integración real.** No incluye llamadas a la API de Anthropic, no usa keys reales y no modifica código ni tests.

---

## 3. Estado de main usado como base

| Campo | Valor |
|---|---|
| Commit | `169468e` |
| Contenido | PUENTE-5D — Corrección falsos positivos B-06 — cerrado |
| Tests | 262/262 OK |
| Código real | Ninguno — todo es mock / fake / simulado |
| API real | NO habilitada |
| Keys | NO presentes |

---

## 4. Microciclos cerrados de PUENTE-5

| Microciclo | Descripción | Commit en main |
|---|---|---|
| PUENTE-5A | Contrato documental de integración Claude Haiku real, sin ejecución | `12ec0e4` |
| PUENTE-5B | Cliente Haiku fake/local — función pura, 0 imports, sin red | `4888c49` |
| PUENTE-5C | Auditoría técnica del cliente fake — dictamen B) APTO CON OBSERVACIONES | (read-only, sin commit propio) |
| PUENTE-5D | Corrección de falsos positivos B-06 con helper `_es_token()` | `169468e` |
| PUENTE-5E | Auditoría técnica de corrección B-06 — dictamen A) APTO PARA PR | (read-only, sin commit propio) |
| PUENTE-5Z | Este cierre documental | rama activa |

---

## 5. Estado del cliente Haiku fake/local

### Qué recibe (7 campos de entrada)

| Campo | Tipo | Descripción |
|---|---|---|
| `texto_original` | string | Instrucción a clasificar |
| `contexto_actual` | string \| null | Contexto del sistema |
| `estado_del_ciclo` | string \| null | Estado actual del ciclo |
| `autorizaciones_disponibles` | list | Autorizaciones disponibles |
| `reglas_plic` | list | Reglas PLIC activas |
| `historial_resumido` | string | Resumen del historial |
| `modo_seguro` | bool | Debe ser `True` para procesar |

### Qué devuelve (11 campos de salida)

| Campo | Tipo | Valores |
|---|---|---|
| `decision` | string | `"continuar_documental"` \| `"pedir_autorizacion"` \| `"no_ejecutar"` \| `"reformular"` |
| `riesgo` | string | `"bajo"` \| `"medio"` \| `"alto"` \| `"prohibido"` |
| `requiere_ariel` | bool | Si requiere autorización de Ariel |
| `requiere_torre` | bool | Si requiere confirmación de Torre |
| `motivo` | string | Explicación de la decisión |
| `accion_segura_sugerida` | string \| null | Acción sugerida |
| `opciones_para_ariel` | list \| null | Opciones para revisión |
| `bloqueo` | bool | Si la instrucción está bloqueada |
| `evidencia` | any \| null | Evidencia adicional |
| `proveedor` | string | Siempre `"haiku_fake"` |
| `modo` | string | Siempre `"fake_local_sin_api"` |

### Qué simula

- La forma del output que tendría un cliente Claude Haiku real integrado al sistema PLIC.
- El mismo contrato de 9 campos del Cerebro Mock (extendido a 11 con `proveedor` y `modo`).
- La lógica de clasificación de instrucciones usando reglas locales deterministas.

### Qué bloquea

| Condición | Decisión |
|---|---|
| `modo_seguro` no es `True` | `no_ejecutar / prohibido` |
| Entrada no es dict | `reformular / medio` |
| API real, API key, token, secret, .env, producción, navegador, Playwright, credencial, clave | `no_ejecutar / prohibido` |
| Texto vacío | `reformular / medio` |

### Qué nunca ejecuta

- Ninguna acción real de ningún tipo.
- No llama a ningún endpoint.
- No lee variables de entorno.
- No accede a archivos.
- No usa subprocess.
- No tiene efectos secundarios.
- Es una función pura con cero imports.

---

## 6. Estado del sistema completo

### Cerebro Portero Mock

| Característica | Valor |
|---|---|
| Archivo | `src/plic_puente_agentes/cerebro_mock.py` |
| Función | `cerebro_portero_mock(entrada: dict) -> dict` |
| Imports | Cero |
| Reglas de prioridad | 17 ordenadas |
| Output | 9 campos |
| Tests | 121 |
| Estado | ESTABLE — cerrado en PUENTE-4Z |

### Mano Local Simulada

| Característica | Valor |
|---|---|
| Archivo | `src/plic_puente_agentes/mano_local_simulada.py` |
| Función | `mano_local_simulada(entrada: dict) -> dict` |
| Imports | Cero |
| Acciones simuladas | 10 |
| Tests | 52 |
| Estado | ESTABLE — cerrado en PUENTE-4Z |

### Cliente Haiku Fake

| Característica | Valor |
|---|---|
| Archivo | `src/plic_puente_agentes/cliente_haiku_fake.py` |
| Función | `cliente_haiku_fake(entrada: dict) -> dict` |
| Imports | Cero |
| Reglas de prioridad | 8 (entrada, modo_seguro, vacío, prohibidas_frase, prohibidas_token, continuidad, merge_frase, merge_token, delegación, default) |
| Helper | `_es_token()` — word-boundary sin regex |
| Output | 11 campos |
| Tests | 89 |
| Estado | ESTABLE — cerrado en PUENTE-5D |

### Totales del sistema

| Métrica | Valor |
|---|---|
| Archivos de código | 3 módulos Python |
| Total imports entre los 3 | **0** |
| Total tests | **262/262 OK** |
| API real | NO |
| Dependencias externas | 0 |

---

## 7. Backlogs cerrados en PUENTE-5

### B-06 — Falsos positivos del cliente Haiku fake (cerrado en PUENTE-5D)

| Caso | Problema | Corrección |
|---|---|---|
| `"tissue"` → disparaba `"issue"` | Substring sin límite de palabra | `_es_token()` en `_MERGE_TOKEN` |
| `"tokenización"` → disparaba `"token"` | Substring sin límite de palabra | `_es_token()` en `_PROHIBIDAS_TOKEN` |
| `"continuamente"` → disparaba `"continua"` | Substring sin límite de palabra | `_es_token()` en `_PALABRAS_CONTINUIDAD` |
| `"secretaría"` → disparaba `"secret"` | Substring sin límite de palabra | `_es_token()` en `_PROHIBIDAS_TOKEN` |

**Técnica aplicada:** helper `_es_token(texto, token)` — idéntico al patrón de `cerebro_mock.py` y `mano_local_simulada.py`. Sin imports. Sin regex.

---

## 8. Tests

### Distribución

| Módulo | Tests |
|---|---|
| `test_cerebro_mock.py` | 121 |
| `test_mano_local_simulada.py` | 52 |
| `test_cliente_haiku_fake.py` | 89 (66 PUENTE-5B + 23 PUENTE-5D) |
| **Total** | **262** |

### Cobertura

| Área | Tests |
|---|---|
| Cerebro Mock: prioridades, contexto, estado, autorizaciones, backlogs 1-5 | 121 |
| Mano Local Simulada: 10 acciones, formatos, seguridad, backlogs | 52 |
| Cliente Haiku Fake: identidad, modo_seguro, entrada inválida, texto vacío, prohibidos, continuidad, merge, delegación, default, campos, aislamiento | 66 |
| Cliente Haiku Fake: correcciones B-06 (4 falsos positivos + disparadores reales + prioridades) | 23 |

### Resultado

```
python -m unittest discover -s tests

Ran 262 tests in 0.011s

OK
```

**262/262 pasan. Sin errores. Sin warnings.**

---

## 9. Qué queda habilitado

| Capacidad | Estado |
|---|---|
| Uso del cliente fake/local en tests y desarrollo | **HABILITADO** |
| Simulación de salida tipo Haiku (11 campos, misma forma del contrato) | **HABILITADO** |
| Auditoría documental del contrato de integración | **HABILITADO** — ver `docs/puente-5a-contrato-haiku-real.md` |
| Pruebas unitarias locales de las 3 funciones | **HABILITADO** — 262/262 OK |
| Verificación de que el contrato es integrable sin API real | **HABILITADO** — cliente fake es la prueba |
| Word-boundary detection para keywords de seguridad | **HABILITADO** — `_es_token()` en los 3 módulos |

---

## 10. Qué NO queda habilitado

| Ítem | Estado |
|---|---|
| API real (`api.anthropic.com`) | **NO — prohibición absoluta** |
| Claude Haiku real | **NO — prohibición absoluta** |
| SDK real (`anthropic` Python SDK) | **NO — prohibición absoluta** |
| API keys / `ANTHROPIC_API_KEY` | **NO — prohibición absoluta** |
| Archivos `.env` | **NO — prohibición absoluta** |
| Secrets en repo | **NO — prohibición absoluta** |
| Navegador real (Chromium, Firefox) | **NO — requiere ciclo específico** |
| Playwright real | **NO — requiere ciclo específico** |
| Producción | **NO — prohibición absoluta** |
| Workflows de CI/CD | **NO — prohibición absoluta** |
| Automatización externa (bots, webhooks, triggers) | **NO — requiere diseño y prueba controlada** |
| Conexión entre cliente fake y Mano Local real | **NO — requiere ciclo dedicado** |
| Reemplazo del Cerebro Mock por cliente Haiku | **NO — requiere PUENTE-6 completo** |

---

## 11. Riesgos residuales

| Riesgo | Nivel | Mitigación |
|---|---|---|
| Confundir `proveedor: "haiku_fake"` como autorización real | Bajo | El campo es inmutable y siempre visible en el output |
| Usar el cliente fake como bypass de seguridad | Bajo | Las reglas de prioridad del PLIC son independientes del cliente |
| Escalar prematuramente a API real sin contrato | Alto | Requiere PUENTE-6A (contrato) + autorización explícita de Ariel |
| Keys en prompt o logs durante prueba futura | Alto | Protocolo documentado en `puente-5z-condiciones-para-api-real.md` |
| Haiku real autoriza algo prohibido | Alto | Capa R-02 post-output (no delegable a Haiku) — documentada en PUENTE-5A |
| Tests no deterministas en integración real | Medio | Usar mocks de red / fixtures antes de llamadas reales |

---

## 12. Dictamen de cierre de fase

**FASE PUENTE-5 (cliente Haiku fake/local) — CERRADA.**

Los 5 microciclos activos de PUENTE-5 están cerrados en `main`. El cliente Haiku fake es una función pura con cero imports, 89 tests, word-boundary detection, y compatibilidad de contrato con el Cerebro Mock y la Mano Local. No se usó API real, no se usaron keys, no se tocó producción. El sistema tiene 3 módulos puros y 262/262 tests pasando.

**El próximo paso requiere autorización explícita de Ariel antes de iniciar PUENTE-6.**
