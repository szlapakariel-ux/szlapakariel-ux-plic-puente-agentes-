# PUENTE-6D-A — Contrato operativo para primera llamada real

## 1. Nombre del contrato

| Campo | Valor |
|---|---|
| Contrato | PUENTE-6D-A |
| Tipo | Documental — sin ejecución real |
| Fecha | 2026-05-04 |
| Rama base | `main` |
| Commit base | `425b52001efe114a67866144ad1735b1155ae8f8` (B-07 incluido) |
| Fase previa cerrada | PUENTE-6B-BACKLOG — validación de `request_id` cerrada en main |
| Tests al abrir | 339/339 OK |

**Este contrato no ejecuta ninguna llamada real.** No usa API real, no usa SDK real, no usa keys reales, no modifica código, no modifica tests.

---

## 2. Objetivo de PUENTE-6D-A

Definir de forma verificable y sin ejecutar ninguna acción real:

- Qué es y qué no es una "primera llamada real" en el contexto de PLIC.
- Qué precondiciones deben cumplirse antes de intentar cualquier llamada real.
- Cuál es el prompt exacto permitido para la primera prueba.
- Qué modelo está autorizado para la primera prueba.
- Cómo se maneja la variable `ANTHROPIC_API_KEY` de forma segura.
- Qué datos están prohibidos en la entrada, en la salida y en los logs.
- Qué evidencia debe quedar registrada.
- Cuáles son las condiciones de corte obligatorias.
- Cuál es el fallback obligatorio si algo falla.
- Qué criterios deben cumplirse para habilitar PUENTE-6D real.

PUENTE-6D-A no autoriza ninguna llamada real. Solo define el piso operativo para que PUENTE-6D real sea responsable y trazable.

---

## 3. Qué significa "primera llamada real"

Una "primera llamada real" es una invocación efectiva de `POST https://api.anthropic.com/v1/messages` con:
- Una `ANTHROPIC_API_KEY` válida cargada desde variable de entorno local.
- Un payload mínimo y controlado.
- Un modelo autorizado.
- Un prompt exacto definido en este contrato.
- Un `request_id` no vacío para trazabilidad.
- Un timeout fijo.
- Un máximo de tokens fijo.
- Exactamente una llamada — sin retry, sin batch, sin streaming.

La primera llamada real **no es** una ejecución autónoma ni una automatización. Es una prueba controlada, supervisada por Ariel en tiempo real, con kill switch manual disponible.

---

## 4. Qué NO se ejecuta en este ciclo (PUENTE-6D-A)

| Ítem | Estado |
|---|---|
| Llamada real a `api.anthropic.com` | NO — prohibición absoluta en este ciclo |
| Lectura de `ANTHROPIC_API_KEY` | NO — ni desde entorno ni desde archivo |
| Uso del SDK `anthropic` | NO — no importado ni instalado |
| Archivo `.env` | NO |
| Modificación de código Python | NO |
| Modificación de tests | NO |
| Instalación de dependencias | NO |
| Claude Haiku real | NO |
| Navegador real | NO |
| Playwright real | NO |
| Workflows de CI/CD | NO |
| Acciones sobre repos prohibidos | NO |

---

## 5. Precondiciones obligatorias

Antes de iniciar PUENTE-6D real, deben cumplirse **todas** estas condiciones:

| Precondición | Verificación |
|---|---|
| PUENTE-6A cerrado en `main` | Commit `9b9d82f` en `main` — contrato prueba API real |
| PUENTE-6B cerrado en `main` | Commit `0adf9ab` en `main` — cliente API real preparado sin llamada |
| B-07 cerrado en `main` | Commit `425b520` en `main` — validación de `request_id` |
| `python -m unittest discover -s tests` → 339/339 OK | Verificado en `main` antes de crear rama |
| Autorización explícita de Ariel en la sesión activa | Requerida para PUENTE-6D real — no implícita |
| `ANTHROPIC_API_KEY` no existe en ningún archivo del repo | Verificación manual previa |
| `.env` no existe en el repo | Verificación manual previa |
| SDK `anthropic` no importado en código existente | Verificado — cero imports en todos los módulos |
| No hay workflows activos que se disparen con el push | Verificación previa obligatoria |
| Rama de trabajo dedicada para PUENTE-6D real | No trabajar directamente en `main` |
| Kill switch manual disponible | Ariel puede interrumpir la prueba en cualquier momento |
| PUENTE-6D-B auditado y aprobado | PUENTE-6D real requiere que PUENTE-6D-B esté cerrado en `main` |

