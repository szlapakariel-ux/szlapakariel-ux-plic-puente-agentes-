import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from plic_puente_agentes.cliente_api_real_preparado import cliente_api_real_preparado

_ENTRADA_BASE = {
    "prompt": "Clasificá esta instrucción: revisar el documento.",
    "modo_seguro": True,
    "proveedor": "anthropic",
    "modelo": "claude-3-5-haiku-latest",
    "timeout": 10,
    "max_tokens": 64,
    "request_id": "test-request-001",
    "permitir_llamada_real": False,
}


def _e(**kwargs):
    entrada = dict(_ENTRADA_BASE)
    entrada.update(kwargs)
    return entrada


class TestClienteApiRealPreparadoIdentidad(unittest.TestCase):
    def test_proveedor_es_anthropic_preparado(self):
        r = cliente_api_real_preparado(_ENTRADA_BASE)
        self.assertEqual(r["proveedor"], "anthropic_preparado")

    def test_modo_es_api_real_preparada_sin_llamada(self):
        r = cliente_api_real_preparado(_ENTRADA_BASE)
        self.assertEqual(r["modo"], "api_real_preparada_sin_llamada")


class TestClienteApiRealPreparadoEntradaInvalida(unittest.TestCase):
    def test_entrada_no_dict_bloquea(self):
        r = cliente_api_real_preparado("no soy dict")
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_invalida")

    def test_entrada_lista_bloquea(self):
        r = cliente_api_real_preparado([1, 2, 3])
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_invalida")

    def test_entrada_none_bloquea(self):
        r = cliente_api_real_preparado(None)
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_invalida")

    def test_entrada_int_bloquea(self):
        r = cliente_api_real_preparado(42)
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])

    def test_entrada_invalida_proveedor_sigue_siendo_anthropic_preparado(self):
        r = cliente_api_real_preparado("x")
        self.assertEqual(r["proveedor"], "anthropic_preparado")
        self.assertEqual(r["modo"], "api_real_preparada_sin_llamada")


class TestClienteApiRealPreparadoModoSeguro(unittest.TestCase):
    def test_modo_seguro_false_bloquea(self):
        r = cliente_api_real_preparado(_e(modo_seguro=False))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "modo_seguro_requerido")

    def test_modo_seguro_none_bloquea(self):
        r = cliente_api_real_preparado(_e(modo_seguro=None))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "modo_seguro_requerido")

    def test_modo_seguro_entero_bloquea(self):
        r = cliente_api_real_preparado(_e(modo_seguro=1))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "modo_seguro_requerido")

    def test_modo_seguro_string_bloquea(self):
        r = cliente_api_real_preparado(_e(modo_seguro="true"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "modo_seguro_requerido")

    def test_modo_seguro_ausente_bloquea(self):
        entrada = {k: v for k, v in _ENTRADA_BASE.items() if k != "modo_seguro"}
        r = cliente_api_real_preparado(entrada)
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "modo_seguro_requerido")


class TestClienteApiRealPreparadoLlamadaReal(unittest.TestCase):
    def test_permitir_llamada_real_true_bloquea(self):
        r = cliente_api_real_preparado(_e(permitir_llamada_real=True))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "llamada_real_no_autorizada")

    def test_llamada_real_motivo_menciona_puente_6b(self):
        r = cliente_api_real_preparado(_e(permitir_llamada_real=True))
        self.assertIn("PUENTE-6B", r["motivo"])

    def test_llamada_real_motivo_menciona_puente_6c(self):
        r = cliente_api_real_preparado(_e(permitir_llamada_real=True))
        self.assertIn("PUENTE-6C", r["motivo"])

    def test_permitir_llamada_real_false_no_bloquea_por_este_motivo(self):
        r = cliente_api_real_preparado(_e(permitir_llamada_real=False))
        self.assertNotEqual(r["error_tipo"], "llamada_real_no_autorizada")

    def test_permitir_llamada_real_ausente_no_bloquea_por_este_motivo(self):
        entrada = {k: v for k, v in _ENTRADA_BASE.items() if k != "permitir_llamada_real"}
        r = cliente_api_real_preparado(entrada)
        self.assertNotEqual(r["error_tipo"], "llamada_real_no_autorizada")


