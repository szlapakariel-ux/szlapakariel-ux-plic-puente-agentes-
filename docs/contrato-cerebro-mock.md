# Contrato del Cerebro Portero Mock

## 1. Nombre del contrato

**Contrato Cerebro Portero Mock — v0.1**

Corresponde al microciclo PUENTE-1A.
Sin implementación activa. Sin conexiones reales. Solo definición de interfaz.

---

## 2. Objetivo del Cerebro Portero Mock

Proveer una versión simulada del Cerebro Portero que:

- Recibe una entrada estructurada con la intención de Ariel y el estado del ciclo.
- Devuelve una decisión estructurada sin llamar a Claude Haiku ni a ninguna API real.
- Permite probar el motor de reglas PLIC y el flujo de decisión de forma local y controlada.
- Sirve como referencia para la implementación real en PUENTE-5.

---

## 3. Qué problema resuelve

Ariel opera en modo "cartero" cuando debe:

- Redactar mensajes largos para cada agente.
- Traducir manualmente instrucciones cortas en acciones específicas.
- Decidir personalmente si una acción es segura antes de ejecutarla.

El Cerebro Portero Mock resuelve esto permitiendo:

- Que Ariel envíe frases cortas o respuestas de una palabra.
- Que el sistema interprete la intención, clasifique el riesgo y proponga la acción segura.
- Que Torre reformule si la intención es ambigua, sin que Ariel deba redactar de nuevo.

---

## 4. Entrada mínima esperada

El Cerebro Portero Mock recibe un objeto con los siguientes campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `texto_original` | string | El mensaje exacto enviado por Ariel, sin modificar. |
| `contexto_actual` | string | Resumen del estado del sistema en el momento del mensaje. |
| `proyecto_detectado` | string \| null | Nombre del proyecto o repo al que aplica la intención, si puede inferirse. |
| `estado_del_ciclo` | string | Microciclo activo en el momento del mensaje (ej. `"PUENTE-1A"`). |
| `riesgo_inicial` | string | Clasificación inicial de riesgo antes del análisis: `"bajo"`, `"medio"`, `"alto"`, `"prohibido"`. |
| `ultima_respuesta_portero` | string \| null | La última decisión registrada por el Portero, para dar continuidad al contexto. |
| `autorizaciones_disponibles` | string[] | Lista de autorizaciones explícitas activas en esta sesión (ej. `["push_a_rama_docs"]`). |

### Ejemplo de entrada

```json
{
  "texto_original": "seguí con lo del celu",
  "contexto_actual": "Estamos en PUENTE-1A, rama docs/puente-1a-contrato-cerebro-mock, sin PR abierto.",
  "proyecto_detectado": null,
  "estado_del_ciclo": "PUENTE-1A",
  "riesgo_inicial": "medio",
  "ultima_respuesta_portero": "continuar_documental",
  "autorizaciones_disponibles": ["commit_documental", "push_rama_docs"]
}
```

---

## 5. Salida mínima esperada

El Cerebro Portero Mock devuelve un objeto con los siguientes campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `intencion_detectada` | string | Descripción breve de lo que el sistema interpretó que Ariel quiere hacer. |
| `confianza` | string | Nivel de certeza de la interpretación: `"alta"`, `"media"`, `"baja"`. |
| `riesgo` | string | Clasificación de riesgo de la acción interpretada: `"bajo"`, `"medio"`, `"alto"`, `"prohibido"`. |
| `decision` | string | La decisión tomada por el Portero (ver sección 6). |
| `requiere_ariel` | boolean | Si la acción requiere confirmación explícita de Ariel antes de ejecutarse. |
| `requiere_torre` | boolean | Si la acción requiere que Torre reformule o estructure antes de continuar. |
| `accion_segura_sugerida` | string \| null | La acción concreta que el sistema propone ejecutar, si la decisión lo permite. |
| `opciones_para_ariel` | string[] | Lista de opciones cortas que Ariel puede elegir con una sola palabra o número. |
| `motivo` | string | Justificación breve de la decisión tomada, registrable en evidencia. |

### Ejemplo de salida

```json
{
  "intencion_detectada": "Continuar con el microciclo activo relacionado con el proyecto de celular o móvil",
  "confianza": "baja",
  "riesgo": "medio",
  "decision": "pedir_autorizacion",
  "requiere_ariel": true,
  "requiere_torre": false,
  "accion_segura_sugerida": null,
  "opciones_para_ariel": [
    "1) Continuar PUENTE-1A (contrato cerebro mock)",
    "2) Aclarar a qué proyecto 'celu' hace referencia",
    "3) Suspender y volver luego"
  ],
  "motivo": "La intención 'seguí con lo del celu' es ambigua. No hay proyecto detectado. Confianza baja. Se requiere aclaración antes de avanzar."
}
```

---

## 6. Decisiones posibles

El campo `decision` puede contener solo uno de estos valores:

| Decisión | Descripción |
|---|---|
| `continuar_documental` | La acción es segura, documental y puede ejecutarse sin confirmación adicional. |
| `pedir_autorizacion` | La acción requiere confirmación explícita de Ariel antes de ejecutarse. |
| `reformular` | La intención es ambigua o incompleta. Torre debe reformularla antes de continuar. |
| `suspender` | La acción debe pausarse hasta un contexto más claro o un nuevo microciclo. |
| `declarar_bloqueo` | El sistema encontró un estado inesperado que impide continuar. Se registra y escala. |
| `escalar_a_ariel` | La acción supera el nivel de riesgo aceptable para el Portero. Solo Ariel puede autorizarla. |
| `no_ejecutar` | La acción viola una regla PLIC o es de riesgo `prohibido`. No se ejecuta bajo ninguna circunstancia. |

