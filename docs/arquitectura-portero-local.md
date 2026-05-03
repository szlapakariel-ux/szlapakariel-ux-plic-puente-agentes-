# Arquitectura del Portero Local

## Visión general

El Portero Local es un sistema de 4 capas que actúa como intermediario entre Ariel y los agentes externos. Su función es decidir, no ejecutar ciegamente.

```
┌─────────────────────────────────┐
│  Capa 1 — Cerebro Portero       │  ← Razona y decide
├─────────────────────────────────┤
│  Capa 2 — Reglas PLIC           │  ← Filtra y clasifica riesgo
├─────────────────────────────────┤
│  Capa 3 — Mano local            │  ← Ejecuta solo lo autorizado
├─────────────────────────────────┤
│  Capa 4 — Registro / evidencia  │  ← Registra todo
└─────────────────────────────────┘
```

---

## Capa 1 — Cerebro Portero

**Implementación futura:** Claude Haiku vía API (microciclo PUENTE-5 en adelante).

### Responsabilidades

- Recibir la intención de acción proveniente de un agente externo.
- Interpretar el significado real de la intención (qué quiere hacer, sobre qué, con qué impacto).
- Aplicar las reglas PLIC para clasificar el nivel de riesgo.
- Decidir entre tres caminos:
  - **Avanzar**: la acción está dentro del alcance autorizado, es segura, y puede ejecutarse.
  - **Frenar**: la acción viola una regla PLIC o supera el riesgo aceptable.
  - **Escalar a Ariel**: la acción requiere autorización explícita del operador humano.
- Generar una justificación registrable de su decisión.

### Lo que NO hace el Cerebro

- No ejecuta acciones directamente.
- No almacena secrets ni tokens.
- No toma decisiones irreversibles sin confirmación.
- No ignora las reglas PLIC aunque la intención parezca razonable.

---

## Capa 2 — Reglas PLIC

Las reglas PLIC son el conjunto de restricciones que el Cerebro Portero aplica a toda intención recibida.

### Reglas activas

| Regla | Descripción |
|---|---|
| **Anti-cartero** | El sistema no debe generar trabajo repetitivo para Ariel. Si una acción requiere que Ariel la ejecute manualmente, el sistema debe primero intentar delegarla al Portero o declinarla. |
| **Un microciclo por vez** | Solo se trabaja en un microciclo activo. No se inician nuevas fases sin cerrar la anterior. |
| **Autorización explícita** | Ninguna acción de riesgo medio o alto puede ejecutarse sin confirmación de Ariel. |
| **No producción** | El sistema nunca toca entornos de producción, bases de datos reales ni repos activos externos. |
| **No secrets** | El sistema no almacena, transmite ni expone tokens, cookies, credenciales ni claves de API. |
| **No workflows** | El sistema no crea ni modifica flujos de CI/CD, GitHub Actions ni procesos automatizados externos. |
| **Cierre verificable** | Ninguna acción se considera completada sin evidencia registrada de su resultado. |

### Clasificación de riesgo

| Nivel | Descripción | Acción del Portero |
|---|---|---|
| **Bajo** | Solo lectura, sin efectos externos | Avanza |
| **Medio** | Escritura local, efecto reversible | Avanza con registro |
| **Alto** | Efecto externo o irreversible | Escala a Ariel |
| **Crítico** | Toca producción, secrets o repos reales | Frena siempre |

---

## Capa 3 — Mano local

**Implementación futura:** Playwright local controlado (microciclo PUENTE-4 en adelante).

### Responsabilidades

- Ejecutar en el entorno local del operador las acciones que el Cerebro autorizó.
- Actuar como transporte entre agentes: leer el estado de una interfaz y escribir acciones mínimas necesarias.
- Operar un navegador controlado para interactuar con interfaces que no tienen API disponible.
- Registrar cada acción tomada antes y después de ejecutarla.

### Restricciones

- Nunca ejecuta acciones sensibles (envío de formularios, confirmaciones irreversibles) sin autorización explícita previa.
- Nunca actúa sobre páginas externas a las autorizadas en el microciclo activo.
- Nunca almacena el estado de sesión (cookies, tokens) más allá de la ejecución actual.
- Nunca abre conexiones externas no declaradas.

---

## Capa 4 — Registro / evidencia

### Responsabilidades

- Registrar el estado del sistema antes y después de cada acción.
- Registrar todas las acciones realizadas, con justificación.
- Registrar todas las acciones prohibidas o bloqueadas, con causa.
- Registrar los bloqueos encontrados (errores, violaciones de reglas, fallas de red).
- Proveer un mecanismo de recuperación interna: si el sistema se interrumpe, el registro permite reconstruir el estado.

### Estructura de un registro mínimo

```
timestamp: <ISO 8601>
microciclo: <nombre>
intención: <descripción de lo que se quería hacer>
clasificación_riesgo: <bajo | medio | alto | crítico>
decisión: <avanzar | frenar | escalar>
justificación: <texto>
resultado: <completado | bloqueado | escalado>
```

---

## Flujo de decisión completo

```
Intención recibida
       │
       ▼
Capa 1: ¿Qué quiere hacer?
       │
       ▼
Capa 2: ¿Viola alguna regla PLIC?
    ├── Sí → FRENA + registra
    └── No → ¿Cuál es el nivel de riesgo?
                 ├── Bajo/Medio → Capa 3: Ejecuta + registra
                 ├── Alto → Escala a Ariel + registra
                 └── Crítico → FRENA siempre + registra
```
