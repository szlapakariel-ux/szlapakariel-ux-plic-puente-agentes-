import unittest
from plic_puente_agentes.cliente_haiku_fake import cliente_haiku_fake

_ENTRADA_BASE = {
    "texto_original": "revisá el contrato",
    "contexto_actual": None,
    "estado_del_ciclo": None,
    "autorizaciones_disponibles": [],
    "reglas_plic": [],
    "historial_resumido": "",
    "modo_seguro": True,
}


def _e(**kwargs):
    entrada = dict(_ENTRADA_BASE)
    entrada.update(kwargs)
    return entrada


class TestClienteHaikuFakeIdentidad(unittest.TestCase):
    def test_proveedor_es_haiku_fake(self):
        r = cliente_haiku_fake(_e())
        self.assertEqual(r["proveedor"], "haiku_fake")

    def test_modo_es_fake_local_sin_api(self):
        r = cliente_haiku_fake(_e())
        self.assertEqual(r["modo"], "fake_local_sin_api")


class TestClienteHaikuFakeModoSeguro(unittest.TestCase):
    def test_modo_seguro_false_bloquea(self):
        r = cliente_haiku_fake(_e(modo_seguro=False))
        self.assertEqual(r["decision"], "no_ejecutar")

    def test_modo_seguro_false_riesgo_prohibido(self):
        r = cliente_haiku_fake(_e(modo_seguro=False))
        self.assertEqual(r["riesgo"], "prohibido")

    def test_modo_seguro_false_requiere_ariel(self):
        r = cliente_haiku_fake(_e(modo_seguro=False))
        self.assertTrue(r["requiere_ariel"])

    def test_modo_seguro_false_requiere_torre(self):
        r = cliente_haiku_fake(_e(modo_seguro=False))
        self.assertTrue(r["requiere_torre"])

    def test_modo_seguro_false_bloqueo_true(self):
        r = cliente_haiku_fake(_e(modo_seguro=False))
        self.assertTrue(r["bloqueo"])

    def test_modo_seguro_none_bloquea(self):
        r = cliente_haiku_fake(_e(modo_seguro=None))
        self.assertEqual(r["decision"], "no_ejecutar")

    def test_modo_seguro_ausente_bloquea(self):
        entrada = {k: v for k, v in _ENTRADA_BASE.items() if k != "modo_seguro"}
        r = cliente_haiku_fake(entrada)
        self.assertEqual(r["decision"], "no_ejecutar")


class TestClienteHaikuFakeEntradaInvalida(unittest.TestCase):
    def test_entrada_no_dict_decision_reformular(self):
        r = cliente_haiku_fake("texto plano")
        self.assertEqual(r["decision"], "reformular")

    def test_entrada_no_dict_bloqueo_true(self):
        r = cliente_haiku_fake("texto plano")
        self.assertTrue(r["bloqueo"])

    def test_entrada_no_dict_requiere_ariel(self):
        r = cliente_haiku_fake(42)
        self.assertTrue(r["requiere_ariel"])

    def test_entrada_no_dict_requiere_torre(self):
        r = cliente_haiku_fake(None)
        self.assertTrue(r["requiere_torre"])

    def test_entrada_no_dict_proveedor_igual(self):
        r = cliente_haiku_fake([])
        self.assertEqual(r["proveedor"], "haiku_fake")


class TestClienteHaikuFakeTextoVacio(unittest.TestCase):
    def test_texto_vacio_decision_reformular(self):
        r = cliente_haiku_fake(_e(texto_original=""))
        self.assertEqual(r["decision"], "reformular")

    def test_texto_vacio_riesgo_medio(self):
        r = cliente_haiku_fake(_e(texto_original=""))
        self.assertEqual(r["riesgo"], "medio")

    def test_texto_vacio_requiere_ariel(self):
        r = cliente_haiku_fake(_e(texto_original=""))
        self.assertTrue(r["requiere_ariel"])

    def test_texto_vacio_requiere_torre(self):
        r = cliente_haiku_fake(_e(texto_original=""))
        self.assertTrue(r["requiere_torre"])

    def test_texto_solo_espacios_reformula(self):
        r = cliente_haiku_fake(_e(texto_original="   "))
        self.assertEqual(r["decision"], "reformular")


