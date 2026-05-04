# PUENTE-6D-A — Checklist operativo para ejecución de primera llamada real

**Este checklist debe completarse manualmente por Ariel antes de iniciar PUENTE-6D real.**
**Todos los ítems deben estar marcados como OK antes de ejecutar cualquier llamada real.**
**Si algún ítem no puede marcarse como OK, la prueba debe bloquearse.**

---

## Estado de este checklist

| Campo | Valor |
|---|---|
| Checklist | PUENTE-6D-A — Operativo |
| Tipo | Documental — para completar manualmente antes de PUENTE-6D real |
| Ciclo que lo completa | PUENTE-6D real (fecha y sesión a definir) |
| Estado actual | PENDIENTE — no iniciar PUENTE-6D real hasta completar todos los ítems |

---

## Bloque 1 — Estado de main

- [ ] **1.1** `git rev-parse main` devuelve el commit esperado (mínimo `425b520` o posterior que incluya PUENTE-6D-B auditado).
- [ ] **1.2** `python -m unittest discover -s tests` → todos los tests pasan (mínimo 339/339, más los de PUENTE-6D-B si aplica).
- [ ] **1.3** `git status --short` en `main` → working tree limpio, sin cambios staged ni unstaged.
- [ ] **1.4** PUENTE-6D-A está en `main` (este documento).
- [ ] **1.5** PUENTE-6D-B está en `main` (preparación técnica del cliente real).
- [ ] **1.6** PUENTE-6D-C está en `main` (auditoría técnica de PUENTE-6D-B) con dictamen A) o B).

---

## Bloque 2 — Autorización

- [ ] **2.1** Ariel otorgó autorización explícita en la sesión activa para ejecutar PUENTE-6D real.
- [ ] **2.2** La autorización menciona explícitamente "primera llamada real" y "PUENTE-6D real".
- [ ] **2.3** No se asumió autorización implícita por el merge de PUENTE-6D-B ni de ningún ciclo previo.

---

## Bloque 3 — Unicidad de la llamada

- [ ] **3.1** Se ejecutará exactamente **una** llamada real en esta prueba.
- [ ] **3.2** No hay retry automático (`retry=0`).
- [ ] **3.3** No hay batch.
- [ ] **3.4** No hay streaming.
- [ ] **3.5** La prueba se detiene inmediatamente si cualquier condición de corte se activa.

---

## Bloque 4 — Prompt

- [ ] **4.1** El prompt es exactamente: `Respondé exactamente: PLIC_OK`
- [ ] **4.2** No hay variaciones, traducciones ni adiciones al prompt.
- [ ] **4.3** El prompt no contiene datos sensibles, nombres propios, paths del sistema ni instrucciones de acción real.
- [ ] **4.4** El prompt fue verificado visualmente por Ariel antes de la llamada.

---

## Bloque 5 — Modelo

- [ ] **5.1** El modelo es `claude-haiku-4-5-20251001` (único autorizado — actualizado en PUENTE-6D-MODELO-FIX).
- [ ] **5.2** No se usa ningún otro modelo.
- [ ] **5.3** El modelo fue verificado en el payload antes del envío.

---

## Bloque 6 — request_id

- [ ] **6.1** El `request_id` es un string no vacío.
- [ ] **6.2** El `request_id` es único para esta prueba (preferiblemente UUID generado localmente).
- [ ] **6.3** El `request_id` no contiene datos sensibles.
- [ ] **6.4** El `request_id` fue registrado antes de la llamada para trazabilidad.

---

## Bloque 7 — Timeout y max_tokens

- [ ] **7.1** `timeout <= 10` segundos.
- [ ] **7.2** `max_tokens <= 50`.
- [ ] **7.3** Ambos valores fueron verificados en el código antes de la llamada.

---

## Bloque 8 — Variable de entorno

- [ ] **8.1** El nombre `ANTHROPIC_API_KEY` se usa solo como referencia textual en este checklist y en el código — **nunca su valor real**.
- [ ] **8.2** La variable de entorno `ANTHROPIC_API_KEY` está definida en la sesión local del operador antes de la prueba.
- [ ] **8.3** No existe ningún archivo `.env` en el repo.
- [ ] **8.4** No existe ningún archivo en el repo que contenga el valor real de la key.
- [ ] **8.5** `git grep -r "sk-ant" .` → sin resultados.
- [ ] **8.6** `git grep -r "ANTHROPIC_API_KEY\s*=" .` → sin resultados que incluyan el valor real (solo referencias textuales).

---

## Bloque 9 — Prohibición de imprimir la key

- [ ] **9.1** El código de PUENTE-6D real no imprime `api_key` en ningún punto.
- [ ] **9.2** No hay `print(api_key)`, `logging.info(api_key)`, `print(os.environ)` ni equivalentes en el código.
- [ ] **9.3** El código fue revisado visualmente por Ariel antes de la llamada.

---

## Bloque 10 — Prohibición de imprimir el entorno

