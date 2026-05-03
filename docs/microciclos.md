# Microciclos del Portero Local

## Principio de microciclos

Cada microciclo es una unidad mínima de trabajo con:

- **Alcance definido**: qué se hace y qué no se hace.
- **Condición de inicio**: qué debe estar completo antes de empezar.
- **Condición de cierre**: qué evidencia confirma que el microciclo terminó.
- **Prohibiciones específicas**: qué está explícitamente fuera del alcance.

Solo un microciclo puede estar activo a la vez.
Un microciclo no puede cerrarse sin evidencia verificable de su resultado.

---

## Estado actual

| Microciclo | Estado |
|---|---|
| PUENTE-0 | **ACTIVO** |
| PUENTE-1 | Pendiente |
| PUENTE-2 | Pendiente |
| PUENTE-3 | Pendiente |
| PUENTE-4 | Pendiente |
| PUENTE-5 | Pendiente |
| PUENTE-6 | Pendiente |

---

## PUENTE-0 — Arquitectura documental

**Estado:** ACTIVO

**Objetivo:** Establecer la base documental del repo sin implementar código.

**Alcance:**
- Crear README.md.
- Crear docs/arquitectura-portero-local.md.
- Crear docs/reglas-seguridad.md.
- Crear docs/draft-recuperado.md.
- Crear docs/microciclos.md.
- Hacer commit documental.
- Hacer push a rama de trabajo.

**Prohibiciones:**
- No implementar código ejecutable.
- No conectar APIs reales.
- No usar Playwright.
- No abrir PR.
- No hacer merge.

**Condición de cierre:** Commit realizado y push exitoso con los 5 archivos documentales.

---

## PUENTE-1 — Mock del Cerebro Portero

**Estado:** Pendiente (requiere cierre de PUENTE-0)

**Objetivo:** Implementar una versión simulada del Cerebro Portero sin llamadas a Claude Haiku real.

**Alcance previsto:**
- Función que recibe una intención y devuelve una decisión simulada.
- Respuestas hardcodeadas para prueba.
- Tests unitarios mínimos.
- Sin llamadas a API real.

**Prohibiciones:**
- No conectar Claude Haiku API real.
- No implementar Playwright.
- No tocar producción.

---

## PUENTE-2 — Mock de reglas PLIC

**Estado:** Pendiente (requiere cierre de PUENTE-1)

**Objetivo:** Implementar el motor de reglas PLIC como módulo separado, con pruebas.

**Alcance previsto:**
- Módulo de clasificación de riesgo (bajo / medio / alto / crítico).
- Validación de prohibiciones absolutas.
- Tests unitarios para cada regla.
- Sin ejecución de acciones reales.

**Prohibiciones:**
- No conectar APIs reales.
- No implementar Playwright.
- No tocar producción.

---

## PUENTE-3 — Mock de mano local

**Estado:** Pendiente (requiere cierre de PUENTE-2)

**Objetivo:** Definir la interfaz de la Mano Local sin Playwright real, usando stubs.

**Alcance previsto:**
- Interfaz abstracta de la Mano Local.
- Stubs que simulan acciones de navegador (leer página, hacer clic, escribir texto).
- Tests que validan el flujo sin abrir navegador real.
- Revisión del draft recuperado como referencia de diseño.

**Prohibiciones:**
- No abrir navegador real.
- No ejecutar Playwright real.
- No conectar URLs reales.

---

## PUENTE-4 — Primer Playwright local controlado

**Estado:** Pendiente (requiere cierre de PUENTE-3 y autorización explícita)

**Objetivo:** Ejecutar Playwright real sobre una página dummy local, con registro de evidencia.

**Alcance previsto:**
- Página HTML dummy local (sin dependencias externas).
- Script Playwright que navega la página dummy.
- Registro de cada acción tomada.
- Sin acceso a internet.
- Sin credenciales.

**Condición especial:** Requiere autorización explícita de Ariel antes de iniciar.

**Prohibiciones:**
- No navegar páginas externas.
- No usar credenciales.
- No tocar producción.

---

## PUENTE-5 — Integración mínima con Claude Haiku API

**Estado:** Pendiente (requiere cierre de PUENTE-4 y microciclo de secrets separado)

**Objetivo:** Conectar el Cerebro Portero con Claude Haiku API real, en modo solo lectura.

**Alcance previsto:**
- Llamada real a Claude Haiku API.
- Respuesta del Cerebro basada en modelo real.
- Sin acciones externas como resultado de la respuesta.
- Registro de la decisión devuelta.

**Condición especial:** Requiere microciclo previo para configurar secrets de forma segura. Requiere autorización explícita de Ariel.

**Prohibiciones:**
- No ejecutar acciones externas basadas en respuesta del modelo.
- No almacenar la API key en el repo.
- No tocar producción.

---

## PUENTE-6 — Puente controlado con herramienta real, solo lectura

**Estado:** Pendiente (requiere cierre de PUENTE-5 y autorización explícita)

**Objetivo:** Integrar Cerebro + Reglas PLIC + Mano Local en un flujo completo de solo lectura.

**Alcance previsto:**
- El Cerebro recibe una intención real.
- Las reglas PLIC la clasifican.
- La Mano Local ejecuta una acción de solo lectura (leer el estado de una página).
- El registro captura el flujo completo.

**Condición especial:** Requiere autorización explícita de Ariel para cada sesión. Solo lectura. Sin acciones irreversibles.

**Prohibiciones:**
- No ejecutar acciones de escritura.
- No tocar producción.
- No almacenar secrets.
- No abrir PRs ni hacer merges.

---

## Nota sobre microciclos futuros

Los microciclos PUENTE-7 en adelante no están definidos en esta fase.
Serán diseñados cuando PUENTE-6 esté cerrado y con evidencia verificable.