class TestClienteHaikuFakeProhibidos(unittest.TestCase):
    def test_api_real_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="usá la api real"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")
        self.assertTrue(r["bloqueo"])

    def test_api_key_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="dame la api key"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_token_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="usá el token de acceso"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_env_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="leé el archivo .env"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_produccion_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="mandalo a producción"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_produccion_sin_tilde_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="mandalo a produccion"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_navegador_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="abrí el navegador"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_playwright_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="usá playwright para hacer clic"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_secret_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="usá el secret del vault"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_prohibido_requiere_ariel(self):
        r = cliente_haiku_fake(_e(texto_original="mandalo a producción"))
        self.assertTrue(r["requiere_ariel"])

    def test_prohibido_requiere_torre(self):
        r = cliente_haiku_fake(_e(texto_original="mandalo a producción"))
        self.assertTrue(r["requiere_torre"])


class TestClienteHaikuFakeContinuidad(unittest.TestCase):
    def test_segui_continua_documental(self):
        r = cliente_haiku_fake(_e(texto_original="seguí con el siguiente paso"))
        self.assertEqual(r["decision"], "continuar_documental")

    def test_segui_sin_tilde_continua(self):
        r = cliente_haiku_fake(_e(texto_original="segui adelante"))
        self.assertEqual(r["decision"], "continuar_documental")

    def test_continua_continua_documental(self):
        r = cliente_haiku_fake(_e(texto_original="continuá con el ciclo"))
        self.assertEqual(r["decision"], "continuar_documental")

    def test_siguiente_continua_documental(self):
        r = cliente_haiku_fake(_e(texto_original="siguiente paso documental"))
        self.assertEqual(r["decision"], "continuar_documental")

    def test_continuidad_riesgo_bajo(self):
        r = cliente_haiku_fake(_e(texto_original="seguí adelante"))
        self.assertEqual(r["riesgo"], "bajo")

    def test_continuidad_no_requiere_ariel(self):
        r = cliente_haiku_fake(_e(texto_original="seguí adelante"))
        self.assertFalse(r["requiere_ariel"])

    def test_continuidad_requiere_torre(self):
        r = cliente_haiku_fake(_e(texto_original="seguí adelante"))
        self.assertTrue(r["requiere_torre"])

    def test_continuidad_no_bloqueo(self):
        r = cliente_haiku_fake(_e(texto_original="seguí adelante"))
        self.assertFalse(r["bloqueo"])


class TestClienteHaikuFakeMerge(unittest.TestCase):
    def test_merge_pide_autorizacion(self):
        r = cliente_haiku_fake(_e(texto_original="hacé el merge del branch"))
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_pr_pide_autorizacion(self):
        r = cliente_haiku_fake(_e(texto_original="abrí un pr con los cambios"))
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_issue_pide_autorizacion(self):
        r = cliente_haiku_fake(_e(texto_original="cerrá el issue pendiente"))
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_merge_riesgo_alto(self):
        r = cliente_haiku_fake(_e(texto_original="hacé el merge del branch"))
        self.assertEqual(r["riesgo"], "alto")

    def test_merge_requiere_ariel(self):
        r = cliente_haiku_fake(_e(texto_original="hacé el merge del branch"))
        self.assertTrue(r["requiere_ariel"])

    def test_merge_requiere_torre(self):
        r = cliente_haiku_fake(_e(texto_original="hacé el merge del branch"))
        self.assertTrue(r["requiere_torre"])

    def test_merge_no_bloqueo(self):
        r = cliente_haiku_fake(_e(texto_original="hacé el merge del branch"))
        self.assertFalse(r["bloqueo"])


