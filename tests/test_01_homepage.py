# tests/test_01_homepage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_home_title_and_logo(open_home):
    d = open_home

    # Verificar que el título de la página contiene AIEP
    assert "AIEP" in d.title.upper()

    # Esperar a que aparezca un logo con alt que contenga "AIEP"
    logo = WebDriverWait(d, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt*="AIEP" i]'))
    )

    # Validar que el logo existe y tiene un src válido
    src = logo.get_attribute("src")
    assert src is not None and src.strip() != ""
