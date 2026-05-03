# Contrato de Contexto, Estado y Autorizaciones — Cerebro Portero Mock

## 1. Nombre del contrato

**Contrato de uso de `contexto_actual`, `estado_del_ciclo` y `autorizaciones_disponibles` para el Cerebro Portero Mock**

Versión: 1.0 — PUENTE-3A
Referencia: `docs/contrato-cerebro-mock.md` (PUENTE-1A), `docs/reglas-plic-cerebro-mock.md` (PUENTE-2A)
Implementación objetivo: `src/plic_puente_agentes/cerebro_mock.py`

---

## 2. Objetivo

Definir el significado operativo de los tres campos de contexto del contrato PUENTE-1A que hasta PUENTE-2B eran aceptados por el Cerebro Portero Mock pero no evaluados:

- `contexto_actual` — qué está pasando en el ciclo activo
- `estado_del_ciclo` — en qué fase se encuentra el trabajo
- `autorizaciones_disponibles` — qué acciones están habilitadas explícitamente

Este contrato establece las reglas que el Cerebro Mock deberá seguir al usar estos campos en PUENTE-3B.

---

## 3. Problema que resuelve

Hasta PUENTE-2B, el Cerebro Mock toma decisiones basándose únicamente en `texto_original`. Esto genera dos tipos de decisiones incorrectas:

| Problema | Ejemplo | Decisión actual | Decisión esperada |
|---|---|---|---|
| Falsa continuación | Ariel dice "seguí" pero el ciclo ya está cerrado | `continuar_documental` | `reformular` — no hay ciclo activo |
| Falso bloqueo | Ariel dice "mergealo" con autorización explícita documentada | `pedir_autorizacion` | `continuar_documental` o `pedir_autorizacion` con contexto correcto |
| Cartero involuntario | Ariel dice "1" sin que el Portero haya presentado opciones | `continuar_documental` | `reformular` — no hay opciones previas activas |
| Scope inválido | Ariel dice "diagnóstico SOFSE" estando en un ciclo de otro proyecto | `pedir_autorizacion` | `pedir_autorizacion` con motivo que incluye el contexto del repo activo |

---

## 4. Definición de `contexto_actual`

El campo `contexto_actual` es un dict que describe el estado operativo del sistema en el momento de la consulta. Sus subcampos son:

| Subcampo | Tipo | Descripción |
|---|---|---|
| `proyecto_activo` | string o null | Nombre del proyecto sobre el cual se trabaja actualmente (ej. `"plic-puente-agentes"`) |
| `ultimo_microciclo` | string o null | Identificador del último microciclo iniciado (ej. `"PUENTE-2B"`) |
| `ultimo_pr` | string o null | Número o identificador del último PR abierto (ej. `"#6"`) |
| `ultima_decision` | string o null | Última decisión emitida por el Portero en este ciclo (ej. `"pedir_autorizacion"`) |
| `ultimo_bloqueo` | string o null | Descripción del último bloqueo activo, o null si no hay bloqueo |
| `ultimo_mensaje_ariel` | string o null | Último texto enviado por Ariel antes del actual |
| `ultimo_output_portero` | dict o null | Última respuesta completa del Portero, o null si es la primera interacción |
| `repo_autorizado_actual` | string o null | Repo sobre el cual el Portero tiene autorización en este ciclo (ej. `"szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-"`) |

**Regla de uso:** Si `contexto_actual` no está presente o es null, el Portero debe comportarse como si no hubiera contexto — lo que implica mayor conservadurismo en las decisiones.

---

## 5. Definición de `estado_del_ciclo`

El campo `estado_del_ciclo` es un string que representa la fase actual del microciclo activo. Los valores válidos son:

