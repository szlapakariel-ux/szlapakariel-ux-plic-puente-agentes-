# Reglas PLIC — Contrato para el Cerebro Portero Mock

## 1. Nombre del contrato

**Reglas PLIC para el Cerebro Portero Mock**

Versión: 1.0 — PUENTE-2A
Referencia: `docs/contrato-cerebro-mock.md` (PUENTE-1A)
Implementación objetivo: `src/plic_puente_agentes/cerebro_mock.py`

---

## 2. Objetivo

Las reglas PLIC definen el criterio de decisión del Cerebro Portero Mock: qué puede continuar, qué debe pausarse, qué debe reformularse y qué está prohibido bajo cualquier circunstancia.

El Cerebro Portero Mock evalúa la intención recibida, aplica estas reglas en orden de prioridad, y devuelve una decisión estructurada. No ejecuta acciones. No llama APIs. No abre navegador. Solo decide.

---

## 3. Principio central

**Estabilizar → cerrar → medir → subir un nivel.**

Ningún nivel puede saltarse. Ningún ciclo puede cerrarse sin evidencia verificable. Ninguna automatización puede activarse sin prueba previa en modo documental.

---

## 4. Reglas base

Las siguientes reglas son el núcleo del criterio PLIC. Se aplican en todo contexto, con independencia del proyecto o el estado del ciclo activo.

| # | Regla |
|---|---|
| R-01 | Un microciclo por vez — no iniciar el siguiente hasta cerrar el actual |
| R-02 | Un objetivo por ciclo — no agregar alcance durante la ejecución |
| R-03 | No subir de nivel si el nivel actual no está cerrado con evidencia verificable |
| R-04 | No automatizar si la acción no fue probada en modo documental primero |
| R-05 | No sumar agentes al sistema si falta protocolo de coordinación |
| R-06 | No tocar código si falta diagnóstico documental previo |
| R-07 | No tocar producción sin checklist explícito aprobado por Ariel |
| R-08 | No tocar secrets bajo ninguna circunstancia en este ciclo |
| R-09 | No crear workflows sin autorización explícita de Ariel |
| R-10 | No abrir navegador ni usar Playwright sin ciclo específico autorizado |
| R-11 | No usar API real sin ciclo específico autorizado |
| R-12 | No usar Claude Haiku real sin ciclo específico autorizado |
| R-13 | No modificar repos prohibidos: torre-control, agente-saas, auditoria-sofse, plic-laboratorio-portero |
| R-14 | No convertir a Ariel en cartero — el sistema existe para reducir su carga, no para trasladarla |
| R-15 | Si hay ambigüedad en la intención, reformular antes de ejecutar |

---

## 5. Jerarquía de reglas

Cuando dos reglas entran en conflicto, gana la de mayor jerarquía:

| Prioridad | Principio |
|---|---|
| 1 (mayor) | Prohibición explícita gana sobre instrucción general |
| 2 | Seguridad gana sobre velocidad |
| 3 | Cierre verificable gana sobre entusiasmo |
| 4 | Repo autorizado gana sobre conveniencia |
| 5 | Autorización explícita gana sobre inferencia |

**Consecuencia directa:** si una intención menciona una acción prohibida y una acción permitida, la acción prohibida tiene prioridad y la decisión es `no_ejecutar`.

---

## 6. Niveles de riesgo

| Nivel | Significado | Acción por defecto |
|---|---|---|
| `bajo` | Acción documental o de continuación confirmada | Puede continuar |
| `medio` | Intención ambigua o sin contexto suficiente | Reformular antes de continuar |
| `alto` | Acción que afecta sistemas reales o requiere autorización | Pedir autorización explícita |
| `prohibido` | Acción explícitamente vedada por las reglas PLIC | No ejecutar bajo ninguna circunstancia |

---

## 7. Acciones prohibidas por defecto

Las siguientes acciones tienen riesgo `prohibido` y siempre resultan en decisión `no_ejecutar`, independientemente del contexto o de otras instrucciones:

| Acción prohibida | Motivo |
|---|---|
| Producción | Afecta sistemas activos sin red de seguridad |
| Secrets | Exposición de credenciales es irreversible |
| Tokens | Equivalente funcional a secrets |
| Credenciales | Equivalente funcional a secrets |
| Workflows | Automatización no auditada puede escalar sin control |
| Merge a main sin autorización | Afecta la rama base del proyecto |
| Force push | Destruye historial verificable |
| Borrar archivos | Pérdida de evidencia sin posibilidad de auditoría |
| Cerrar issues reales sin autorización | Afecta el estado del proyecto para terceros |
| Comentar issues reales sin autorización | Genera comunicación externa no revisada |
| Usar APIs reales | Efectos secundarios externos fuera del scope del mock |
| Abrir navegador automatizado | Playwright implica ejecución real no controlada |
| Ejecutar Playwright real | Mismo riesgo que navegador automatizado |

---

## 8. Decisiones permitidas

El Cerebro Portero Mock puede emitir exactamente estas decisiones:

| Decisión | Cuándo aplicar |
|---|---|
| `continuar_documental` | La intención es clara, el riesgo es bajo y el ciclo está activo |
| `pedir_autorizacion` | La acción requiere aprobación explícita de Ariel antes de continuar |
| `reformular` | La intención es ambigua, incompleta o no se puede evaluar con certeza |
| `suspender` | Se solicita pausar el ciclo activo de forma explícita |
| `declarar_bloqueo` | El ciclo no puede avanzar por una condición bloqueante no resuelta |
| `escalar_a_ariel` | La decisión supera la capacidad del Portero y debe ser resuelta por Ariel directamente |
| `no_ejecutar` | La acción está prohibida por las reglas PLIC o implica riesgo `prohibido` |

