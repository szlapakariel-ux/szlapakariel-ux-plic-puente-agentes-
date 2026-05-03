import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from plic_puente_agentes.mano_local_simulada import mano_local_simulada

_CAMPOS_REQUERIDOS = {
    "accion_simulada", "destino_simulado", "payload_simulado",
    "resultado_simulado", "requiere_autorizacion", "bloqueo",
    "motivo", "evidencia",
}


def _entrada(decision, accion="", **kwargs):
    base = {
        "decision_del_cerebro": decision,
        "accion_segura_sugerida": accion,
        "contexto_actual": None,
        "repo_autorizado": "szlapakariel-ux-plic-puente-agentes-",
        "autorizaciones_disponibles": [],
        "modo_simulado": True,
    }
    base.update(kwargs)
    return base


class TestManoLocalSimuladaModoSimulado(unittest.TestCase):
    """Test 1 — modo_simulado False bloquea."""

    def test_modo_simulado_false_bloquea(self):
        r = mano_local_simulada({**_entrada("continuar_documental"), "modo_simulado": False})
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["requiere_autorizacion"])
        self.assertEqual(r["resultado_simulado"], "bloqueado")
        self.assertIn("simulado", r["motivo"])

    def test_modo_simulado_ausente_bloquea(self):
        r = mano_local_simulada({"decision_del_cerebro": "continuar_documental"})
        self.assertTrue(r["bloqueo"])

    def test_modo_simulado_none_bloquea(self):
        r = mano_local_simulada({**_entrada("continuar_documental"), "modo_simulado": None})
        self.assertTrue(r["bloqueo"])


class TestManoLocalSimuladaNoEjecutar(unittest.TestCase):
    """Test 2 — no_ejecutar no prepara acción externa."""

    def test_no_ejecutar_bloquea(self):
        r = mano_local_simulada(_entrada("no_ejecutar"))
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["resultado_simulado"], "no_ejecutado")
        self.assertEqual(r["accion_simulada"], "no_accion")
        self.assertEqual(r["payload_simulado"], {})

    def test_no_ejecutar_no_requiere_autorizacion(self):
        r = mano_local_simulada(_entrada("no_ejecutar"))
        self.assertFalse(r["requiere_autorizacion"])


class TestManoLocalSimuladaPedirAutorizacion(unittest.TestCase):
    """Test 3 — pedir_autorizacion queda pendiente."""

    def test_pedir_autorizacion_requiere_autorizacion(self):
        r = mano_local_simulada(_entrada("pedir_autorizacion", "hacer algo"))
        self.assertTrue(r["requiere_autorizacion"])
        self.assertFalse(r["bloqueo"])
        self.assertEqual(r["resultado_simulado"], "pendiente_autorizacion")

    def test_pedir_autorizacion_destino_torre(self):
        r = mano_local_simulada(_entrada("pedir_autorizacion"))
        self.assertEqual(r["destino_simulado"], "torre")


class TestManoLocalSimuladaReformular(unittest.TestCase):
    """Test 4 — reformular prepara prompt para Torre."""

    def test_reformular_prepara_prompt(self):
        r = mano_local_simulada(_entrada("reformular", "clarificar el objetivo"))
        self.assertEqual(r["accion_simulada"], "preparar_prompt_reformulado")
        self.assertEqual(r["destino_simulado"], "torre")
        self.assertEqual(r["resultado_simulado"], "preparado")
        self.assertFalse(r["bloqueo"])
        self.assertFalse(r["requiere_autorizacion"])


class TestManoLocalSimuladaContinuarDocumental(unittest.TestCase):
    """Test 5 — continuar_documental prepara orden documental."""

    def test_continuar_documental_prepara_orden(self):
        r = mano_local_simulada(_entrada("continuar_documental", "avanzar al siguiente paso"))
        self.assertEqual(r["accion_simulada"], "preparar_orden_documental")
        self.assertEqual(r["destino_simulado"], "ejecutor_simulado")
        self.assertEqual(r["resultado_simulado"], "preparado")
        self.assertFalse(r["bloqueo"])
        self.assertFalse(r["requiere_autorizacion"])


class TestManoLocalSimuladaDeclararBloqueo(unittest.TestCase):
    """Test 6 — declarar_bloqueo registra bloqueo."""

    def test_declarar_bloqueo_registra(self):
        r = mano_local_simulada(_entrada("declarar_bloqueo"))
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["accion_simulada"], "registrar_bloqueo")
        self.assertEqual(r["resultado_simulado"], "bloqueado")
        self.assertEqual(r["destino_simulado"], "registro_local")


class TestManoLocalSimuladaSuspender(unittest.TestCase):
    """Test 7 — suspender suspende ciclo."""

    def test_suspender_suspende(self):
        r = mano_local_simulada(_entrada("suspender"))
        self.assertFalse(r["bloqueo"])
        self.assertEqual(r["accion_simulada"], "suspender_ciclo")
        self.assertEqual(r["resultado_simulado"], "suspendido")
        self.assertEqual(r["destino_simulado"], "registro_local")


