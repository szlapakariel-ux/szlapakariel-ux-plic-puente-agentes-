_PROVEEDOR = "haiku_fake"
_MODO = "fake_local_sin_api"

_PALABRAS_PROHIBIDAS = (
    "api real",
    "api key",
    "apikey",
    "api_key",
    "secret",
    "token",
    ".env",
    "produccion",
    "producción",
    "navegador",
    "playwright",
)

_PALABRAS_CONTINUIDAD = ("seguí", "segui", "continuá", "continua", "siguiente")

_PALABRAS_MERGE = ("merge", " pr ", "pull request", "issue")

_PALABRAS_DELEGACION = (
    "pasalo a claude",
    "pasalo a codex",
    "mandalo a otro agente",
)


def _salida(
    decision,
    riesgo,
    requiere_ariel,
    requiere_torre,
    motivo,
    accion_segura_sugerida=None,
    opciones_para_ariel=None,
    bloqueo=False,
    evidencia=None,
):
    return {
        "decision": decision,
        "riesgo": riesgo,
        "requiere_ariel": requiere_ariel,
        "requiere_torre": requiere_torre,
        "motivo": motivo,
        "accion_segura_sugerida": accion_segura_sugerida,
        "opciones_para_ariel": opciones_para_ariel,
        "bloqueo": bloqueo,
        "evidencia": evidencia,
        "proveedor": _PROVEEDOR,
        "modo": _MODO,
    }


def cliente_haiku_fake(entrada):
    if not isinstance(entrada, dict):
        return _salida(
            decision="reformular",
            riesgo="medio",
            requiere_ariel=True,
            requiere_torre=True,
            motivo="La entrada debe ser un dict con los campos requeridos.",
            bloqueo=True,
        )

    modo_seguro = entrada.get("modo_seguro")
    if modo_seguro is not True:
        return _salida(
            decision="no_ejecutar",
            riesgo="prohibido",
            requiere_ariel=True,
            requiere_torre=True,
            motivo="El cliente fake exige modo_seguro=True. Sin esta flag, ninguna instrucción es procesada.",
            bloqueo=True,
        )

    texto = entrada.get("texto_original", "")
    if not isinstance(texto, str):
        texto = ""
    texto_lower = texto.lower().strip()

    if not texto_lower:
        return _salida(
            decision="reformular",
            riesgo="medio",
            requiere_ariel=True,
            requiere_torre=True,
            motivo="texto_original está vacío. No hay instrucción que clasificar.",
            bloqueo=False,
        )

    for palabra in _PALABRAS_PROHIBIDAS:
        if palabra in texto_lower:
            return _salida(
                decision="no_ejecutar",
                riesgo="prohibido",
                requiere_ariel=True,
                requiere_torre=True,
                motivo=f"Instrucción contiene término prohibido: '{palabra}'. Bloqueado por contrato PUENTE-5A.",
                bloqueo=True,
            )

    for palabra in _PALABRAS_CONTINUIDAD:
        if palabra in texto_lower:
            return _salida(
                decision="continuar_documental",
                riesgo="bajo",
                requiere_ariel=False,
                requiere_torre=True,
                motivo="Intención de continuación reconocida. Torre confirma contexto del próximo paso documental antes de ejecutar.",
                bloqueo=False,
            )

    for palabra in _PALABRAS_MERGE:
        if palabra in texto_lower:
            return _salida(
                decision="pedir_autorizacion",
                riesgo="alto",
                requiere_ariel=True,
                requiere_torre=True,
                motivo="Instrucción contiene término que requiere autorización explícita (merge, PR, issue). No se puede ejecutar sin revisión.",
                bloqueo=False,
            )

    for frase in _PALABRAS_DELEGACION:
        if frase in texto_lower:
            return _salida(
                decision="reformular",
                riesgo="medio",
                requiere_ariel=False,
                requiere_torre=True,
                motivo="Instrucción solicita delegación a otro agente. El sistema no delega decisiones sin revisión humana.",
                bloqueo=False,
            )

    return _salida(
        decision="reformular",
        riesgo="medio",
        requiere_ariel=False,
        requiere_torre=True,
        motivo="Instrucción no reconocida por el cliente fake. Torre debe confirmar el contexto antes de avanzar.",
        bloqueo=False,
    )
