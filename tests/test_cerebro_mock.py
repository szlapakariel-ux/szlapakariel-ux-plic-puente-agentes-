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


class TestCerebroMockContextoEstado(unittest.TestCase):
    """PUENTE-3B: evaluación de estado_del_ciclo en decisiones de continuidad."""

    def test_segui_estado_cerrado_decision(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "cerrado"})
        self.assertEqual(r["decision"], "continuar_documental")

    def test_segui_estado_cerrado_riesgo(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "cerrado"})
        self.assertEqual(r["riesgo"], "bajo")

    def test_segui_estado_pr_abierto_decision(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "pr_abierto"})
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_segui_estado_pr_abierto_riesgo(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "pr_abierto"})
        self.assertEqual(r["riesgo"], "medio")

    def test_segui_estado_pr_abierto_requiere_ariel(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "pr_abierto"})
        self.assertTrue(r["requiere_ariel"])

    def test_segui_estado_bloqueado_decision(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "bloqueado"})
        self.assertEqual(r["decision"], "declarar_bloqueo")

    def test_segui_estado_bloqueado_riesgo(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "bloqueado"})
        self.assertEqual(r["riesgo"], "alto")

    def test_segui_estado_bloqueado_requiere_ariel(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "bloqueado"})
        self.assertTrue(r["requiere_ariel"])


class TestCerebroMockContextoActual(unittest.TestCase):
    """PUENTE-3B: evaluación de contexto_actual para opciones previas."""

    def test_uno_con_opciones_previas_decision(self):
        r = cerebro_mock({
            "texto_original": "1",
            "contexto_actual": {
                "ultimo_output_portero": {
                    "opciones_para_ariel": ["1) Continuar con docs", "2) Suspender"]
                }
            },
        })
        self.assertEqual(r["decision"], "continuar_documental")

    def test_uno_con_opciones_previas_riesgo(self):
        r = cerebro_mock({
            "texto_original": "1",
            "contexto_actual": {
                "ultimo_output_portero": {
                    "opciones_para_ariel": ["1) Continuar con docs"]
                }
            },
        })
        self.assertEqual(r["riesgo"], "bajo")

    def test_uno_sin_opciones_previas_decision(self):
        r = cerebro_mock({
            "texto_original": "1",
            "contexto_actual": {"ultimo_output_portero": None},
        })
        self.assertEqual(r["decision"], "reformular")

    def test_uno_sin_opciones_previas_riesgo(self):
        r = cerebro_mock({
            "texto_original": "1",
            "contexto_actual": {"ultimo_output_portero": None},
        })
        self.assertEqual(r["riesgo"], "medio")

    def test_uno_sin_opciones_previas_requiere_ariel(self):
        r = cerebro_mock({
            "texto_original": "1",
            "contexto_actual": {"ultimo_output_portero": None},
        })
        self.assertTrue(r["requiere_ariel"])


