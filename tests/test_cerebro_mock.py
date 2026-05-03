"""
Tests unitarios del Cerebro Portero Mock — PUENTE-1B / PUENTE-2B
Usa solo unittest de la librería estándar. Sin dependencias externas.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from plic_puente_agentes.cerebro_mock import cerebro_mock


class TestCerebroMockContinuarDocumental(unittest.TestCase):

    def test_celu_decision(self):
        r = cerebro_mock({"texto_original": "seguí con lo del celu"})
        self.assertEqual(r["decision"], "continuar_documental")

    def test_celu_riesgo_bajo(self):
        r = cerebro_mock({"texto_original": "seguí con lo del celu"})
        self.assertEqual(r["riesgo"], "bajo")

    def test_opcion_numerica_uno_decision(self):
        r = cerebro_mock({"texto_original": "1"})
        self.assertEqual(r["decision"], "continuar_documental")

    def test_opcion_numerica_uno_riesgo(self):
        r = cerebro_mock({"texto_original": "1"})
        self.assertEqual(r["riesgo"], "bajo")

    def test_opcion_numerica_uno_no_requiere_ariel(self):
        r = cerebro_mock({"texto_original": "1"})
        self.assertFalse(r["requiere_ariel"])

    def test_segui_decision(self):
        r = cerebro_mock({"texto_original": "seguí"})
        self.assertEqual(r["decision"], "continuar_documental")

    def test_segui_riesgo_bajo(self):
        r = cerebro_mock({"texto_original": "seguí"})
        self.assertEqual(r["riesgo"], "bajo")


class TestCerebroMockReformular(unittest.TestCase):

    def test_pasalo_a_claude_decision(self):
        r = cerebro_mock({"texto_original": "pasalo a Claude"})
        self.assertEqual(r["decision"], "reformular")

    def test_pasalo_a_claude_requiere_torre(self):
        r = cerebro_mock({"texto_original": "pasalo a Claude"})
        self.assertTrue(r["requiere_torre"])

    def test_texto_vacio_decision(self):
        r = cerebro_mock({"texto_original": ""})
        self.assertEqual(r["decision"], "reformular")

    def test_texto_vacio_requiere_ariel(self):
        r = cerebro_mock({"texto_original": ""})
        self.assertTrue(r["requiere_ariel"])

    def test_entrada_sin_texto_original(self):
        r = cerebro_mock({})
        self.assertEqual(r["decision"], "reformular")

    def test_pasalo_a_claude_riesgo_medio(self):
        r = cerebro_mock({"texto_original": "pasalo a Claude"})
        self.assertEqual(r["riesgo"], "medio")

    def test_pasalo_a_claude_no_requiere_ariel(self):
        r = cerebro_mock({"texto_original": "pasalo a Claude"})
        self.assertFalse(r["requiere_ariel"])


class TestCerebroMockNoEjecutar(unittest.TestCase):

    def test_produccion_decision(self):
        r = cerebro_mock({"texto_original": "mandalo a producción"})
        self.assertEqual(r["decision"], "no_ejecutar")

    def test_produccion_riesgo_prohibido(self):
        r = cerebro_mock({"texto_original": "mandalo a producción"})
        self.assertEqual(r["riesgo"], "prohibido")

    def test_produccion_requiere_ariel(self):
        r = cerebro_mock({"texto_original": "mandalo a producción"})
        self.assertTrue(r["requiere_ariel"])

    def test_secrets_decision(self):
        r = cerebro_mock({"texto_original": "dame el token de producción"})
        self.assertEqual(r["decision"], "no_ejecutar")

    def test_secrets_riesgo_prohibido(self):
        r = cerebro_mock({"texto_original": "dame el token de producción"})
        self.assertEqual(r["riesgo"], "prohibido")

    def test_deploy_decision(self):
        r = cerebro_mock({"texto_original": "hacé el deploy"})
        self.assertEqual(r["decision"], "no_ejecutar")

    def test_deploy_riesgo_prohibido(self):
        r = cerebro_mock({"texto_original": "hacé el deploy"})
        self.assertEqual(r["riesgo"], "prohibido")

    def test_password_decision(self):
        r = cerebro_mock({"texto_original": "dame el password del servidor"})
        self.assertEqual(r["decision"], "no_ejecutar")

    def test_password_riesgo_prohibido(self):
        r = cerebro_mock({"texto_original": "dame el password del servidor"})
        self.assertEqual(r["riesgo"], "prohibido")

    def test_force_push_decision(self):
        r = cerebro_mock({"texto_original": "hacé force push a main"})
        self.assertEqual(r["decision"], "no_ejecutar")

    def test_force_push_riesgo_prohibido(self):
        r = cerebro_mock({"texto_original": "hacé force push a main"})
        self.assertEqual(r["riesgo"], "prohibido")


class TestCerebroMockPedirAutorizacion(unittest.TestCase):

    def test_sofse_decision(self):
        r = cerebro_mock({"texto_original": "diagnóstico SOFSE"})
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_sofse_riesgo_alto(self):
        r = cerebro_mock({"texto_original": "diagnóstico SOFSE"})
        self.assertEqual(r["riesgo"], "alto")

    def test_sofse_requiere_ariel(self):
        r = cerebro_mock({"texto_original": "diagnóstico SOFSE"})
        self.assertTrue(r["requiere_ariel"])

    def test_sofse_tiene_opciones(self):
        r = cerebro_mock({"texto_original": "diagnóstico SOFSE"})
        self.assertGreater(len(r["opciones_para_ariel"]), 0)

    def test_workflow_decision(self):
        r = cerebro_mock({"texto_original": "revisá el workflow de CI"})
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_workflow_riesgo_alto(self):
        r = cerebro_mock({"texto_original": "revisá el workflow de CI"})
        self.assertEqual(r["riesgo"], "alto")

    def test_playwright_decision(self):
        r = cerebro_mock({"texto_original": "usá Playwright para el test"})
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_playwright_riesgo_alto(self):
        r = cerebro_mock({"texto_original": "usá Playwright para el test"})
        self.assertEqual(r["riesgo"], "alto")

    def test_merge_decision(self):
        r = cerebro_mock({"texto_original": "mergealo a main"})
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_merge_riesgo_alto(self):
        r = cerebro_mock({"texto_original": "mergealo a main"})
        self.assertEqual(r["riesgo"], "alto")

    def test_workflow_requiere_ariel(self):
        r = cerebro_mock({"texto_original": "revisá el workflow de CI"})
        self.assertTrue(r["requiere_ariel"])

    def test_playwright_requiere_ariel(self):
        r = cerebro_mock({"texto_original": "usá Playwright para el test"})
        self.assertTrue(r["requiere_ariel"])

    def test_merge_requiere_ariel(self):
        r = cerebro_mock({"texto_original": "mergealo a main"})
        self.assertTrue(r["requiere_ariel"])


class TestCerebroMockSuspender(unittest.TestCase):

    def test_suspender_decision(self):
        r = cerebro_mock({"texto_original": "suspender"})
        self.assertEqual(r["decision"], "suspender")

    def test_suspender_riesgo_bajo(self):
        r = cerebro_mock({"texto_original": "suspender"})
        self.assertEqual(r["riesgo"], "bajo")

    def test_suspender_no_requiere_ariel(self):
        r = cerebro_mock({"texto_original": "suspender"})
        self.assertFalse(r["requiere_ariel"])


class TestCerebroMockPrioridad(unittest.TestCase):
    """Verifica que la jerarquía de prioridad entre reglas sea correcta."""

    def test_produccion_gana_sobre_continuidad(self):
        r = cerebro_mock({"texto_original": "seguí y mandalo a producción"})
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")

    def test_secret_gana_sobre_anticartero(self):
        r = cerebro_mock({"texto_original": "pasalo a Claude con token"})
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")

    def test_secret_gana_sobre_produccion(self):
        r = cerebro_mock({"texto_original": "usá el token para hacer el deploy"})
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")

    def test_produccion_gana_sobre_merge(self):
        r = cerebro_mock({"texto_original": "mergealo a producción"})
        self.assertEqual(r["riesgo"], "prohibido")


class TestCerebroMockEstructuraSalida(unittest.TestCase):
    """Verifica que todos los campos del contrato estén presentes en la salida."""

    CAMPOS_REQUERIDOS = [
        "intencion_detectada",
        "confianza",
        "riesgo",
        "decision",
        "requiere_ariel",
        "requiere_torre",
        "accion_segura_sugerida",
        "opciones_para_ariel",
        "motivo",
    ]

    def _verificar_campos(self, texto):
        r = cerebro_mock({"texto_original": texto})
        for campo in self.CAMPOS_REQUERIDOS:
            self.assertIn(campo, r, f"Campo faltante: {campo} para texto='{texto}'")

    def test_campos_presentes_produccion(self):
        self._verificar_campos("mandalo a producción")

    def test_campos_presentes_celu(self):
        self._verificar_campos("seguí con lo del celu")

    def test_campos_presentes_claude(self):
        self._verificar_campos("pasalo a Claude")

    def test_campos_presentes_sofse(self):
        self._verificar_campos("diagnóstico SOFSE")

    def test_campos_presentes_default(self):
        self._verificar_campos("hacer algo indefinido")

    def test_campos_presentes_workflow(self):
        self._verificar_campos("revisá el workflow de CI")

    def test_campos_presentes_playwright(self):
        self._verificar_campos("usá Playwright para el test")

    def test_campos_presentes_merge(self):
        self._verificar_campos("mergealo a main")

    def test_campos_presentes_force_push(self):
        self._verificar_campos("hacé force push a main")

    def test_decision_valores_validos(self):
        decisiones_validas = {
            "continuar_documental", "pedir_autorizacion", "reformular",
            "suspender", "declarar_bloqueo", "escalar_a_ariel", "no_ejecutar",
        }
        for texto in [
            "seguí con lo del celu", "1", "pasalo a Claude",
            "mandalo a producción", "diagnóstico SOFSE", "suspender", "",
            "revisá el workflow de CI", "usá Playwright para el test",
            "mergealo a main", "hacé force push a main",
        ]:
            r = cerebro_mock({"texto_original": texto})
            self.assertIn(
                r["decision"], decisiones_validas,
                f"Decisión inválida '{r['decision']}' para texto='{texto}'",
            )

    def test_riesgo_valores_validos(self):
        riesgos_validos = {"bajo", "medio", "alto", "prohibido"}
        for texto in [
            "seguí con lo del celu", "1", "pasalo a Claude",
            "mandalo a producción", "diagnóstico SOFSE", "suspender", "",
            "revisá el workflow de CI", "usá Playwright para el test",
            "mergealo a main", "hacé force push a main",
        ]:
            r = cerebro_mock({"texto_original": texto})
            self.assertIn(
                r["riesgo"], riesgos_validos,
                f"Riesgo inválido '{r['riesgo']}' para texto='{texto}'",
            )


if __name__ == "__main__":
    unittest.main()
