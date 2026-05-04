import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from plic_puente_agentes.cliente_api_real_bloqueado import cliente_api_real_bloqueado

_ENTRADA_BASE = {
    "prompt": "Respondé exactamente: PLIC_OK",
    "modo_seguro": True,
    "proveedor": "anthropic",
    "modelo": "claude-haiku-4-5-20251001",
    "timeout": 10,
    "max_tokens": 50,
    "request_id": "test-request-gate-001",
    "permitir_llamada_real": False,
    "autorizacion_ariel": "PUENTE-6D-B-SIN-LLAMADA-REAL",
    "contrato_puente_6d_a_confirmado": True,
    "dry_run": True,
}


def _e(**kwargs):
    entrada = dict(_ENTRADA_BASE)
    entrada.update(kwargs)
    return entrada


class TestClienteApiRealBloqueadoIdentidad(unittest.TestCase):
    def test_proveedor_es_anthropic_gate(self):
        r = cliente_api_real_bloqueado(_ENTRADA_BASE)
        self.assertEqual(r["proveedor"], "anthropic_gate")

    def test_modo_es_llamada_real_bloqueada_por_defecto(self):
        r = cliente_api_real_bloqueado(_ENTRADA_BASE)
        self.assertEqual(r["modo"], "llamada_real_bloqueada_por_defecto")

    def test_llamada_real_ejecutada_siempre_false_caso_valido(self):
        r = cliente_api_real_bloqueado(_ENTRADA_BASE)
        self.assertFalse(r["llamada_real_ejecutada"])

    def test_llamada_real_ejecutada_siempre_false_en_bloqueo(self):
        r = cliente_api_real_bloqueado("no soy dict")
        self.assertFalse(r["llamada_real_ejecutada"])

    def test_llamada_real_ejecutada_siempre_false_modo_seguro_false(self):
        r = cliente_api_real_bloqueado(_e(modo_seguro=False))
        self.assertFalse(r["llamada_real_ejecutada"])


class TestClienteApiRealBloqueadoEntradaInvalida(unittest.TestCase):
    def test_entrada_no_dict_bloquea(self):
        r = cliente_api_real_bloqueado("no soy dict")
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["llamada_real_bloqueada"])
        self.assertEqual(r["error_tipo"], "entrada_invalida")

    def test_entrada_lista_bloquea(self):
        r = cliente_api_real_bloqueado([1, 2, 3])
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_invalida")

    def test_entrada_none_bloquea(self):
        r = cliente_api_real_bloqueado(None)
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_invalida")


class TestClienteApiRealBloqueadoModoSeguro(unittest.TestCase):
    def test_modo_seguro_false_bloquea(self):
        r = cliente_api_real_bloqueado(_e(modo_seguro=False))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["llamada_real_bloqueada"])
        self.assertEqual(r["error_tipo"], "modo_seguro_requerido")

    def test_modo_seguro_none_bloquea(self):
        r = cliente_api_real_bloqueado(_e(modo_seguro=None))
        self.assertEqual(r["error_tipo"], "modo_seguro_requerido")

    def test_modo_seguro_entero_bloquea(self):
        r = cliente_api_real_bloqueado(_e(modo_seguro=1))
        self.assertEqual(r["error_tipo"], "modo_seguro_requerido")

    def test_modo_seguro_string_bloquea(self):
        r = cliente_api_real_bloqueado(_e(modo_seguro="true"))
        self.assertEqual(r["error_tipo"], "modo_seguro_requerido")


class TestClienteApiRealBloqueadoContrato(unittest.TestCase):
    def test_contrato_no_confirmado_false_bloquea(self):
        r = cliente_api_real_bloqueado(_e(contrato_puente_6d_a_confirmado=False))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["llamada_real_bloqueada"])
        self.assertEqual(r["error_tipo"], "contrato_no_confirmado")

    def test_contrato_no_confirmado_ausente_bloquea(self):
        entrada = {k: v for k, v in _ENTRADA_BASE.items() if k != "contrato_puente_6d_a_confirmado"}
        r = cliente_api_real_bloqueado(entrada)
        self.assertEqual(r["error_tipo"], "contrato_no_confirmado")

    def test_contrato_no_confirmado_none_bloquea(self):
        r = cliente_api_real_bloqueado(_e(contrato_puente_6d_a_confirmado=None))
        self.assertEqual(r["error_tipo"], "contrato_no_confirmado")