class TestCerebroMockAutorizaciones(unittest.TestCase):
    """PUENTE-3B: evaluación de autorizaciones_disponibles."""

    def test_merge_sin_autorizacion_motivo_menciona_campo(self):
        r = cerebro_mock({"texto_original": "mergealo a main"})
        self.assertIn("puede_mergear", r["motivo"])

    def test_merge_con_autorizacion_decision(self):
        r = cerebro_mock({
            "texto_original": "mergealo a main",
            "autorizaciones_disponibles": ["puede_mergear"],
        })
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_merge_con_autorizacion_riesgo(self):
        r = cerebro_mock({
            "texto_original": "mergealo a main",
            "autorizaciones_disponibles": ["puede_mergear"],
        })
        self.assertEqual(r["riesgo"], "alto")

    def test_comentar_issue_decision(self):
        r = cerebro_mock({"texto_original": "comentá el issue"})
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_comentar_issue_riesgo(self):
        r = cerebro_mock({"texto_original": "comentá el issue"})
        self.assertEqual(r["riesgo"], "alto")

    def test_cerrar_issue_decision(self):
        r = cerebro_mock({"texto_original": "cerrá el issue"})
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_cerrar_issue_riesgo(self):
        r = cerebro_mock({"texto_original": "cerrá el issue"})
        self.assertEqual(r["riesgo"], "alto")

    def test_api_real_sin_autorizacion_decision(self):
        r = cerebro_mock({"texto_original": "usá API real"})
        self.assertEqual(r["decision"], "no_ejecutar")

    def test_api_real_sin_autorizacion_riesgo(self):
        r = cerebro_mock({"texto_original": "usá API real"})
        self.assertEqual(r["riesgo"], "prohibido")

    def test_api_real_con_autorizacion_decision(self):
        r = cerebro_mock({
            "texto_original": "usá API real",
            "autorizaciones_disponibles": ["puede_usar_api_real"],
        })
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_api_real_con_autorizacion_riesgo(self):
        r = cerebro_mock({
            "texto_original": "usá API real",
            "autorizaciones_disponibles": ["puede_usar_api_real"],
        })
        self.assertEqual(r["riesgo"], "alto")

    def test_produccion_con_autorizacion_decision(self):
        r = cerebro_mock({
            "texto_original": "mandalo a producción",
            "autorizaciones_disponibles": ["puede_tocar_produccion"],
        })
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_produccion_con_autorizacion_riesgo(self):
        r = cerebro_mock({
            "texto_original": "mandalo a producción",
            "autorizaciones_disponibles": ["puede_tocar_produccion"],
        })
        self.assertEqual(r["riesgo"], "alto")

    def test_secrets_con_autorizacion_decision(self):
        r = cerebro_mock({
            "texto_original": "usa el token",
            "autorizaciones_disponibles": ["puede_tocar_secrets"],
        })
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_secrets_con_autorizacion_riesgo(self):
        r = cerebro_mock({
            "texto_original": "usa el token",
            "autorizaciones_disponibles": ["puede_tocar_secrets"],
        })
        self.assertEqual(r["riesgo"], "alto")

    def test_sofse_con_repo_autorizado_distinto_motivo(self):
        repo = "szlapakariel-ux/szlapakariel-ux-plic-puente-agentes-"
        r = cerebro_mock({
            "texto_original": "diagnóstico SOFSE",
            "contexto_actual": {"repo_autorizado_actual": repo},
        })
        self.assertEqual(r["decision"], "pedir_autorizacion")
        self.assertIn(repo, r["motivo"])

    def test_api_real_gana_sobre_continuidad(self):
        r = cerebro_mock({"texto_original": "seguí y usá API real"})
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")


class TestCerebroMockFalsoPositivos(unittest.TestCase):
    """PUENTE-3C-BACKLOG: verifica que keywords cortas no generan falsos positivos."""

    # B-01: "ci" no dispara en palabras españolas
    def test_microciclo_no_dispara_workflow(self):
        r = cerebro_mock({"texto_original": "el microciclo avanza"})
        self.assertNotEqual(r["decision"], "pedir_autorizacion")
        self.assertEqual(r["decision"], "reformular")

    def test_accion_documental_no_dispara_workflow(self):
        r = cerebro_mock({"texto_original": "la acción documental está lista"})
        self.assertNotEqual(r["riesgo"], "alto")
        self.assertEqual(r["decision"], "reformular")

    def test_servicio_activo_no_dispara_workflow(self):
        r = cerebro_mock({"texto_original": "servicio activo"})
        self.assertEqual(r["decision"], "reformular")

    # B-02: "prod" no dispara en palabras como producto/producir/reproducir
    def test_producto_no_dispara_produccion(self):
        r = cerebro_mock({"texto_original": "revisá el producto"})
        self.assertNotEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["decision"], "reformular")

    def test_producir_documentacion_no_dispara_produccion(self):
        r = cerebro_mock({"texto_original": "vamos a producir documentación"})
        self.assertNotEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["decision"], "reformular")

    def test_reproducir_no_dispara_produccion(self):
        r = cerebro_mock({"texto_original": "reproducir el caso"})
        self.assertNotEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["decision"], "reformular")

    # Disparadores reales siguen funcionando
    def test_activar_ci_dispara_workflow(self):
        r = cerebro_mock({"texto_original": "activar CI"})
        self.assertEqual(r["decision"], "pedir_autorizacion")
        self.assertEqual(r["riesgo"], "alto")

    def test_github_actions_dispara_workflow(self):
        r = cerebro_mock({"texto_original": "github actions"})
        self.assertEqual(r["decision"], "pedir_autorizacion")
        self.assertEqual(r["riesgo"], "alto")

    def test_crear_workflow_dispara_workflow(self):
        r = cerebro_mock({"texto_original": "crear workflow"})
        self.assertEqual(r["decision"], "pedir_autorizacion")
        self.assertEqual(r["riesgo"], "alto")

    def test_mandalo_a_prod_dispara_produccion(self):
        r = cerebro_mock({"texto_original": "mandalo a prod"})
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")

    def test_deploy_a_produccion_dispara_produccion(self):
        r = cerebro_mock({"texto_original": "deploy a producción"})
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")

    def test_entorno_prod_dispara_produccion(self):
        r = cerebro_mock({"texto_original": "entorno prod"})
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")


