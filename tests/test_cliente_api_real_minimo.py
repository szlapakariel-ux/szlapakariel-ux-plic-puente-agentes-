"""
Tests para cliente_api_real_minimo — PUENTE-6E-B.

Invariantes verificadas:
- Sin llamada real: 0 requests HTTP reales en toda la suite
- Sin imports de red en nivel de módulo
- secret_expuesto siempre False
- llamada_real_ejecutada solo True cuando se inyecta _http_ejecutor
- cantidad_llamadas siempre 0 o 1
"""

import json
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from plic_puente_agentes.cliente_api_real_minimo import (
    _sanitizar_body_error,
    cliente_api_real_minimo,
)

_MODELO = "claude-haiku-4-5-20251001"

_ENTRADA_BASE = {
    "prompt": "Respondé exactamente: PLIC_OK",
    "modo_seguro": True,
    "modelo": _MODELO,
    "max_tokens": 16,
    "timeout": 5,
    "permitir_llamada_real": False,
}


def _e(**kwargs):
    entrada = dict(_ENTRADA_BASE)
    entrada.update(kwargs)
    return entrada


def _http_ok(api_key, payload, timeout):
    respuesta = {
        "id": "msg_test",
        "type": "message",
        "role": "assistant",
        "model": _MODELO,
        "content": [{"type": "text", "text": "PLIC_OK"}],
        "usage": {
            "input_tokens": 18,
            "output_tokens": 8,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
        },
    }
    return 200, json.dumps(respuesta), None


def _http_401(api_key, payload, timeout):
    return 401, None, '{"type":"error","error":{"type":"authentication_error"}}'


def _http_400(api_key, payload, timeout):
    return 400, None, '{"type":"error","error":{"type":"invalid_request_error","message":"bad field"}}'


def _http_429(api_key, payload, timeout):
    return 429, None, '{"type":"error","error":{"type":"rate_limit_error"}}'


def _http_503(api_key, payload, timeout):
    return 503, None, '{"type":"error","error":{"type":"overloaded_error"}}'


def _http_red_caida(api_key, payload, timeout):
    return 0, None, "error_red: [Errno -2] Name or service not known"


def _http_respuesta_invalida(api_key, payload, timeout):
    return 200, "esto no es json", None


def _http_content_vacio(api_key, payload, timeout):
    respuesta = {
        "id": "msg_test",
        "type": "message",
        "role": "assistant",
        "model": _MODELO,
        "content": [],
        "usage": {"input_tokens": 5, "output_tokens": 0},
    }
    return 200, json.dumps(respuesta), None


def _http_sin_content(api_key, payload, timeout):
    respuesta = {"id": "msg_test", "type": "message", "model": _MODELO}
    return 200, json.dumps(respuesta), None


_ENV_CON_KEY = {"ANTHROPIC_API_KEY": "sk-test-fake-key-para-tests-no-real"}


class TestIdentidad(unittest.TestCase):
    def test_modulo_es_importable(self):
        import plic_puente_agentes.cliente_api_real_minimo as m
        self.assertIsNotNone(m)

    def test_funcion_principal_existe(self):
        self.assertTrue(callable(cliente_api_real_minimo))

    def test_funcion_sanitizar_existe(self):
        self.assertTrue(callable(_sanitizar_body_error))


class TestAislamiento(unittest.TestCase):
    """El módulo no debe importar redes a nivel global."""

    def test_sin_anthropic_sdk(self):
        self.assertNotIn("anthropic", sys.modules)

    def test_sin_requests(self):
        self.assertNotIn("requests", sys.modules)

    def test_sin_urllib_request_en_nivel_modulo(self):
        # urllib.request solo debe aparecer dentro de _ejecutar_http, no al importar
        import plic_puente_agentes.cliente_api_real_minimo as m
        import inspect
        source = inspect.getsource(m)
        # El import de urllib.request debe estar dentro de la función _ejecutar_http
        lines = source.splitlines()
        in_ejecutar_http = False
        for line in lines:
            stripped = line.strip()
            if "def _ejecutar_http" in stripped:
                in_ejecutar_http = True
            elif stripped.startswith("def ") and in_ejecutar_http:
                in_ejecutar_http = False
            if "import urllib" in stripped and not in_ejecutar_http:
                self.fail("urllib importado fuera de _ejecutar_http")

    def test_sin_http_client_en_nivel_modulo(self):
        self.assertNotIn("http.client", sys.modules)


