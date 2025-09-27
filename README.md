# Proyecto de Automatización de Pruebas AIEP

Este proyecto implementa pruebas automatizadas con **Selenium** y **pytest** para validar el correcto funcionamiento del sitio web institucional de AIEP.

## Objetivo

El propósito principal es garantizar que las funcionalidades críticas de la página se mantengan estables:

1. La **página principal** carga correctamente y contiene el logo institucional.
2. Los **enlaces de navegación** llevan a secciones válidas.
3. El **formulario de admisión** puede completarse y enviarse exitosamente.

Además, se generan **capturas de pantalla** y **archivos HTML** como evidencia de cada ejecución.

---

## Estructura del proyecto

```
.
├── artifacts/                  # Evidencias generadas (screenshots + HTML)
└── tests/                      # Casos de prueba
    ├── conftest.py             # Configuración de pytest y Selenium
    ├── test_01_homepage.py     # Prueba de título y logo en la home
    ├── test_02_nav_links.py    # Prueba de navegación por menú
    └── test_03_form_smoke.py   # Prueba de formulario de admisión
```

---

## Requisitos

* Python 3.11+
* Google Chrome instalado
* Dependencias de Python (instalables vía `pip`):

```bash
pip install pytest selenium webdriver-manager
```

---

## Ejecución de las pruebas

### Todas las pruebas

```bash
pytest -v tests/
```

### Ejecutar una prueba específica

```bash
pytest -v tests/test_03_form_smoke.py::test_admision_form
```

### Modo headless (sin abrir navegador)

```bash
HEADLESS=1 pytest -v tests/
```

---

## Evidencias generadas

En cada ejecución se guardan archivos en la carpeta `artifacts/`:

* `screenshot-*.png`: Captura de pantalla del estado final del test.
* `page-*.html`: Fuente HTML de la página al finalizar.

Ejemplo:

```
artifacts/
├── screenshot-20250927-153210.png
└── page-20250927-153210.html
```

---

## Descripción de las pruebas

### 1. `test_01_homepage.py`

* Verifica que el título de la página contiene "AIEP".
* Valida la existencia del logo institucional.

### 2. `test_02_nav_links.py`

* Abre el menú principal (en desktop o móvil).
* Intenta hacer clic en uno de los enlaces principales (Admisión, Escuelas, Sedes, etc.).
* Comprueba que la nueva sección tiene un encabezado `<h1>` válido.

### 3. `test_03_form_smoke.py`

* Navega hasta la sección **Admisión**.
* Completa los campos del formulario con datos de prueba.
* Selecciona sede y carrera.
* Marca la casilla de aceptación de términos.
* Intenta enviar el formulario.
* Verifica señales de actividad: spinner de carga o página de éxito.

---

## Notas importantes

* El formulario puede estar protegido con **validaciones adicionales** (como reCAPTCHA). La automatización llena y envía, pero puede no alcanzar siempre la página final de "éxito".
* Los mensajes de error de ChromeDriver relacionados con `PHONE_REGISTRATION_ERROR` o `DEPRECATED_ENDPOINT` fueron mitigados con opciones en `conftest.py`.
* Los artefactos de pruebas **no deben subirse a Git**. Se recomienda usar un `.gitignore` que excluya la carpeta `artifacts/` salvo un `.gitkeep` para mantener la estructura.

---

## Licencia

Uso académico y de aprendizaje. No destinado a producción.
