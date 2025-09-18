import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===== Cấu hình =====
USERNAME = "admin"  # Thay bằng tên đăng nhập thật
PASSWORD = "admin"  # Thay bằng mật khẩu thật
URL = "http://learnpresshi.local/wp-admin"
CREATE_COURSE_URL = "http://learnpresshi.local/wp-admin/post-new.php?post_type=lp_course"

@pytest.mark.ui
def test_add_section_to_course():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # ===== Đăng nhập admin =====
        driver.get("http://learnpresshi.local/wp-admin")
        driver.find_element(By.ID, "user_login").send_keys("admin")
        driver.find_element(By.ID, "user_pass").send_keys("admin")
        driver.find_element(By.ID, "wp-submit").click()
        time.sleep(2)

        # ===== Vào danh sách khóa học =====
        driver.get("http://learnpresshi.local/wp-admin/edit.php?post_type=lp_course")
        time.sleep(2)
        
        # =====  Tạo khóa học mới =====
        CREATE_COURSE_URL = "http://learnpresshi.local/wp-admin/post-new.php?post_type=lp_course"
        driver.get(CREATE_COURSE_URL)
        time.sleep(2)

        # ---- Viết tiêu đề khóa học ----
        title_field = driver.find_element(By.ID, "title")
        title_field.send_keys("Khóa học Selenium Tự động")

        # ---- Viết mô tả khóa học ----
        driver.switch_to.frame(driver.find_element(By.ID, "content_ifr"))  # Chuyển vào iframe mô tả
        body = driver.find_element(By.ID, "tinymce")
        body.send_keys("Đây là mô tả tự động cho khóa học Selenium.")
        driver.switch_to.default_content()

        # ---- Click nút Publish ----
        publish_btn = driver.find_element(By.ID, "publish")
        publish_btn.click()

        time.sleep(3)
        print("✅ Tạo khóa học thành công!")

        # ===== Scroll tới phần Curriculum =====
        curriculum = driver.find_element(By.ID, "lp-course-edit-curriculum")
        driver.execute_script("arguments[0].scrollIntoView(true);", curriculum)
        time.sleep(1)

        # ===== Nhập tên Section =====
        section_title = "Chương 1: Giới thiệu Selenium"
        new_section_input = curriculum.find_element(By.CLASS_NAME, "lp-section-title-new-input")
        new_section_input.click()
        new_section_input.send_keys(section_title)

        # ===== Click nút Add Section =====
        add_btn = curriculum.find_element(By.CLASS_NAME, "lp-btn-add-section")
        add_btn.click()
        time.sleep(2)

        # ===== Tìm phần section-content mới được thêm =====
        section_contents = driver.find_elements(By.CLASS_NAME, "section-content")
        last_section_content = section_contents[-1]  # lấy section mới nhất

        # ===== Điền mô tả vào class="lp-section-description-input" =====
        description_input = last_section_content.find_element(By.CLASS_NAME, "lp-section-description-input")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", description_input)
        wait.until(EC.visibility_of(description_input))
        description_input.clear()
        description_input.send_keys("Đây là phần mô tả chi tiết cho Chương 1.")
        description_input.send_keys(Keys.ENTER)  # ⏎ Enter để lưu mô tả
        print("✅ Đã điền mô tả và nhấn Enter.")
        time.sleep(10)

        # ===== Xác định section mới nhất =====
        last_section = driver.find_elements(By.CLASS_NAME, "section")[-1]  # lấy section mới nhất

        # ===== Tìm nút Add Lesson bên trong section này =====
        lesson_button = last_section.find_element(
            By.CSS_SELECTOR, ".section-actions button.lp-btn-select-item-type[data-item-type='lp_lesson']"
        )

        # ===== Cuộn và click =====
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lesson_button)
        wait.until(EC.element_to_be_clickable(lesson_button))
        lesson_button.click()
        print("✅ Đã click vào nút Add Lesson trong section vừa tạo.")
        time.sleep(2)

        # ===== Chờ ô nhập title xuất hiện trong section mới =====
        lesson_title_input = wait.until(
            EC.visibility_of(last_section.find_element(By.CLASS_NAME, "lp-add-item-type-title-input"))
        )
        lesson_title_input.clear()
        lesson_title_input.send_keys("Bài học giới thiệu Selenium")
        lesson_title_input.send_keys(Keys.ENTER)
        print("✅ Đã tạo Lesson với tiêu đề.")
        time.sleep(2)

        # ===== Xác định section mới nhất =====
        last_section = driver.find_elements(By.CLASS_NAME, "section")[-1]  # lấy section mới nhất

        # ===== Tìm nút Add Lesson bên trong section này =====
        lesson_button = last_section.find_element(
            By.CSS_SELECTOR, ".section-actions button.lp-btn-select-item-type[data-item-type='lp_lesson']"
        )

        # ===== Cuộn và click =====
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lesson_button)
        wait.until(EC.element_to_be_clickable(lesson_button))
        lesson_button.click()
        print("✅ Đã click vào nút Add Lesson trong section vừa tạo.")
        time.sleep(2)

        # ===== Chờ input title xuất hiện trong section mới =====
        lesson_title_input = wait.until(
            EC.visibility_of(last_section.find_element(By.CLASS_NAME, "lp-add-item-type-title-input"))
        )
        lesson_title_input.clear()
        lesson_title_input.send_keys("Bài học giới thiệu Selenium")
        print("✅ Đã nhập tiêu đề bài học.")

        # ===== Click nút Add Lesson (nút xác nhận) =====
        add_lesson_confirm = last_section.find_element(
            By.CSS_SELECTOR, "button.lp-btn-add-item.button.button-primary"
        )
        wait.until(EC.element_to_be_clickable(add_lesson_confirm))
        add_lesson_confirm.click()
        print("✅ Đã click nút xác nhận Add Lesson.")
        time.sleep(2)

        # Tìm section mới nhất
        last_section = driver.find_elements(By.CSS_SELECTOR, ".section:not(.lp-hidden)")[-1]

        # 1. Click nút Add Quiz
        add_quiz_btn = last_section.find_element(
            By.CSS_SELECTOR,
            'button.lp-btn-select-item-type.button[data-item-type="lp_quiz"]'
        )
        add_quiz_btn.click()
        print("✅ Đã click vào nút Add Quiz.")

        # 2. Điền tiêu đề quiz
        quiz_title_input = last_section.find_element(
            By.CSS_SELECTOR,
            "input.lp-add-item-type-title-input"
        )
        quiz_title_input.send_keys("Bài kiểm tra Selenium")
        quiz_title_input.send_keys(Keys.ENTER)
        print("✅ Đã tạo Quiz với tiêu đề.")

        # ===== 1. Tìm section mới nhất =====
        last_section = driver.find_elements(By.CSS_SELECTOR, ".section:not(.lp-hidden)")[-1]

        # ===== 2. Tìm và click nút "Select items" =====
        select_items_btn = last_section.find_element(
            By.CSS_SELECTOR,
            "button.button.lp-btn-show-popup-items-to-select"
        )
        select_items_btn.click()
        print("✅ Đã click nút Select items.")

        # Chờ popup container xuất hiện
        popup_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".lp-select-items-html-container"))
        )

        # ===== Chờ danh sách lesson xuất hiện =====
        list_items = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".list-items"))
        )
        print("✅ Danh sách bài học đã hiển thị.")

        # ===== Chọn 2 lesson đầu tiên =====
        lesson_items = list_items.find_elements(By.CSS_SELECTOR, ".lp-select-item")
        if len(lesson_items) >= 2:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lesson_items[0])
            lesson_items[0].click()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lesson_items[1])
            lesson_items[1].click()
            print("✅ Đã chọn 2 bài học đầu tiên.")
        else:
            print("⚠️ Không đủ 2 bài học để chọn.")

        # ===== Click nút Add =====
        add_items_btn = popup_container.find_element(
            By.CSS_SELECTOR, "button.button.lp-btn-add-items-selected"
        )
        wait.until(EC.element_to_be_clickable(add_items_btn))
        add_items_btn.click()
        print("✅ Đã click nút Add để thêm lesson vào quiz.")
        time.sleep(2)

        # ===== Click lại nút Select items =====
        select_items_btn = last_section.find_element(
            By.CSS_SELECTOR,
            "button.button.lp-btn-show-popup-items-to-select"
        )
        wait.until(EC.element_to_be_clickable(select_items_btn))
        select_items_btn.click()
        print("✅ Đã click nút Select items (lần 2).")

        # ===== Chờ popup container xuất hiện =====
        popup_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".lp-select-items-html-container"))
        )
        print("✅ Popup Select items đã hiển thị.")

        # ===== Chuyển sang tab Quiz =====
        quiz_tab = popup_container.find_element(
            By.CSS_SELECTOR, 'li[data-type="lp_quiz"] a'
        )
        wait.until(EC.element_to_be_clickable(quiz_tab))
        quiz_tab.click()
        print("✅ Đã click tab Quiz trong popup.")
        time.sleep(1)

                # ===== Chờ danh sách quiz xuất hiện =====
        quiz_list_items = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".list-items"))
        )
        print("✅ Danh sách quiz đã hiển thị.")

        # ===== Chọn 2 quiz đầu tiên =====
        quiz_items = quiz_list_items.find_elements(By.CSS_SELECTOR, ".lp-select-item")
        if len(quiz_items) >= 2:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", quiz_items[0])
            quiz_items[0].click()
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", quiz_items[1])
            quiz_items[1].click()
            print("✅ Đã chọn 2 quiz đầu tiên.")
        else:
            print("⚠️ Không đủ 2 quiz để chọn.")

        # ===== Click nút Add =====
        add_quiz_items_btn = popup_container.find_element(
            By.CSS_SELECTOR, "button.button.lp-btn-add-items-selected"
        )
        wait.until(EC.element_to_be_clickable(add_quiz_items_btn))
        add_quiz_items_btn.click()
        print("✅ Đã click nút Add để thêm quiz vào section.")
        time.sleep(2)

        
       

    finally:
        driver.quit()