| Estado | Descripción | Acciones seguras |
|---|---|---|
| `no_iniciado` | Ningún ciclo activo — punto de partida | Documentar, diagnosticar |
| `en_diagnostico` | Se está analizando el estado del sistema | Solo lectura, documentar hallazgos |
| `en_documentacion` | Se está redactando documentación o contrato | Crear/modificar docs, sin código |
| `en_codigo` | Se está modificando código o tests | Modificar src/, modificar tests/ |
| `en_auditoria` | Se está auditando un ciclo anterior | Solo lectura |
| `pr_abierto` | Hay un PR abierto esperando merge | Solo revisar, no crear código nuevo |
| `mergeado` | El PR fue mergeado, ciclo en proceso de cierre | Actualizar documentación de cierre |
| `cerrado` | Ciclo completamente cerrado con evidencia | Ninguna — iniciar nuevo ciclo |
| `bloqueado` | Hay una condición que impide avanzar | Documentar bloqueo, escalar |
| `suspendido` | El ciclo fue pausado por Ariel | Ninguna hasta nueva instrucción |

**Regla de uso:** El Portero debe verificar que la acción solicitada es coherente con el estado del ciclo. Por ejemplo, `"seguí"` con `estado_del_ciclo = "cerrado"` debe derivar en `reformular`, no en `continuar_documental`.

---

## 6. Definición de `autorizaciones_disponibles`

El campo `autorizaciones_disponibles` es una lista de strings que representan las acciones explícitamente autorizadas por Ariel para el ciclo activo. Los valores válidos son:

| Autorización | Descripción |
|---|---|
| `puede_documentar` | Crear o modificar archivos de documentación |
| `puede_diagnosticar` | Leer y analizar el estado del sistema |
| `puede_modificar_codigo` | Modificar `src/` o `tests/` |
| `puede_abrir_pr` | Abrir un PR hacia main |
| `puede_mergear` | Hacer merge de un PR autorizado |
| `puede_comentar_issue` | Agregar comentarios en issues del repo autorizado |
| `puede_cerrar_issue` | Cerrar issues del repo autorizado |
| `puede_usar_api_real` | Usar APIs externas (Claude Haiku, etc.) |
| `puede_usar_navegador` | Usar Playwright o navegador automatizado |
| `puede_tocar_produccion` | Actuar sobre entornos de producción |
| `puede_tocar_secrets` | Leer o escribir secrets o credenciales |

**Regla de uso:** Si `autorizaciones_disponibles` no contiene la autorización requerida para la acción solicitada, la decisión debe ser `pedir_autorizacion`, no `continuar_documental` ni `no_ejecutar`. La diferencia es importante: `no_ejecutar` se reserva para prohibiciones absolutas (secrets, producción); `pedir_autorizacion` se usa cuando la acción sería válida con la autorización correcta.

**Regla especial:** `puede_tocar_produccion` y `puede_tocar_secrets` NUNCA pueden estar en `autorizaciones_disponibles`. Si aparecen, deben ser ignoradas — son prohibiciones absolutas por diseño del sistema.

---

## 7. Regla central

> **El Cerebro Mock no debe decidir solo por `texto_original`. Debe combinar los cuatro campos disponibles.**

El orden de evaluación es:

```
1. Verificar prohibiciones absolutas en texto_original
   (producción, secrets, force push, etc.) → si aplica: no_ejecutar / prohibido

2. Verificar coherencia con estado_del_ciclo
   (¿la acción pedida tiene sentido en este estado?) → si no: reformular o escalar_a_ariel

3. Verificar autorizaciones_disponibles
   (¿la acción está explícitamente autorizada?) → si no: pedir_autorizacion

4. Verificar contexto_actual
   (¿hay contexto suficiente para ejecutar?) → si no: reformular

5. Evaluar texto_original con las reglas PLIC
   → decisión final
```

---

## 8. Casos esperados

### 8.1 Ariel dice "seguí" con ciclo cerrado

| Campo | Valor |
|---|---|
| `texto_original` | `"seguí"` |
| `estado_del_ciclo` | `"cerrado"` |