class TestSecretInvariante(unittest.TestCase):
    def _resultado(self, **kwargs):
        with patch.dict("os.environ", _ENV_CON_KEY):
            return cliente_api_real_minimo(
                _e(permitir_llamada_real=True, **kwargs),
                _http_ejecutor=_http_ok,
            )

    def test_secret_expuesto_siempre_false_bloqueo(self):
        res = cliente_api_real_minimo(_e())
        self.assertFalse(res["secret_expuesto"])

    def test_secret_expuesto_siempre_false_exito(self):
        res = self._resultado()
        self.assertFalse(res["secret_expuesto"])

    def test_secret_expuesto_siempre_false_error_401(self):
        with patch.dict("os.environ", _ENV_CON_KEY):
            res = cliente_api_real_minimo(
                _e(permitir_llamada_real=True), _http_ejecutor=_http_401
            )
        self.assertFalse(res["secret_expuesto"])


class TestLlamadaRealInvariante(unittest.TestCase):
    """llamada_real_ejecutada solo True cuando se inyecta ejecutor y autorización."""

    def test_sin_permitir_llamada_real_no_ejecutada(self):
        res = cliente_api_real_minimo(_e(permitir_llamada_real=False))
        self.assertFalse(res["llamada_real_ejecutada"])

    def test_cantidad_llamadas_cero_cuando_bloqueado(self):
        res = cliente_api_real_minimo(_e(permitir_llamada_real=False))
        self.assertEqual(res["cantidad_llamadas"], 0)

    def test_llamada_real_ejecutada_con_ejecutor_ok(self):
        with patch.dict("os.environ", _ENV_CON_KEY):
            res = cliente_api_real_minimo(
                _e(permitir_llamada_real=True), _http_ejecutor=_http_ok
            )
        self.assertTrue(res["llamada_real_ejecutada"])

    def test_cantidad_llamadas_uno_con_ejecutor_ok(self):
        with patch.dict("os.environ", _ENV_CON_KEY):
            res = cliente_api_real_minimo(
                _e(permitir_llamada_real=True), _http_ejecutor=_http_ok
            )
        self.assertEqual(res["cantidad_llamadas"], 1)

    def test_llamada_real_ejecutada_con_ejecutor_error(self):
        with patch.dict("os.environ", _ENV_CON_KEY):
            res = cliente_api_real_minimo(
                _e(permitir_llamada_real=True), _http_ejecutor=_http_401
            )
        self.assertTrue(res["llamada_real_ejecutada"])

    def test_cantidad_llamadas_uno_con_error(self):
        with patch.dict("os.environ", _ENV_CON_KEY):
            res = cliente_api_real_minimo(
                _e(permitir_llamada_real=True), _http_ejecutor=_http_401
            )
        self.assertEqual(res["cantidad_llamadas"], 1)


class TestEntradaInvalida(unittest.TestCase):
    def test_no_dict(self):
        res = cliente_api_real_minimo("texto")
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "entrada_invalida")

    def test_none(self):
        res = cliente_api_real_minimo(None)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "entrada_invalida")

    def test_lista(self):
        res = cliente_api_real_minimo([])
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "entrada_invalida")


class TestModoSeguro(unittest.TestCase):
    def test_modo_seguro_false_rechazado(self):
        res = cliente_api_real_minimo(_e(modo_seguro=False))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "modo_seguro_requerido")

    def test_modo_seguro_none_rechazado(self):
        res = cliente_api_real_minimo(_e(modo_seguro=None))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "modo_seguro_requerido")

    def test_modo_seguro_ausente_rechazado(self):
        entrada = dict(_ENTRADA_BASE)
        del entrada["modo_seguro"]
        res = cliente_api_real_minimo(entrada)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "modo_seguro_requerido")

    def test_modo_seguro_string_rechazado(self):
        res = cliente_api_real_minimo(_e(modo_seguro="true"))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "modo_seguro_requerido")


