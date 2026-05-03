"""
Cerebro Portero Mock — PUENTE-1B
Decisiones simuladas según contrato de PUENTE-1A.
Sin API real. Sin Claude Haiku. Sin conexiones externas.
"""

_PALABRAS_PROHIBIDAS = ("producción", "produccion")
_PALABRAS_SECRETS = ("secrets", "token", "clave", "credencial")


def cerebro_mock(entrada: dict) -> dict:
    """
    Evalúa una intención de Ariel y devuelve una decisión estructurada.
    Implementación mock con reglas hardcodeadas según contrato PUENTE-1A.
    No llama a ninguna API. No abre conexiones. No ejecuta herramientas.
    """
    texto = entrada.get("texto_original", "")

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

    # Regla 1 — producción: riesgo prohibido
    if any(p in texto_lower for p in _PALABRAS_PROHIBIDAS):
        return _respuesta(
            intencion="Acción sobre entorno de producción",
            confianza="alta",
            riesgo="prohibido",
            decision="no_ejecutar",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[],
            motivo="Producción es riesgo prohibido según reglas PLIC. No se ejecuta bajo ninguna circunstancia.",
        )

    # Regla 2 — secrets / tokens / credenciales: riesgo prohibido
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

    # Regla 3 — "pasalo a Claude"
    if "pasalo a claude" in texto_lower:
        return _respuesta(
            intencion="Transferir contexto o tarea activa al agente Claude",
            confianza="media",
            riesgo="medio",
            decision="reformular",
            requiere_ariel=False,
            requiere_torre=True,
            accion=None,
            opciones=[],
            motivo="La intención es reconocible pero Torre debe estructurar qué contexto transferir y en qué formato antes de que el ejecutor lo reciba.",
        )

    # Regla 4 — "1" (opción numérica)
    if texto.strip() == "1":
        return _respuesta(
            intencion="Selección de opción 1 de la lista anterior del Portero",
            confianza="alta",
            riesgo="bajo",
            decision="continuar_documental",
            requiere_ariel=False,
            requiere_torre=True,
            accion="Continuar con la acción correspondiente a la opción 1 del contexto previo",
            opciones=[],
            motivo="Respuesta numérica unívoca en contexto de opciones previas. Riesgo bajo. Acción clara.",
        )

    # Regla 5 — "seguí con lo del celu"
    if "seguí con lo del celu" in texto_lower or "segui con lo del celu" in texto_lower:
        return _respuesta(
            intencion="Continuar microciclo activo relacionado con proyecto móvil/celular",
            confianza="media",
            riesgo="bajo",
            decision="continuar_documental",
            requiere_ariel=False,
            requiere_torre=True,
            accion="Retomar el microciclo activo vinculado al proyecto de celular según contexto previo",
            opciones=[],
            motivo="Intención de continuación reconocida. Riesgo bajo. Torre confirma contexto antes de ejecutar.",
        )

    # Regla 6 — SOFSE
    if "sofse" in texto_lower:
        return _respuesta(
            intencion="Diagnóstico o acción sobre el proyecto SOFSE",
            confianza="media",
            riesgo="alto",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Autorizar diagnóstico de solo lectura sobre SOFSE",
                "2) Aclarar alcance del diagnóstico",
                "3) Rechazar — no tocar SOFSE en este ciclo",
            ],
            motivo="SOFSE es un proyecto externo real con riesgo alto. Cualquier acción sobre él requiere autorización explícita de Ariel antes de continuar.",
        )

    # Regla 7 — suspender
    if "suspender" in texto_lower:
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

    # Regla 9 — default
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
