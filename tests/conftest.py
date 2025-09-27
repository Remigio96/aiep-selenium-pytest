# tests/conftest.py
import os, time
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.aiep.cl"


@pytest.fixture(scope="session")
def outdir():
    p = Path("artifacts")
    p.mkdir(exist_ok=True)
    return p


@pytest.fixture
def driver(outdir):
    opts = Options()
    if os.getenv("HEADLESS", "0") == "1":
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,768")

    # 🔇 Silenciar logs molestos de ChromeDriver (GCM / PHONE_REGISTRATION_ERROR)
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    opts.add_argument("--log-level=3")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-popup-blocking")

    drv = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=opts
    )
    yield drv

    # evidencia básica por test
    ts = time.strftime("%Y%m%d-%H%M%S")
    drv.save_screenshot(str(outdir / f"screenshot-{ts}.png"))
    html = drv.page_source
    (outdir / f"page-{ts}.html").write_text(html, encoding="utf-8")
    drv.quit()


@pytest.fixture
def open_home(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    return driver
