# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestAvisoOk(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://event4us.pythonanywhere.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_aviso_ok(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Entrar").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("celamyrrha")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("mm659732")
        driver.find_element_by_css_selector("button.btn.btn-default").click()
        driver.find_element_by_link_text("Painel").click()
        driver.find_element_by_link_text("Acessar").click()
        driver.find_element_by_link_text("Adicionar Aviso").click()
        driver.find_element_by_id("id_titulo").clear()
        driver.find_element_by_id("id_titulo").send_keys(u"Inscrições encerradas")
        driver.find_element_by_id("id_conteudo").clear()
        driver.find_element_by_id("id_conteudo").send_keys(u"As inscrições do evento foram encerradas, agora falta pouco!")
        driver.find_element_by_css_selector("button.btn.btn-default").click()
        driver.find_element_by_xpath("//a[contains(@href, '/eventos/novo-evento-de-django/avisos/3/exclui/')]").click()
        try: self.assertEqual(u"× Aviso excluído com sucesso.", driver.find_element_by_css_selector("div.alert.alert-warning").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