**Decisión esperada:** `reformular` / `medio`
**Motivo:** No hay ciclo activo. "Seguí" no tiene referente. Torre debe reformular o Ariel debe iniciar nuevo ciclo.
**`requiere_ariel`:** `true`

---

### 8.2 Ariel dice "seguí" con PR abierto

| Campo | Valor |
|---|---|
| `texto_original` | `"seguí"` |
| `estado_del_ciclo` | `"pr_abierto"` |

**Decisión esperada:** `reformular` / `medio`
**Motivo:** Hay un PR abierto esperando merge. "Seguí" es ambiguo — ¿seguir con el merge o con otra cosa? Torre debe clarificar.
**`requiere_ariel`:** `true`
**`requiere_torre`:** `true`

---

### 8.3 Ariel dice "mergealo" con autorización ausente

| Campo | Valor |
|---|---|
| `texto_original` | `"mergealo"` |
| `autorizaciones_disponibles` | `[]` o sin `"puede_mergear"` |

**Decisión esperada:** `pedir_autorizacion` / `alto`
**Motivo:** Merge es acción que requiere autorización explícita. No está en `autorizaciones_disponibles`.
**`requiere_ariel`:** `true`

---

### 8.4 Ariel dice "mergealo" con autorización explícita

| Campo | Valor |
|---|---|
| `texto_original` | `"mergealo"` |
| `autorizaciones_disponibles` | `["puede_mergear", "puede_abrir_pr"]` |
| `estado_del_ciclo` | `"pr_abierto"` |

**Decisión esperada:** `continuar_documental` / `bajo`
**Motivo:** El merge está autorizado y el estado es coherente. Torre confirma antes de ejecutar.
**`requiere_ariel`:** `false`
**`requiere_torre`:** `true`

---

### 8.5 Ariel dice "1" con opciones previas disponibles

| Campo | Valor |
|---|---|
| `texto_original` | `"1"` |
| `contexto_actual.ultimo_output_portero` | Dict con `opciones_para_ariel` no vacío |

**Decisión esperada:** `continuar_documental` / `bajo`
**Motivo:** Hay opciones previas activas y Ariel eligió la primera. Acción clara y segura.
**`requiere_ariel`:** `false`
**`requiere_torre`:** `true`

---

### 8.6 Ariel dice "1" sin opciones previas

| Campo | Valor |
|---|---|
| `texto_original` | `"1"` |
| `contexto_actual.ultimo_output_portero` | null o `opciones_para_ariel: []` |

**Decisión esperada:** `reformular` / `medio`
**Motivo:** El "1" no tiene referente. No hay opciones previas sobre las que responder.
**`requiere_ariel`:** `true`

---

### 8.7 Ariel dice "pasalo a Claude" sin protocolo

| Campo | Valor |
|---|---|
| `texto_original` | `"pasalo a Claude"` |
| `contexto_actual` | null o sin `repo_autorizado_actual` |

**Decisión esperada:** `reformular` / `medio`
**Motivo:** Anti-cartero. Torre debe estructurar qué contexto transferir, a qué agente y en qué formato.
**`requiere_torre`:** `true`

---

### 8.8 Ariel dice "diagnóstico SOFSE" sin repo autorizado

| Campo | Valor |
|---|---|
| `texto_original` | `"diagnóstico SOFSE"` |
| `contexto_actual.repo_autorizado_actual` | `"szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-"` (diferente de SOFSE) |

**Decisión esperada:** `pedir_autorizacion` / `alto`
**Motivo:** SOFSE no es el repo activo. El motivo debe aclarar que se requiere autorización explícita y ciclo específico para SOFSE.
**`requiere_ariel`:** `true`
**`opciones_para_ariel`:** deben incluir opción de autorizar diagnóstico de SOFSE en ciclo separado

---

### 8.9 Ariel dice "suspender" en cualquier estado

| Campo | Valor |
|---|---|
| `texto_original` | `"suspender"` |
| `estado_del_ciclo` | cualquier valor |

