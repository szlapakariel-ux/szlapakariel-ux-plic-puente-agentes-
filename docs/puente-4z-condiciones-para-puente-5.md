# PUENTE-4Z — Condiciones para avanzar a PUENTE-5

## 1. Objetivo de PUENTE-5 (sin implementarlo)

PUENTE-5 es la fase de integración real: conexión con APIs reales (Claude Haiku u otros modelos), uso de navegador real o Playwright real, o ejecución de acciones externas concretas en lugar de simularlas.

**PUENTE-5 NO está implementado aquí.** Este documento solo describe las condiciones mínimas para que pueda iniciarse en el futuro.

El primer microciclo propuesto es **PUENTE-5A — Contrato documental de integración Claude Haiku real**, sin ninguna ejecución real incluida en ese ciclo.

---

## 2. Condiciones mínimas para pensar en PUENTE-5

Antes de iniciar cualquier microciclo de PUENTE-5, deben cumplirse TODAS las siguientes condiciones:

1. PUENTE-4Z está cerrado en `main` con evidencia verificable.
2. Los 173 tests de la fase mock pasan en `main`.
3. Ariel dio autorización explícita para iniciar PUENTE-5.
4. Existe un contrato documental previo aprobado (PUENTE-5A o equivalente).
5. El alcance del primer microciclo de PUENTE-5 está acotado: un solo componente nuevo a la vez.
6. El primer ciclo NO toca producción.
7. El primer ciclo NO usa secrets reales (usa variables de entorno en entorno controlado local, si acaso).
8. No se usa navegador real ni Playwright real hasta que haya un ciclo específico y autorizado para eso.
9. No se conecta API real hasta que haya un contrato específico aprobado.
10. No se crea automatización externa (bots, webhooks, triggers) hasta prueba controlada y documentada.

Si alguna de estas condiciones no se cumple: **BLOQUEADO. No iniciar PUENTE-5.**

---

## 3. Checklist previo obligatorio

### Antes del primer microciclo de PUENTE-5

- [ ] PUENTE-4Z cerrado en `main`.
- [ ] `python -m unittest discover -s tests` → 173/173 OK en `main`.
- [ ] Ariel dio autorización explícita con alcance definido.
- [ ] Contrato documental previo (PUENTE-5A) creado y aprobado.
- [ ] Alcance del primer ciclo es un único componente nuevo.
- [ ] Sin producción en el primer ciclo.
- [ ] Sin secrets reales en el primer ciclo (o protocolo explícito si es necesario).
- [ ] Sin navegador real salvo ciclo específico autorizado.
- [ ] Sin Playwright real salvo ciclo específico autorizado.
- [ ] Sin API real hasta contrato específico aprobado.
- [ ] Sin automatización externa hasta prueba controlada documentada.
- [ ] Sin mezclar Haiku real + navegador + automatización en el mismo ciclo inicial.

---

## 4. Diferencia entre niveles del sistema

### Mock

- Función pura.
- Sin imports externos.
- Sin I/O.
- Sin red.
- Sin subprocess.
- Simula decisiones y payloads sin ejecutarlos.
- **Riesgo: cero** (no puede afectar ningún sistema externo).
- **Estado actual:** COMPLETO en la fase mock (PUENTE-4Z).

### API real

- Llamada HTTP a un endpoint externo (Claude Haiku, Codex, GitHub API, etc.).
- Requiere API key o token.
- Produce efectos reales (tokens consumidos, respuestas reales, posibles efectos secundarios).
- **Riesgo: alto** — requiere contrato específico, protocolo de keys, y ciclo dedicado.
- **Estado:** NO habilitado. Requiere PUENTE-5A + autorización.

### Agente real

- Proceso autónomo que toma decisiones y ejecuta acciones en un loop sin intervención humana continua.
- Puede encadenar múltiples acciones.
- **Riesgo: muy alto** — puede producir efectos acumulativos e irreversibles.
- **Estado:** NO habilitado en ninguna fase actual. Requiere diseño, prueba controlada y protocolo de kill-switch.

### Mano local real

- Ejecuta acciones físicas en el sistema local (crear archivos, ejecutar comandos, hacer commits reales, etc.).
- A diferencia de la mano local simulada, produce efectos reales.
- **Riesgo: alto** — puede modificar el estado del repo o del sistema de archivos.
- **Estado:** NO habilitado. Requiere ciclo específico con protocolo de reversibilidad.

### Navegador real