class TestManoLocalSimuladaAccionesExternas(unittest.TestCase):
    """Tests 8 y 9 — acciones hacia Claude/issue quedan como payload simulado."""

    def test_accion_hacia_claude_es_simulada(self):
        r = mano_local_simulada(_entrada("continuar_documental", "pasalo a claude para análisis"))
        self.assertEqual(r["accion_simulada"], "preparar_prompt_claude")
        self.assertEqual(r["destino_simulado"], "claude_api")
        self.assertFalse(r["bloqueo"])
        self.assertIn("accion_sugerida", r["payload_simulado"])

    def test_accion_hacia_codex_es_simulada(self):
        r = mano_local_simulada(_entrada("continuar_documental", "mandalo a codex"))
        self.assertEqual(r["accion_simulada"], "preparar_prompt_codex")
        self.assertEqual(r["destino_simulado"], "codex_api")
        self.assertFalse(r["bloqueo"])

    def test_accion_hacia_issue_es_simulada(self):
        r = mano_local_simulada(_entrada("continuar_documental", "comentá el issue #5"))
        self.assertEqual(r["accion_simulada"], "preparar_comentario_issue")
        self.assertEqual(r["destino_simulado"], "github_issue")
        self.assertFalse(r["bloqueo"])

    def test_accion_hacia_pr_es_simulada(self):
        r = mano_local_simulada(_entrada("continuar_documental", "comentar el pr"))
        self.assertEqual(r["accion_simulada"], "preparar_comentario_pr")
        self.assertEqual(r["destino_simulado"], "github_pr")
        self.assertFalse(r["bloqueo"])


class TestManoLocalSimuladaTerminosRestringidos(unittest.TestCase):
    """Tests 10 y 11 — producción y secrets bloquean."""

    def test_produccion_en_decision_bloquea(self):
        r = mano_local_simulada(_entrada("produccion", "algo"))
        self.assertTrue(r["bloqueo"])
        self.assertTrue(r["requiere_autorizacion"])
        self.assertEqual(r["resultado_simulado"], "bloqueado")

    def test_produccion_en_accion_bloquea(self):
        r = mano_local_simulada(_entrada("continuar_documental", "mandalo a produccion"))
        self.assertTrue(r["bloqueo"])

    def test_secrets_en_accion_bloquea(self):
        r = mano_local_simulada(_entrada("continuar_documental", "usar secrets del repo"))
        self.assertTrue(r["bloqueo"])
        self.assertIn("simulacion", r["motivo"])

    def test_token_en_accion_bloquea(self):
        r = mano_local_simulada(_entrada("continuar_documental", "usar token de acceso"))
        self.assertTrue(r["bloqueo"])

    def test_playwright_en_accion_bloquea(self):
        r = mano_local_simulada(_entrada("continuar_documental", "abrir con playwright"))
        self.assertTrue(r["bloqueo"])

    def test_navegador_en_accion_bloquea(self):
        r = mano_local_simulada(_entrada("continuar_documental", "abrir navegador"))
        self.assertTrue(r["bloqueo"])


class TestManoLocalSimuladaEstructura(unittest.TestCase):
    """Test 12 — salida contiene todos los campos requeridos."""

    def _verificar_campos(self, resultado):
        for campo in _CAMPOS_REQUERIDOS:
            self.assertIn(campo, resultado, f"Campo faltante: {campo}")

    def test_campos_en_continuar_documental(self):
        self._verificar_campos(mano_local_simulada(_entrada("continuar_documental")))

    def test_campos_en_reformular(self):
        self._verificar_campos(mano_local_simulada(_entrada("reformular")))

    def test_campos_en_no_ejecutar(self):
        self._verificar_campos(mano_local_simulada(_entrada("no_ejecutar")))

    def test_campos_en_pedir_autorizacion(self):
        self._verificar_campos(mano_local_simulada(_entrada("pedir_autorizacion")))

    def test_campos_en_declarar_bloqueo(self):
        self._verificar_campos(mano_local_simulada(_entrada("declarar_bloqueo")))

    def test_campos_en_suspender(self):
        self._verificar_campos(mano_local_simulada(_entrada("suspender")))

    def test_campos_en_bloqueo_modo_simulado(self):
        self._verificar_campos(mano_local_simulada({**_entrada("continuar_documental"), "modo_simulado": False}))

    def test_evidencia_es_dict(self):
        r = mano_local_simulada(_entrada("continuar_documental"))
        self.assertIsInstance(r["evidencia"], dict)

    def test_payload_simulado_es_dict(self):
        r = mano_local_simulada(_entrada("continuar_documental"))
        self.assertIsInstance(r["payload_simulado"], dict)