---

## 7. Riesgos posibles

| Nivel | Descripción | Ejemplo |
|---|---|---|
| `bajo` | Solo lectura, sin efectos externos, dentro del microciclo activo. | Leer un archivo, crear un documento. |
| `medio` | Escritura local o acción reversible con efecto en el repo. | Commit documental, push a rama de trabajo. |
| `alto` | Efecto externo, irreversible o que involucra sistemas reales. | Abrir PR, hacer merge, llamar API. |
| `prohibido` | Viola una regla PLIC absoluta o afecta producción, secrets o repos prohibidos. | Hacer push a main directamente, usar API key real, tocar torre-control. |

---

## 8. Reglas anti-cartero

El Cerebro Portero Mock debe respetar estas reglas para no generar carga operativa en Ariel:

| Regla | Descripción |
|---|---|
| **Ariel no redacta prompts largos** | El sistema debe poder operar con frases cortas, palabras sueltas o respuestas numéricas de Ariel. |
| **Ariel puede responder con frase corta u opción** | Las `opciones_para_ariel` deben ser elegibles con "1", "2", "3" o una palabra clave. |
| **El Portero estructura** | La responsabilidad de convertir la intención en una acción estructurada es del Portero, no de Ariel. |
| **Torre reformula** | Si la intención es ambigua, Torre recibe la decisión `reformular` y produce un mensaje claro para el ejecutor, sin volver a Ariel. |
| **El ejecutor no recibe texto crudo ambiguo** | Ningún agente ejecutor recibe la frase original de Ariel directamente. Siempre recibe la `accion_segura_sugerida` o la reformulación de Torre. |

---

## 9. Casos de ejemplo

### Caso 1: "seguí con lo del celu"

```json
{
  "texto_original": "seguí con lo del celu",
  "intencion_detectada": "Continuar microciclo activo relacionado con proyecto móvil/celular",
  "confianza": "baja",
  "riesgo": "medio",
  "decision": "pedir_autorizacion",
  "requiere_ariel": true,
  "requiere_torre": false,
  "accion_segura_sugerida": null,
  "opciones_para_ariel": ["1) Continuar PUENTE-1A", "2) Aclarar proyecto", "3) Suspender"],
  "motivo": "Intención ambigua. Proyecto no detectado. Se requiere aclaración."
}
```

### Caso 2: "1"

```json
{
  "texto_original": "1",
  "intencion_detectada": "Selección de opción 1 de la lista anterior presentada por el Portero",
  "confianza": "alta",
  "riesgo": "bajo",
  "decision": "continuar_documental",
  "requiere_ariel": false,
  "requiere_torre": false,
  "accion_segura_sugerida": "Continuar con la acción correspondiente a la opción 1 del contexto previo",
  "opciones_para_ariel": [],
  "motivo": "Respuesta numérica unívoca en contexto de opciones previas. Riesgo bajo. Acción clara."
}
```

### Caso 3: "pasalo a Claude"

```json
{
  "texto_original": "pasalo a Claude",
  "intencion_detectada": "Transferir el contexto o la tarea activa al agente Claude",
  "confianza": "media",
  "riesgo": "medio",
  "decision": "reformular",
  "requiere_ariel": false,
  "requiere_torre": true,
  "accion_segura_sugerida": null,
  "opciones_para_ariel": [],
  "motivo": "La intención es reconocible pero requiere que Torre estructure qué contexto transferir y bajo qué formato, para que el ejecutor no reciba texto ambiguo."
}
```

### Caso 4: "mandalo a producción"

```json
{
  "texto_original": "mandalo a producción",
  "intencion_detectada": "Deploy o push de algún artefacto a entorno de producción",
  "confianza": "alta",
  "riesgo": "prohibido",
  "decision": "no_ejecutar",
  "requiere_ariel": false,
  "requiere_torre": false,
  "accion_segura_sugerida": null,
  "opciones_para_ariel": [],
  "motivo": "Producción es un nivel de riesgo prohibido según reglas PLIC. No se ejecuta bajo ninguna circunstancia en este sistema."
}
```

### Caso 5: "diagnóstico SOFSE"

```json
{
  "texto_original": "diagnóstico SOFSE",
  "intencion_detectada": "Ejecutar o consultar un diagnóstico relacionado con el proyecto SOFSE",
  "confianza": "media",
  "riesgo": "alto",
  "decision": "escalar_a_ariel",
  "requiere_ariel": true,
  "requiere_torre": false,
  "accion_segura_sugerida": null,
  "opciones_para_ariel": [
    "1) Autorizar diagnóstico de solo lectura sobre SOFSE",
    "2) Aclarar alcance del diagnóstico",
    "3) Rechazar — no tocar SOFSE en este ciclo"
  ],
  "motivo": "SOFSE es un proyecto externo con riesgo alto. El diagnóstico puede implicar lectura de datos reales. Se escala a Ariel para autorización explícita."
}
```

---

## 10. Límites del Cerebro Portero Mock

El Cerebro Portero Mock **no puede**:

- Decidir acciones sobre entornos de producción.
- Autorizar el uso de secrets, tokens o credenciales.
- Hacer merge de pull requests.
- Cerrar issues.
- Ejecutar herramientas reales (Playwright, CLI, APIs).
- Llamar a Claude Haiku API real ni a ninguna otra API externa.
- Iniciar un nuevo microciclo sin evidencia de cierre del anterior.
- Ignorar una regla PLIC aunque la intención parezca razonable.