---

## 9. Reglas anti-cartero

El sistema Puente de Agentes existe para que Ariel no sea el intermediario manual entre intenciones y ejecuciones. Las siguientes reglas garantizan eso:

| Regla | Descripción |
|---|---|
| AC-01 | Ariel puede escribir frases cortas o imprecisas — el Portero las estructura |
| AC-02 | Ariel puede responder con opciones numéricas (1, 2, 3) — el Portero interpreta |
| AC-03 | El Portero estructura la intención antes de pasarla a Torre |
| AC-04 | Torre reformula las órdenes ambiguas antes de pasarlas al ejecutor |
| AC-05 | El ejecutor nunca recibe texto crudo de Ariel directamente |
| AC-06 | Si Ariel debe actuar como cartero (copiar/pegar entre agentes), se documenta la causa raíz y se propone mejora |

---

## 10. Casos mínimos y decisión esperada

Los siguientes casos son el conjunto mínimo de entradas que el Cerebro Portero Mock debe evaluar correctamente bajo las reglas PLIC:

| Entrada (`texto_original`) | Riesgo | Decisión | `requiere_ariel` | `requiere_torre` | Motivo resumido |
|---|---|---|---|---|---|
| `"seguí"` | `medio` | `reformular` | `true` | `false` | Intención ambigua sin contexto |
| `"1"` | `bajo` | `continuar_documental` | `false` | `false` | Opción numérica en contexto activo |
| `"pasalo a Claude"` | `medio` | `reformular` | `false` | `true` | Torre debe reformular antes de pasar |
| `"mandalo a producción"` | `prohibido` | `no_ejecutar` | `true` | `false` | Producción es acción prohibida |
| `"usa el token"` | `prohibido` | `no_ejecutar` | `true` | `false` | Token es equivalente a secret |
| `"abrí navegador"` | `prohibido` | `no_ejecutar` | `true` | `false` | Navegador automatizado es acción prohibida |
| `"creá workflow"` | `prohibido` | `no_ejecutar` | `true` | `false` | Workflow sin autorización es acción prohibida |
| `"mergealo"` | `prohibido` | `no_ejecutar` | `true` | `false` | Merge sin autorización explícita es prohibido |
| `"diagnóstico SOFSE"` | `alto` | `pedir_autorizacion` | `true` | `false` | SOFSE es proyecto de riesgo alto |
| `"suspender"` | `bajo` | `suspender` | `false` | `false` | Suspensión explícita del ciclo |

---

## 11. Salida esperada por tipo de caso

Para cada caso, la salida del Cerebro Portero Mock debe incluir los siguientes campos del contrato PUENTE-1A:

| Campo | Tipo | Descripción |
|---|---|---|
| `intencion_detectada` | string | Clasificación de la intención detectada |
| `confianza` | string | Nivel de confianza en la clasificación: `alta`, `media`, `baja` |
| `riesgo` | string | `bajo`, `medio`, `alto`, `prohibido` |
| `decision` | string | Una de las 7 decisiones permitidas |
| `requiere_ariel` | bool | `true` si se necesita intervención de Ariel |
| `requiere_torre` | bool | `true` si Torre debe reformular antes de continuar |
| `accion_segura_sugerida` | string | Texto descriptivo de la acción segura recomendada |
| `opciones_para_ariel` | list | Lista de opciones numeradas si `requiere_ariel` es `true` |
| `motivo` | string | Explicación breve de la decisión tomada |

### Ejemplo: caso `"mandalo a producción"`

```json
{
  "intencion_detectada": "accion_prohibida",
  "confianza": "alta",
  "riesgo": "prohibido",
  "decision": "no_ejecutar",
  "requiere_ariel": true,
  "requiere_torre": false,
  "accion_segura_sugerida": "No ejecutar. Producción está fuera del scope autorizado.",
  "opciones_para_ariel": [
    "1. Confirmar que fue un error y continuar con otro objetivo.",
    "2. Suspender el ciclo activo.",
    "3. Escalar para definir un microciclo de deploy separado."
  ],
  "motivo": "La palabra 'producción' activa bloqueo absoluto según reglas PLIC."
}
```

### Ejemplo: caso `"1"` (opción numérica)

```json
{
  "intencion_detectada": "confirmacion_numerica",
  "confianza": "alta",
  "riesgo": "bajo",
  "decision": "continuar_documental",
  "requiere_ariel": false,
  "requiere_torre": false,
  "accion_segura_sugerida": "Continuar con la opción seleccionada.",
  "opciones_para_ariel": [],
  "motivo": "Opción numérica reconocida. Continuación documental habilitada."
}
```

### Ejemplo: caso `"diagnóstico SOFSE"`

```json
{
  "intencion_detectada": "accion_proyecto_riesgo_alto",
  "confianza": "alta",
  "riesgo": "alto",
  "decision": "pedir_autorizacion",
  "requiere_ariel": true,
  "requiere_torre": false,
  "accion_segura_sugerida": "Pausar y esperar autorización explícita de Ariel antes de continuar.",
  "opciones_para_ariel": [
    "1. Autorizar diagnóstico de SOFSE en modo solo-lectura.",
    "2. Rechazar y continuar con otro objetivo.",
    "3. Escalar para definir microciclo específico de auditoría SOFSE."
  ],
  "motivo": "SOFSE es proyecto de riesgo alto. Requiere autorización explícita antes de cualquier acción."
}
```