---

## 6. Modelo permitido para futura prueba

| Modelo | Estado |
|---|---|
| `claude-3-5-haiku-latest` | AUTORIZADO para primera llamada real |
| `claude-3-haiku-20240307` | Autorizado como alternativa |
| Cualquier otro modelo | PROHIBIDO en primera prueba |

El modelo `claude-3-5-haiku-latest` es el más económico de la familia Claude 3.5 y el apropiado para una primera prueba mínima de conectividad.

---

## 7. Variable de entorno — solo como referencia documental

La variable `ANTHROPIC_API_KEY` puede aparecer en este documento **únicamente como nombre textual de referencia**. Su valor real nunca puede aparecer en ningún artefacto del repo.

| Referencia permitida | Referencia prohibida |
|---|---|
| El texto `ANTHROPIC_API_KEY` como nombre | El valor real de la key (ej: `sk-ant-...`) |
| `os.environ.get("ANTHROPIC_API_KEY")` en bloque documental marcado como no-ejecutable | Cualquier valor que empiece por `sk-` |
| Mencionar que la key debe cargarse desde entorno | Imprimirla, loguearla, commitearla |

Protocolo de carga segura (referencia documental — no ejecutar en este ciclo):

```python
# Referencia documental — no ejecutar en este ciclo
import os
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("ANTHROPIC_API_KEY no está definida en el entorno")
# NUNCA imprimir api_key ni incluirla en logs
```

---

## 8. Prohibición absoluta del valor real de la key

El valor real de `ANTHROPIC_API_KEY` **nunca puede aparecer** en:

| Artefacto prohibido |
|---|
| Cualquier archivo del repo (en cualquier rama) |
| Documentos (`.md`) |
| Prompts enviados al modelo |
| Logs de cualquier tipo |
| Output de tests |
| Comentarios de código |
| Cuerpos de PR |
| Comentarios de PR o issues |
| Variables de entorno exportadas en scripts |
| Archivos `.env` en cualquier ubicación del repo |
| `print()`, `logging`, `sys.stdout` o equivalentes |

La única forma válida de existencia de la key es como variable de entorno en la sesión local del operador, cargada manualmente antes de la prueba y sin persistencia en archivos.

---

## 9. Prompt exacto permitido para futura prueba

```
Respondé exactamente: PLIC_OK
```

| Propiedad | Valor |
|---|---|
| Longitud | 26 caracteres |
| Idioma | Español |
| Sin datos sensibles | CONFIRMADO |
| Sin nombres propios | CONFIRMADO |
| Sin paths del sistema | CONFIRMADO |
| Sin instrucciones de acción real | CONFIRMADO |
| Respuesta esperada | `PLIC_OK` (texto exacto o variante mínima aceptable) |

**No se permite ningún otro prompt en la primera llamada real.** Cualquier modificación al prompt requiere un nuevo ciclo de contrato y auditoría.

---

## 10. Parámetros máximos para futura prueba

| Parámetro | Valor máximo | Restricción |
|---|---|---|
| `timeout` | `<= 10` segundos | Fijo en primera prueba — no configurable |
| `max_tokens` | `<= 50` | Mínimo suficiente para `PLIC_OK` |
| `request_id` | string no vacío | Obligatorio — bloqueado por B-07 si está ausente |
| `modo_seguro` | `True` (identidad estricta) | Rechaza `1`, `"true"`, `None` |
| `permitir_llamada_real` | `True` solo en PUENTE-6D real autorizado | `False` o ausente en cualquier otro ciclo |
| retry | `0` | Sin reintento automático en primera prueba |
| streaming | prohibido | Solo respuesta completa |
| batch | prohibido | Una sola llamada por prueba |

---

## 11. Salida esperada futura

