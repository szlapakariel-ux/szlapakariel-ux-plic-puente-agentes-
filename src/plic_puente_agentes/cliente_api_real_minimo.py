"""
Cliente real mínimo de Anthropic — PUENTE-6E-B.

NO ejecuta llamadas reales a menos que `permitir_llamada_real=True`
y `ANTHROPIC_API_KEY` esté disponible en el entorno.
Toda llamada real requiere microciclo separado con autorización explícita.
"""

import json
import os

_PROVEEDOR = "anthropic"
_MODO = "api_real_minima"
_MODELO_AUTORIZADO = "claude-haiku-4-5-20251001"
_MAX_TOKENS_MAXIMO = 50
_TIMEOUT_MAXIMO = 10
_API_VERSION = "2023-06-01"
_ENDPOINT = "https://api.anthropic.com/v1/messages"
_BODY_ERROR_LIMITE = 1000
_PATRONES_SECRET = ("sk-ant", "api_key", "authorization", "x-api-key")


def _sanitizar_body_error(raw):
    """Limita y revisa el body del error antes de devolverlo."""
    if not raw:
        return None
    texto = raw if isinstance(raw, str) else raw.decode("utf-8", errors="replace")
    texto_lower = texto.lower()
    for patron in _PATRONES_SECRET:
        if patron in texto_lower:
            return "[body omitido: posible credencial detectada]"
    if len(texto) > _BODY_ERROR_LIMITE:
        texto = texto[:_BODY_ERROR_LIMITE] + "...[truncado]"
    return texto


