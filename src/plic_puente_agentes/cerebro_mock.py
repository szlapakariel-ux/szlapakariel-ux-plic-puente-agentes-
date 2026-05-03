"""
Cerebro Portero Mock — PUENTE-2B
Decisiones simuladas según reglas PLIC documentadas en PUENTE-2A.
Sin API real. Sin Claude Haiku. Sin conexiones externas.
"""

_PALABRAS_SECRETS = ("secret", "secrets", "token", "clave", "credencial", "contraseña", "password", "api key")
_PALABRAS_PRODUCCION = ("producción", "produccion", "prod", "deploy", "publicar")
_PALABRAS_BORRAR = ("borrar", "eliminar", "force push", "reset hard")
_PALABRAS_WORKFLOW = ("workflow", "github actions", "ci", "action")
_PALABRAS_NAVEGADOR = ("navegador", "playwright", "browser", "chromium")
_PALABRAS_MERGE = ("merge", "mergealo", "cerrar pr", "aprobar pr")
_PALABRAS_REPOS_REALES = ("sofse", "auditoria-sofse", "agente-saas", "torre-control")
_PALABRAS_SUSPENSION = ("suspender", "frenar", "parar")
_PALABRAS_ANTICARTERO = ("pasalo a claude", "pasalo a codex", "mandalo a otro agente")
_PALABRAS_CONTINUIDAD = ("seguí", "seguir", "continuá", "seguimos")


