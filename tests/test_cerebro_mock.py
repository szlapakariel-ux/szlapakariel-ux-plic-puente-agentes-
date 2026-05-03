"""
Tests unitarios del Cerebro Portero Mock — PUENTE-1B
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

    def test_decision_valores_validos(self):
        decisiones_validas = {
            "continuar_documental", "pedir_autorizacion", "reformular",
            "suspender", "declarar_bloqueo", "escalar_a_ariel", "no_ejecutar",
        }
        for texto in [
            "seguí con lo del celu", "1", "pasalo a Claude",
            "mandalo a producción", "diagnóstico SOFSE", "suspender", "",
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
        ]:
            r = cerebro_mock({"texto_original": texto})
            self.assertIn(
                r["riesgo"], riesgos_validos,
                f"Riesgo inválido '{r['riesgo']}' para texto='{texto}'",
            )


if __name__ == "__main__":
    unittest.main()