class TestClienteHaikuFakeDelegacion(unittest.TestCase):
    def test_pasalo_a_claude_reformula(self):
        r = cliente_haiku_fake(_e(texto_original="pasalo a Claude para que decida"))
        self.assertEqual(r["decision"], "reformular")

    def test_pasalo_a_codex_reformula(self):
        r = cliente_haiku_fake(_e(texto_original="pasalo a Codex"))
        self.assertEqual(r["decision"], "reformular")

    def test_mandalo_a_otro_agente_reformula(self):
        r = cliente_haiku_fake(_e(texto_original="mandalo a otro agente para procesar"))
        self.assertEqual(r["decision"], "reformular")

    def test_delegacion_riesgo_medio(self):
        r = cliente_haiku_fake(_e(texto_original="pasalo a Claude para que decida"))
        self.assertEqual(r["riesgo"], "medio")

    def test_delegacion_no_requiere_ariel(self):
        r = cliente_haiku_fake(_e(texto_original="pasalo a Claude para que decida"))
        self.assertFalse(r["requiere_ariel"])

    def test_delegacion_requiere_torre(self):
        r = cliente_haiku_fake(_e(texto_original="pasalo a Claude para que decida"))
        self.assertTrue(r["requiere_torre"])


class TestClienteHaikuFakeDefault(unittest.TestCase):
    def test_default_decision_reformular(self):
        r = cliente_haiku_fake(_e(texto_original="revisá el documento"))
        self.assertEqual(r["decision"], "reformular")

    def test_default_riesgo_medio(self):
        r = cliente_haiku_fake(_e(texto_original="revisá el documento"))
        self.assertEqual(r["riesgo"], "medio")

    def test_default_no_requiere_ariel(self):
        r = cliente_haiku_fake(_e(texto_original="revisá el documento"))
        self.assertFalse(r["requiere_ariel"])

    def test_default_requiere_torre(self):
        r = cliente_haiku_fake(_e(texto_original="revisá el documento"))
        self.assertTrue(r["requiere_torre"])

    def test_default_no_bloqueo(self):
        r = cliente_haiku_fake(_e(texto_original="revisá el documento"))
        self.assertFalse(r["bloqueo"])


class TestClienteHaikuFakeCampos(unittest.TestCase):
    _CAMPOS_ESPERADOS = {
        "decision", "riesgo", "requiere_ariel", "requiere_torre",
        "motivo", "accion_segura_sugerida", "opciones_para_ariel",
        "bloqueo", "evidencia", "proveedor", "modo",
    }

    def test_salida_contiene_todos_los_campos(self):
        r = cliente_haiku_fake(_e())
        self.assertEqual(set(r.keys()), self._CAMPOS_ESPERADOS)

    def test_salida_modo_seguro_false_contiene_todos_los_campos(self):
        r = cliente_haiku_fake(_e(modo_seguro=False))
        self.assertEqual(set(r.keys()), self._CAMPOS_ESPERADOS)

    def test_salida_entrada_no_dict_contiene_todos_los_campos(self):
        r = cliente_haiku_fake("texto")
        self.assertEqual(set(r.keys()), self._CAMPOS_ESPERADOS)

    def test_salida_prohibido_contiene_todos_los_campos(self):
        r = cliente_haiku_fake(_e(texto_original="mandalo a producción"))
        self.assertEqual(set(r.keys()), self._CAMPOS_ESPERADOS)


class TestClienteHaikuFakeAislamiento(unittest.TestCase):
    def test_no_importa_cerebro_mock(self):
        import plic_puente_agentes.cliente_haiku_fake as mod
        self.assertNotIn("cerebro_mock", dir(mod))

    def test_no_importa_mano_local(self):
        import plic_puente_agentes.cliente_haiku_fake as mod
        self.assertNotIn("mano_local_simulada", dir(mod))

    def test_no_importa_requests(self):
        import plic_puente_agentes.cliente_haiku_fake as mod
        self.assertNotIn("requests", dir(mod))

    def test_no_importa_anthropic(self):
        import plic_puente_agentes.cliente_haiku_fake as mod
        self.assertNotIn("anthropic", dir(mod))

    def test_no_importa_os(self):
        import plic_puente_agentes.cliente_haiku_fake as mod
        self.assertNotIn("os", dir(mod))

    def test_no_importa_subprocess(self):
        import plic_puente_agentes.cliente_haiku_fake as mod
        self.assertNotIn("subprocess", dir(mod))


