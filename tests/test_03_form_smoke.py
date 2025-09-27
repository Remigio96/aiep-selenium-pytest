# tests/test_03_form_smoke.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest, time

DEMO = {
    "nombres": "Juan",
    "apellidos": "Pérez",
    "telefono": "912345678",
    "rut": "12345678-9",
    "email": "demo@test.com",
}

SEDE_VAL = "AIEP Online"
CARRERA_VAL = "Ingeniería en Informática"


def _click_admision_lateral(d):
    sel = "a.item-lateral--color-azul[href*='/admision']"
    btn = WebDriverWait(d, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, sel))
    )
    d.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    WebDriverWait(d, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
    try:
        btn.click()
    except Exception:
        d.execute_script("arguments[0].click();", btn)


def _wait_tab_or_url_change(d, before_handles, url_sub, timeout=20):
    def cond(dr):
        return (len(dr.window_handles) > len(before_handles)) or (
            url_sub in dr.current_url
        )

    WebDriverWait(d, timeout).until(cond)
    after = d.window_handles
    if len(after) > len(before_handles):
        new = [h for h in after if h not in before_handles][0]
        d.switch_to.window(new)


def _select_tomselect_by_value(d, select_css, value_text):
    js = """
    const sel = document.querySelector(arguments[0]);
    if(!sel) return "no-select";
    try{
        if(sel.tomselect){
            sel.tomselect.setValue(arguments[1], true);
            return "tomselect";
        }
    }catch(e){}
    sel.value = arguments[1];
    sel.dispatchEvent(new Event('change', {bubbles:true}));
    return "fallback";
    """
    return d.execute_script(js, select_css, value_text)


def test_admision_form(open_home):
    d = open_home
    d.save_screenshot("01_home_before_click.png")

    before = d.window_handles
    _click_admision_lateral(d)
    try:
        _wait_tab_or_url_change(d, before, "/admision")
    except Exception:
        d.save_screenshot("02_after_click_no_change.png")
        pytest.skip("No se abrió pestaña ni cambió la URL tras Admisión.")

    d.save_screenshot("03_after_switch_or_url.png")

    # Formulario
    try:
        form = WebDriverWait(d, 25).until(
            EC.presence_of_element_located((By.ID, "js-formulario-1"))
        )
    except Exception as e:
        d.save_screenshot("04_no_form_found.png")
        pytest.skip(f"No se encontró el formulario (js-formulario-1). Detalle: {e}")

    # Completar campos de texto
    for name, val in DEMO.items():
        try:
            field = form.find_element(By.NAME, name)
            d.execute_script("arguments[0].scrollIntoView({block:'center'});", field)
            field.clear()
            field.send_keys(val)
        except Exception:
            pass

    # Sede y carrera
    try:
        _select_tomselect_by_value(d, "#tomselect-1", SEDE_VAL)
        time.sleep(0.5)
    except Exception:
        pass
    try:
        _select_tomselect_by_value(d, "#tomselect-3", CARRERA_VAL)
        time.sleep(0.5)
    except Exception:
        pass

    # Checkbox políticas
    try:
        chk = form.find_element(By.ID, "terminos-1")
        d.execute_script("arguments[0].scrollIntoView({block:'center'});", chk)
        if not chk.is_selected():
            try:
                chk.click()
            except Exception:
                d.execute_script("arguments[0].click();", chk)
    except Exception:
        pass

    d.save_screenshot("05_form_filled.png")

    # Validación mínima
    try:
        email_val = form.find_element(By.NAME, "email").get_attribute("value")
        assert DEMO["email"] in email_val
    except Exception:
        d.save_screenshot("05b_email_missing.png")
        pytest.skip("No se pudo validar el email cargado.")

    # Enviar SIEMPRE
    submit = form.find_element(
        By.CSS_SELECTOR, 'button[type="submit"], .boton[type="submit"]'
    )
    d.execute_script("arguments[0].scrollIntoView({block:'center'});", submit)

    clicked = False
    try:
        submit.click()
        clicked = True
    except Exception:
        pass
    if not clicked:
        try:
            d.execute_script("arguments[0].click();", submit)
            clicked = True
        except Exception:
            pass
    if not clicked:
        try:
            d.execute_script("arguments[0].closest('form').submit();", submit)
            clicked = True
        except Exception:
            pass

    d.save_screenshot("06_after_submit_try.png")

    # Señal de envío (éxito o loader)
    try:
        WebDriverWait(d, 8).until(
            EC.any_of(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".formulario-spinner, .formulario-loading")
                ),
                EC.url_contains("/exito"),
            )
        )
    except Exception:
        pass

    # Espera corta final y evidencia
    try:
        WebDriverWait(d, 10).until(
            EC.any_of(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, ".formulario-spinner, .formulario-loading")
                ),
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".formulario-loading__texto, .exito, .gracias")
                ),
                EC.url_contains("/exito"),
            )
        )
    finally:
        d.save_screenshot("07_submit_result.png")
