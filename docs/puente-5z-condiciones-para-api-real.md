# PUENTE-5Z — Condiciones para una prueba futura con API real

## 1. Objetivo de este documento

Establecer, de forma documental y sin ejecutar ninguna acción real, cuáles son las condiciones mínimas necesarias antes de intentar cualquier integración con la API real de Anthropic (Claude Haiku u otro modelo). Este documento **no habilita ninguna integración real**. Solo define el piso de seguridad requerido para que una futura autorización sea responsable.

---

## 2. Condiciones mínimas antes de cualquier API real

| Condición | Descripción |
|---|---|
| PUENTE-5Z cerrado en `main` | El cierre de fase debe estar mergeado antes de arrancar cualquier ciclo de integración real |
| 262/262 tests OK en `main` | Todos los tests existentes deben pasar sin errores en la rama base |
| Autorización explícita de Ariel | Ningún ciclo de API real puede iniciarse sin instrucción explícita de Ariel en la sesión activa |
| Contrato documental PUENTE-6A aprobado | Debe existir y estar mergeado un documento de contrato que especifique exactamente qué se va a llamar, con qué parámetros, cuántas veces, y qué se espera |
| Alcance único y acotado | Una sola función, un solo endpoint, un solo test — sin generalización |
| Sin producción | Toda prueba real es estrictamente en entorno local o de desarrollo aislado |
| Sin navegador ni Playwright | Ninguna prueba real de API activa navegador, Playwright, ni automatización de interfaz |
| Sin workflows de CI/CD | Las pruebas reales no deben ejecutarse en pipelines automáticos |
| Sin secrets en repo | Ninguna key debe existir en el repositorio, en ningún archivo, en ninguna rama |
| Variable de entorno controlada | La API key solo puede existir como variable de entorno en la sesión local, nunca en código |
| Logs sin keys | Todo log de prueba debe confirmar que no contiene la key en texto plano |
| Fallback al cliente fake | Si la llamada real falla, el sistema debe poder continuar con el cliente fake sin modificar el código base |

---

## 3. Checklist previo obligatorio (en orden)

Antes de iniciar PUENTE-6 (o cualquier ciclo de integración real), se deben verificar **todos** estos ítems:

- [ ] PUENTE-5Z mergeado en `main` con evidencia verificable (commit hash)
- [ ] `python -m unittest discover -s tests` → 262/262 OK en `main`
- [ ] Autorización explícita de Ariel en la sesión activa (instrucción directa, no implícita)
- [ ] Documento `puente-6a-contrato-api-real.md` escrito, revisado y mergeado
- [ ] El contrato especifica: modelo, endpoint, parámetros exactos, respuesta esperada, límite de llamadas
- [ ] Rama de trabajo dedicada (no trabajar directo en `main`)
- [ ] Confirmar que `ANTHROPIC_API_KEY` no está en ningún archivo del repo
- [ ] Confirmar que `.env` no existe en el repo ni en `.gitignore` sin estar ignorado
- [ ] Definir procedimiento de log: qué se registra, qué no
- [ ] Definir procedimiento de rollback: cómo volver al cliente fake si la llamada falla
- [ ] Confirmar que ningún browser, Playwright, subprocess externo será invocado
- [ ] Confirmar que ningún workflow de CI se activará con el push

---

## 4. Diferencias entre los tipos de cliente

| Tipo | Archivo | Llama API | Usa key | Determinista | Tests actuales |
|---|---|---|---|---|---|
| **Cliente fake/local** | `cliente_haiku_fake.py` | NO | NO | SÍ — función pura | 89 |
| **Cliente real (SDK)** | no existe aún | SÍ | SÍ | NO | 0 |
| **Cliente real (HTTP directo)** | no existe aún | SÍ | SÍ | NO | 0 |
| **Agente real completo** | no existe aún | SÍ | SÍ | NO | 0 |
| **Ejecución real** | no existe aún | SÍ + acciones | SÍ | NO | 0 |

### Qué hace el cliente fake que el real NO puede garantizar