class TestManoLocalSimuladaAislamientoYRegresion(unittest.TestCase):
    """Tests 13-15 — sin red, sin dependencias, sin efecto sobre cerebro_mock."""

    def test_no_usa_requests(self):
        import sys
        self.assertNotIn("requests", sys.modules)

    def test_no_usa_urllib(self):
        import plic_puente_agentes.mano_local_simulada as m
        import inspect
        source = inspect.getsource(m)
        self.assertNotIn("urllib", source)
        self.assertNotIn("http.client", source)
        self.assertNotIn("subprocess", source)

    def test_entrada_no_dict_devuelve_bloqueo(self):
        r = mano_local_simulada("texto plano")
        self.assertTrue(r["bloqueo"])

    def test_entrada_none_devuelve_bloqueo(self):
        r = mano_local_simulada(None)
        self.assertTrue(r["bloqueo"])

    def test_decision_desconocida_bloquea(self):
        r = mano_local_simulada(_entrada("hacer_algo_raro"))
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["resultado_simulado"], "desconocido")

    def test_cerebro_mock_no_modificado(self):
        from plic_puente_agentes.cerebro_mock import cerebro_mock
        r = cerebro_mock({"texto_original": "seguí"})
        self.assertEqual(r["decision"], "continuar_documental")

    def test_tests_cerebro_mock_siguen_pasando(self):
        from plic_puente_agentes.cerebro_mock import cerebro_mock
        r = cerebro_mock({"texto_original": "producción"})
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")


class TestManoLocalFalsoPositivos(unittest.TestCase):
    """PUENTE-4C-BACKLOG: verifica corrección de B-ML-01, B-ML-02, B-ML-03."""

    # B-ML-01: "prod" no dispara en palabras que lo contienen internamente
    def test_producir_documentacion_no_bloquea(self):
        r = mano_local_simulada(_entrada("continuar_documental", "producir documentacion del sistema"))
        self.assertFalse(r["bloqueo"])
        self.assertEqual(r["resultado_simulado"], "preparado")

    def test_reproducir_el_caso_no_bloquea(self):
        r = mano_local_simulada(_entrada("continuar_documental", "reproducir el caso base"))
        self.assertFalse(r["bloqueo"])

    def test_revisar_producto_no_bloquea(self):
        r = mano_local_simulada(_entrada("continuar_documental", "revisar el producto final"))
        self.assertFalse(r["bloqueo"])

    # B-ML-01: disparadores reales de "prod" siguen bloqueando
    def test_mandalo_a_prod_bloquea(self):
        r = mano_local_simulada(_entrada("continuar_documental", "mandalo a prod"))
        self.assertTrue(r["bloqueo"])
        self.assertEqual(r["resultado_simulado"], "bloqueado")

    def test_entorno_prod_bloquea(self):
        r = mano_local_simulada(_entrada("continuar_documental", "entorno prod"))
        self.assertTrue(r["bloqueo"])

    def test_deploy_a_prod_bloquea(self):
        r = mano_local_simulada(_entrada("continuar_documental", "deploy a prod"))
        self.assertTrue(r["bloqueo"])

    # B-ML-02: "pr" no mapea en palabras que lo contienen internamente
    def test_preparar_documento_no_mapea_pr(self):
        r = mano_local_simulada(_entrada("continuar_documental", "preparar el documento"))
        self.assertNotEqual(r["accion_simulada"], "preparar_comentario_pr")
        self.assertEqual(r["accion_simulada"], "preparar_orden_documental")

    def test_comprimir_archivos_no_mapea_pr(self):
        r = mano_local_simulada(_entrada("continuar_documental", "comprimir archivos"))
        self.assertNotEqual(r["accion_simulada"], "preparar_comentario_pr")

    def test_propuesta_documental_no_mapea_pr(self):
        r = mano_local_simulada(_entrada("continuar_documental", "propuesta documental"))
        self.assertNotEqual(r["accion_simulada"], "preparar_comentario_pr")

    # B-ML-02: disparadores reales de PR siguen mapeando
    def test_abrir_pr_mapea_pr(self):
        r = mano_local_simulada(_entrada("continuar_documental", "abrir pr de revision"))
        self.assertEqual(r["accion_simulada"], "preparar_comentario_pr")
        self.assertEqual(r["destino_simulado"], "github_pr")
        self.assertFalse(r["bloqueo"])

    def test_comentar_pr_mapea_pr(self):
        r = mano_local_simulada(_entrada("continuar_documental", "comentar pr"))
        self.assertEqual(r["accion_simulada"], "preparar_comentario_pr")

    def test_pull_request_mapea_pr(self):
        r = mano_local_simulada(_entrada("continuar_documental", "pull request de revision"))
        self.assertEqual(r["accion_simulada"], "preparar_comentario_pr")
        self.assertEqual(r["destino_simulado"], "github_pr")

    def test_pr_aislado_mapea_pr(self):
        r = mano_local_simulada(_entrada("continuar_documental", "revisá el pr"))
        self.assertEqual(r["accion_simulada"], "preparar_comentario_pr")

    # B-ML-03: "issue" como token aislado mapea correctamente
    def test_comentar_issue_mapea_issue(self):
        r = mano_local_simulada(_entrada("continuar_documental", "comentar issue"))
        self.assertEqual(r["accion_simulada"], "preparar_comentario_issue")
        self.assertEqual(r["destino_simulado"], "github_issue")
        self.assertFalse(r["bloqueo"])

    def test_github_issue_mapea_issue(self):
        r = mano_local_simulada(_entrada("continuar_documental", "github issue #5"))
        self.assertEqual(r["accion_simulada"], "preparar_comentario_issue")


if __name__ == "__main__":
    unittest.main()