class TestClienteApiRealPreparadoPrompt(unittest.TestCase):
    def test_prompt_vacio_bloquea(self):
        r = cliente_api_real_preparado(_e(prompt=""))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "prompt_vacio")

    def test_prompt_solo_espacios_bloquea(self):
        r = cliente_api_real_preparado(_e(prompt="   "))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "prompt_vacio")

    def test_prompt_con_secret_bloquea(self):
        r = cliente_api_real_preparado(_e(prompt="usar secret del vault"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_sensible")

    def test_prompt_con_token_bloquea(self):
        r = cliente_api_real_preparado(_e(prompt="usar token de acceso"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_sensible")

    def test_prompt_con_api_key_bloquea(self):
        r = cliente_api_real_preparado(_e(prompt="incluir api key aquí"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_sensible")

    def test_prompt_con_env_bloquea(self):
        r = cliente_api_real_preparado(_e(prompt="leer archivo .env del proyecto"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_sensible")

    def test_prompt_con_clave_bloquea(self):
        r = cliente_api_real_preparado(_e(prompt="obtener la clave del sistema"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_sensible")

    def test_prompt_con_contraseña_bloquea(self):
        r = cliente_api_real_preparado(_e(prompt="cambiar contraseña del usuario"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_sensible")

    # Falsos positivos — no deben bloquear por entrada_sensible
    def test_tokenizacion_no_bloquea(self):
        r = cliente_api_real_preparado(_e(prompt="proceso de tokenización del texto"))
        self.assertNotEqual(r["error_tipo"], "entrada_sensible")

    def test_secretaria_no_bloquea(self):
        r = cliente_api_real_preparado(_e(prompt="contactar a la secretaría"))
        self.assertNotEqual(r["error_tipo"], "entrada_sensible")


class TestClienteApiRealPreparadoProveedor(unittest.TestCase):
    def test_proveedor_no_autorizado_bloquea(self):
        r = cliente_api_real_preparado(_e(proveedor="openai"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "proveedor_no_autorizado")

    def test_proveedor_vacio_bloquea(self):
        r = cliente_api_real_preparado(_e(proveedor=""))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "proveedor_no_autorizado")

    def test_proveedor_anthropic_pasa(self):
        r = cliente_api_real_preparado(_ENTRADA_BASE)
        self.assertNotEqual(r["error_tipo"], "proveedor_no_autorizado")


class TestClienteApiRealPreparadoModelo(unittest.TestCase):
    def test_modelo_no_autorizado_bloquea(self):
        r = cliente_api_real_preparado(_e(modelo="gpt-4"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "modelo_no_autorizado")

    def test_modelo_vacio_bloquea(self):
        r = cliente_api_real_preparado(_e(modelo=""))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "modelo_no_autorizado")

    def test_modelo_haiku_latest_pasa(self):
        r = cliente_api_real_preparado(_e(modelo="claude-3-5-haiku-latest"))
        self.assertNotEqual(r["error_tipo"], "modelo_no_autorizado")

    def test_modelo_haiku_fecha_pasa(self):
        r = cliente_api_real_preparado(_e(modelo="claude-3-haiku-20240307"))
        self.assertNotEqual(r["error_tipo"], "modelo_no_autorizado")


class TestClienteApiRealPreparadoTimeout(unittest.TestCase):
    def test_timeout_excesivo_bloquea(self):
        r = cliente_api_real_preparado(_e(timeout=11))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "timeout_excesivo")

    def test_timeout_justo_en_limite_no_bloquea(self):
        r = cliente_api_real_preparado(_e(timeout=10))
        self.assertNotEqual(r["error_tipo"], "timeout_excesivo")

    def test_timeout_menor_no_bloquea(self):
        r = cliente_api_real_preparado(_e(timeout=5))
        self.assertNotEqual(r["error_tipo"], "timeout_excesivo")


class TestClienteApiRealPreparadoMaxTokens(unittest.TestCase):
    def test_max_tokens_excesivo_bloquea(self):
        r = cliente_api_real_preparado(_e(max_tokens=301))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "max_tokens_excesivo")

    def test_max_tokens_en_limite_no_bloquea(self):
        r = cliente_api_real_preparado(_e(max_tokens=300))
        self.assertNotEqual(r["error_tipo"], "max_tokens_excesivo")

    def test_max_tokens_minimo_no_bloquea(self):
        r = cliente_api_real_preparado(_e(max_tokens=1))
        self.assertNotEqual(r["error_tipo"], "max_tokens_excesivo")


class TestClienteApiRealPreparadoCasoValido(unittest.TestCase):
    def setUp(self):
        self.r = cliente_api_real_preparado(_ENTRADA_BASE)

    def test_caso_valido_ok_true(self):
        self.assertTrue(self.r["ok"])

    def test_caso_valido_bloqueo_false(self):
        self.assertFalse(self.r["bloqueo"])

    def test_caso_valido_response_text_vacio(self):
        self.assertEqual(self.r["response_text"], "")

    def test_caso_valido_fallback_usado_false(self):
        self.assertFalse(self.r["fallback_usado"])

    def test_caso_valido_evidencia_indica_no_ejecucion(self):
        self.assertIn("sin_ejecucion", self.r["evidencia"])

    def test_caso_valido_request_preparado_no_es_none(self):
        self.assertIsNotNone(self.r["request_preparado"])

    def test_caso_valido_request_preparado_no_contiene_api_key(self):
        rp = str(self.r["request_preparado"])
        self.assertNotIn("api_key", rp.lower())
        self.assertNotIn("sk-ant", rp.lower())

    def test_caso_valido_request_preparado_no_contiene_headers(self):
        rp = self.r["request_preparado"]
        self.assertNotIn("headers", rp)

    def test_caso_valido_request_preparado_no_contiene_authorization(self):
        rp = str(self.r["request_preparado"])
        self.assertNotIn("Authorization", rp)
        self.assertNotIn("authorization", rp)

    def test_caso_valido_tokens_estimados_es_local(self):
        self.assertIsNotNone(self.r["tokens_estimados"])
        self.assertIsInstance(self.r["tokens_estimados"], int)
        self.assertGreater(self.r["tokens_estimados"], 0)

    def test_caso_valido_costo_estimado_sin_llamada(self):
        self.assertEqual(self.r["costo_estimado"], "no_calculado_sin_llamada")

    def test_caso_valido_proveedor_es_anthropic_preparado(self):
        self.assertEqual(self.r["proveedor"], "anthropic_preparado")

    def test_caso_valido_modo_es_preparada_sin_llamada(self):
        self.assertEqual(self.r["modo"], "api_real_preparada_sin_llamada")

    def test_caso_valido_error_tipo_vacio(self):
        self.assertEqual(self.r["error_tipo"], "")

    def test_caso_valido_modelo_en_salida(self):
        self.assertEqual(self.r["modelo"], "claude-3-5-haiku-latest")


class TestClienteApiRealPreparadoCampos(unittest.TestCase):
    def test_salida_contiene_13_campos(self):
        r = cliente_api_real_preparado(_ENTRADA_BASE)
        campos_esperados = {
            "ok", "proveedor", "modo", "modelo", "request_preparado",
            "response_text", "error_tipo", "fallback_usado", "tokens_estimados",
            "costo_estimado", "evidencia", "bloqueo", "motivo",
        }
        self.assertEqual(set(r.keys()), campos_esperados)

    def test_salida_bloqueo_contiene_13_campos(self):
        r = cliente_api_real_preparado("invalido")
        campos_esperados = {
            "ok", "proveedor", "modo", "modelo", "request_preparado",
            "response_text", "error_tipo", "fallback_usado", "tokens_estimados",
            "costo_estimado", "evidencia", "bloqueo", "motivo",
        }
        self.assertEqual(set(r.keys()), campos_esperados)


class TestClienteApiRealPreparadoRequestId(unittest.TestCase):
    def test_request_id_ausente_bloquea(self):
        entrada = {k: v for k, v in _ENTRADA_BASE.items() if k != "request_id"}
        r = cliente_api_real_preparado(entrada)
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "request_id_invalido")

    def test_request_id_vacio_bloquea(self):
        r = cliente_api_real_preparado(_e(request_id=""))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "request_id_invalido")

    def test_request_id_solo_espacios_bloquea(self):
        r = cliente_api_real_preparado(_e(request_id="   "))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "request_id_invalido")

    def test_request_id_none_bloquea(self):
        r = cliente_api_real_preparado(_e(request_id=None))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "request_id_invalido")

    def test_request_id_int_bloquea(self):
        r = cliente_api_real_preparado(_e(request_id=123))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "request_id_invalido")

    def test_request_id_bool_bloquea(self):
        r = cliente_api_real_preparado(_e(request_id=True))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "request_id_invalido")

    def test_request_id_valido_no_bloquea_por_este_motivo(self):
        r = cliente_api_real_preparado(_e(request_id="req-001"))
        self.assertNotEqual(r["error_tipo"], "request_id_invalido")

    def test_request_id_valido_ok_true(self):
        r = cliente_api_real_preparado(_e(request_id="req-001"))
        self.assertTrue(r["ok"])

    def test_request_id_valido_bloqueo_false(self):
        r = cliente_api_real_preparado(_e(request_id="req-001"))
        self.assertFalse(r["bloqueo"])

    def test_request_id_invalido_bloqueo_true(self):
        r = cliente_api_real_preparado(_e(request_id=""))
        self.assertTrue(r["bloqueo"])

    def test_request_id_invalido_ok_false(self):
        r = cliente_api_real_preparado(_e(request_id=""))
        self.assertFalse(r["ok"])

    def test_request_id_valido_aparece_en_request_preparado(self):
        r = cliente_api_real_preparado(_e(request_id="uuid-xyz-123"))
        self.assertIsNotNone(r["request_preparado"])
        self.assertEqual(r["request_preparado"]["request_id"], "uuid-xyz-123")

    def test_request_id_invalido_motivo_menciona_trazabilidad(self):
        r = cliente_api_real_preparado(_e(request_id=""))
        self.assertIn("trazabilidad", r["motivo"])


class TestClienteApiRealPreparadoAislamiento(unittest.TestCase):
    def test_no_importa_anthropic_sdk(self):
        import sys
        self.assertNotIn("anthropic", sys.modules)

    def test_no_importa_requests(self):
        import sys
        self.assertNotIn("requests", sys.modules)

    def test_no_importa_urllib_request(self):
        import sys
        self.assertNotIn("urllib.request", sys.modules)

    def test_no_importa_http_client(self):
        import sys
        self.assertNotIn("http.client", sys.modules)

    def test_no_modifica_cerebro_mock(self):
        from plic_puente_agentes.cerebro_mock import cerebro_mock
        r = cerebro_mock({"texto_original": "revisar documento", "modo_seguro": True})
        self.assertIn("decision", r)

    def test_no_modifica_mano_local_simulada(self):
        from plic_puente_agentes.mano_local_simulada import mano_local_simulada
        r = mano_local_simulada({"accion": "leer_archivo", "modo_seguro": True, "parametros": {}})
        self.assertIn("resultado_simulado", r)

    def test_no_modifica_cliente_haiku_fake(self):
        from plic_puente_agentes.cliente_haiku_fake import cliente_haiku_fake
        r = cliente_haiku_fake({"texto_original": "revisar documento", "modo_seguro": True})
        self.assertIn("decision", r)


if __name__ == "__main__":
    unittest.main()