def cerebro_mock(entrada: dict) -> dict:
    texto = entrada.get("texto_original", "") if isinstance(entrada, dict) else ""

    if not isinstance(texto, str) or not texto.strip():
        return _respuesta(
            intencion="Intención no reconocible — texto vacío o inválido",
            confianza="baja",
            riesgo="medio",
            decision="reformular",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=["1) Reenviar con texto claro", "2) Suspender sesión"],
            motivo="El texto original está vacío o no es una cadena válida. No es posible interpretar la intención.",
        )

    texto_lower = texto.lower()

    # Prioridad 1 — secrets / credenciales: prohibido
    if any(p in texto_lower for p in _PALABRAS_SECRETS):
        return _respuesta(
            intencion="Acceso o manipulación de credenciales o secrets",
            confianza="alta",
            riesgo="prohibido",
            decision="no_ejecutar",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[],
            motivo="Secrets y credenciales son prohibición absoluta según reglas PLIC. No se ejecuta.",
        )

    # Prioridad 2 — producción / deploy: prohibido
    if any(p in texto_lower for p in _PALABRAS_PRODUCCION):
        return _respuesta(
            intencion="Acción sobre entorno de producción o deploy",
            confianza="alta",
            riesgo="prohibido",
            decision="no_ejecutar",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[],
            motivo="Producción y deploy son riesgo prohibido según reglas PLIC. No se ejecuta bajo ninguna circunstancia.",
        )

    # Prioridad 3 — borrar / force push / reset hard: prohibido
    if any(p in texto_lower for p in _PALABRAS_BORRAR):
        return _respuesta(
            intencion="Acción destructiva — borrado, eliminación o reset forzado",
            confianza="alta",
            riesgo="prohibido",
            decision="no_ejecutar",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[],
            motivo="Borrar archivos y force push son prohibición absoluta según reglas PLIC.",
        )

    # Prioridad 4 — workflows / CI: alto
    if any(p in texto_lower for p in _PALABRAS_WORKFLOW):
        return _respuesta(
            intencion="Acción relacionada con workflows o CI/CD",
            confianza="alta",
            riesgo="alto",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Autorizar revisión de workflow en modo solo-lectura",
                "2) Rechazar — sin tocar CI/CD en este ciclo",
                "3) Escalar para definir microciclo específico de workflows",
            ],
            motivo="Workflows y CI/CD requieren autorización explícita de Ariel antes de continuar.",
        )

    # Prioridad 5 — navegador / Playwright: alto
    if any(p in texto_lower for p in _PALABRAS_NAVEGADOR):
        return _respuesta(
            intencion="Acción que requiere navegador o Playwright",
            confianza="alta",
            riesgo="alto",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Autorizar uso de navegador en microciclo específico",
                "2) Rechazar — sin navegador en este ciclo",
            ],
            motivo="Navegador y Playwright requieren ciclo específico autorizado.",
        )

    # Prioridad 6 — merge / PR: alto
    if any(p in texto_lower for p in _PALABRAS_MERGE):
        return _respuesta(
            intencion="Acción de merge o gestión de PR",
            confianza="alta",
            riesgo="alto",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Autorizar merge con revisión previa",
                "2) Rechazar — sin merge en este ciclo",
            ],
            motivo="Merge y PR requieren autorización explícita de Ariel antes de ejecutar.",
        )

    # Prioridad 7 — repos reales: alto
    if any(p in texto_lower for p in _PALABRAS_REPOS_REALES):
        return _respuesta(
            intencion="Acción que involucra repositorio o proyecto real externo",
            confianza="alta",
            riesgo="alto",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Autorizar acción de solo-lectura sobre el proyecto mencionado",
                "2) Rechazar — sin tocar repos externos en este ciclo",
                "3) Escalar para definir microciclo específico",
            ],
            motivo="El texto involucra un repositorio o proyecto real externo. Requiere autorización explícita.",
        )

    # Prioridad 8 — suspensión: bajo
    if any(p in texto_lower for p in _PALABRAS_SUSPENSION):
        return _respuesta(
            intencion="Solicitud de pausa o suspensión del ciclo activo",
            confianza="alta",
            riesgo="bajo",
            decision="suspender",
            requiere_ariel=False,
            requiere_torre=False,
            accion=None,
            opciones=[],
            motivo="Ariel solicitó suspender. Se pausa el ciclo activo hasta nueva instrucción.",
        )

    # Prioridad 9 — anti-cartero: medio
    if any(p in texto_lower for p in _PALABRAS_ANTICARTERO):
        return _respuesta(
            intencion="Transferencia directa a otro agente sin estructuración",
            confianza="media",
            riesgo="medio",
            decision="reformular",
            requiere_ariel=False,
            requiere_torre=True,
            accion=None,
            opciones=[],
            motivo="Torre debe reformular la intención antes de transferir para evitar que Ariel actúe como cartero.",
        )

    # Prioridad 10 — continuidad segura: bajo
    if texto.strip() == "1" or any(p in texto_lower for p in _PALABRAS_CONTINUIDAD):
        return _respuesta(
            intencion="Continuación del ciclo activo",
            confianza="alta",
            riesgo="bajo",
            decision="continuar_documental",
            requiere_ariel=False,
            requiere_torre=True,
            accion="Continuar con el objetivo activo según contexto previo",
            opciones=[],
            motivo="Intención de continuación reconocida. Riesgo bajo. Torre confirma contexto antes de ejecutar.",
        )

    # Prioridad 12 — default: medio
    return _respuesta(
        intencion="Intención no clasificada por las reglas actuales del mock",
        confianza="baja",
        riesgo="medio",
        decision="reformular",
        requiere_ariel=False,
        requiere_torre=True,
        accion=None,
        opciones=[
            "1) Reformular la intención con más detalle",
            "2) Suspender y volver luego",
        ],
        motivo="El texto no coincide con ninguna regla conocida. Torre debe reformular antes de continuar.",
    )


def _respuesta(
    intencion: str,
    confianza: str,
    riesgo: str,
    decision: str,
    requiere_ariel: bool,
    requiere_torre: bool,
    accion,
    opciones: list,
    motivo: str,
) -> dict:
    return {
        "intencion_detectada": intencion,
        "confianza": confianza,
        "riesgo": riesgo,
        "decision": decision,
        "requiere_ariel": requiere_ariel,
        "requiere_torre": requiere_torre,
        "accion_segura_sugerida": accion,
        "opciones_para_ariel": opciones,
        "motivo": motivo,
    }