class TestCerebroMockEstadosSuspendidoMergeado(unittest.TestCase):
    """PUENTE-4D-BACKLOG: B-04 estado suspendido + B-05 estado mergeado."""

    # B-04: estado suspendido + continuidad → pedir_autorizacion / medio
    def test_segui_estado_suspendido_decision(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "suspendido"})
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_segui_estado_suspendido_riesgo(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "suspendido"})
        self.assertEqual(r["riesgo"], "medio")

    def test_continua_estado_suspendido_decision(self):
        r = cerebro_mock({"texto_original": "continuá", "estado_del_ciclo": "suspendido"})
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_continua_estado_suspendido_riesgo(self):
        r = cerebro_mock({"texto_original": "continuá", "estado_del_ciclo": "suspendido"})
        self.assertEqual(r["riesgo"], "medio")

    def test_uno_estado_suspendido_decision(self):
        r = cerebro_mock({"texto_original": "1", "estado_del_ciclo": "suspendido"})
        self.assertEqual(r["decision"], "pedir_autorizacion")

    def test_uno_estado_suspendido_riesgo(self):
        r = cerebro_mock({"texto_original": "1", "estado_del_ciclo": "suspendido"})
        self.assertEqual(r["riesgo"], "medio")

    def test_suspendido_motivo_menciona_suspendido(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "suspendido"})
        self.assertIn("suspendido", r["motivo"])

    def test_suspendido_requiere_ariel(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "suspendido"})
        self.assertTrue(r["requiere_ariel"])

    def test_suspendido_requiere_torre(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "suspendido"})
        self.assertTrue(r["requiere_torre"])

    # B-05: estado mergeado + continuidad → continuar_documental / bajo
    def test_segui_estado_mergeado_decision(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "mergeado"})
        self.assertEqual(r["decision"], "continuar_documental")

    def test_segui_estado_mergeado_riesgo(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "mergeado"})
        self.assertEqual(r["riesgo"], "bajo")

    def test_continua_estado_mergeado_decision(self):
        r = cerebro_mock({"texto_original": "continuá", "estado_del_ciclo": "mergeado"})
        self.assertEqual(r["decision"], "continuar_documental")

    def test_continua_estado_mergeado_riesgo(self):
        r = cerebro_mock({"texto_original": "continuá", "estado_del_ciclo": "mergeado"})
        self.assertEqual(r["riesgo"], "bajo")

    def test_uno_estado_mergeado_decision(self):
        r = cerebro_mock({"texto_original": "1", "estado_del_ciclo": "mergeado"})
        self.assertEqual(r["decision"], "continuar_documental")

    def test_uno_estado_mergeado_riesgo(self):
        r = cerebro_mock({"texto_original": "1", "estado_del_ciclo": "mergeado"})
        self.assertEqual(r["riesgo"], "bajo")

    def test_mergeado_motivo_menciona_mergeado(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "mergeado"})
        self.assertIn("mergeado", r["motivo"])

    def test_mergeado_no_requiere_ariel(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "mergeado"})
        self.assertFalse(r["requiere_ariel"])

    def test_mergeado_requiere_torre(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "mergeado"})
        self.assertTrue(r["requiere_torre"])

    # Prioridad: reglas restrictivas ganan sobre los estados
    def test_produccion_gana_sobre_suspendido(self):
        r = cerebro_mock({"texto_original": "seguí y mandalo a producción", "estado_del_ciclo": "suspendido"})
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")

    def test_api_real_gana_sobre_mergeado(self):
        r = cerebro_mock({"texto_original": "seguí y usá API real", "estado_del_ciclo": "mergeado"})
        self.assertEqual(r["decision"], "no_ejecutar")
        self.assertEqual(r["riesgo"], "prohibido")

    def test_merge_gana_sobre_suspendido(self):
        r = cerebro_mock({"texto_original": "seguí y mergealo", "estado_del_ciclo": "suspendido"})
        self.assertEqual(r["decision"], "pedir_autorizacion")
        self.assertEqual(r["riesgo"], "alto")

    # Regresión: estado cerrado sigue funcionando
    def test_segui_estado_cerrado_regresion_decision(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "cerrado"})
        self.assertEqual(r["decision"], "continuar_documental")

    def test_segui_estado_cerrado_regresion_riesgo(self):
        r = cerebro_mock({"texto_original": "seguí", "estado_del_ciclo": "cerrado"})
        self.assertEqual(r["riesgo"], "bajo")


if __name__ == "__main__":
    unittest.main()
