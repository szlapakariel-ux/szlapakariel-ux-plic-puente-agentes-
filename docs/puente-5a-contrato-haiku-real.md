# PUENTE-5A — Contrato de integración Claude Haiku real (sin ejecución)

## 1. Nombre del contrato

| Campo | Valor |
|---|---|
| Contrato | PUENTE-5A |
| Tipo | Documental — sin ejecución real |
| Fecha | 2026-05-03 |
| Commit base | `9aa3dc7` |
| Rama base | `main` |
| Estado de la fase mock | CERRADO — PUENTE-4Z en main |
| Tests en main | 173/173 OK |

---

## 2. Objetivo del contrato

Definir el contrato de integración de Claude Haiku real como primera capacidad real del sistema PLIC — Puente de Agentes / Portero Local.

**Este contrato es solo documental.** No incluye ninguna llamada real a la API de Anthropic, ningún uso de keys reales, y ninguna modificación a `cerebro_mock.py`, `mano_local_simulada.py`, ni a los tests.

El contrato establece:
- qué input se enviaría a Haiku en el futuro;
- qué output se esperaría;
- cómo se manejarían errores;
- qué campos del Cerebro Mock se usarían como input del prompt;
- qué campos de la Mano Local se usarían como receptor de la decisión;
- el protocolo de keys (dónde viven, cómo se usan);
- qué NO se hace en este primer ciclo real.

---

## 3. Diferencia entre mock y real

### Cerebro Mock (estado actual)

| Característica | Valor |
|---|---|
| Implementación | Función pura Python |
| Imports | Ninguno |
| I/O | Ninguno |
| Red | Ninguna |
| Decisiones | Reglas deterministas (17 prioridades) |
| Riesgo | Cero |
| Tests | 173/173 OK |

El Cerebro Mock recibe un dict con 3 campos (`texto`, `contexto`, `estado_del_ciclo`) y devuelve un dict con 9 campos de forma determinista, sin efectos secundarios.

### Cerebro Haiku real (no implementado — solo contrato)

| Característica | Valor |
|---|---|
| Implementación | Llamada HTTP a `api.anthropic.com/v1/messages` |
| Imports | `anthropic` SDK (o `requests`) |
| I/O | Red — HTTP request/response |
| Red | Sí — requiere conexión a internet |
| Decisiones | Generativas — no deterministas |
| Riesgo | Alto — tokens consumidos, respuestas variables, posibles efectos |
| Tests | Requieren mocks de red o fixtures — ciclo separado |

---

## 4. Qué resuelve Haiku que el mock no resuelve

| Capacidad | Mock | Haiku real |
|---|---|---|
| Clasificar texto libre ambiguo | Parcial (reglas keyword) | Sí — comprensión semántica |
| Detectar intención implícita | No | Sí |
| Generar motivo en lenguaje natural | No (strings fijos) | Sí |
| Adaptarse a contexto complejo | No | Sí |
| Manejar idiomas o variantes | Solo español literal | Sí |
| Responder a textos no previstos | Cae en regla genérica | Puede inferir intención |

### Qué NO resuelve ni cambia Haiku

- La arquitectura de decisiones de seguridad sigue siendo responsabilidad del sistema PLIC.
- Las prohibiciones absolutas (producción, secrets en repo, repos prohibidos) no se delegan a Haiku.
- La mano local sigue siendo la ejecutora — Haiku solo informaría la decisión, no la ejecutaría.
- Los controles de autorización (requiere_ariel, requiere_torre) siguen siendo externos a Haiku.

---

## 5. Schema de input a Haiku (propuesto)

En un ciclo futuro real (PUENTE-5B o posterior), el input a Haiku tomaría la siguiente forma:

### Prompt del sistema (system prompt)

```
Eres el Cerebro Portero del sistema PLIC. Tu función es clasificar instrucciones humanas
y decidir si son seguras para ejecutar localmente.

Debes devolver SIEMPRE un JSON con exactamente estos campos:
- intencion: string breve
- confianza: "alta" | "media" | "baja"
- riesgo: "bajo" | "medio" | "alto" | "prohibido"
- decision: "ejecutar" | "continuar_documental" | "pedir_autorizacion" | "no_ejecutar"
- requiere_ariel: true | false
- requiere_torre: true | false
- accion: string | null
- opciones: lista de strings | null
- motivo: string explicativo

Reglas absolutas que nunca puedes violar:
1. Si el texto menciona producción, la decisión es siempre "no_ejecutar" con riesgo "prohibido".
2. Si el texto menciona secrets, keys, tokens o credenciales, la decisión es "no_ejecutar".
3. Si el texto menciona navegador real, Playwright, o automatización externa, es "no_ejecutar".
4. Si el texto menciona repos prohibidos (torre-control, agente-saas, auditoria-sofse,
   plic-laboratorio-portero), es "no_ejecutar".
5. Nunca debes ejecutar acciones reales — solo clasificar y decidir.
```

