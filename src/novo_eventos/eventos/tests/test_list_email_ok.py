# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestListEmailOk(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://event4us.pythonanywhere.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_list_email_ok(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Eventos").click()
        driver.find_element_by_link_text("Listar").click()
        driver.find_element_by_css_selector("h4").click()
        driver.find_element_by_id("id_nome").clear()
        driver.find_element_by_id("id_nome").send_keys("Bianca")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("bianca@gmail.com")
        driver.find_element_by_id("id_mensagem").clear()
        driver.find_element_by_id("id_mensagem").send_keys(u"Gostaria de receber mais informações sobre o valor do curso.")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
    
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