| Propiedad | Cliente fake | Cliente real |
|---|---|---|
| Output 100% predecible | SÍ | NO — el modelo puede variar |
| Cero latencia de red | SÍ | NO |
| Cero costo por llamada | SÍ | NO |
| Ejecutable sin credenciales | SÍ | NO |
| Testeable sin mocks de red | SÍ | NO |
| Función pura sin efectos | SÍ | NO |

### Qué puede hacer el cliente real que el fake NO puede

| Capacidad | Cliente fake | Cliente real |
|---|---|---|
| Razonamiento semántico real | NO | SÍ |
| Respuestas a instrucciones arbitrarias | NO — solo las reglas hardcodeadas | SÍ |
| Adaptación al contexto conversacional | NO | SÍ |
| Clasificaciones no previstas en las reglas | NO | SÍ |

---

## 5. Reglas para no escalar prematuramente

| Regla | Descripción |
|---|---|
| R-01 | No se puede escalar a API real sin PUENTE-5Z en `main` |
| R-02 | No se puede escalar sin autorización explícita de Ariel en la sesión activa |
| R-03 | No se puede escalar sin contrato documental previo (PUENTE-6A) |
| R-04 | No se puede reemplazar el Cerebro Mock por Haiku real — son componentes separados con roles distintos |
| R-05 | No se puede usar el cliente fake como evidencia de que el cliente real funciona — son artefactos distintos |
| R-06 | No se puede agregar la API key al repo bajo ningún nombre ni formato |
| R-07 | No se puede ejecutar la prueba real en producción ni en CI/CD |
| R-08 | No se puede escalar a un agente real sin primero probar la función de llamada de forma aislada |
| R-09 | No se puede generalizar: una prueba exitosa de un modelo no autoriza otros modelos ni endpoints |
| R-10 | No se puede considerar la prueba real como cierre de fase — requiere su propio ciclo de auditoría |

---

## 6. Próximo microciclo propuesto: PUENTE-6A

**PUENTE-6A — Contrato documental para prueba mínima de API real, sin ejecución**

### Objetivo

Producir un documento de contrato que especifique, de forma verificable y sin ejecutar ninguna acción real:
- Qué modelo se va a llamar (Claude Haiku 3.5 o el disponible en el momento)
- Qué endpoint exacto (`/v1/messages`)
- Qué parámetros mínimos (system, user, max_tokens)
- Qué respuesta se espera (formato, campos mínimos obligatorios)
- Cuántas llamadas se harán en la prueba (máximo 1 en la primera iteración)
- Cómo se verificará que la respuesta cumple el contrato de 11 campos
- Cómo se hará rollback al cliente fake si la llamada falla

### Alcance

- Solo redacción documental.
- Sin escribir código que llame a la API.
- Sin instalar el SDK de Anthropic.
- Sin crear archivos `.env`.
- Sin agregar keys a ningún archivo.

### Restricciones

- Solo lectura de código existente + redacción de documento.
- Sin API real.
- Sin Claude Haiku real.
- Sin navegador ni Playwright.
- Sin secrets.
- Sin producción.
- Sin workflows.

### Condición de inicio

> No iniciar PUENTE-6A hasta que PUENTE-5Z esté cerrado en `main` con evidencia verificable (commit + push) **y** autorización explícita de Ariel.

---

## 7. Condiciones de bloqueo absoluto

Las siguientes condiciones bloquean cualquier ciclo de integración real, sin excepciones ni workarounds:

| Condición de bloqueo | Nivel |
|---|---|
| No hay autorización explícita de Ariel en la sesión activa | ABSOLUTO |
| PUENTE-5Z no está en `main` | ABSOLUTO |
| Algún test falla en `main` | ABSOLUTO |
| La API key estaría en un archivo del repo | ABSOLUTO |
| La prueba requiere browser, Playwright o subprocess externo | ABSOLUTO |
| La prueba se ejecutaría en producción | ABSOLUTO |
| La prueba se ejecutaría en un workflow de CI/CD automático | ABSOLUTO |
| No existe contrato documental PUENTE-6A mergeado | ABSOLUTO |
| El alcance excede una sola función aislada | ABSOLUTO |
| No hay rollback definido al cliente fake | ABSOLUTO |
