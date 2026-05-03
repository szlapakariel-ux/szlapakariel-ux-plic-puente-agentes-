"""
Cerebro Portero Mock — PUENTE-4D-BACKLOG
Corrección de estados suspendido y mergeado en continuidad.
Sin API real. Sin Claude Haiku. Sin I/O.
"""

_PALABRAS_SECRETS = ("secret", "secrets", "token", "clave", "credencial", "contraseña", "password", "api key")
_PALABRAS_PRODUCCION = ("producción", "produccion", "deploy", "publicar")
_TOKENS_PRODUCCION = ("prod",)
_PALABRAS_BORRAR = ("borrar", "eliminar", "force push", "reset hard")
_PALABRAS_WORKFLOW = (
    "workflow", "github actions", "github action",
    "continuous integration", "integración continua",
    "github ci", "ci pipeline", "action workflow", "actions workflow",
)
_TOKENS_WORKFLOW = ("ci",)
_PALABRAS_NAVEGADOR = ("navegador", "playwright", "browser", "chromium")
_PALABRAS_MERGE = ("merge", "mergealo", "cerrar pr", "aprobar pr")
_PALABRAS_REPOS_REALES = ("sofse", "auditoria-sofse", "agente-saas", "torre-control")
_PALABRAS_SUSPENSION = ("suspender", "frenar", "parar")
_PALABRAS_ANTICARTERO = ("pasalo a claude", "pasalo a codex", "mandalo a otro agente")
_PALABRAS_CONTINUIDAD = ("seguí", "seguir", "continuá", "seguimos")
_PALABRAS_API_REAL = ("api real", "usá api", "usa api", "usar api real")
_PALABRAS_ISSUE_COMENTAR = ("comentá el issue", "comenta el issue", "comentar issue", "comentar el issue")
_PALABRAS_ISSUE_CERRAR = ("cerrá el issue", "cerrar el issue", "cerrar issue", "cerrá issue")

_AUTORIZACIONES_PROHIBIDAS = frozenset({"puede_tocar_produccion", "puede_tocar_secrets"})


def _es_token(texto_lower, token):
    """Verifica si token aparece como palabra completa en texto_lower."""
    idx = texto_lower.find(token)
    while idx != -1:
        antes = idx == 0 or not texto_lower[idx - 1].isalpha()
        despues = (idx + len(token) == len(texto_lower) or
                   not texto_lower[idx + len(token)].isalpha())
        if antes and despues:
            return True
        idx = texto_lower.find(token, idx + 1)
    return False


