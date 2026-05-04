# PUENTE-6D-A — Resultado: Contrato operativo primera llamada real

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-6D-A |
| Rama base | `main` |
| Commit base | `425b52001efe114a67866144ad1735b1155ae8f8` (B-07 incluido) |
| Rama de trabajo | `docs/puente-6d-a-contrato-operativo-primera-llamada-real` |
| Tests al iniciar | 339/339 OK |
| Estado de B-07 | Cerrado en main — validación de `request_id` activa |
| Estado de PUENTE-6B | Cerrado en main — cliente API real preparado sin llamada |
| Estado de PUENTE-6A | Cerrado en main — contrato prueba API real |

---

## 2. Documentos creados

| Archivo | Tipo | Descripción |
|---|---|---|
| `docs/puente-6d-a-contrato-operativo-primera-llamada-real.md` | Documental | Contrato completo: objetivo, precondiciones, modelo, variable de entorno, prompt exacto, parámetros, salida esperada, evidencia, condiciones de corte, fallback, reglas de no escalada, criterios, bloqueos, dictamen |
| `docs/puente-6d-a-checklist-ejecucion-primera-llamada-real.md` | Documental | Checklist operativo de 19 bloques para completar manualmente antes de PUENTE-6D real |
| `docs/puente-6d-a-resultado-contrato-operativo.md` | Documental | Este archivo — resultado del microciclo |

---

## 3. Qué queda habilitado

| Capacidad | Estado |
|---|---|
| Referencia documental al endpoint `/v1/messages` | **HABILITADO** — solo en docs, sin llamada real |
| Definición del prompt exacto para futura prueba | **HABILITADO** — `"Respondé exactamente: PLIC_OK"` |
| Definición del protocolo de manejo seguro de `ANTHROPIC_API_KEY` | **HABILITADO** — solo nombre como referencia textual |
| Inicio de PUENTE-6D-B (preparación técnica, sin llamada real) | **HABILITADO** — requiere autorización explícita de Ariel + este contrato en `main` |
| Uso del cliente fake como fallback | **HABILITADO** — `cliente_haiku_fake` sigue siendo el componente activo |
| Auditoría documental de este contrato | **HABILITADO** |
| Checklist operativo para uso manual | **HABILITADO** |

---

## 4. Qué NO queda habilitado

| Ítem | Estado |
|---|---|
| Llamada real a `api.anthropic.com` | **NO — requiere PUENTE-6D real + autorización explícita de Ariel** |
| Instalación del SDK `anthropic` | **NO — requiere PUENTE-6D-B + autorización explícita de Ariel** |
| Uso de `ANTHROPIC_API_KEY` con valor real | **NO — prohibición absoluta en cualquier archivo del repo** |
| Archivo `.env` | **NO — prohibición absoluta** |
| Claude Haiku real | **NO — requiere PUENTE-6D real** |
| Modificación de `cerebro_mock.py` | **NO — prohibición absoluta** |
| Modificación de `mano_local_simulada.py` | **NO — prohibición absoluta** |
| Modificación de `cliente_haiku_fake.py` | **NO — prohibición absoluta** |
| Modificación de `cliente_api_real_preparado.py` | **NO — prohibición absoluta** |
| Modificación de tests existentes | **NO — prohibición absoluta** |
| Producción | **NO — prohibición absoluta** |
| Navegador real | **NO — requiere ciclo específico** |
| Playwright real | **NO — requiere ciclo específico** |
| Workflows de CI/CD | **NO — prohibición absoluta** |
| Ejecución real por Mano Local | **NO — requiere ciclo separado posterior a PUENTE-6D** |
| Mezcla de primera llamada real con Mano Local real | **NO — prohibición absoluta en primera prueba** |

---

## 5. Checklist de seguridad

| Verificación | Estado |
|---|---|
| Sin código ejecutable nuevo | CONFIRMADO — solo markdown |
| Sin imports nuevos | CONFIRMADO — cero nuevos archivos `.py` |
| Sin modificación de `cerebro_mock.py` | CONFIRMADO |
| Sin modificación de `mano_local_simulada.py` | CONFIRMADO |
| Sin modificación de `cliente_haiku_fake.py` | CONFIRMADO |
| Sin modificación de `cliente_api_real_preparado.py` | CONFIRMADO |
| Sin modificación de tests | CONFIRMADO |
| Sin scripts (`.sh`) | CONFIRMADO |
| Sin workflows (`.yml`/`.yaml`) | CONFIRMADO |
| Sin secrets | CONFIRMADO |
| Sin `.env` | CONFIRMADO |
| Sin API keys reales | CONFIRMADO — solo nombre `ANTHROPIC_API_KEY` como texto de referencia |
| Sin llamada a API real | CONFIRMADO |
| Sin Claude Haiku real | CONFIRMADO |
| Sin SDK real instalado | CONFIRMADO |
| Sin navegador abierto | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin repos prohibidos tocados | CONFIRMADO — `torre-control`, `agente-saas`, `auditoria-sofse`, `plic-laboratorio-portero` no tocados |
| Tests existentes pasan | CONFIRMADO — 339/339 OK |

---

## 6. Riesgos