class TestClienteApiRealBloqueadoDryRun(unittest.TestCase):
    def test_dry_run_false_bloquea(self):
        r = cliente_api_real_bloqueado(_e(dry_run=False))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["llamada_real_bloqueada"])
        self.assertEqual(r["error_tipo"], "dry_run_requerido")

    def test_dry_run_ausente_bloquea(self):
        entrada = {k: v for k, v in _ENTRADA_BASE.items() if k != "dry_run"}
        r = cliente_api_real_bloqueado(entrada)
        self.assertEqual(r["error_tipo"], "dry_run_requerido")

    def test_dry_run_none_bloquea(self):
        r = cliente_api_real_bloqueado(_e(dry_run=None))
        self.assertEqual(r["error_tipo"], "dry_run_requerido")


class TestClienteApiRealBloqueadoPermitirLlamadaReal(unittest.TestCase):
    def test_permitir_llamada_real_true_bloquea(self):
        r = cliente_api_real_bloqueado(_e(permitir_llamada_real=True))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["llamada_real_bloqueada"])
        self.assertFalse(r["llamada_real_ejecutada"])
        self.assertEqual(r["error_tipo"], "llamada_real_bloqueada_por_defecto")

    def test_permitir_llamada_real_true_motivo_menciona_puente_6d_b(self):
        r = cliente_api_real_bloqueado(_e(permitir_llamada_real=True))
        self.assertIn("PUENTE-6D-B", r["motivo"])

    def test_permitir_llamada_real_true_motivo_menciona_puente_6d_c(self):
        r = cliente_api_real_bloqueado(_e(permitir_llamada_real=True))
        self.assertIn("PUENTE-6D-C", r["motivo"])