- [ ] **10.1** El código no imprime `os.environ`, `os.environ.copy()`, ni ninguna forma de dump del entorno.
- [ ] **10.2** No hay ningún logger que capture variables de entorno automáticamente.

---

## Bloque 11 — Headers

- [ ] **11.1** El header `Authorization` no aparece en ningún log.
- [ ] **11.2** El header `Authorization` no aparece en ningún output de test.
- [ ] **11.3** El header `Authorization` no aparece en ningún documento del repo.
- [ ] **11.4** El código no loguea el objeto `headers` ni el objeto `request` completo antes de enmascarar.

---

## Bloque 12 — Fallback

- [ ] **12.1** `cliente_haiku_fake` responde correctamente antes de la llamada real (test de smoke previo).
- [ ] **12.2** `cliente_api_real_preparado` responde con `ok=True` para la misma entrada (sin llamada real).
- [ ] **12.3** El fallback no requiere modificar código para activarse.
- [ ] **12.4** El código de PUENTE-6D real activa el fallback automáticamente si cualquier condición de corte se dispara.

---

## Bloque 13 — Kill switch

- [ ] **13.1** Ariel puede interrumpir la prueba en cualquier momento desde el teclado (Ctrl+C o equivalente).
- [ ] **13.2** La prueba no es autónoma — requiere presencia activa de Ariel.
- [ ] **13.3** No hay ningún mecanismo de re-ejecución automática si la prueba falla.

---

## Bloque 14 — No producción

- [ ] **14.1** La prueba se ejecuta en el entorno local de Ariel — no en ningún servidor remoto.
- [ ] **14.2** No hay ningún proceso de CI/CD que pudiera ejecutar esta prueba automáticamente.
- [ ] **14.3** No hay ningún webhook, scheduler ni trigger que pudiera activar la prueba.
- [ ] **14.4** Los resultados de la prueba no se publican automáticamente en ningún sistema externo.

---

## Bloque 15 — No navegador

- [ ] **15.1** No se usa ningún navegador real durante la prueba.
- [ ] **15.2** No se usa Playwright durante la prueba.
- [ ] **15.3** No se usa Selenium ni ningún driver de navegador.

---

## Bloque 16 — No Playwright

- [ ] **16.1** `playwright` no está instalado en el entorno de la prueba.
- [ ] **16.2** El código de PUENTE-6D real no importa `playwright`.
- [ ] **16.3** No hay scripts que invoquen Playwright.

---

## Bloque 17 — No workflows

- [ ] **17.1** No existe ningún archivo en `.github/workflows/` en el repo.
- [ ] **17.2** `git diff main...HEAD -- .github/` → sin cambios.
- [ ] **17.3** El push de PUENTE-6D real no disparará ningún workflow automático.

---

## Bloque 18 — No secrets en repo

- [ ] **18.1** `git grep -r "sk-ant" .` → sin resultados en ninguna rama.
- [ ] **18.2** No existe ningún archivo `.env` en ninguna ubicación del repo.
- [ ] **18.3** No existe ningún archivo de credenciales (`.pem`, `.key`, `.p12`, `credentials.json`) en el repo.
- [ ] **18.4** El `.gitignore` incluye `.env` y `*.env`.

---

## Bloque 19 — Reporte final mínimo

Al terminar PUENTE-6D real (con éxito o con corte), debe quedar registrado como mínimo:

- [ ] **19.1** Timestamp de inicio y fin de la prueba (UTC).
- [ ] **19.2** `request_id` usado.
- [ ] **19.3** Modelo usado.
- [ ] **19.4** Si hubo respuesta (`ok=True` o `ok=False`).
- [ ] **19.5** Texto de la respuesta si es `PLIC_OK` o variante inocua (nunca si contiene secreto).
- [ ] **19.6** `error_tipo` si hubo error.
- [ ] **19.7** Si se activó fallback (`fallback_usado=True/False`).
- [ ] **19.8** Confirmación de que la key no aparece en ningún log.

---

## Resumen de bloqueo automático

Si cualquiera de estos ítems está marcado como FAIL o no puede verificarse, **la prueba queda bloqueada**:

| Ítem crítico | Bloquea si |
|---|---|
| Autorización de Ariel (2.1) | No está en la sesión activa |
| Tests en main (1.2) | Algún test falla |
| Prompt exacto (4.1) | Difiere de `"Respondé exactamente: PLIC_OK"` |
| request_id no vacío (6.1) | Está vacío, ausente o no es string |
| timeout <= 10 (7.1) | Es mayor a 10 |
| max_tokens <= 50 (7.2) | Es mayor a 50 |
| Key no en repo (8.5) | `git grep "sk-ant"` tiene resultados |
| No producción (14.1) | La prueba se ejecuta en servidor remoto |
| No workflow (17.3) | El push dispara CI automático |
| Fallback disponible (12.1) | `cliente_haiku_fake` no responde |