class TestPermitirLlamadaReal(unittest.TestCase):
    def test_false_bloquea(self):
        res = cliente_api_real_minimo(_e(permitir_llamada_real=False))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "llamada_real_no_autorizada")

    def test_none_invalido(self):
        res = cliente_api_real_minimo(_e(permitir_llamada_real=None))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "permitir_llamada_real_invalido")

    def test_string_invalido(self):
        res = cliente_api_real_minimo(_e(permitir_llamada_real="true"))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "permitir_llamada_real_invalido")

    def test_ausente_invalido(self):
        entrada = dict(_ENTRADA_BASE)
        del entrada["permitir_llamada_real"]
        res = cliente_api_real_minimo(entrada)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "permitir_llamada_real_invalido")


class TestPrompt(unittest.TestCase):
    def test_prompt_vacio_rechazado(self):
        res = cliente_api_real_minimo(_e(prompt=""))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "prompt_invalido")

    def test_prompt_solo_espacios_rechazado(self):
        res = cliente_api_real_minimo(_e(prompt="   "))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "prompt_invalido")

    def test_prompt_none_rechazado(self):
        res = cliente_api_real_minimo(_e(prompt=None))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "prompt_invalido")

    def test_prompt_entero_rechazado(self):
        res = cliente_api_real_minimo(_e(prompt=42))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "prompt_invalido")

    def test_prompt_valido_acepta(self):
        res = cliente_api_real_minimo(_e())
        self.assertNotEqual(res["error_tipo"], "prompt_invalido")


class TestModelo(unittest.TestCase):
    def test_modelo_no_autorizado_rechazado(self):
        res = cliente_api_real_minimo(_e(modelo="claude-3-opus-20240229"))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "modelo_no_autorizado")

    def test_modelo_none_rechazado(self):
        res = cliente_api_real_minimo(_e(modelo=None))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "modelo_no_autorizado")

    def test_modelo_vacio_rechazado(self):
        res = cliente_api_real_minimo(_e(modelo=""))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "modelo_no_autorizado")

    def test_modelo_autorizado_acepta(self):
        res = cliente_api_real_minimo(_e())
        self.assertNotEqual(res["error_tipo"], "modelo_no_autorizado")


class TestMaxTokens(unittest.TestCase):
    def test_max_tokens_cero_rechazado(self):
        res = cliente_api_real_minimo(_e(max_tokens=0))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "max_tokens_fuera_de_rango")

    def test_max_tokens_51_rechazado(self):
        res = cliente_api_real_minimo(_e(max_tokens=51))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "max_tokens_fuera_de_rango")

    def test_max_tokens_negativo_rechazado(self):
        res = cliente_api_real_minimo(_e(max_tokens=-1))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "max_tokens_fuera_de_rango")

    def test_max_tokens_string_rechazado(self):
        res = cliente_api_real_minimo(_e(max_tokens="16"))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "max_tokens_invalido")

    def test_max_tokens_bool_rechazado(self):
        res = cliente_api_real_minimo(_e(max_tokens=True))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "max_tokens_invalido")

    def test_max_tokens_1_acepta(self):
        res = cliente_api_real_minimo(_e(max_tokens=1))
        self.assertNotIn(res["error_tipo"], ("max_tokens_invalido", "max_tokens_fuera_de_rango"))

    def test_max_tokens_50_acepta(self):
        res = cliente_api_real_minimo(_e(max_tokens=50))
        self.assertNotIn(res["error_tipo"], ("max_tokens_invalido", "max_tokens_fuera_de_rango"))


class TestTimeout(unittest.TestCase):
    def test_timeout_cero_rechazado(self):
        res = cliente_api_real_minimo(_e(timeout=0))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "timeout_fuera_de_rango")

    def test_timeout_11_rechazado(self):
        res = cliente_api_real_minimo(_e(timeout=11))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "timeout_fuera_de_rango")

    def test_timeout_negativo_rechazado(self):
        res = cliente_api_real_minimo(_e(timeout=-1))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "timeout_fuera_de_rango")

    def test_timeout_bool_rechazado(self):
        res = cliente_api_real_minimo(_e(timeout=True))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "timeout_invalido")

    def test_timeout_string_rechazado(self):
        res = cliente_api_real_minimo(_e(timeout="5"))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "timeout_invalido")

    def test_timeout_10_acepta(self):
        res = cliente_api_real_minimo(_e(timeout=10))
        self.assertNotIn(res["error_tipo"], ("timeout_invalido", "timeout_fuera_de_rango"))

    def test_timeout_float_acepta(self):
        res = cliente_api_real_minimo(_e(timeout=5.0))
        self.assertNotIn(res["error_tipo"], ("timeout_invalido", "timeout_fuera_de_rango"))


