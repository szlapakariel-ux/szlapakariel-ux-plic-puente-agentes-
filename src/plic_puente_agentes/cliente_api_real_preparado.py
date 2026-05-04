_PROVEEDOR = "anthropic_preparado"
_MODO = "api_real_preparada_sin_llamada"

_MODELOS_PERMITIDOS = (
    "claude-3-5-haiku-latest",
    "claude-3-haiku-20240307",
)

_TIMEOUT_MAXIMO = 10
_MAX_TOKENS_MAXIMO = 300

_TERMINOS_SENSIBLES_FRASE = (
    "api key",
    "api_key",
    "apikey",
    ".env",
    "contraseña",
    "password",
    "clave",
    "secreto",
    "secrets",
)

_TERMINOS_SENSIBLES_TOKEN = (
    "secret",
    "token",
)


def _es_token(texto, token):
    pos = texto.find(token)
    while pos != -1:
        antes = pos == 0 or not texto[pos - 1].isalpha()
        despues = pos + len(token) >= len(texto) or not texto[pos + len(token)].isalpha()
        if antes and despues:
            return True
        pos = texto.find(token, pos + 1)
    return False


def _salida(
    ok,
    motivo,
    error_tipo,
    bloqueo,
    request_preparado=None,
    response_text="",
    fallback_usado=False,
    tokens_estimados=None,
    costo_estimado="no_calculado_sin_llamada",
    evidencia=None,
    modelo="",
):
    return {
        "ok": ok,
        "proveedor": _PROVEEDOR,
        "modo": _MODO,
        "modelo": modelo,
        "request_preparado": request_preparado,
        "response_text": response_text,
        "error_tipo": error_tipo,
        "fallback_usado": fallback_usado,
        "tokens_estimados": tokens_estimados,
        "costo_estimado": costo_estimado,
        "evidencia": evidencia,
        "bloqueo": bloqueo,
        "motivo": motivo,
    }


def _bloqueo(error_tipo, motivo, modelo=""):
    return _salida(
        ok=False,
        motivo=motivo,
        error_tipo=error_tipo,
        bloqueo=True,
        modelo=modelo,
        evidencia="no_ejecutado_bloqueo_previo",
    )


def cliente_api_real_preparado(entrada):
    if not isinstance(entrada, dict):
        return _bloqueo(
            error_tipo="entrada_invalida",
            motivo="La entrada debe ser un dict con los campos requeridos.",
        )

    modo_seguro = entrada.get("modo_seguro")
    if modo_seguro is not True:
        return _bloqueo(
            error_tipo="modo_seguro_requerido",
            motivo="modo_seguro debe ser True. Sin esta flag ninguna preparación es procesada.",
        )

    permitir_llamada_real = entrada.get("permitir_llamada_real", False)
    if permitir_llamada_real is True:
        return _bloqueo(
            error_tipo="llamada_real_no_autorizada",
            motivo="PUENTE-6B no permite llamadas reales. permitir_llamada_real debe ser False o ausente. La primera llamada real requiere PUENTE-6C y autorización explícita de Ariel.",
        )

    prompt = entrada.get("prompt", "")
    if not isinstance(prompt, str):
        prompt = ""
    prompt_lower = prompt.lower().strip()

    if not prompt_lower:
        return _bloqueo(
            error_tipo="prompt_vacio",
            motivo="prompt está vacío. No hay instrucción que preparar.",
        )

    for frase in _TERMINOS_SENSIBLES_FRASE:
        if frase in prompt_lower:
            return _bloqueo(
                error_tipo="entrada_sensible",
                motivo=f"El prompt contiene un término sensible prohibido: '{frase}'. No se puede preparar una solicitud con datos sensibles.",
            )

    for termino in _TERMINOS_SENSIBLES_TOKEN:
        if _es_token(prompt_lower, termino):
            return _bloqueo(
                error_tipo="entrada_sensible",
                motivo=f"El prompt contiene un término sensible prohibido: '{termino}'. No se puede preparar una solicitud con datos sensibles.",
            )

    proveedor = entrada.get("proveedor", "")
    if proveedor != "anthropic":
        return _bloqueo(
            error_tipo="proveedor_no_autorizado",
            motivo=f"El proveedor '{proveedor}' no está autorizado. Solo se acepta 'anthropic'.",
        )

    modelo = entrada.get("modelo", "")
    if modelo not in _MODELOS_PERMITIDOS:
        return _bloqueo(
            error_tipo="modelo_no_autorizado",
            motivo=f"El modelo '{modelo}' no está en la lista de modelos permitidos: {list(_MODELOS_PERMITIDOS)}.",
            modelo=modelo,
        )

    timeout = entrada.get("timeout", 0)
    if not isinstance(timeout, (int, float)) or timeout > _TIMEOUT_MAXIMO:
        return _bloqueo(
            error_tipo="timeout_excesivo",
            motivo=f"timeout debe ser un número <= {_TIMEOUT_MAXIMO} segundos. Valor recibido: {timeout}.",
            modelo=modelo,
        )

    max_tokens = entrada.get("max_tokens", 0)
    if not isinstance(max_tokens, int) or max_tokens > _MAX_TOKENS_MAXIMO:
        return _bloqueo(
            error_tipo="max_tokens_excesivo",
            motivo=f"max_tokens debe ser un entero <= {_MAX_TOKENS_MAXIMO}. Valor recibido: {max_tokens}.",
            modelo=modelo,
        )

    request_id = entrada.get("request_id", "sin_request_id")
    prompt_resumido = prompt_lower[:50] + "..." if len(prompt_lower) > 50 else prompt_lower

    # Estimación local de tokens: ~4 caracteres por token (sin tokenizer real)
    tokens_estimados = max(1, len(prompt) // 4) + max_tokens

    request_preparado = {
        "proveedor": proveedor,
        "modelo": modelo,
        "prompt_resumido": prompt_resumido,
        "timeout": timeout,
        "max_tokens": max_tokens,
        "request_id": request_id,
    }

    return _salida(
        ok=True,
        motivo="Request preparado correctamente. No se ejecutó ninguna llamada real. Requiere PUENTE-6C y autorización de Ariel para llamada real.",
        error_tipo="",
        bloqueo=False,
        request_preparado=request_preparado,
        response_text="",
        fallback_usado=False,
        tokens_estimados=tokens_estimados,
        costo_estimado="no_calculado_sin_llamada",
        evidencia="preparado_sin_ejecucion_real — PUENTE-6B — llamada_real_no_realizada",
        modelo=modelo,
    )
