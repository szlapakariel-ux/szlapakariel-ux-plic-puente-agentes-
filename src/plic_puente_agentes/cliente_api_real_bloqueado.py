_PROVEEDOR = "anthropic_gate"
_MODO = "llamada_real_bloqueada_por_defecto"

_PROMPT_AUTORIZADO = "Respondé exactamente: PLIC_OK"
_AUTORIZACION_VALIDA = "PUENTE-6D-B-SIN-LLAMADA-REAL"
_MODELO_AUTORIZADO = "claude-3-5-haiku-latest"
_TIMEOUT_MAXIMO = 10
_MAX_TOKENS_MAXIMO = 50

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
    modelo="",
    request_id="",
    prompt_validado=False,
    fallback_usado=False,
    evidencia=None,
    proximo_paso_seguro="",
):
    return {
        "ok": ok,
        "proveedor": _PROVEEDOR,
        "modo": _MODO,
        "modelo": modelo,
        "llamada_real_ejecutada": False,
        "llamada_real_bloqueada": True,
        "request_id": request_id,
        "prompt_validado": prompt_validado,
        "error_tipo": error_tipo,
        "fallback_usado": fallback_usado,
        "evidencia": evidencia,
        "bloqueo": bloqueo,
        "motivo": motivo,
        "proximo_paso_seguro": proximo_paso_seguro,
    }


def _bloqueo(error_tipo, motivo, modelo="", request_id=""):
    return _salida(
        ok=False,
        motivo=motivo,
        error_tipo=error_tipo,
        bloqueo=True,
        modelo=modelo,
        request_id=request_id,
        evidencia="no_ejecutado_bloqueo_previo",
    )


def cliente_api_real_bloqueado(entrada):
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

    contrato = entrada.get("contrato_puente_6d_a_confirmado")
    if contrato is not True:
        return _bloqueo(
            error_tipo="contrato_no_confirmado",
            motivo="contrato_puente_6d_a_confirmado debe ser True. El contrato PUENTE-6D-A debe estar cerrado en main antes de usar este gate.",
        )

    dry_run = entrada.get("dry_run")
    if dry_run is not True:
        return _bloqueo(
            error_tipo="dry_run_requerido",
            motivo="dry_run debe ser True. PUENTE-6D-B solo opera en modo dry_run — sin ejecución real.",
        )

    permitir_llamada_real = entrada.get("permitir_llamada_real", False)
    if permitir_llamada_real is True:
        return _bloqueo(
            error_tipo="llamada_real_bloqueada_por_defecto",
            motivo="PUENTE-6D-B no ejecuta llamadas reales aunque permitir_llamada_real venga en True. La primera llamada real requiere PUENTE-6D-C (auditoría técnica) y autorización explícita de Ariel para PUENTE-6D real.",
        )

    autorizacion = entrada.get("autorizacion_ariel", "")
    if autorizacion != _AUTORIZACION_VALIDA:
        return _bloqueo(
            error_tipo="autorizacion_invalida",
            motivo=f"autorizacion_ariel debe ser exactamente '{_AUTORIZACION_VALIDA}'. Valor recibido no coincide.",
        )

    prompt = entrada.get("prompt", "")
    if not isinstance(prompt, str):
        prompt = ""
    if prompt != _PROMPT_AUTORIZADO:
        prompt_lower = prompt.lower().strip()
        for frase in _TERMINOS_SENSIBLES_FRASE:
            if frase in prompt_lower:
                return _bloqueo(
                    error_tipo="entrada_sensible",
                    motivo=f"El prompt contiene un término sensible prohibido: '{frase}'.",
                )
        for termino in _TERMINOS_SENSIBLES_TOKEN:
            if _es_token(prompt_lower, termino):
                return _bloqueo(
                    error_tipo="entrada_sensible",
                    motivo=f"El prompt contiene un término sensible prohibido: '{termino}'.",
                )
        return _bloqueo(
            error_tipo="prompt_no_autorizado",
            motivo=f"El prompt debe ser exactamente '{_PROMPT_AUTORIZADO}'. No se permite ningún otro prompt en PUENTE-6D-B.",
        )

    request_id = entrada.get("request_id", None)
    if not isinstance(request_id, str) or not request_id.strip():
        return _bloqueo(
            error_tipo="request_id_invalido",
            motivo="request_id es obligatorio para trazabilidad. Debe ser un string no vacío.",
        )

    proveedor = entrada.get("proveedor", "")
    if proveedor != "anthropic":
        return _bloqueo(
            error_tipo="proveedor_no_autorizado",
            motivo=f"El proveedor '{proveedor}' no está autorizado. Solo se acepta 'anthropic'.",
            request_id=request_id,
        )

    modelo = entrada.get("modelo", "")
    if modelo != _MODELO_AUTORIZADO:
        return _bloqueo(
            error_tipo="modelo_no_autorizado",
            motivo=f"El modelo '{modelo}' no está autorizado. Solo se acepta '{_MODELO_AUTORIZADO}' en PUENTE-6D-B.",
            modelo=modelo,
            request_id=request_id,
        )

    timeout = entrada.get("timeout", None)
    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout > _TIMEOUT_MAXIMO:
        return _bloqueo(
            error_tipo="timeout_invalido",
            motivo=f"timeout debe ser un número <= {_TIMEOUT_MAXIMO} segundos. Valor recibido: {timeout}.",
            modelo=modelo,
            request_id=request_id,
        )

    max_tokens = entrada.get("max_tokens", None)
    if not isinstance(max_tokens, int) or isinstance(max_tokens, bool) or max_tokens > _MAX_TOKENS_MAXIMO:
        return _bloqueo(
            error_tipo="max_tokens_invalido",
            motivo=f"max_tokens debe ser un entero <= {_MAX_TOKENS_MAXIMO}. Valor recibido: {max_tokens}.",
            modelo=modelo,
            request_id=request_id,
        )

    return _salida(
        ok=True,
        motivo="Gate validado correctamente. La llamada real sigue bloqueada por diseño en PUENTE-6D-B. Requiere PUENTE-6D-C (auditoría técnica) y autorización explícita de Ariel para PUENTE-6D real.",
        error_tipo="",
        bloqueo=False,
        modelo=modelo,
        request_id=request_id,
        prompt_validado=True,
        fallback_usado=False,
        evidencia="gate_validado_sin_ejecucion_real — PUENTE-6D-B — llamada_real_bloqueada_por_diseno",
        proximo_paso_seguro="PUENTE-6D-C auditoría técnica del gate antes de cualquier llamada real",
    )