def cerebro_mock(entrada: dict) -> dict:
    texto = entrada.get("texto_original", "") if isinstance(entrada, dict) else ""

    if isinstance(entrada, dict):
        contexto = entrada.get("contexto_actual")
        estado = entrada.get("estado_del_ciclo")
        autorizaciones_raw = entrada.get("autorizaciones_disponibles") or []
        if not isinstance(autorizaciones_raw, list):
            autorizaciones_raw = []
        autorizaciones = [a for a in autorizaciones_raw if a not in _AUTORIZACIONES_PROHIBIDAS]
    else:
        contexto = None
        estado = None
        autorizaciones = []

    if not isinstance(texto, str) or not texto.strip():
        return _respuesta(
            intencion="Intención no reconocible — texto vacío o inválido",
            confianza="baja",
            riesgo="medio",
            decision="reformular",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=["1) Reenviar con texto claro", "2) Suspender sesión"],
            motivo="El texto original está vacío o no es una cadena válida. No es posible interpretar la intención.",
        )

    texto_lower = texto.lower()

    # Prioridad 1 — secrets / credenciales
    if any(p in texto_lower for p in _PALABRAS_SECRETS):
        if "puede_tocar_secrets" in (entrada.get("autorizaciones_disponibles") or []):
            return _respuesta(
                intencion="Acceso o manipulación de credenciales o secrets",
                confianza="alta",
                riesgo="alto",
                decision="pedir_autorizacion",
                requiere_ariel=True,
                requiere_torre=True,
                accion=None,
                opciones=[],
                motivo="puede_tocar_secrets aparece en autorizaciones_disponibles, pero es prohibición absoluta del sistema. Requiere autorización explícita y ciclo específico.",
            )
        return _respuesta(
            intencion="Acceso o manipulación de credenciales o secrets",
            confianza="alta",
            riesgo="prohibido",
            decision="no_ejecutar",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[],
            motivo="Secrets y credenciales son prohibición absoluta según reglas PLIC. No se ejecuta.",
        )

    # Prioridad 2 — producción / deploy
    if (any(p in texto_lower for p in _PALABRAS_PRODUCCION) or
            any(_es_token(texto_lower, t) for t in _TOKENS_PRODUCCION)):
        if "puede_tocar_produccion" in (entrada.get("autorizaciones_disponibles") or []):
            return _respuesta(
                intencion="Acción sobre entorno de producción o deploy",
                confianza="alta",
                riesgo="alto",
                decision="pedir_autorizacion",
                requiere_ariel=True,
                requiere_torre=True,
                accion=None,
                opciones=[
                    "1) Autorizar acción en producción con revisión explícita",
                    "2) Rechazar — sin tocar producción en este ciclo",
                ],
                motivo="puede_tocar_produccion está en autorizaciones_disponibles, pero producción requiere verificación previa de Torre. La autorización disponible no equivale a ejecución automática.",
            )
        return _respuesta(
            intencion="Acción sobre entorno de producción o deploy",
            confianza="alta",
            riesgo="prohibido",
            decision="no_ejecutar",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[],
            motivo="Producción y deploy son riesgo prohibido según reglas PLIC. No se ejecuta bajo ninguna circunstancia.",
        )

    # Prioridad 3 — borrar / force push / reset hard
    if any(p in texto_lower for p in _PALABRAS_BORRAR):
        return _respuesta(
            intencion="Acción destructiva — borrado, eliminación o reset forzado",
            confianza="alta",
            riesgo="prohibido",
            decision="no_ejecutar",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[],
            motivo="Borrar archivos y force push son prohibición absoluta según reglas PLIC.",
        )

    # Prioridad 4 — API real
    if any(p in texto_lower for p in _PALABRAS_API_REAL):
        if "puede_usar_api_real" in autorizaciones:
            return _respuesta(
                intencion="Uso de API real o Claude Haiku",
                confianza="alta",
                riesgo="alto",
                decision="pedir_autorizacion",
                requiere_ariel=True,
                requiere_torre=True,
                accion=None,
                opciones=[
                    "1) Autorizar uso de API real en microciclo específico (PUENTE-5+)",
                    "2) Rechazar — sin API real en este ciclo",
                ],
                motivo="puede_usar_api_real está en autorizaciones_disponibles, pero el uso de API real requiere ciclo específico autorizado (PUENTE-5+). La autorización disponible no habilita ejecución inmediata.",
            )
        return _respuesta(
            intencion="Uso de API real o Claude Haiku",
            confianza="alta",
            riesgo="prohibido",
            decision="no_ejecutar",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[],
            motivo="API real no está en autorizaciones_disponibles y no está habilitada en este ciclo. Requiere PUENTE-5 o posterior.",
        )

    # Prioridad 5 — estado_del_ciclo: pr_abierto + continuidad
    if estado == "pr_abierto" and (
        texto.strip() == "1" or any(p in texto_lower for p in _PALABRAS_CONTINUIDAD)
    ):
        return _respuesta(
            intencion="Continuación solicitada con PR abierto",
            confianza="alta",
            riesgo="medio",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Autorizar merge del PR abierto antes de continuar",
                "2) Cerrar PR sin merge y continuar en nueva rama",
                "3) Suspender hasta decisión sobre el PR",
            ],
            motivo="estado_del_ciclo es 'pr_abierto'. Hay un PR abierto esperando resolución. No se puede avanzar hasta cerrarlo o decidir qué hacer con él.",
        )

    # Prioridad 6 — estado_del_ciclo: bloqueado + continuidad
    if estado == "bloqueado" and (
        texto.strip() == "1" or any(p in texto_lower for p in _PALABRAS_CONTINUIDAD)
    ):
        return _respuesta(
            intencion="Continuación solicitada con ciclo bloqueado",
            confianza="alta",
            riesgo="alto",
            decision="declarar_bloqueo",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Documentar bloqueo y escalar a Ariel",
                "2) Suspender ciclo hasta resolución del bloqueo",
            ],
            motivo="estado_del_ciclo es 'bloqueado'. Hay una condición bloqueante activa. No se puede continuar sin resolver o documentar el bloqueo.",
        )

    # Prioridad 7 — workflows / CI
    if (any(p in texto_lower for p in _PALABRAS_WORKFLOW) or
            any(_es_token(texto_lower, t) for t in _TOKENS_WORKFLOW)):
        return _respuesta(
            intencion="Acción relacionada con workflows o CI/CD",
            confianza="alta",
            riesgo="alto",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Autorizar revisión de workflow en modo solo-lectura",
                "2) Rechazar — sin tocar CI/CD en este ciclo",
                "3) Escalar para definir microciclo específico de workflows",
            ],
            motivo="Workflows y CI/CD requieren autorización explícita de Ariel antes de continuar.",
        )

    # Prioridad 8 — navegador / Playwright
    if any(p in texto_lower for p in _PALABRAS_NAVEGADOR):
        if "puede_usar_navegador" in autorizaciones:
            motivo_nav = "puede_usar_navegador está en autorizaciones_disponibles, pero el uso de navegador requiere ciclo específico autorizado (PUENTE-4+). La autorización disponible no habilita ejecución inmediata."
        else:
            motivo_nav = "Navegador y Playwright requieren ciclo específico autorizado (PUENTE-4+). puede_usar_navegador no está en autorizaciones_disponibles."
        return _respuesta(
            intencion="Acción que requiere navegador o Playwright",
            confianza="alta",
            riesgo="alto",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Autorizar uso de navegador en microciclo específico",
                "2) Rechazar — sin navegador en este ciclo",
            ],
            motivo=motivo_nav,
        )

    # Prioridad 9 — merge / PR
    if any(p in texto_lower for p in _PALABRAS_MERGE):
        if "puede_mergear" in autorizaciones:
            motivo_merge = "puede_mergear está en autorizaciones_disponibles, pero el merge requiere verificación previa de Torre antes de ejecutar."
        else:
            motivo_merge = "Merge y PR requieren autorización explícita de Ariel. puede_mergear no está en autorizaciones_disponibles."
        return _respuesta(
            intencion="Acción de merge o gestión de PR",
            confianza="alta",
            riesgo="alto",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Autorizar merge con revisión previa",
                "2) Rechazar — sin merge en este ciclo",
            ],
            motivo=motivo_merge,
        )

    # Prioridad 10 — issue: comentar
    if any(p in texto_lower for p in _PALABRAS_ISSUE_COMENTAR):
        if "puede_comentar_issue" in autorizaciones:
            motivo_comentar = "puede_comentar_issue está en autorizaciones_disponibles, pero comentar un issue real requiere verificación previa de Torre."
        else:
            motivo_comentar = "Comentar un issue real requiere autorización explícita. puede_comentar_issue no está en autorizaciones_disponibles."
        return _respuesta(
            intencion="Comentar en issue real del repositorio",
            confianza="alta",
            riesgo="alto",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Autorizar comentario en issue con texto revisado",
                "2) Rechazar — sin comentarios en issues en este ciclo",
            ],
            motivo=motivo_comentar,
        )

    # Prioridad 11 — issue: cerrar
    if any(p in texto_lower for p in _PALABRAS_ISSUE_CERRAR):
        if "puede_cerrar_issue" in autorizaciones:
            motivo_cerrar = "puede_cerrar_issue está en autorizaciones_disponibles, pero cerrar un issue real requiere verificación previa de Torre."
        else:
            motivo_cerrar = "Cerrar un issue real requiere autorización explícita. puede_cerrar_issue no está en autorizaciones_disponibles."
        return _respuesta(
            intencion="Cerrar issue real del repositorio",
            confianza="alta",
            riesgo="alto",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Autorizar cierre del issue con confirmación",
                "2) Rechazar — sin cierre de issues en este ciclo",
            ],
            motivo=motivo_cerrar,
        )

    # Prioridad 12 — repos reales (con contexto de repo autorizado)
    if any(p in texto_lower for p in _PALABRAS_REPOS_REALES):
        repo_actual = None
        if isinstance(contexto, dict):
            repo_actual = contexto.get("repo_autorizado_actual")
        if repo_actual:
            motivo_repo = f"El texto menciona un proyecto externo que no coincide con el repo autorizado actual ({repo_actual}). Requiere autorización explícita y ciclo específico."
        else:
            motivo_repo = "El texto involucra un repositorio o proyecto real externo. Requiere autorización explícita."
        return _respuesta(
            intencion="Acción que involucra repositorio o proyecto real externo",
            confianza="alta",
            riesgo="alto",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Autorizar acción de solo-lectura sobre el proyecto mencionado",
                "2) Rechazar — sin tocar repos externos en este ciclo",
                "3) Escalar para definir microciclo específico",
            ],
            motivo=motivo_repo,
        )

    # Prioridad 13 — suspensión
    if any(p in texto_lower for p in _PALABRAS_SUSPENSION):
        return _respuesta(
            intencion="Solicitud de pausa o suspensión del ciclo activo",
            confianza="alta",
            riesgo="bajo",
            decision="suspender",
            requiere_ariel=False,
            requiere_torre=False,
            accion=None,
            opciones=[],
            motivo="Ariel solicitó suspender. Se pausa el ciclo activo hasta nueva instrucción.",
        )

    # Prioridad 14 — anti-cartero
    if any(p in texto_lower for p in _PALABRAS_ANTICARTERO):
        return _respuesta(
            intencion="Transferencia directa a otro agente sin estructuración",
            confianza="media",
            riesgo="medio",
            decision="reformular",
            requiere_ariel=False,
            requiere_torre=True,
            accion=None,
            opciones=[],
            motivo="Torre debe reformular la intención antes de transferir para evitar que Ariel actúe como cartero.",
        )

    # B-04 — estado_del_ciclo: suspendido + continuidad
    if estado == "suspendido" and (
        texto.strip() == "1" or any(p in texto_lower for p in _PALABRAS_CONTINUIDAD)
    ):
        return _respuesta(
            intencion="Continuación solicitada con ciclo suspendido",
            confianza="alta",
            riesgo="medio",
            decision="pedir_autorizacion",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=[
                "1) Revisar el estado del ciclo suspendido con Ariel antes de continuar",
                "2) Cerrar el ciclo suspendido y abrir uno nuevo",
                "3) Mantener suspensión hasta nueva instrucción",
            ],
            motivo="estado_del_ciclo es 'suspendido'. Un ciclo suspendido no puede retomarse automáticamente — requiere revisión y autorización explícita de Ariel y Torre antes de continuar.",
        )

    # Prioridad 15 — "1" con/sin opciones previas (cuando contexto_actual está presente)
    if texto.strip() == "1" and contexto is not None:
        ultimo_output = None
        if isinstance(contexto, dict):
            ultimo_output = contexto.get("ultimo_output_portero")
        opciones_previas = None
        if isinstance(ultimo_output, dict):
            opciones_previas = ultimo_output.get("opciones_para_ariel")
        if opciones_previas and isinstance(opciones_previas, list) and len(opciones_previas) > 0:
            return _respuesta(
                intencion="Elección de opción 1 del menú previo del Portero",
                confianza="alta",
                riesgo="bajo",
                decision="continuar_documental",
                requiere_ariel=False,
                requiere_torre=True,
                accion="Continuar con la opción 1 del último output del Portero",
                opciones=[],
                motivo="texto_original '1' interpretado como elección de opción 1 usando contexto_actual.ultimo_output_portero.opciones_para_ariel.",
            )
        return _respuesta(
            intencion="Opción numérica sin contexto suficiente",
            confianza="baja",
            riesgo="medio",
            decision="reformular",
            requiere_ariel=True,
            requiere_torre=True,
            accion=None,
            opciones=["1) Reenviar con texto explícito", "2) Suspender sesión"],
            motivo="texto_original es '1' pero contexto_actual no contiene opciones_para_ariel previas válidas. No es posible interpretar a qué opción refiere.",
        )

    # Prioridad 16 — continuidad segura
    if texto.strip() == "1" or any(p in texto_lower for p in _PALABRAS_CONTINUIDAD):
        if estado == "cerrado":
            motivo_cont = "Intención de continuación reconocida. estado_del_ciclo es 'cerrado' — el ciclo anterior está completo. Torre confirma contexto del nuevo ciclo antes de ejecutar."
        elif estado == "mergeado":
            motivo_cont = "Intención de continuación reconocida. estado_del_ciclo es 'mergeado' — el ciclo anterior fue mergeado correctamente. Torre confirma contexto del próximo paso documental antes de ejecutar."
        else:
            motivo_cont = "Intención de continuación reconocida. Riesgo bajo. Torre confirma contexto antes de ejecutar."
        return _respuesta(
            intencion="Continuación del ciclo activo",
            confianza="alta",
            riesgo="bajo",
            decision="continuar_documental",
            requiere_ariel=False,
            requiere_torre=True,
            accion="Continuar con el objetivo activo según contexto previo",
            opciones=[],
            motivo=motivo_cont,
        )

    # Prioridad 17 — default
    return _respuesta(
        intencion="Intención no clasificada por las reglas actuales del mock",
        confianza="baja",
        riesgo="medio",
        decision="reformular",
        requiere_ariel=False,
        requiere_torre=True,
        accion=None,
        opciones=[
            "1) Reformular la intención con más detalle",
            "2) Suspender y volver luego",
        ],
        motivo="El texto no coincide con ninguna regla conocida. Torre debe reformular antes de continuar.",
    )


def _respuesta(
    intencion: str,
    confianza: str,
    riesgo: str,
    decision: str,
    requiere_ariel: bool,
    requiere_torre: bool,
    accion,
    opciones: list,
    motivo: str,
) -> dict:
    return {
        "intencion_detectada": intencion,
        "confianza": confianza,
        "riesgo": riesgo,
        "decision": decision,
        "requiere_ariel": requiere_ariel,
        "requiere_torre": requiere_torre,
        "accion_segura_sugerida": accion,
        "opciones_para_ariel": opciones,
        "motivo": motivo,
    }