La función de PUENTE-6D real debe devolver como mínimo estos campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `ok` | bool | `True` si la llamada fue exitosa, `False` en cualquier error |
| `proveedor` | string | `"anthropic_real"` si llegó a la API; `"anthropic_preparado"` o `"haiku_fake"` si hubo fallback |
| `modelo` | string | Modelo usado o intentado |
| `request_id` | string | Identificador de trazabilidad — no vacío |
| `response_text` | string \| null | Texto de la respuesta del modelo o `null` si falló |
| `error_tipo` | string | Tipo de error o `""` si `ok=True` |
| `fallback_usado` | bool | `True` si se usó cliente fake o cliente preparado como fallback |
| `evidencia` | dict \| null | Fragmento no sensible de la respuesta — ver sección 12 |
| `bloqueo` | bool | `True` si la prueba fue cortada por condición de corte |

---

## 12. Evidencia permitida en output y logs

| Dato | Permitido |
|---|---|
| Timestamp de la llamada (UTC) | SÍ |
| `request_id` | SÍ |
| Modelo solicitado | SÍ |
| Si hubo respuesta (bool) | SÍ |
| Texto de la respuesta si no contiene secreto | SÍ — solo si es `PLIC_OK` o variante inocua |
| Duración aproximada en segundos | SÍ |
| `fallback_usado` (bool) | SÍ |
| `ok` (bool) | SÍ |
| `error_tipo` (string) | SÍ |

---

## 13. Evidencia prohibida en output y logs

| Dato | Prohibición |
|---|---|
| Headers HTTP (incluido `Authorization`) | PROHIBIDO ABSOLUTO |
| Valor de `ANTHROPIC_API_KEY` (completo o parcial) | PROHIBIDO ABSOLUTO |
| Variables de entorno completas (`os.environ`) | PROHIBIDO ABSOLUTO |
| Traceback con secretos | PROHIBIDO ABSOLUTO |
| Cuerpo completo de respuesta si contiene datos sensibles | PROHIBIDO ABSOLUTO |
| IP o metadata de red sensible | PROHIBIDO |
| Tokens de sesión u otros credentials | PROHIBIDO ABSOLUTO |

---

## 14. Condiciones de corte

Si alguna de estas condiciones ocurre durante PUENTE-6D real, la prueba debe detenerse inmediatamente y activar el fallback:

| Condición | Acción inmediata |
|---|---|
| `ANTHROPIC_API_KEY` no disponible en entorno | Cortar antes de llamar — reportar sin mostrar el entorno |
| Error de autenticación (`authentication_error`) | Cortar — no reintentar — reportar sin mostrar la key |
| Rate limit (`rate_limit_error`) | Cortar — esperar mínimo 60 segundos antes de cualquier reintento en ciclo futuro |
| Costo inesperado (tokens de salida > 50 en una sola prueba) | Cortar — revisar el prompt antes de continuar |
| Respuesta vacía o malformada (sin `content[0].text`) | Cortar — `error_tipo: "schema"` |
| Respuesta distinta de `PLIC_OK` o variante inocua | Cortar — registrar respuesta completa solo si no contiene secreto |
| Respuesta que sugiere ejecutar una acción real | Cortar — `error_tipo: "corte"` — reportar a Ariel |
| Aparición de cualquier secret en la entrada al modelo | Cortar antes de enviar — nunca enviar |
| Aparición de cualquier secret en la respuesta del modelo | Cortar — no loguear la respuesta completa |
| Timeout superado (> 10 segundos) | Cortar — activar fallback — reportar latencia |
| Pérdida de conectividad de red | Cortar — activar fallback |
| Error no clasificado | Cortar — `error_tipo: "desconocido"` — activar fallback |

---

## 15. Fallback obligatorio

Si cualquier condición de corte se activa, el sistema debe:

1. Registrar `fallback_usado=True` en la salida.
2. Continuar usando `cliente_haiku_fake` o `cliente_api_real_preparado` (sin llamada real) según corresponda.
3. No modificar código durante la prueba para activar el fallback — el fallback debe estar disponible sin cambios.
4. Reportar a Ariel la condición de corte y el motivo.

El fallback garantiza que PLIC puede seguir operando sin la API real en cualquier momento.

---

## 16. Reglas de no escalada

Durante PUENTE-6D real y en cualquier prueba posterior de API real:

