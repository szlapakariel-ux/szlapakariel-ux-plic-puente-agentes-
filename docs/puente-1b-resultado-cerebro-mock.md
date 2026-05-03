# PUENTE-1B — Resultado: Cerebro Portero Mock

## 1. Estado inicial

| Campo | Valor |
|---|---|
| Microciclo | PUENTE-1B |
| Rama base | `main` |
| Commit base | `227a3378eaf68763446c1e80e952e1ff62f97146` |
| Rama de trabajo | `feat/puente-1b-cerebro-mock` |
| Estado de PUENTE-1A | Cerrado — contrato mergeado a main |
| Contrato de referencia | `docs/contrato-cerebro-mock.md` |

---

## 2. Archivos creados

| Archivo | Tipo | Descripción |
|---|---|---|
| `src/plic_puente_agentes/__init__.py` | Python | Marcador de paquete. Sin lógica. |
| `src/plic_puente_agentes/cerebro_mock.py` | Python | Implementación de `cerebro_mock()` con reglas hardcodeadas. |
| `tests/test_cerebro_mock.py` | Python | 29 tests unitarios con `unittest` de librería estándar. |
| `docs/puente-1b-resultado-cerebro-mock.md` | Documental | Este archivo — evidencia de cierre del ciclo. |

---

## 3. Qué implementa cerebro_mock

La función `cerebro_mock(entrada: dict) -> dict` ubicada en `src/plic_puente_agentes/cerebro_mock.py`:

- Recibe un `dict` con el campo `texto_original` (y opcionalmente los demás campos del contrato PUENTE-1A).
- Evalúa el texto contra 9 reglas hardcodeadas en orden de prioridad.
- Devuelve un `dict` con los 9 campos del contrato: `intencion_detectada`, `confianza`, `riesgo`, `decision`, `requiere_ariel`, `requiere_torre`, `accion_segura_sugerida`, `opciones_para_ariel`, `motivo`.
- No realiza ninguna llamada externa. No usa imports fuera de la librería estándar Python.

---

## 4. Qué NO implementa

| Capacidad | Estado |
|---|---|
| Claude Haiku API | No implementado — PUENTE-5 en adelante |
| Gemini API | No implementado |
| Playwright / navegador | No implementado — PUENTE-4 en adelante |
| Motor de reglas dinámico | No implementado — reglas hardcodeadas únicamente |
| Persistencia de estado | No implementado |
| Contexto entre llamadas | No implementado — cada llamada es independiente |
| Campos de entrada opcionales usados | No implementado — solo `texto_original` es evaluado |

---

## 5. Reglas hardcodeadas incluidas

| # | Condición | Decisión | Riesgo |
|---|---|---|---|
| 1 | Texto contiene "producción" | `no_ejecutar` | `prohibido` |
| 2 | Texto contiene "secrets", "token", "clave" o "credencial" | `no_ejecutar` | `prohibido` |
| 3 | Texto contiene "pasalo a Claude" | `reformular` | `medio` |
| 4 | Texto es exactamente `"1"` | `continuar_documental` | `bajo` |
| 5 | Texto contiene "seguí con lo del celu" | `continuar_documental` | `bajo` |
| 6 | Texto contiene "SOFSE" o "sofse" | `pedir_autorizacion` | `alto` |
| 7 | Texto contiene "suspender" | `suspender` | `bajo` |
| 8 | Texto vacío o no es string | `reformular` | `medio` |
| 9 | Cualquier otro texto (default) | `reformular` | `medio` |

---

## 6. Tests creados

29 tests organizados en 6 clases:

| Clase | Tests | Qué cubre |
|---|---|---|
| `TestCerebroMockContinuarDocumental` | 5 | `"seguí con lo del celu"`, `"1"` |
| `TestCerebroMockReformular` | 5 | `"pasalo a Claude"`, texto vacío, entrada sin campo |
| `TestCerebroMockNoEjecutar` | 5 | `"mandalo a producción"`, `"token"` |
| `TestCerebroMockPedirAutorizacion` | 4 | `"diagnóstico SOFSE"` |
| `TestCerebroMockSuspender` | 3 | `"suspender"` |
| `TestCerebroMockEstructuraSalida` | 7 | Campos requeridos, valores válidos de decisión y riesgo |

---

## 7. Resultado del test

```
python -m unittest discover -s tests -v

Ran 29 tests in 0.001s

OK
```

Todos los tests pasan. Sin errores. Sin warnings.

---

## 8. Confirmaciones de seguridad

| Verificación | Estado |
|---|---|
| Sin Claude Haiku API real | CONFIRMADO |
| Sin API real de ningún tipo | CONFIRMADO |
| Sin imports externos | CONFIRMADO — solo `sys`, `os`, `unittest` de stdlib |
| Sin secrets ni .env | CONFIRMADO |
| Sin workflows | CONFIRMADO |
| Sin producción | CONFIRMADO |
| Sin navegador | CONFIRMADO |
| Sin Playwright | CONFIRMADO |
| Sin dependencias instaladas | CONFIRMADO — solo stdlib Python |
| Sin torre-control | CONFIRMADO |
| Sin agente-saas | CONFIRMADO |
| Sin auditoria-sofse | CONFIRMADO |
| Sin plic-laboratorio-portero | CONFIRMADO |
| Sin PR abierto | CONFIRMADO |
| Sin merge | CONFIRMADO |

---

## 9. Próximo microciclo sugerido

**PUENTE-1C — Auditoría técnica del Cerebro Portero Mock y decisión de integración mínima**

Objetivo: revisar la implementación de PUENTE-1B, validar que el contrato está respetado, identificar casos edge no cubiertos, y decidir si se necesita una integración mínima antes de avanzar a PUENTE-2 (Mock de reglas PLIC) o si PUENTE-1B es suficiente para cerrar la fase 1.

> Este microciclo no debe iniciarse hasta que PUENTE-1B esté cerrado con evidencia verificable (commit + push).
