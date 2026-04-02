import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class TestLibreriaQA:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.url = "file://" + os.path.abspath("index.html")
        self.driver.get(self.url)
        yield
        self.driver.quit()

    def capture(self, name):
        if not os.path.exists("screenshots"): os.makedirs("screenshots")
        self.driver.save_screenshot(f"screenshots/{name}.png")

    def login(self, u, p):
        self.driver.find_element(By.ID, "username").send_keys(u)
        self.driver.find_element(By.ID, "password").send_keys(p)
        self.driver.find_element(By.ID, "btn-login").click()

    # HU01: Login (Camino Feliz y Negativo)
    def test_hu01_login_fallido(self):
        self.login("admin", "incorrecta")
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        assert "incorrectas" in alert.text
        alert.accept()
        self.capture("HU01_Login_Negativo")

    # HU02: Crear (Camino Feliz)
    def test_hu02_crear_libro(self):
        self.login("admin", "1234")
        self.driver.find_element(By.ID, "title").send_keys("Libro de Prueba")
        self.driver.find_element(By.ID, "author").send_keys("Autor QA")
        self.driver.find_element(By.ID, "year").send_keys("2024")
        self.driver.find_element(By.CSS_SELECTOR, "#genre option[value='Ficción']").click()
        self.driver.find_element(By.ID, "btn-action").click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "toast")))
        self.capture("HU02_Crear_Feliz")

    # HU03: Lectura y Persistencia
    def test_hu03_verificar_lista(self):
        self.test_hu02_crear_libro()
        tabla = self.driver.find_element(By.ID, "book-list").text
        assert "Libro de Prueba" in tabla
        self.capture("HU03_Lectura")

    # HU04: Edición (Prueba de Límites/Negativa)
    def test_hu04_editar_vacio(self):
        self.test_hu02_crear_libro()
        self.driver.find_element(By.CLASS_NAME, "btn-edit").click()
        self.driver.find_element(By.ID, "title").clear() # Límite: Campo obligatorio vacío
        self.driver.find_element(By.ID, "btn-action").click()
        # El sistema no debería agregar una fila vacía (según la lógica del HTML)
        self.capture("HU04_Edicion_Negativa")

    # HU05: Eliminación
    def test_hu05_eliminar_libro(self):
        self.test_hu02_crear_libro()
        self.driver.find_element(By.CLASS_NAME, "btn-delete").click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "toast")))
        self.capture("HU05_Eliminar")