- Instancia real de Chromium/Firefox controlado por Playwright u otro framework.
- Puede navegar, hacer clic, autenticarse, enviar formularios.
- **Riesgo: alto** — puede autenticarse con credenciales reales y ejecutar acciones irreversibles.
- **Estado:** NO habilitado. Requiere ciclo específico (PUENTE-5+) con entorno aislado.

---

## 5. Reglas para no subir mal de nivel

### No conectar API real sin contrato

Nunca llamar a un endpoint externo (Claude Haiku, GitHub API, cualquier API) sin que exista un contrato documental aprobado que especifique:
- qué endpoint se llama;
- qué payload se envía;
- qué respuesta se espera;
- cómo se manejan errores;
- qué pasa si la respuesta es inesperada.

### No usar keys sin protocolo

Nunca incluir una API key o secret en código, en archivos del repo, o en variables de entorno sin que exista un protocolo explícito de:
- dónde viven las keys (fuera del repo, en entorno local controlado);
- quién tiene acceso;
- cómo se rotan;
- cómo se invalidan en caso de exposición accidental.

### No abrir navegador sin ciclo dedicado

El uso de Playwright real o cualquier navegador controlado requiere un microciclo específico (ej. PUENTE-5C o equivalente) que incluya:
- contrato previo;
- entorno aislado;
- sin autenticación real en el primer ciclo de prueba;
- sin acciones irreversibles.

### No crear workflows sin autorización

Ningún workflow de GitHub Actions, CI/CD, o automatización similar puede crearse sin autorización explícita de Ariel y ciclo específico. Los workflows pueden disparar acciones externas automáticamente y son difíciles de auditar en tiempo real.

### No tocar producción

Prohibición absoluta. Sin excepciones. En ningún microciclo de PUENTE-5 (ni de ninguna fase) se toca producción sin un ciclo completamente separado, auditado, y con reversibilidad documentada.

### No mezclar componentes nuevos en el mismo ciclo inicial

El primer ciclo de PUENTE-5 debe introducir UN solo componente nuevo a la vez:
- Si es Haiku real: solo Haiku, sin navegador, sin automatización.
- Si es navegador: solo navegador, sin Haiku real, sin automatización externa.
- Mezclar en el primer ciclo aumenta el riesgo exponencialmente y dificulta la auditoría.

---

## 6. Propuesta de siguiente microciclo

### PUENTE-5A — Contrato documental de integración Claude Haiku real (sin ejecución)

**Objetivo:** Definir el contrato de integración de Claude Haiku real como primera capacidad real del sistema. Solo documental. Sin ninguna llamada real incluida en este ciclo.

**Alcance:**
- Definir qué input se enviaría a Haiku.
- Definir qué output se esperaría.
- Definir cómo se manejan errores.
- Definir qué campos del Cerebro Mock se pasarían como prompt.
- Definir qué campos de la Mano Local se usarían como receptor.
- Definir el protocolo de keys (dónde viven, cómo se usan en local).
- Definir qué NO se hace en este primer ciclo.

**Restricciones de PUENTE-5A:**
- Solo documental.
- Sin llamadas reales a Haiku.
- Sin uso de keys reales.
- Sin modificar `cerebro_mock.py` ni `mano_local_simulada.py`.
- Sin producción.
- Sin navegador.
- Sin Playwright.
- Sin workflows.

**Condición de inicio:** PUENTE-4Z cerrado en main + autorización explícita de Ariel.

---

## 7. Condiciones de bloqueo

Las siguientes condiciones bloquean automáticamente el inicio de PUENTE-5 o cualquier microciclo dentro de él:

| Condición de bloqueo | Descripción |
|---|---|
| PUENTE-4Z no cerrado en main | La fase mock no está completa — no se avanza |
| Tests < 173/173 | Hay regresiones en la base — no se avanza |
| Sin autorización explícita de Ariel | No hay mandato claro — no se avanza |
| Sin contrato documental previo | Saltar PUENTE-5A está prohibido — no se avanza |
| Ciclo incluye más de un componente real nuevo | Riesgo demasiado alto sin auditoría separada |
| Ciclo incluye producción | Prohibición absoluta |
| Ciclo incluye secrets sin protocolo | Prohibición absoluta |
| Ciclo incluye API real sin contrato | Prohibición — requiere PUENTE-5A primero |
| Ciclo incluye navegador sin autorización | Requiere ciclo dedicado y entorno aislado |
| Ciclo incluye Playwright sin autorización | Requiere ciclo dedicado y entorno aislado |
| Ciclo toca repos prohibidos | torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero — prohibición absoluta |

> Si cualquiera de estas condiciones se activa: **FRENAR. REPORTAR BLOQUEO. NO IMPROVISAR.**
