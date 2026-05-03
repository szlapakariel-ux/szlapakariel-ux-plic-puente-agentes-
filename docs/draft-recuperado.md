# Registro del Draft Recuperado

## Contexto del incidente

Durante el desarrollo previo del sistema PLIC, ocurrió el incidente denominado **"import asyncio"**: una pérdida de continuidad que impidió recuperar el desarrollo completo.

Este documento registra el único artefacto confirmado y resguardado de ese incidente.

---

## Artefacto recuperado

**Ruta local:**
```
c:\Users\szlap\OneDrive\Desktop\rescate-import-asyncio\import_asyncio_recuperado.py
```

**Nombre:** `import_asyncio_recuperado.py`

**Estado:** Draft parcial. No es código completo ni ejecutable en su forma actual.

---

## Contenido del artefacto

El archivo recuperado contiene:

- Imports de Python `asyncio`.
- Referencias a **Playwright** para control de navegador.
- Estructura parcial de un flujo de navegación automatizada.
- Placeholders sin implementar (funciones incompletas, valores hardcodeados de prueba).

### Lo que representa

El draft representa **la mano local** del sistema: la capa de Playwright que actuaría como transporte entre agentes, navegando interfaces y ejecutando acciones controladas.

**No representa** el sistema completo. En particular, no incluye:

- El Cerebro Portero (Claude Haiku).
- Las reglas PLIC.
- El registro de evidencia.
- La lógica de decisión (avanzar / frenar / escalar).

---

## Tratamiento autorizado de este artefacto

| Acción | Estado |
|---|---|
| Usar como referencia conceptual | Autorizado |
| Consultar para diseño de Capa 3 (Mano local) | Autorizado (microciclo PUENTE-3 en adelante) |
| Copiar como código ejecutable en este repo | **Prohibido en PUENTE-0** |
| Ejecutar el draft directamente | **Prohibido hasta PUENTE-4** |
| Convertir el draft en script activo | **Prohibido sin microciclo dedicado** |
| Exponer secrets o tokens del draft | **Prohibido absolutamente** |

---

## Nota sobre los placeholders

El draft contiene placeholders intencionales: valores de prueba, URLs ficticias, y funciones sin implementar. Estos placeholders **no deben** ser completados hasta el microciclo correspondiente y con autorización explícita.

---

## Uso futuro

El draft recuperado será utilizado como referencia de diseño en:

- **PUENTE-3** — Mock de mano local sin navegador real.
- **PUENTE-4** — Primer Playwright local controlado con página dummy.

En esas fases, el código del draft será revisado, adaptado y validado antes de cualquier ejecución.

---

## Estado de este registro

Este documento es únicamente un registro de existencia y contexto del artefacto.
No contiene código ejecutable.
No contiene secrets.
No activa ningún proceso.