class TestApiKeyAusente(unittest.TestCase):
    def test_sin_key_bloquea(self):
        with patch.dict("os.environ", {}, clear=False):
            os_env_backup = {}
            if "ANTHROPIC_API_KEY" in os.environ:
                os_env_backup["ANTHROPIC_API_KEY"] = os.environ.pop("ANTHROPIC_API_KEY")
            try:
                res = cliente_api_real_minimo(_e(permitir_llamada_real=True))
            finally:
                os.environ.update(os_env_backup)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "anthropic_api_key_ausente")

    def test_key_vacia_bloquea(self):
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": ""}):
            res = cliente_api_real_minimo(_e(permitir_llamada_real=True))
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "anthropic_api_key_ausente")


class TestCasoValido(unittest.TestCase):
    def _ejecutar(self, ejecutor=_http_ok, **kwargs):
        with patch.dict("os.environ", _ENV_CON_KEY):
            return cliente_api_real_minimo(
                _e(permitir_llamada_real=True, **kwargs),
                _http_ejecutor=ejecutor,
            )

    def test_ok_true(self):
        res = self._ejecutar()
        self.assertTrue(res["ok"])

    def test_respuesta_plic_ok(self):
        res = self._ejecutar()
        self.assertEqual(res["respuesta_texto"], "PLIC_OK")

    def test_modelo_devuelto(self):
        res = self._ejecutar()
        self.assertEqual(res["modelo"], _MODELO)

    def test_status_code_200(self):
        res = self._ejecutar()
        self.assertEqual(res["status_code"], 200)

    def test_usage_input_tokens(self):
        res = self._ejecutar()
        self.assertEqual(res["usage"]["input_tokens"], 18)

    def test_usage_output_tokens(self):
        res = self._ejecutar()
        self.assertEqual(res["usage"]["output_tokens"], 8)

    def test_usage_cache_creation(self):
        res = self._ejecutar()
        self.assertEqual(res["usage"]["cache_creation_input_tokens"], 0)

    def test_usage_cache_read(self):
        res = self._ejecutar()
        self.assertEqual(res["usage"]["cache_read_input_tokens"], 0)

    def test_error_tipo_none(self):
        res = self._ejecutar()
        self.assertIsNone(res["error_tipo"])

    def test_body_error_none(self):
        res = self._ejecutar()
        self.assertIsNone(res["body_error_sanitizado"])

    def test_llamada_real_ejecutada_true(self):
        res = self._ejecutar()
        self.assertTrue(res["llamada_real_ejecutada"])

    def test_cantidad_llamadas_uno(self):
        res = self._ejecutar()
        self.assertEqual(res["cantidad_llamadas"], 1)

    def test_secret_expuesto_false(self):
        res = self._ejecutar()
        self.assertFalse(res["secret_expuesto"])


