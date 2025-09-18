import time
import random
import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

# ===== Cấu hình =====
USERNAME = "admin"
PASSWORD = "admin"
BASE_URL = "http://learnpresshi.local/wp-admin"

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def login_admin(driver, wait):
    driver.get(BASE_URL)
    wait.until(EC.presence_of_element_located((By.ID, "user_login"))).send_keys(USERNAME)
    driver.find_element(By.ID, "user_pass").send_keys(PASSWORD)
    driver.find_element(By.ID, "wp-submit").click()
    time.sleep(2)
    print("✅ Đăng nhập thành công!")

def create_lesson(driver, wait):
    LESSON_URL = f"{BASE_URL}/edit.php?post_type=lp_lesson"
    driver.get(LESSON_URL)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".page-title-action"))).click()
    random_number = random.randint(1000, 9999)
    driver.find_element(By.ID, "title").send_keys(f"Lesson Selenium Tự động {random_number}")
    driver.switch_to.frame(driver.find_element(By.ID, "content_ifr"))
    driver.find_element(By.ID, "tinymce").send_keys("Mô tả tự động cho lesson.")
    driver.switch_to.default_content()
    driver.find_element(By.ID, "publish").click()
    time.sleep(2)
    print("✅ Lesson đã được tạo!")

def create_question(driver, wait):
    QUESTION_URL = f"{BASE_URL}/post-new.php?post_type=lp_question"
    driver.get(QUESTION_URL)

    random_number = random.randint(1000, 9999)
    driver.find_element(By.ID, "title").send_keys(f"Question Selenium Tự động {random_number}")
    driver.switch_to.frame(driver.find_element(By.ID, "content_ifr"))
    driver.find_element(By.ID, "tinymce").send_keys("Mô tả tự động cho question.")
    driver.switch_to.default_content()
    driver.find_element(By.ID, "publish").click()
    time.sleep(2)

    # Chọn type random
    question_types = wait.until(EC.presence_of_all_elements_located((
        By.CSS_SELECTOR,
        '.question-types li[data-type]'
    )))
    chosen = random.choice(question_types)
    chosen.find_element(By.TAG_NAME, "a").click()
    time.sleep(1)

    # Điền mark, hint, explanation
    mark_input = wait.until(EC.presence_of_element_located((By.ID, "_lp_mark")))
    mark_input.clear()
    mark_val = random.randint(1, 10)
    mark_input.send_keys(str(mark_val))
    hint_input = wait.until(EC.presence_of_element_located((By.ID, "_lp_hint")))
    hint_input.send_keys(f"Gợi ý {random.randint(100,999)}")
    exp_input = wait.until(EC.presence_of_element_located((By.ID, "_lp_explanation")))
    exp_input.send_keys(f"Giải thích {random.randint(100,999)}")

    # Update
    update_btn = driver.find_element(By.ID, "publish")
    try:
        update_btn.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", update_btn)
    print("✅ Question đã được tạo và lưu!")

def create_quiz(driver, wait):
    QUIZ_URL = f"{BASE_URL}/edit.php?post_type=lp_quiz"
    driver.get(QUIZ_URL)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".page-title-action"))).click()

    random_number = random.randint(1000, 9999)
    driver.find_element(By.ID, "title").send_keys(f"Quiz Selenium Tự động {random_number}")
    driver.switch_to.frame(driver.find_element(By.ID, "content_ifr"))
    driver.find_element(By.ID, "tinymce").send_keys("Mô tả tự động cho quiz.")
    driver.switch_to.default_content()
    driver.find_element(By.ID, "publish").click()
    time.sleep(2)

    # Thêm question vào quiz
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#quiz-editor .select-item"))).click()
    checkboxes = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".question-item.lp_question.addable input[type='checkbox']")
    ))
    for cb in checkboxes[:4]:
        cb.click()
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.button.button-primary.checkout")
    )).click()
    print("✅ Quiz đã được tạo và thêm question!")

def create_course_with_section(driver, wait):
    COURSE_URL = f"{BASE_URL}/post-new.php?post_type=lp_course"
    driver.get(COURSE_URL)
    driver.find_element(By.ID, "title").send_keys("Khóa học Selenium Tự động")
    driver.switch_to.frame(driver.find_element(By.ID, "content_ifr"))
    driver.find_element(By.ID, "tinymce").send_keys("Mô tả tự động cho khóa học.")
    driver.switch_to.default_content()
    driver.find_element(By.ID, "publish").click()
    time.sleep(2)

    curriculum = driver.find_element(By.ID, "lp-course-edit-curriculum")
    driver.execute_script("arguments[0].scrollIntoView(true);", curriculum)
    section_input = curriculum.find_element(By.CLASS_NAME, "lp-section-title-new-input")
    section_input.send_keys("Chương 1: Giới thiệu Selenium")
    curriculum.find_element(By.CLASS_NAME, "lp-btn-add-section").click()
    time.sleep(1)

    last_section = driver.find_elements(By.CLASS_NAME, "section")[-1]
    # Add lesson
    lesson_btn = last_section.find_element(
        By.CSS_SELECTOR, ".section-actions button.lp-btn-select-item-type[data-item-type='lp_lesson']"
    )
    lesson_btn.click()
    input_field = last_section.find_element(By.CLASS_NAME, "lp-add-item-type-title-input")
    input_field.send_keys("Bài học giới thiệu Selenium")
    input_field.send_keys(Keys.ENTER)
    time.sleep(1)

    # Add quiz
    quiz_btn = last_section.find_element(
        By.CSS_SELECTOR, ".section-actions button.lp-btn-select-item-type[data-item-type='lp_quiz']"
    )
    quiz_btn.click()
    quiz_field = last_section.find_element(By.CLASS_NAME, "lp-add-item-type-title-input")
    quiz_field.send_keys("Bài kiểm tra Selenium")
    quiz_field.send_keys(Keys.ENTER)
    time.sleep(1)

    driver.find_element(By.ID, "publish").click()
    print("✅ Khóa học đã được tạo cùng section, lesson, quiz!")

@pytest.mark.ui
def test_create_lesson_question_quiz_course():
    driver, wait = setup_driver()
    try:
        login_admin(driver, wait)
        create_lesson(driver, wait)
        create_question(driver, wait)
        create_quiz(driver, wait)
        create_course_with_section(driver, wait)
    finally:
        time.sleep(5)
        driver.quit()
