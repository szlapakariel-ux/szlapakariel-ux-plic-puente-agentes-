# Reglas de Seguridad — Portero Local

## Estado de este documento

Fase: **PUENTE-0** — Documental.
Sin implementación activa. Sin conexiones reales.

---

## Prohibiciones absolutas

Las siguientes prohibiciones aplican en todos los microciclos, sin excepción.
No existe contexto que las anule.

### Secretos y credenciales

- **No almacenar secrets.** El sistema no guarda tokens, claves de API, contraseñas ni claves privadas en ningún archivo del repo.
- **No transmitir secrets.** El sistema no envía credenciales por ningún canal, incluso si el receptor parece confiable.
- **No leer cookies de sesión.** El sistema no accede a cookies de sesión de navegadores reales.
- **No exponer tokens.** Ningún token de autenticación puede aparecer en logs, commits, ni mensajes de salida.

### Entornos de producción

- **No tocar producción.** El sistema no interactúa con bases de datos, APIs, repos ni servicios que estén en uso real.
- **No hacer deploy.** El sistema no lanza procesos de despliegue ni modifica infraestructura activa.
- **No modificar configuración de producción.** El sistema no toca variables de entorno, DNS, load balancers ni configuraciones de red reales.

### Automatización y workflows

- **No crear workflows.** El sistema no genera archivos `.github/workflows/` ni ningún otro flujo de CI/CD.
- **No modificar workflows existentes.** El sistema no edita flujos de automatización sin autorización explícita y microciclo dedicado.
- **No automatizar sin prueba previa.** Ningún proceso automatizado se activa sin haber sido validado en entorno de prueba.

### Acciones remotas

- **No hacer acciones remotas sin autorización.** El sistema no ejecuta push, merge, deploy, ni ninguna acción que afecte sistemas externos sin confirmación explícita de Ariel.
- **No cerrar issues.** El sistema no cierra issues de GitHub ni de ningún sistema de tickets sin instrucción directa.
- **No mergear pull requests.** El sistema no hace merge de PRs bajo ninguna circunstancia sin autorización explícita.
- **No hacer force push.** Prohibido en todos los contextos.

### APIs y conexiones externas

- **No usar API real sin microciclo separado.** Ninguna llamada a Claude Haiku, Gemini, ni cualquier otra API externa puede ocurrir sin un microciclo específico autorizado para eso.
- **No conectar Claude real.** En las fases de mock, solo se usan respuestas simuladas.
- **No conectar Gemini real.** Igual que con Claude: solo mocks hasta el microciclo correspondiente.
- **No abrir navegador automatizado sin autorización.** Playwright solo se activa en PUENTE-4 o posterior, con página dummy, y con autorización explícita.

---

## Reglas operativas

Estas reglas regulan el comportamiento del sistema durante cada sesión de trabajo.

| Regla | Descripción |
|---|---|
| **Un microciclo activo** | Solo se trabaja en un microciclo a la vez. No se avanza al siguiente sin cierre verificable del actual. |
| **Cierre verificable** | Un microciclo se considera cerrado cuando existe evidencia registrada (commit, log, reporte) de su resultado. |
| **Autorización explícita** | Toda acción de riesgo medio, alto o crítico requiere confirmación de Ariel antes de ejecutarse. |
| **Sin improvisación** | Si el sistema encuentra un estado inesperado, frena y reporta. No improvisa soluciones. |
| **Sin correcciones silenciosas** | Si el sistema detecta un error, lo registra y escala. No lo corrige en silencio. |

---

## Repos prohibidos

El sistema no debe tocar, leer, modificar ni hacer referencia operativa a los siguientes repos:

- `torre-control`
- `agente-saas`
- `auditoria-sofse`
- `plic-laboratorio-portero`

Cualquier intención que involucre estos repos debe ser frenada y reportada a Ariel.

---

## Jerarquía de decisión ante conflicto

Si una regla entra en conflicto con una instrucción recibida, se aplica este orden de precedencia:

1. Prohibiciones absolutas (siempre ganan).
2. Reglas operativas del microciclo activo.
3. Instrucción de Ariel.
4. Lógica del Cerebro Portero.

No existe instrucción que anule una prohibición absoluta.