class TestClienteHaikuFakeB06FalsosPositivos(unittest.TestCase):
    """B-06 — falsos positivos corregidos: tissue/issue, tokenización/token,
    continuamente/continua, secretaría/secret."""

    # --- issue / tissue ---

    def test_tissue_no_pide_autorizacion(self):
        r = cliente_haiku_fake(_e(texto_original="no hay tissue aquí"))
        self.assertNotEqual(r["decision"], "pedir_autorizacion")

    def test_tissue_no_es_alto(self):
        r = cliente_haiku_fake(_e(texto_original="no hay tissue aquí"))
        self.assertNotEqual(r["riesgo"], "alto")

    def test_issue_real_pide_autorizacion(self):
        r = cliente_haiku_fake(_e(texto_original="comentar issue"))
        self.assertEqual(r["decision"], "pedir_autorizacion")
        self.assertEqual(r["riesgo"], "alto")

    def test_github_issue_pide_autorizacion(self):
        r = cliente_haiku_fake(_e(texto_original="github issue pendiente"))
        self.assertEqual(r["decision"], "pedir_autorizacion")
        self.assertEqual(r["riesgo"], "alto")

    def test_issue_numero_pide_autorizacion(self):
        r = cliente_haiku_fake(_e(texto_original="cerrá el issue #5"))
        self.assertEqual(r["decision"], "pedir_autorizacion")
        self.assertEqual(r["riesgo"], "alto")

    # --- token / tokenización ---

    def test_tokenizacion_no_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="tokenización del texto"))
        self.assertNotEqual(r["decision"], "no_ejecutar")
        self.assertFalse(r["bloqueo"])

    def test_tokenizar_no_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="tokenizar texto"))
        self.assertNotEqual(r["decision"], "no_ejecutar")
        self.assertFalse(r["bloqueo"])

    def test_usar_token_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="usar token"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")
        self.assertTrue(r["bloqueo"])

    def test_api_token_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="api token de acceso"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_bearer_token_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="bearer token para auth"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_token_solo_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="token"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    # --- continua / continuamente ---

    def test_continuamente_no_continua_documental(self):
        r = cliente_haiku_fake(_e(texto_original="revisar continuamente"))
        self.assertNotEqual(r["decision"], "continuar_documental")

    def test_continua_real_continua_documental(self):
        r = cliente_haiku_fake(_e(texto_original="continua con el ciclo"))
        self.assertEqual(r["decision"], "continuar_documental")
        self.assertEqual(r["riesgo"], "bajo")

    def test_continuar_real_continua_documental(self):
        r = cliente_haiku_fake(_e(texto_original="continuar con el paso"))
        self.assertEqual(r["decision"], "continuar_documental")
        self.assertEqual(r["riesgo"], "bajo")

    def test_continua_solo_continua_documental(self):
        r = cliente_haiku_fake(_e(texto_original="continuá"))
        self.assertEqual(r["decision"], "continuar_documental")

    # --- secret / secretaría ---

    def test_secretaria_no_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="reunión de secretaría"))
        self.assertNotEqual(r["decision"], "no_ejecutar")
        self.assertFalse(r["bloqueo"])

    def test_secretario_no_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="preguntá al secretario"))
        self.assertNotEqual(r["decision"], "no_ejecutar")
        self.assertFalse(r["bloqueo"])

    def test_secret_solo_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="secret"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_secrets_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="secrets del vault"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_credencial_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="usá la credencial"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    def test_clave_bloquea(self):
        r = cliente_haiku_fake(_e(texto_original="dame la clave"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertTrue(r["bloqueo"])

    # --- prioridades: prohibido gana sobre continuidad ---

    def test_segui_con_token_prohibido_gana(self):
        r = cliente_haiku_fake(_e(texto_original="seguí y usar token"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")

    def test_continua_con_api_key_prohibido_gana(self):
        r = cliente_haiku_fake(_e(texto_original="continuá y api key"))
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")