def _ejecutar_http(api_key, payload_dict, timeout):
    """Ejecuta la llamada HTTP real. Solo se llama cuando está explícitamente autorizado."""
    import urllib.request
    import urllib.error

    body_bytes = json.dumps(payload_dict, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        _ENDPOINT,
        data=body_bytes,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": _API_VERSION,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status_code = resp.status
            response_body = resp.read().decode("utf-8")
        return status_code, response_body, None
    except urllib.error.HTTPError as exc:
        status_code = exc.code
        try:
            raw = exc.read(_BODY_ERROR_LIMITE + 100)
        except Exception:
            raw = b""
        return status_code, None, _sanitizar_body_error(raw)
    except urllib.error.URLError as exc:
        return 0, None, f"error_red: {str(exc.reason)[:200]}"
    except OSError as exc:
        return 0, None, f"timeout_o_red: {str(exc)[:200]}"


def _salida(
    *,
    ok,
    respuesta_texto=None,
    modelo="",
    status_code=0,
    usage=None,
    error_tipo=None,
    body_error_sanitizado=None,
    llamada_real_ejecutada=False,
    cantidad_llamadas=0,
):
    return {
        "ok": ok,
        "respuesta_texto": respuesta_texto,
        "modelo": modelo,
        "status_code": status_code,
        "usage": usage or {
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
        },
        "error_tipo": error_tipo,
        "body_error_sanitizado": body_error_sanitizado,
        "llamada_real_ejecutada": llamada_real_ejecutada,
        "cantidad_llamadas": cantidad_llamadas,
        "secret_expuesto": False,
    }


def cliente_api_real_minimo(entrada, _http_ejecutor=None):
    """
    Cliente real mínimo de Anthropic para PUENTE-6E-B.

    Por defecto bloquea toda llamada real. Para ejecutar una llamada real:
    - `permitir_llamada_real` debe ser `True`
    - `ANTHROPIC_API_KEY` debe estar disponible en el entorno
    - Solo se permite dentro de un microciclo autorizado

    `_http_ejecutor` es un hook de testeo; si se provee, reemplaza la llamada
    HTTP real. En producción nunca se pasa.
    """
    if not isinstance(entrada, dict):
        return _salida(ok=False, error_tipo="entrada_invalida")

    modo_seguro = entrada.get("modo_seguro")
    if modo_seguro is not True:
        return _salida(ok=False, error_tipo="modo_seguro_requerido")

    permitir = entrada.get("permitir_llamada_real")
    if permitir is not False and permitir is not True:
        return _salida(ok=False, error_tipo="permitir_llamada_real_invalido")

    prompt = entrada.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        return _salida(ok=False, error_tipo="prompt_invalido")

    modelo = entrada.get("modelo")
    if modelo != _MODELO_AUTORIZADO:
        return _salida(ok=False, error_tipo="modelo_no_autorizado")

    max_tokens = entrada.get("max_tokens")
    if not isinstance(max_tokens, int) or isinstance(max_tokens, bool):
        return _salida(ok=False, error_tipo="max_tokens_invalido")
    if max_tokens < 1 or max_tokens > _MAX_TOKENS_MAXIMO:
        return _salida(ok=False, error_tipo="max_tokens_fuera_de_rango")

    timeout = entrada.get("timeout", _TIMEOUT_MAXIMO)
    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool):
        return _salida(ok=False, error_tipo="timeout_invalido")
    if timeout <= 0 or timeout > _TIMEOUT_MAXIMO:
        return _salida(ok=False, error_tipo="timeout_fuera_de_rango")

    if not permitir:
        return _salida(ok=False, error_tipo="llamada_real_no_autorizada")

    key_presente = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if not key_presente:
        return _salida(ok=False, error_tipo="anthropic_api_key_ausente")

    api_key = os.environ["ANTHROPIC_API_KEY"]

    payload = {
        "model": _MODELO_AUTORIZADO,
        "max_tokens": max_tokens,
        "temperature": 0.0,
        "messages": [{"role": "user", "content": prompt}],
    }

    ejecutor = _http_ejecutor if _http_ejecutor is not None else _ejecutar_http

    try:
        status_code, response_body, body_error = ejecutor(api_key, payload, timeout)
    except Exception as exc:
        return _salida(
            ok=False,
            error_tipo="error_ejecutor",
            body_error_sanitizado=str(exc)[:200],
            llamada_real_ejecutada=True,
            cantidad_llamadas=1,
        )

    if response_body is None:
        tipo_error = _clasificar_error(status_code, body_error)
        return _salida(
            ok=False,
            error_tipo=tipo_error,
            status_code=status_code,
            body_error_sanitizado=body_error,
            llamada_real_ejecutada=True,
            cantidad_llamadas=1,
        )

    try:
        data = json.loads(response_body)
    except (ValueError, TypeError):
        return _salida(
            ok=False,
            error_tipo="respuesta_inesperada",
            status_code=status_code,
            llamada_real_ejecutada=True,
            cantidad_llamadas=1,
        )

    contenido = data.get("content")
    if not isinstance(contenido, list) or not contenido:
        return _salida(
            ok=False,
            error_tipo="respuesta_inesperada",
            status_code=status_code,
            modelo=data.get("model", ""),
            llamada_real_ejecutada=True,
            cantidad_llamadas=1,
        )

    texto = "".join(
        bloque.get("text", "")
        for bloque in contenido
        if isinstance(bloque, dict) and bloque.get("type") == "text"
    ).strip()

    usage_raw = data.get("usage") or {}
    usage = {
        "input_tokens": usage_raw.get("input_tokens", 0),
        "output_tokens": usage_raw.get("output_tokens", 0),
        "cache_creation_input_tokens": usage_raw.get("cache_creation_input_tokens", 0),
        "cache_read_input_tokens": usage_raw.get("cache_read_input_tokens", 0),
    }

    return _salida(
        ok=True,
        respuesta_texto=texto,
        modelo=data.get("model", ""),
        status_code=status_code,
        usage=usage,
        llamada_real_ejecutada=True,
        cantidad_llamadas=1,
    )


def _clasificar_error(status_code, body_error):
    if status_code == 401:
        return "auth_error"
    if status_code == 400:
        return "bad_request"
    if status_code == 429:
        return "rate_limit"
    if status_code == 503:
        return "servicio_no_disponible"
    if status_code == 0:
        if body_error and "timeout" in str(body_error).lower():
            return "timeout"
        return "error_red"
    return "http_error"
