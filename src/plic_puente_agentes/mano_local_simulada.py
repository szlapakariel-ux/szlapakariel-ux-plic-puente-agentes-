"""
Mano Local Simulada — PUENTE-4C-BACKLOG
Transforma decisiones del Cerebro Portero en acciones simuladas.
Sin API real. Sin navegador. Sin I/O. Sin imports.
"""

_PALABRAS_PELIGROSAS = (
    "produccion", "producción", "secret", "secrets",
    "token", "workflow", "navegador", "playwright", "api real",
)
_TOKENS_PELIGROSOS = ("prod",)

_FRASES_PR = (
    "pull request", "pull-request",
    "abrir pr", "comentar pr", "cerrar pr",
)

_DECISIONES_BLOQUEO = ("no_ejecutar", "declarar_bloqueo")

_MAPA_DECISION = {
    "reformular": ("preparar_prompt_reformulado", "torre", "preparado"),
    "continuar_documental": ("preparar_orden_documental", "ejecutor_simulado", "preparado"),
    "declarar_bloqueo": ("registrar_bloqueo", "registro_local", "bloqueado"),
    "suspender": ("suspender_ciclo", "registro_local", "suspendido"),
    "pedir_autorizacion": ("preparar_solicitud_autorizacion", "torre", "pendiente_autorizacion"),
    "no_ejecutar": ("no_accion", "ninguno", "no_ejecutado"),
}

_MAPA_ACCION_SUGERIDA = {
    "claude": ("preparar_prompt_claude", "claude_api"),
    "codex": ("preparar_prompt_codex", "codex_api"),
}


def _es_token(texto_lower, token):
    """Verifica si token aparece como palabra completa en texto_lower."""
    idx = texto_lower.find(token)
    while idx != -1:
        antes = idx == 0 or not texto_lower[idx - 1].isalpha()
        despues = (idx + len(token) == len(texto_lower) or
                   not texto_lower[idx + len(token)].isalpha())
        if antes and despues:
            return True
        idx = texto_lower.find(token, idx + 1)
    return False


