"""Selenium tests for the Task List app (run with pytest).

Install:  pip install pytest selenium

1) Start the server first, in its own terminal:   python app.py
2) Then run the tests in another terminal:        pytest -v
Needs Chrome installed; a visible Chrome window opens during the tests.
"""
import atexit
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "http://localhost:5001"
PAUSE = 1  # seconds to wait after each browser action so you can watch it

# ---- one visible Chrome browser ------------------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(2)
atexit.register(driver.quit)


def pause():
    time.sleep(PAUSE)


def open_clean_page():
    """Open the application in the browser and clear leftover tasks."""
    driver.get(URL)
    if driver.find_elements(By.ID, "clear-btn"):
        driver.find_element(By.ID, "clear-btn").click()
    pause()


def add_task(text):
    driver.find_element(By.ID, "task-input").send_keys(text)
    pause()
    driver.find_element(By.ID, "add-btn").click()
    pause()


def task_texts():
    return [li.text for li in driver.find_elements(By.CSS_SELECTOR, "li.task")]


def test_page_title_and_empty_state():
    open_clean_page()
    assert driver.title == "Task List"
    assert driver.find_element(By.TAG_NAME, "h1").text == "Task List"
    assert driver.find_element(By.ID, "empty-message").is_displayed()


def test_add_tasks():
    open_clean_page()
    add_task("Write tests")
    add_task("Ship it")
    assert task_texts() == ["Write tests", "Ship it"]


def test_empty_input_is_blocked():
    open_clean_page()
    driver.find_element(By.ID, "add-btn").click()  # 'required' blocks submit
    pause()
    assert task_texts() == []
    assert driver.find_element(By.ID, "empty-message").is_displayed()


def test_whitespace_task_is_ignored():
    open_clean_page()
    add_task("   ")
    assert task_texts() == []
    assert driver.find_element(By.ID, "empty-message").is_displayed()


def test_html_is_shown_as_text():
    open_clean_page()
    add_task("<b>bold</b>")
    assert task_texts() == ["<b>bold</b>"]


def test_clear_all():
    open_clean_page()
    add_task("Temporary")
    driver.find_element(By.ID, "clear-btn").click()
    pause()
    assert task_texts() == []
    assert driver.find_element(By.ID, "empty-message").is_displayed()