class TestCamposRespuesta(unittest.TestCase):
    """Verifica que todos los campos del contrato PUENTE-6E-A estén presentes."""

    _CAMPOS_REQUERIDOS = [
        "ok",
        "respuesta_texto",
        "modelo",
        "status_code",
        "usage",
        "error_tipo",
        "body_error_sanitizado",
        "llamada_real_ejecutada",
        "cantidad_llamadas",
        "secret_expuesto",
    ]

    _CAMPOS_USAGE = [
        "input_tokens",
        "output_tokens",
        "cache_creation_input_tokens",
        "cache_read_input_tokens",
    ]

    def _resultado_bloqueado(self):
        return cliente_api_real_minimo(_e())

    def _resultado_exitoso(self):
        with patch.dict("os.environ", _ENV_CON_KEY):
            return cliente_api_real_minimo(
                _e(permitir_llamada_real=True), _http_ejecutor=_http_ok
            )

    def test_todos_los_campos_presentes_bloqueado(self):
        res = self._resultado_bloqueado()
        for campo in self._CAMPOS_REQUERIDOS:
            self.assertIn(campo, res, f"Campo faltante: {campo}")

    def test_todos_los_campos_presentes_exitoso(self):
        res = self._resultado_exitoso()
        for campo in self._CAMPOS_REQUERIDOS:
            self.assertIn(campo, res, f"Campo faltante: {campo}")

    def test_usage_tiene_todos_los_subcampos_bloqueado(self):
        res = self._resultado_bloqueado()
        for campo in self._CAMPOS_USAGE:
            self.assertIn(campo, res["usage"], f"Subcampo usage faltante: {campo}")

    def test_usage_tiene_todos_los_subcampos_exitoso(self):
        res = self._resultado_exitoso()
        for campo in self._CAMPOS_USAGE:
            self.assertIn(campo, res["usage"], f"Subcampo usage faltante: {campo}")

    def test_ok_es_bool(self):
        res = self._resultado_exitoso()
        self.assertIsInstance(res["ok"], bool)

    def test_secret_expuesto_es_bool(self):
        res = self._resultado_exitoso()
        self.assertIsInstance(res["secret_expuesto"], bool)

    def test_llamada_real_ejecutada_es_bool(self):
        res = self._resultado_exitoso()
        self.assertIsInstance(res["llamada_real_ejecutada"], bool)

    def test_cantidad_llamadas_es_int(self):
        res = self._resultado_exitoso()
        self.assertIsInstance(res["cantidad_llamadas"], int)


class TestErroresHTTP(unittest.TestCase):
    def _ejecutar(self, ejecutor):
        with patch.dict("os.environ", _ENV_CON_KEY):
            return cliente_api_real_minimo(
                _e(permitir_llamada_real=True), _http_ejecutor=ejecutor
            )

    def test_401_auth_error(self):
        res = self._ejecutar(_http_401)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "auth_error")
        self.assertEqual(res["status_code"], 401)

    def test_401_llamada_ejecutada(self):
        res = self._ejecutar(_http_401)
        self.assertTrue(res["llamada_real_ejecutada"])

    def test_400_bad_request(self):
        res = self._ejecutar(_http_400)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "bad_request")
        self.assertEqual(res["status_code"], 400)

    def test_400_body_capturado(self):
        res = self._ejecutar(_http_400)
        self.assertIsNotNone(res["body_error_sanitizado"])

    def test_429_rate_limit(self):
        res = self._ejecutar(_http_429)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "rate_limit")
        self.assertEqual(res["status_code"], 429)

    def test_503_servicio_no_disponible(self):
        res = self._ejecutar(_http_503)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "servicio_no_disponible")
        self.assertEqual(res["status_code"], 503)

    def test_red_caida_error_red(self):
        res = self._ejecutar(_http_red_caida)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "error_red")

    def test_respuesta_invalida_json(self):
        res = self._ejecutar(_http_respuesta_invalida)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "respuesta_inesperada")

    def test_content_vacio_inesperado(self):
        res = self._ejecutar(_http_content_vacio)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "respuesta_inesperada")

    def test_sin_content_key_inesperado(self):
        res = self._ejecutar(_http_sin_content)
        self.assertFalse(res["ok"])
        self.assertEqual(res["error_tipo"], "respuesta_inesperada")


class TestSanitizarBodyError(unittest.TestCase):
    def test_none_devuelve_none(self):
        self.assertIsNone(_sanitizar_body_error(None))

    def test_vacio_devuelve_none(self):
        self.assertIsNone(_sanitizar_body_error(""))

    def test_texto_normal_devuelto(self):
        result = _sanitizar_body_error('{"error": "invalid_request"}')
        self.assertIn("invalid_request", result)

    def test_truncado_a_1000(self):
        largo = "x" * 1500
        result = _sanitizar_body_error(largo)
        self.assertIn("truncado", result)
        self.assertLessEqual(len(result), 1020)

    def test_patron_sk_ant_omitido(self):
        result = _sanitizar_body_error("sk-ant-api03-xxx-secret")
        self.assertIn("omitido", result)

    def test_patron_api_key_omitido(self):
        result = _sanitizar_body_error('{"api_key": "valor-secreto"}')
        self.assertIn("omitido", result)

    def test_patron_authorization_omitido(self):
        result = _sanitizar_body_error("Authorization: Bearer token123")
        self.assertIn("omitido", result)

    def test_bytes_decodificados(self):
        result = _sanitizar_body_error(b'{"type": "error"}')
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