### Mensaje del usuario (user message)

```json
{
  "texto": "<instrucción recibida>",
  "contexto": "<contexto_del_sistema | null>",
  "estado_del_ciclo": "<estado_actual | null>"
}
```

### Campos del Cerebro Mock que se mapean como input

| Campo del Cerebro Mock | Rol en prompt Haiku |
|---|---|
| `texto` | Instrucción a clasificar — campo principal |
| `contexto` | Contexto adicional del sistema — enriquece la clasificación |
| `estado_del_ciclo` | Estado actual del ciclo — condiciona decisiones de continuidad |

---

## 6. Schema de output esperado de Haiku (propuesto)

Haiku debe devolver un JSON con exactamente los mismos 9 campos del contrato actual del Cerebro Mock:

```json
{
  "intencion": "string",
  "confianza": "alta" | "media" | "baja",
  "riesgo": "bajo" | "medio" | "alto" | "prohibido",
  "decision": "ejecutar" | "continuar_documental" | "pedir_autorizacion" | "no_ejecutar",
  "requiere_ariel": true | false,
  "requiere_torre": true | false,
  "accion": "string" | null,
  "opciones": ["string"] | null,
  "motivo": "string"
}
```

### Contrato de compatibilidad

El output de Haiku debe ser compatible con el mismo contrato de 9 campos que usa el Cerebro Mock hoy. Esto permite:
- Usar el mismo receptor en la Mano Local.
- Reutilizar los mismos tests de contrato (verificando shape, no contenido).
- Intercambiar mock y real sin romper la interfaz.

---

## 7. Cómo se mapea el output hacia la Mano Local

La Mano Local Simulada recibe hoy el output del Cerebro Mock con estos campos clave:

| Campo del output | Uso en Mano Local |
|---|---|
| `decision` | Determina qué acción (si alguna) se ejecuta |
| `accion` | Nombre de la acción a ejecutar (si `decision == "ejecutar"`) |
| `riesgo` | Condiciona el nivel de log y alerta |
| `requiere_ariel` | Si True, bloquea ejecución hasta confirmación |
| `requiere_torre` | Si True, registra en log de Torre antes de ejecutar |
| `motivo` | Texto explicativo para log y para el usuario |

En integración real con Haiku, el mapeo sería idéntico. La Mano Local no necesita saber si la decisión vino del mock o de Haiku real — solo consume el contrato de 9 campos.

---

## 8. Reglas de seguridad obligatorias para el ciclo real

Estas reglas aplican al ciclo futuro de implementación real (PUENTE-5B o posterior):

### R-01 — Validación de output antes de pasar a Mano Local

El output de Haiku DEBE ser validado antes de ser pasado a la Mano Local:
- Verificar que todos los 9 campos están presentes.
- Verificar que `decision` es uno de los 4 valores permitidos.
- Verificar que `riesgo` es uno de los 4 valores permitidos.
- Si el output no es JSON válido → tratar como `no_ejecutar / prohibido`.
- Si falta algún campo → tratar como `no_ejecutar / prohibido`.

### R-02 — Capa de seguridad no delegable

Las siguientes verificaciones NUNCA se delegan a Haiku — se aplican como post-proceso en el sistema PLIC, sin importar qué devuelva Haiku:

| Condición | Acción forzada |
|---|---|
| Output dice `ejecutar` + texto menciona producción | Forzar `no_ejecutar / prohibido` |
| Output dice `ejecutar` + texto menciona secrets | Forzar `no_ejecutar / prohibido` |
| Output dice `ejecutar` + texto menciona repos prohibidos | Forzar `no_ejecutar / prohibido` |
| Output no es JSON parseable | Forzar `no_ejecutar / prohibido` |
| Llamada a Haiku falla (timeout, error HTTP) | Forzar `no_ejecutar / prohibido` |

### R-03 — Haiku no tiene acceso directo a la Mano Local

Haiku solo retorna un JSON de decisión. No ejecuta acciones. No tiene acceso a funciones, archivos, ni subprocess. El PLIC decide si ejecutar en base al output de Haiku, sujeto a R-01 y R-02.

### R-04 — Logging obligatorio

Cada llamada a Haiku real debe generar un log con:
- timestamp;
- input enviado (texto, contexto, estado);
- output recibido;
- si fue aplicada alguna corrección de seguridad (R-02);
- decisión final ejecutada.

---

## 9. Protocolo de keys y secrets

### Dónde viven las keys

| Elemento | Ubicación |
|---|---|
| `ANTHROPIC_API_KEY` | Variable de entorno local — fuera del repo |
| Archivos `.env` | Fuera del repo — en `.gitignore` |
| Cualquier secret | NUNCA en código fuente, NUNCA en archivos del repo |

### Cómo se usan

```python
import os
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise EnvironmentError("ANTHROPIC_API_KEY no está definida")
```

### Qué NO se hace

