# PLIC — Puente de Agentes / Portero Local

## Qué es este repo

`plic-puente-agentes` es un laboratorio aislado para el desarrollo controlado del **Portero Local**, un sistema que actúa como intermediario inteligente entre Ariel (operador humano) y los agentes externos.

## Estado actual

> **PUENTE-0** — Fase documental. Sin código ejecutable. Sin conexiones reales.

## Qué hace este sistema (cuando esté implementado)

El Portero Local es un sistema que:

- Recibe intenciones de acción de agentes externos.
- Aplica las reglas PLIC para clasificar el riesgo.
- Decide si avanzar, frenar o escalar a Ariel para autorización.
- Registra evidencia de cada decisión.
- Reduce el modo "Ariel-cartero" (Ariel ejecutando manualmente tareas repetitivas).

## Lo que este repo NO es

- No es producción.
- No toca repos reales de producción.
- No ejecuta acciones remotas sin autorización explícita.
- No conecta APIs reales en esta fase.
- No usa Playwright real en esta fase.
- No almacena secrets ni tokens.

## Objetivo central

Reducir el modo **Ariel-cartero**: el patrón donde Ariel debe ejecutar personalmente cada acción repetitiva porque no existe un intermediario confiable que pueda decidir cuándo actuar y cuándo frenar.

El Portero Local es ese intermediario.

## Documentación

| Documento | Descripción |
|---|---|
| [docs/arquitectura-portero-local.md](docs/arquitectura-portero-local.md) | Las 4 capas del sistema |
| [docs/reglas-seguridad.md](docs/reglas-seguridad.md) | Prohibiciones y límites operativos |
| [docs/draft-recuperado.md](docs/draft-recuperado.md) | Registro del artefacto recuperado del incidente |
| [docs/microciclos.md](docs/microciclos.md) | Plan de microciclos futuros |

## Microciclo actual

**PUENTE-0 — Arquitectura documental del Portero Local**

No se ejecuta código. No se abren conexiones. Solo se establece la arquitectura conceptual y los límites del sistema.