| Prohibición | Nivel |
|---|---|
| Conectar navegador real | ABSOLUTO |
| Conectar Playwright real | ABSOLUTO |
| Tocar repos de GitHub real (push, PR, merge) mediante la respuesta del modelo | ABSOLUTO |
| Crear workflows de CI/CD | ABSOLUTO |
| Ejecutar la respuesta del modelo como código | ABSOLUTO |
| Tocar producción | ABSOLUTO |
| Mezclar primera llamada real con Mano Local real | ABSOLUTO — requiere ciclo separado |
| Hacer más de una llamada real por prueba en PUENTE-6D | ABSOLUTO — primera prueba es una sola llamada |
| Escalar a otro modelo sin nuevo contrato | ABSOLUTO |
| Escalar a otro prompt sin nuevo contrato | ABSOLUTO |

---

## 17. Criterios para permitir PUENTE-6D real

Los siguientes criterios deben cumplirse **todos** antes de ejecutar cualquier llamada real:

| Criterio | Verificación requerida |
|---|---|
| Este contrato (PUENTE-6D-A) cerrado en `main` | Commit verificable |
| PUENTE-6D-B (preparación técnica) cerrado en `main` | Commit verificable |
| Auditoría técnica de PUENTE-6D-B aprobada (PUENTE-6D-C) | Dictamen A) o B) |
| Autorización explícita de Ariel en la sesión activa | Texto explícito en la sesión |
| `ANTHROPIC_API_KEY` disponible solo como variable de entorno local | No en ningún archivo |
| Tests pasan en `main` antes de crear rama PUENTE-6D real | Resultado verificado |
| Rama dedicada creada para PUENTE-6D real | No en `main` |
| Kill switch manual disponible | Ariel supervisa en tiempo real |
| Fallback verificado antes de la llamada | `cliente_haiku_fake` responde correctamente |
| Prompt es exactamente `"Respondé exactamente: PLIC_OK"` | Sin modificación |

---

## 18. Condiciones de bloqueo

Las siguientes condiciones bloquean el inicio de cualquier ciclo que involucre llamada real:

| Condición de bloqueo | Nivel |
|---|---|
| No hay autorización explícita de Ariel en la sesión activa | ABSOLUTO |
| PUENTE-6D-A no está en `main` | ABSOLUTO |
| PUENTE-6D-B no está en `main` | ABSOLUTO |
| Algún test falla en `main` | ABSOLUTO |
| La API key estaría en un archivo del repo en cualquier formato | ABSOLUTO |
| No existe rollback definido al cliente fake | ABSOLUTO |
| La prueba se ejecutaría en producción | ABSOLUTO |
| La prueba se ejecutaría en un workflow de CI/CD automático | ABSOLUTO |
| El prompt difiere de `"Respondé exactamente: PLIC_OK"` | ABSOLUTO |
| El modelo difiere de los autorizados en sección 6 | ABSOLUTO |
| `timeout > 10` o `max_tokens > 50` | ABSOLUTO |
| `request_id` está vacío o ausente | ABSOLUTO — bloqueado por B-07 |
| `modo_seguro` no es exactamente `True` | ABSOLUTO |
| No se auditó el código nuevo antes de la primera llamada real | ABSOLUTO |
| Los módulos existentes fueron modificados sin auditoría | ABSOLUTO |

---

## 19. Dictamen esperado del contrato

Una vez que este documento sea auditado y mergeado en `main`, el dictamen esperado es:

**CONTRATO APTO PARA PUENTE-6D-B — con las siguientes condiciones obligatorias:**

1. PUENTE-6D-B solo prepara el cliente real (firma, carga de key desde entorno, estructura de request, manejo de errores, fallback) — no ejecuta ninguna llamada real.
2. La primera llamada real solo ocurre en PUENTE-6D real, con autorización explícita de Ariel y después de PUENTE-6D-C (auditoría técnica).
3. Los 4 módulos existentes (`cerebro_mock`, `mano_local_simulada`, `cliente_haiku_fake`, `cliente_api_real_preparado`) no se modifican en ningún ciclo de PUENTE-6D.
4. El fallback al cliente fake debe estar activo y verificado antes de cualquier llamada real.
5. La API key nunca toca ningún archivo del repo — solo variable de entorno en sesión local del operador.
6. El prompt de la primera llamada real es exactamente `"Respondé exactamente: PLIC_OK"` — sin variaciones.