**Decisión esperada:** `suspender` / `bajo`
**Motivo:** Suspensión siempre es válida. No requiere contexto ni autorización adicional.
**`requiere_ariel`:** `false`
**`requiere_torre`:** `false`

---

## 9. Reglas de prioridad al combinar campos

| Prioridad | Principio | Consecuencia |
|---|---|---|
| 1 (mayor) | Prohibiciones explícitas ganan siempre | `no_ejecutar` aunque haya autorización |
| 2 | `autorizaciones_disponibles` condiciona la acción | Sin autorización → `pedir_autorizacion` |
| 3 | `estado_del_ciclo` evita saltos de fase | Estado incoherente → `reformular` o `escalar_a_ariel` |
| 4 | `contexto_actual` evita Ariel-cartero | Sin contexto suficiente → `reformular` |
| 5 | `texto_original` nunca alcanza solo para acciones sensibles | Merge, PR, APIs → siempre requieren campos adicionales |

---

## 10. Salidas esperadas

Para cada decisión, la salida del Cerebro Portero Mock debe incluir:

| Campo | Descripción |
|---|---|
| `decision` | Una de las 7 decisiones del contrato PUENTE-1A |
| `riesgo` | `bajo`, `medio`, `alto` o `prohibido` |
| `requiere_ariel` | `true` si se necesita intervención de Ariel |
| `requiere_torre` | `true` si Torre debe reformular o confirmar |
| `accion_segura_sugerida` | Texto descriptivo de la acción segura recomendada |
| `opciones_para_ariel` | Lista de opciones numeradas cuando `requiere_ariel` es `true` |
| `motivo` | Explicación que incluye el campo que condicionó la decisión (no solo el texto) |

**Regla sobre `motivo`:** Cuando la decisión fue condicionada por `contexto_actual`, `estado_del_ciclo` o `autorizaciones_disponibles`, el campo `motivo` debe indicarlo explícitamente. No es suficiente decir "se requiere autorización" — debe aclarar cuál campo determinó el resultado y por qué.

---

## 11. Límites de este contrato

Este contrato define el significado y las reglas de uso de los campos de contexto. No habilita ni implica:

| Acción | Estado |
|---|---|
| Uso de API real | NO habilitado — requiere PUENTE-5 |
| Uso de navegador o Playwright | NO habilitado — requiere PUENTE-4 |
| Acceso a producción | NO habilitado — prohibición absoluta |
| Acceso a secrets | NO habilitado — prohibición absoluta |
| Merge automático sin revisión | NO habilitado — siempre requiere Torre |
| Cierre automático de issues | NO habilitado — requiere autorización explícita |
| Ejecución sin `texto_original` | NO habilitado — campo obligatorio en toda llamada |

---

## 12. Criterios para integración técnica en PUENTE-3B

Para que la integración de estos campos en `cerebro_mock.py` sea correcta, deberá cumplir:

| Criterio | Descripción |
|---|---|
| C-01 | La función sigue siendo pura — ningún campo de contexto implica I/O |
| C-02 | `contexto_actual` es evaluado como dict, con manejo defensivo de campos ausentes |
| C-03 | `estado_del_ciclo` usa un set de valores válidos definido como constante |
| C-04 | `autorizaciones_disponibles` usa un set de valores válidos definido como constante |
| C-05 | La ausencia de cualquier campo de contexto debe producir el comportamiento más conservador posible |
| C-06 | `puede_tocar_produccion` y `puede_tocar_secrets` en `autorizaciones_disponibles` son ignorados |
| C-07 | Cada nueva regla de contexto tiene al menos un test dedicado |
| C-08 | Los 56 tests existentes deben seguir pasando sin modificación |
| C-09 | El campo `motivo` de la respuesta debe referenciar el campo de contexto que condicionó la decisión |
| C-10 | Sin imports nuevos — la función sigue sin dependencias externas |