- No hardcodear keys en código.
- No incluir keys en variables de entorno de CI/CD públicos.
- No loggear la key (ni siquiera parcialmente).
- No pasar la key como argumento de función visible en trazas.

### Rotación y revocación

- Si una key es expuesta accidentamente → revocarla en console.anthropic.com inmediatamente.
- Rotar keys periódicamente o ante cualquier duda.
- Solo Ariel tiene acceso a las keys reales.

---

## 10. Manejo de errores

### Errores de red / HTTP

| Error | Comportamiento |
|---|---|
| Timeout | `no_ejecutar / prohibido` + log |
| HTTP 401 (auth) | `no_ejecutar / prohibido` + log + alerta a Ariel |
| HTTP 429 (rate limit) | `no_ejecutar / prohibido` + log + espera |
| HTTP 5xx (server error) | `no_ejecutar / prohibido` + log + retry con backoff |
| Excepción de red | `no_ejecutar / prohibido` + log |

### Errores de output

| Error | Comportamiento |
|---|---|
| JSON inválido | `no_ejecutar / prohibido` |
| Campo faltante | `no_ejecutar / prohibido` |
| Valor fuera de enum | `no_ejecutar / prohibido` |
| Output vacío | `no_ejecutar / prohibido` |

### Principio de fail-safe

**En caso de cualquier error o ambigüedad → la decisión es siempre la más restrictiva (`no_ejecutar / prohibido`).** El sistema nunca ejecuta ante la duda.

---

## 11. Criterios para avanzar a PUENTE-5B

PUENTE-5B (implementación de cliente Haiku sin API real — cliente fake/local) puede iniciarse cuando:

1. Este contrato (PUENTE-5A) está cerrado en `main` con evidencia.
2. Ariel dio autorización explícita para PUENTE-5B.
3. El alcance de PUENTE-5B es solo el cliente Haiku fake — sin llamadas reales.
4. Sin secrets reales en PUENTE-5B.
5. Sin modificar la Mano Local en PUENTE-5B.
6. Los 173 tests siguen pasando al inicio de PUENTE-5B.

**PUENTE-5B propuesto:** Implementar `cerebro_haiku_fake.py` — un cliente que simula la interfaz de Haiku (mismo input/output que este contrato) pero usando respuestas hardcodeadas o fixtures, sin llamar a ningún endpoint real. Solo para verificar que el contrato es integrable antes de usar la API real.

---

## 12. Riesgos identificados

| Riesgo | Nivel | Mitigación |
|---|---|---|
| Output no determinista de Haiku | Alto | Validación R-01 + capa R-02 |
| Consumo inesperado de tokens | Medio | Rate limiting + monitoreo de uso |
| Exposición accidental de key | Alto | Key fuera del repo + .gitignore + protocolo R-00 |
| Respuesta maliciosa / jailbreak | Alto | Capa R-02 — reglas de seguridad no delegables |
| Latencia / timeout | Medio | Fail-safe → no_ejecutar |
| Cambio de schema del SDK | Bajo | Pinear versión del SDK |
| Costos acumulados en pruebas | Medio | Usar cliente fake (PUENTE-5B) antes de API real |
| Haiku autoriza algo prohibido | Alto | Capa R-02 forzada post-output |

---

## 13. Condiciones de bloqueo para el ciclo real

| Condición de bloqueo | Estado |
|---|---|
| Sin este contrato aprobado | BLOQUEADO |
| Sin autorización explícita de Ariel | BLOQUEADO |
| PUENTE-4Z no está en main | BLOQUEADO |
| Tests < 173/173 | BLOQUEADO |
| Key hardcodeada en código | BLOQUEADO — prohibición absoluta |
| Key en archivo del repo | BLOQUEADO — prohibición absoluta |
| Mano Local modificada antes del contrato | BLOQUEADO |
| Más de un componente real nuevo en el mismo ciclo | BLOQUEADO |
| Producción involucrada | BLOQUEADO — prohibición absoluta |
| Navegador o Playwright incluido | BLOQUEADO — requiere ciclo separado |
| Repos prohibidos tocados | BLOQUEADO — prohibición absoluta |

---

## 14. Qué NO se implementa en PUENTE-5A

| Ítem | Estado |
|---|---|
| Llamada real a `api.anthropic.com` | NO — solo contrato |
| Uso de `ANTHROPIC_API_KEY` real | NO |
| Creación de archivo `.env` | NO |
| Modificación de `cerebro_mock.py` | NO |
| Modificación de `mano_local_simulada.py` | NO |
| Nuevos tests de integración | NO |
| Instalación de dependencias (`anthropic` SDK) | NO |
| Workflows o CI | NO |
| Cliente Haiku fake | NO — eso es PUENTE-5B |
| Producción | NO — prohibición absoluta |
| Navegador / Playwright | NO — prohibición absoluta |
| Repos prohibidos | NO — prohibición absoluta |