def mano_local_simulada(entrada: dict) -> dict:
    texto = ""
    if isinstance(entrada, dict):
        modo_simulado = entrada.get("modo_simulado")
        decision = entrada.get("decision_del_cerebro", "") or ""
        accion_sugerida = entrada.get("accion_segura_sugerida", "") or ""
        contexto = entrada.get("contexto_actual")
        repo = entrada.get("repo_autorizado")
        autorizaciones = entrada.get("autorizaciones_disponibles") or []
        if not isinstance(autorizaciones, list):
            autorizaciones = []
        texto = (str(decision) + " " + str(accion_sugerida)).lower()
    else:
        modo_simulado = None
        decision = ""
        accion_sugerida = ""
        contexto = None
        repo = None
        autorizaciones = []

    decision_lower = decision.lower().strip() if decision else ""
    accion_lower = accion_sugerida.lower().strip() if accion_sugerida else ""

    evidencia_base = {
        "decision_recibida": decision,
        "accion_sugerida": accion_sugerida,
        "repo_autorizado": repo,
        "autorizaciones": autorizaciones,
        "modo_simulado": modo_simulado,
    }

    # Regla 1: modo_simulado debe ser True
    if modo_simulado is not True:
        return {
            "accion_simulada": "ninguna",
            "destino_simulado": "ninguno",
            "payload_simulado": {},
            "resultado_simulado": "bloqueado",
            "requiere_autorizacion": True,
            "bloqueo": True,
            "motivo": "la mano local solo funciona en modo simulado",
            "evidencia": evidencia_base,
        }

    # Regla 9: palabras peligrosas y tokens peligrosos en entrada bloquean
    if (any(p in texto for p in _PALABRAS_PELIGROSAS) or
            any(_es_token(texto, t) for t in _TOKENS_PELIGROSOS)):
        return {
            "accion_simulada": "ninguna",
            "destino_simulado": "ninguno",
            "payload_simulado": {},
            "resultado_simulado": "bloqueado",
            "requiere_autorizacion": True,
            "bloqueo": True,
            "motivo": "entrada contiene terminos restringidos — esto es simulacion, no ejecucion real",
            "evidencia": evidencia_base,
        }

    # Regla 2: no_ejecutar
    if decision_lower == "no_ejecutar":
        return {
            "accion_simulada": "no_accion",
            "destino_simulado": "ninguno",
            "payload_simulado": {},
            "resultado_simulado": "no_ejecutado",
            "requiere_autorizacion": False,
            "bloqueo": True,
            "motivo": "el Cerebro emitio no_ejecutar — la mano local no prepara accion externa",
            "evidencia": evidencia_base,
        }

    # Regla 6: declarar_bloqueo
    if decision_lower == "declarar_bloqueo":
        return {
            "accion_simulada": "registrar_bloqueo",
            "destino_simulado": "registro_local",
            "payload_simulado": {"decision": decision, "contexto": contexto},
            "resultado_simulado": "bloqueado",
            "requiere_autorizacion": False,
            "bloqueo": True,
            "motivo": "el Cerebro emitio declarar_bloqueo — ciclo bloqueado",
            "evidencia": evidencia_base,
        }

    # Regla 3: pedir_autorizacion
    if decision_lower == "pedir_autorizacion":
        return {
            "accion_simulada": "preparar_solicitud_autorizacion",
            "destino_simulado": "torre",
            "payload_simulado": {"decision": decision, "accion_sugerida": accion_sugerida},
            "resultado_simulado": "pendiente_autorizacion",
            "requiere_autorizacion": True,
            "bloqueo": False,
            "motivo": "el Cerebro requiere autorizacion antes de continuar",
            "evidencia": evidencia_base,
        }

    # Regla 7: suspender
    if decision_lower == "suspender":
        return {
            "accion_simulada": "suspender_ciclo",
            "destino_simulado": "registro_local",
            "payload_simulado": {"decision": decision},
            "resultado_simulado": "suspendido",
            "requiere_autorizacion": False,
            "bloqueo": False,
            "motivo": "el Cerebro emitio suspender — ciclo suspendido correctamente",
            "evidencia": evidencia_base,
        }

    # Regla 8: accion_sugerida menciona Claude/Codex/issue/PR
    for clave, (accion, destino) in _MAPA_ACCION_SUGERIDA.items():
        if clave in accion_lower:
            return {
                "accion_simulada": accion,
                "destino_simulado": destino,
                "payload_simulado": {"accion_sugerida": accion_sugerida, "decision": decision},
                "resultado_simulado": "preparado",
                "requiere_autorizacion": False,
                "bloqueo": False,
                "motivo": "payload simulado preparado — sin llamada a API ni accion externa real",
                "evidencia": evidencia_base,
            }

    if any(f in accion_lower for f in _FRASES_PR) or _es_token(accion_lower, "pr"):
        return {
            "accion_simulada": "preparar_comentario_pr",
            "destino_simulado": "github_pr",
            "payload_simulado": {"accion_sugerida": accion_sugerida, "decision": decision},
            "resultado_simulado": "preparado",
            "requiere_autorizacion": False,
            "bloqueo": False,
            "motivo": "payload simulado preparado — sin llamada a API ni accion externa real",
            "evidencia": evidencia_base,
        }

    if _es_token(accion_lower, "issue"):
        return {
            "accion_simulada": "preparar_comentario_issue",
            "destino_simulado": "github_issue",
            "payload_simulado": {"accion_sugerida": accion_sugerida, "decision": decision},
            "resultado_simulado": "preparado",
            "requiere_autorizacion": False,
            "bloqueo": False,
            "motivo": "payload simulado preparado — sin llamada a API ni accion externa real",
            "evidencia": evidencia_base,
        }

    # Regla 4: reformular
    if decision_lower == "reformular":
        return {
            "accion_simulada": "preparar_prompt_reformulado",
            "destino_simulado": "torre",
            "payload_simulado": {"accion_sugerida": accion_sugerida, "decision": decision},
            "resultado_simulado": "preparado",
            "requiere_autorizacion": False,
            "bloqueo": False,
            "motivo": "el Cerebro solicita reformulacion — prompt preparado para Torre",
            "evidencia": evidencia_base,
        }

    # Regla 5: continuar_documental
    if decision_lower == "continuar_documental":
        return {
            "accion_simulada": "preparar_orden_documental",
            "destino_simulado": "ejecutor_simulado",
            "payload_simulado": {"accion_sugerida": accion_sugerida, "decision": decision},
            "resultado_simulado": "preparado",
            "requiere_autorizacion": False,
            "bloqueo": False,
            "motivo": "continuacion documental autorizada — orden preparada para ejecutor simulado",
            "evidencia": evidencia_base,
        }

    # Default: decision desconocida
    return {
        "accion_simulada": "ninguna",
        "destino_simulado": "ninguno",
        "payload_simulado": {},
        "resultado_simulado": "desconocido",
        "requiere_autorizacion": True,
        "bloqueo": True,
        "motivo": "decision del Cerebro no reconocida por la mano local",
        "evidencia": evidencia_base,
    }
