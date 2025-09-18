import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

@pytest.mark.ui
def test_create_course_and_add_content():
    # ===== Cấu hình =====
    USERNAME = "admin"
    PASSWORD = "admin"
    URL = "http://learnpresshi.local/wp-admin"
    CREATE_COURSE_URL = "http://learnpresshi.local/wp-admin/post-new.php?post_type=lp_course"

    # ===== Setup ChromeDriver =====
    options = Options()
    options.add_argument("--start-maximized")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # ===== Bước 1: Đăng nhập admin =====
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.ID, "user_login"))).send_keys(USERNAME)
        driver.find_element(By.ID, "user_pass").send_keys(PASSWORD)
        driver.find_element(By.ID, "wp-submit").click()
        time.sleep(2)
        print("✅ Đăng nhập thành công!")
        #  Bước 2: Vào trang danh sách Question =====
        QUESTION_URL = "http://learnpresshi.local/wp-admin/post-new.php?post_type=lp_question"
        driver.get(QUESTION_URL)

        import random 
        # Viết tiêu đề question random ----
        random_number = random.randint(1000, 9999)  # Số ngẫu nhiên 4 chữ số
        title_field = driver.find_element(By.ID, "title")
        title_field.send_keys(f"Question Selenium Tự động {random_number}")
        print(f"✅ Đã nhập tiêu đề: Question Selenium Tự động {random_number}")


        # ---- Viết mô tả question ----
        driver.switch_to.frame(driver.find_element(By.ID, "content_ifr"))  # Chuyển vào iframe mô tả
        body = driver.find_element(By.ID, "tinymce")
        body.send_keys("Đây là mô tả tự động cho question Selenium.")
        driver.switch_to.default_content()

        # ---- Click nút Publish ----
        publish_btn = driver.find_element(By.ID, "publish")
        publish_btn.click()

        time.sleep(3)
        print("✅ Tạo question thành công!")


        from selenium.webdriver import ActionChains
        import random

        # ===== Hover vào .question-types =====
        question_types_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".question-types"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", question_types_element)
        ActionChains(driver).move_to_element(question_types_element).perform()
        print("✅ Đã hover vào 'question-types'.")

        # ===== Chờ 4 <li> type xuất hiện =====
        type_items = wait.until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR,
                '.question-types li[data-type="true_or_false"], '
                '.question-types li[data-type="multi_choice"], '
                '.question-types li[data-type="single_choice"], '
                '.question-types li[data-type="fill_in_blanks"]'
            ))
        )

        # ===== Random chọn 1 type và click vào <a> bên trong =====
        chosen_li = random.choice(type_items)
        type_name = chosen_li.get_attribute("data-type")
        a_tag = chosen_li.find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].click();", a_tag)
        print(f"📝 Đã click chọn loại câu hỏi: {type_name}")
        time.sleep(5)

        # ===== Scroll xuống phần question_settings =====
        question_settings = wait.until(
            EC.presence_of_element_located((By.ID, "question_settings"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", question_settings)
        print("✅ Đã kéo xuống phần 'question_settings'.")

        # ===== Điền số random 1-10 vào _lp_mark =====
        mark_input = wait.until(EC.presence_of_element_located((By.ID, "_lp_mark")))
        random_mark = random.randint(1, 10)
        mark_input.clear()
        mark_input.send_keys(str(random_mark))
        print(f"✅ Đã nhập điểm: {random_mark}")
        mark_input.clear()
        mark_input.send_keys(str(random_mark))
        driver.execute_script("""
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, mark_input)

        # ===== Tìm và điền Hint Question (random) =====
        hint_field_wrapper = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".form-field._lp_hint_field"))
        )
        hint_textarea = hint_field_wrapper.find_element(By.ID, "_lp_hint")
        hint_textarea.clear()
        random_hint_number = random.randint(100, 999)
        hint_textarea.send_keys(f"Gợi ý số {random_hint_number} cho câu hỏi Selenium.")
        print(f"✅ Đã nhập hint: Gợi ý số {random_hint_number} cho câu hỏi Selenium.")

        # ===== Tìm và điền Explanation Question (random) =====
        explanation_textarea = wait.until(
            EC.presence_of_element_located((By.ID, "_lp_explanation"))
        )
        explanation_textarea.clear()
        random_explanation_number = random.randint(100, 999)
        explanation_textarea.send_keys(f"Giải thích số {random_explanation_number} cho câu hỏi Selenium.")
        print(f"✅ Đã nhập explanation: Giải thích số {random_explanation_number} cho câu hỏi Selenium.")



        # ===== Scroll tới nút Update để đảm bảo nó hiển thị =====
        update_btn = wait.until(EC.element_to_be_clickable((By.ID, "publish")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_btn)
        time.sleep(0.5)

        # ===== Nếu vẫn bị che, click bằng JavaScript =====
        try:
            update_btn.click()
        except ElementClickInterceptedException:
            print("⚠ Nút Update bị che, click bằng JavaScript.")
            driver.execute_script("arguments[0].click();", update_btn)

        time.sleep(1)
        print("✅ Đã click nút Update.")

        

    finally:
        # Đóng trình duyệt sau vài giây
        time.sleep(5)
        driver.quit()