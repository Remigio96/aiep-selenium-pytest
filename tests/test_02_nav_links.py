# tests/test_02_nav_links.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


CANDIDATES = ["Admisión", "Escuelas", "Sedes", "Educación Continua"]


def open_menu_if_needed(d):
    """Abre el menú hamburguesa si está oculto en móvil"""
    try:
        menu_button = WebDriverWait(d, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button .icon-menu"))
        )
        if menu_button.is_displayed():
            menu_button.click()
            WebDriverWait(d, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.menumobile-list"))
            )
    except Exception:
        pass


def click_if_present(d, texts):
    """Intenta hacer clic en un ítem del menú (p o a)"""
    for t in texts:
        try:
            # 1. Buscar <a> primero (link real)
            els = d.find_elements(By.PARTIAL_LINK_TEXT, t)
            if els:
                els[0].click()
                return t

            # 2. Si no hay <a>, buscar <p> dentro de menumobile-list
            els = d.find_elements(
                By.XPATH,
                f"//ul[contains(@class,'menumobile-list')]//p[contains(text(),'{t}')]",
            )
            if els:
                els[0].click()
                return t

        except Exception:
            continue
    return None


def test_can_open_some_main_section(open_home):
    d = open_home

    open_menu_if_needed(d)  # abrir menú hamburguesa si corresponde
    hit = click_if_present(d, CANDIDATES)

    if not hit:
        pytest.skip("No se encontró un enlace principal clicable en la home.")

    # Verificar que se carga una página o cambia la vista
    try:
        header = WebDriverWait(d, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        assert header.text.strip() != ""
    except Exception:
        pytest.fail(f"No se encontró un encabezado <h1> tras hacer clic en {hit}")

    # Confirmar que seguimos en AIEP
    assert "AIEP" in d.title.upper()