class TestClienteApiRealBloqueadoAutorizacion(unittest.TestCase):
    def test_autorizacion_incorrecta_bloquea(self):
        r = cliente_api_real_bloqueado(_e(autorizacion_ariel="INCORRECTO"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["llamada_real_bloqueada"])
        self.assertEqual(r["error_tipo"], "autorizacion_invalida")

    def test_autorizacion_ausente_bloquea(self):
        entrada = {k: v for k, v in _ENTRADA_BASE.items() if k != "autorizacion_ariel"}
        r = cliente_api_real_bloqueado(entrada)
        self.assertEqual(r["error_tipo"], "autorizacion_invalida")

    def test_autorizacion_vacia_bloquea(self):
        r = cliente_api_real_bloqueado(_e(autorizacion_ariel=""))
        self.assertEqual(r["error_tipo"], "autorizacion_invalida")

    def test_autorizacion_exacta_no_bloquea_por_este_motivo(self):
        r = cliente_api_real_bloqueado(_ENTRADA_BASE)
        self.assertNotEqual(r["error_tipo"], "autorizacion_invalida")


class TestClienteApiRealBloqueadoPrompt(unittest.TestCase):
    def test_prompt_distinto_bloquea(self):
        r = cliente_api_real_bloqueado(_e(prompt="hola mundo"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["llamada_real_bloqueada"])
        self.assertEqual(r["error_tipo"], "prompt_no_autorizado")

    def test_prompt_vacio_bloquea(self):
        r = cliente_api_real_bloqueado(_e(prompt=""))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "prompt_no_autorizado")

    def test_prompt_con_secret_bloquea(self):
        r = cliente_api_real_bloqueado(_e(prompt="usar secret del vault"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_sensible")

    def test_prompt_con_token_bloquea(self):
        r = cliente_api_real_bloqueado(_e(prompt="usar token de acceso"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_sensible")

    def test_prompt_con_api_key_bloquea(self):
        r = cliente_api_real_bloqueado(_e(prompt="incluir api key aquí"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "entrada_sensible")

    def test_prompt_exacto_plic_ok_no_bloquea_por_prompt(self):
        r = cliente_api_real_bloqueado(_ENTRADA_BASE)
        self.assertNotEqual(r["error_tipo"], "prompt_no_autorizado")

    def test_prompt_exacto_plic_ok_validado(self):
        r = cliente_api_real_bloqueado(_ENTRADA_BASE)
        self.assertTrue(r["prompt_validado"])


class TestClienteApiRealBloqueadoRequestId(unittest.TestCase):
    def test_request_id_ausente_bloquea(self):
        entrada = {k: v for k, v in _ENTRADA_BASE.items() if k != "request_id"}
        r = cliente_api_real_bloqueado(entrada)
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["llamada_real_bloqueada"])
        self.assertEqual(r["error_tipo"], "request_id_invalido")

    def test_request_id_vacio_bloquea(self):
        r = cliente_api_real_bloqueado(_e(request_id=""))
        self.assertEqual(r["error_tipo"], "request_id_invalido")

    def test_request_id_solo_espacios_bloquea(self):
        r = cliente_api_real_bloqueado(_e(request_id="   "))
        self.assertEqual(r["error_tipo"], "request_id_invalido")

    def test_request_id_no_string_bloquea(self):
        r = cliente_api_real_bloqueado(_e(request_id=123))
        self.assertEqual(r["error_tipo"], "request_id_invalido")

    def test_request_id_none_bloquea(self):
        r = cliente_api_real_bloqueado(_e(request_id=None))
        self.assertEqual(r["error_tipo"], "request_id_invalido")

    def test_request_id_valido_en_salida(self):
        r = cliente_api_real_bloqueado(_ENTRADA_BASE)
        self.assertEqual(r["request_id"], "test-request-gate-001")


class TestClienteApiRealBloqueadoProveedor(unittest.TestCase):
    def test_proveedor_no_autorizado_bloquea(self):
        r = cliente_api_real_bloqueado(_e(proveedor="openai"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["llamada_real_bloqueada"])
        self.assertEqual(r["error_tipo"], "proveedor_no_autorizado")

    def test_proveedor_vacio_bloquea(self):
        r = cliente_api_real_bloqueado(_e(proveedor=""))
        self.assertEqual(r["error_tipo"], "proveedor_no_autorizado")


class TestClienteApiRealBloqueadoModelo(unittest.TestCase):
    def test_modelo_no_autorizado_bloquea(self):
        r = cliente_api_real_bloqueado(_e(modelo="gpt-4"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["llamada_real_bloqueada"])
        self.assertEqual(r["error_tipo"], "modelo_no_autorizado")

    def test_modelo_vacio_bloquea(self):
        r = cliente_api_real_bloqueado(_e(modelo=""))
        self.assertEqual(r["error_tipo"], "modelo_no_autorizado")

    def test_modelo_haiku_3_bloquea(self):
        r = cliente_api_real_bloqueado(_e(modelo="claude-3-haiku-20240307"))
        self.assertEqual(r["error_tipo"], "modelo_no_autorizado")

    def test_modelo_autorizado_no_bloquea_por_modelo(self):
        r = cliente_api_real_bloqueado(_ENTRADA_BASE)
        self.assertNotEqual(r["error_tipo"], "modelo_no_autorizado")


class TestClienteApiRealBloqueadoTimeout(unittest.TestCase):
    def test_timeout_mayor_a_10_bloquea(self):
        r = cliente_api_real_bloqueado(_e(timeout=11))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["llamada_real_bloqueada"])
        self.assertEqual(r["error_tipo"], "timeout_invalido")

    def test_timeout_no_numerico_bloquea(self):
        r = cliente_api_real_bloqueado(_e(timeout="diez"))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "timeout_invalido")

    def test_timeout_none_bloquea(self):
        r = cliente_api_real_bloqueado(_e(timeout=None))
        self.assertEqual(r["error_tipo"], "timeout_invalido")

    def test_timeout_10_no_bloquea(self):
        r = cliente_api_real_bloqueado(_e(timeout=10))
        self.assertNotEqual(r["error_tipo"], "timeout_invalido")


class TestClienteApiRealBloqueadoMaxTokens(unittest.TestCase):
    def test_max_tokens_mayor_a_50_bloquea(self):
        r = cliente_api_real_bloqueado(_e(max_tokens=51))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["llamada_real_bloqueada"])
        self.assertEqual(r["error_tipo"], "max_tokens_invalido")

    def test_max_tokens_no_int_bloquea(self):
        r = cliente_api_real_bloqueado(_e(max_tokens=50.5))
        self.assertFalse(r["ok"])
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["error_tipo"], "max_tokens_invalido")

    def test_max_tokens_none_bloquea(self):
        r = cliente_api_real_bloqueado(_e(max_tokens=None))
        self.assertEqual(r["error_tipo"], "max_tokens_invalido")

    def test_max_tokens_50_no_bloquea(self):
        r = cliente_api_real_bloqueado(_e(max_tokens=50))
        self.assertNotEqual(r["error_tipo"], "max_tokens_invalido")


class TestClienteApiRealBloqueadoCasoValido(unittest.TestCase):
    def setUp(self):
        self.r = cliente_api_real_bloqueado(_ENTRADA_BASE)

    def test_caso_valido_ok_true(self):
        self.assertTrue(self.r["ok"])

    def test_caso_valido_bloqueo_false(self):
        self.assertFalse(self.r["bloqueo"])

    def test_caso_valido_llamada_real_ejecutada_false(self):
        self.assertFalse(self.r["llamada_real_ejecutada"])

    def test_caso_valido_llamada_real_bloqueada_true(self):
        self.assertTrue(self.r["llamada_real_bloqueada"])

    def test_caso_valido_prompt_validado_true(self):
        self.assertTrue(self.r["prompt_validado"])

    def test_caso_valido_error_tipo_vacio(self):
        self.assertEqual(self.r["error_tipo"], "")

    def test_caso_valido_fallback_usado_false(self):
        self.assertFalse(self.r["fallback_usado"])

    def test_caso_valido_evidencia_indica_sin_ejecucion_real(self):
        self.assertIn("sin_ejecucion_real", self.r["evidencia"])

    def test_caso_valido_proximo_paso_menciona_puente_6d_c(self):
        self.assertIn("PUENTE-6D-C", self.r["proximo_paso_seguro"])

    def test_caso_valido_no_contiene_headers(self):
        r_str = str(self.r)
        self.assertNotIn("Authorization", r_str)
        self.assertNotIn("authorization", r_str)

    def test_caso_valido_no_contiene_api_key_valor(self):
        r_str = str(self.r).lower()
        self.assertNotIn("sk-ant", r_str)

    def test_caso_valido_proveedor_es_anthropic_gate(self):
        self.assertEqual(self.r["proveedor"], "anthropic_gate")

    def test_caso_valido_modo_es_bloqueada_por_defecto(self):
        self.assertEqual(self.r["modo"], "llamada_real_bloqueada_por_defecto")

    def test_caso_valido_modelo_en_salida(self):
        self.assertEqual(self.r["modelo"], "claude-haiku-4-5-20251001")

    def test_caso_valido_request_id_en_salida(self):
        self.assertEqual(self.r["request_id"], "test-request-gate-001")


class TestClienteApiRealBloqueadoCampos(unittest.TestCase):
    def test_salida_valida_contiene_campos_esperados(self):
        r = cliente_api_real_bloqueado(_ENTRADA_BASE)
        campos_esperados = {
            "ok", "proveedor", "modo", "modelo",
            "llamada_real_ejecutada", "llamada_real_bloqueada",
            "request_id", "prompt_validado", "error_tipo",
            "fallback_usado", "evidencia", "bloqueo",
            "motivo", "proximo_paso_seguro",
        }
        self.assertEqual(set(r.keys()), campos_esperados)

    def test_salida_bloqueo_contiene_campos_esperados(self):
        r = cliente_api_real_bloqueado("invalido")
        campos_esperados = {
            "ok", "proveedor", "modo", "modelo",
            "llamada_real_ejecutada", "llamada_real_bloqueada",
            "request_id", "prompt_validado", "error_tipo",
            "fallback_usado", "evidencia", "bloqueo",
            "motivo", "proximo_paso_seguro",
        }
        self.assertEqual(set(r.keys()), campos_esperados)


class TestClienteApiRealBloqueadoAislamiento(unittest.TestCase):
    def test_no_importa_anthropic_sdk(self):
        self.assertNotIn("anthropic", sys.modules)

    def test_no_importa_requests(self):
        self.assertNotIn("requests", sys.modules)

    def test_no_importa_urllib_request(self):
        self.assertNotIn("urllib.request", sys.modules)

    def test_no_importa_http_client(self):
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

    def test_no_modifica_cliente_api_real_preparado(self):
        from plic_puente_agentes.cliente_api_real_preparado import cliente_api_real_preparado
        r = cliente_api_real_preparado({
            "prompt": "clasificar documento",
            "modo_seguro": True,
            "proveedor": "anthropic",
            "modelo": "claude-haiku-4-5-20251001",
            "timeout": 5,
            "max_tokens": 64,
            "request_id": "test-aislamiento-001",
            "permitir_llamada_real": False,
        })
        self.assertIn("ok", r)


if __name__ == "__main__":
    unittest.main()
