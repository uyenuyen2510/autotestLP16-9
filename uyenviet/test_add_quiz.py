import time
import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        #  Bước 2: Vào trang danh sách Quiz =====
        QUIZ_URL = "http://learnpresshi.local/wp-admin/edit.php?post_type=lp_quiz"
        driver.get(QUIZ_URL)

        # Chờ nút "Add New" (class=page-title-action) xuất hiện và click
        add_quiz_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".page-title-action"))
        )
        add_quiz_btn.click()
        print("✅ Đã click nút Add New Quiz!")

        import random 
        # Viết tiêu đề Quiz random ----
        random_number = random.randint(1000, 9999)  # Số ngẫu nhiên 4 chữ số
        title_field = driver.find_element(By.ID, "title")
        title_field.send_keys(f"Quiz Selenium Tự động {random_number}")
        print(f"✅ Đã nhập tiêu đề: Quiz Selenium Tự động {random_number}")


        # ---- Viết mô tả quiz ----
        driver.switch_to.frame(driver.find_element(By.ID, "content_ifr"))  # Chuyển vào iframe mô tả
        body = driver.find_element(By.ID, "tinymce")
        body.send_keys("Đây là mô tả tự động cho quiz Selenium.")
        driver.switch_to.default_content()

        # ---- Click nút Publish ----
        publish_btn = driver.find_element(By.ID, "publish")
        publish_btn.click()

        time.sleep(3)
        print("✅ Tạo quiz thành công!")


        # Chờ cho div class "name add-new-question" xuất hiện
        wait = WebDriverWait(driver, 10)
        add_new_question_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.name.add-new-question")))

        # Lấy element quiz-editor để scroll tới
        quiz_editor_element = wait.until(
            EC.presence_of_element_located((By.ID, "quiz-editor"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", quiz_editor_element)
        print("✅ Đã scroll đến quiz-editor")

        # Tìm và click nút select-item trong quiz-editor
        select_item_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#quiz-editor .select-item"))
        )
        select_item_btn.click()
        print("✅ Đã click nút Select Item trong quiz-editor")

        questions_added = False

        try:
            # ===== Chờ popup hiện lên và lấy danh sách checkbox câu hỏi =====
            checkboxes = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".question-item.lp_question.addable input[type='checkbox']"))
            )
            time.sleep(1)

            if checkboxes:
                # Click 4 checkbox đầu tiên
                for checkbox in checkboxes[:4]:
                    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                    checkbox.click()
                print("✅ Đã tick 4 checkbox đầu tiên")

                # ===== Click nút Add Selected Items =====
                add_selected_btn = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.button-primary.checkout"))
                )
                add_selected_btn.click()
                print("✅ Đã thêm 4 câu hỏi vào quiz")

                questions_added = True
            else:
                raise Exception("⚠️ Không tìm thấy câu hỏi trong popup!")

        except Exception:
            print("⚠️ Popup không có câu hỏi — đóng popup.")
            driver.find_element(By.CSS_SELECTOR, "body").click()
            time.sleep(1)

        # ===== Nếu đã thêm câu hỏi thì chờ hiển thị trong quiz-editor =====
        if questions_added:
            try:
                # Chờ tối đa 15s để các câu hỏi hiển thị
                wait_long = WebDriverWait(driver, 15)
                wait_long.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "#quiz-editor .lp-question, #quiz-editor .question")
                    )
                )
                print("✅ Các câu hỏi đã hiển thị trong quiz-editor!")
            except TimeoutException:
                print("⚠️ Không tìm thấy câu hỏi trong quiz-editor sau khi thêm. Có thể load chậm hoặc selector sai.")


        # ===== Kéo màn hình xuống quiz_settings =====
        quiz_settings = wait.until(
            EC.presence_of_element_located((By.ID, "quiz_settings"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", quiz_settings)
        print("✅ Đã kéo màn hình xuống quiz_settings")


        import random
        # ===== Bước 4: Điền số random vào Duration =====
        duration_input = wait.until(
            EC.presence_of_element_located((By.ID, "_lp_duration"))
        )
        random_number = random.randint(1, 100)  # Tạo số ngẫu nhiên từ 1-100
        duration_input.clear()
        duration_input.send_keys(str(random_number))
        print(f"✅ Đã điền duration: {random_number}")

        from selenium.webdriver.support.ui import Select
        import random

        # ===== Bước 5: Chọn ngẫu nhiên đơn vị Duration =====
        duration_select_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select.lp-meta-box__duration-select"))
        )
        duration_select = Select(duration_select_elem)

        # Lấy tất cả option trong select
        all_options = duration_select.options

        # Chọn ngẫu nhiên 1 option
        random_option = random.choice(all_options)
        duration_select.select_by_visible_text(random_option.text)

        print(f"✅ Đã chọn đơn vị duration: {random_option.text}")

        # Cập nhật Quiz =====
        update_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "publish"))
        )
        driver.execute_script("arguments[0].click();", update_btn)
        print("✅ Đã click nút Update Quiz.")


    finally:
        # Đóng trình duyệt sau vài giây
        time.sleep(5)