| Riesgo | Nivel | Mitigación |
|---|---|---|
| Filtrado accidental de API key en logs o docs | Alto | Nunca imprimir key; revisión manual de logs antes de guardar; `.env` en `.gitignore`; checklist bloque 8 |
| Confundir este contrato como autorización de llamada real | Bajo | El contrato dice explícitamente que requiere PUENTE-6D-B, PUENTE-6D-C y autorización de Ariel |
| Escalada prematura a llamada real sin completar PUENTE-6D-B | Alto | Bloqueo explícito en condiciones de bloqueo — sección 18 |
| Respuesta del modelo distinta de `PLIC_OK` | Medio | Condición de corte — no escalar sin nuevo contrato |
| Prompt modificado sin nuevo ciclo de auditoría | Alto | Prohibición absoluta — el prompt está fijo en sección 9 |
| Tests no deterministas en PUENTE-6D real | Medio | Tests de prueba real solo verifican estructura — no contenido exacto |
| Confusión entre "modelo sugiere X" y "sistema ejecuta X" | Alto | La respuesta del modelo es solo texto — nunca se ejecuta directamente |
| Key comprometida por commit accidental | Alto | `git grep "sk-ant"` obligatorio en checklist bloque 18 |
| Escalada no autorizada a producción | Alto | Prohibición absoluta — bloqueo en sección 18 |
| Usar `ANTHROPIC_API_KEY` como nombre de variable en código antes de PUENTE-6D-B | Bajo | PUENTE-6D-A solo usa el nombre en documentos markdown |

---

## 7. Condiciones de corte (resumen)

| Condición | Acción |
|---|---|
| Key no disponible | Cortar antes de llamar |
| Error de auth | Cortar — no reintentar |
| Rate limit | Cortar — esperar 60s mínimo antes de reintento en ciclo futuro |
| Costo > 50 tokens output | Cortar — revisar prompt |
| Respuesta vacía o malformada | Cortar — `error_tipo: "schema"` |
| Respuesta distinta de `PLIC_OK` | Cortar — registrar sin escalar |
| Respuesta que sugiere acción real | Cortar — `error_tipo: "corte"` — reportar a Ariel |
| Secret en entrada | Cortar antes de enviar |
| Secret en salida | Cortar — no loguear |
| Timeout > 10s | Cortar — activar fallback |
| Red no disponible | Cortar — activar fallback |
| Error no clasificado | Cortar — `error_tipo: "desconocido"` — activar fallback |

---

## 8. Resultado de tests

```
python -m unittest discover -s tests

Ran 339 tests in 0.011s

OK
```

| Tests existentes | Tests nuevos en este ciclo | Total |
|---|---|---|
| 339 | 0 | **339/339 OK** |

Este ciclo es solo documental — cero tests nuevos, cero modificaciones a tests existentes.

---

## 9. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin código ejecutable en docs creados | CONFIRMADO — solo markdown |
| Valor real de `ANTHROPIC_API_KEY` ausente en todos los docs | CONFIRMADO — solo el nombre como referencia |
| Bloque de código marcado como `# Referencia documental — no ejecutar en este ciclo` | CONFIRMADO — sección 7 del contrato |
| Sin modificación de los 4 módulos Python existentes | CONFIRMADO |
| Sin modificación de los 4 archivos de test existentes | CONFIRMADO |
| Sin archivos `.py` nuevos | CONFIRMADO |
| Sin archivos `.sh` nuevos | CONFIRMADO |
| Sin archivos `.yml`/`.yaml` nuevos | CONFIRMADO |
| Sin archivos `.env` nuevos | CONFIRMADO |
| Sin repos prohibidos tocados | CONFIRMADO |

---

## 10. Próximo microciclo sugerido

**PUENTE-6D-B — Preparación técnica de cliente API real con llamada real bloqueada por defecto**

### Objetivo

Crear el archivo `src/plic_puente_agentes/cliente_haiku_real.py` con:
- La firma de la función `cliente_haiku_real(entrada: dict) -> dict`.
- La carga segura de `ANTHROPIC_API_KEY` desde variable de entorno (no hardcodeada).
- La estructura del payload según el contrato definido en PUENTE-6D-A (prompt exacto, modelo, timeout, max_tokens, request_id).
- El fallback automático a `cliente_haiku_fake` si la key no está disponible o si ocurre cualquier error.
- El manejo de todas las condiciones de corte definidas en PUENTE-6D-A.
- Sin ejecutar ninguna llamada real — `permitir_llamada_real=True` bloqueado por defecto en PUENTE-6D-B.

### Alcance

- Solo crear `cliente_haiku_real.py` (nuevo archivo, no modifica existentes).
- Solo crear tests unitarios del cliente real en modo sin-llamada (con mock de red o con `permitir_llamada_real=False`).
- Sin llamada real a `api.anthropic.com`.
- Sin instalar `anthropic` SDK hasta autorización explícita de Ariel.

### Restricciones

- Sin API real.
- Sin Claude Haiku real.
- Sin `.env`.
- Sin secrets.
- Sin producción.
- Sin workflows.
- Sin modificar los 4 módulos existentes.
- Sin modificar tests existentes.

### Condición de inicio

> No iniciar PUENTE-6D-B hasta que PUENTE-6D-A esté cerrado en `main` con evidencia verificable (commit hash) **y** autorización explícita de Ariel en la sesión activa.
