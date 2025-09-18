import time
import random
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

@pytest.mark.ui
def test_student_enroll_course():
    # ===== Cấu hình =====
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin"
    STUDENT_USERNAME = "student1"
    STUDENT_PASSWORD = "student1"
    URL = "http://learnpresshi.local/wp-admin"
    COURSE_URL = "http://learnpresshi.local/wp-admin/edit.php?post_type=lp_course"

    # ===== Setup ChromeDriver =====
    options = Options()
    options.add_argument("--start-maximized")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)


    try:
        # ===== Bước 1: Đăng nhập admin =====
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.ID, "user_login"))).send_keys(ADMIN_USERNAME)
        driver.find_element(By.ID, "user_pass").send_keys(ADMIN_PASSWORD)
        driver.find_element(By.ID, "wp-submit").click()
        time.sleep(2)
        print("✅ Đăng nhập admin thành công!")

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

        # ===== Kéo xuống Course Settings =====
        course_settings = driver.find_element(By.ID, "course-settings")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", course_settings)
        time.sleep(2)


        # ===== CHỌN LEVEL RANDOM =====
        level_select = Select(wait.until(EC.presence_of_element_located((By.ID, "_lp_level"))))
        backend_value = random.choice([opt.get_attribute("value") for opt in level_select.options if opt.get_attribute("value")])
        level_select.select_by_value(backend_value)

        # ===== CLICK PUBLISH =====
        publish_btn = wait.until(EC.element_to_be_clickable((By.ID, "publish")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", publish_btn)
        time.sleep(1)  # chờ animation/overlay biến mất
        try:
            publish_btn.click()
        except:
            driver.execute_script("arguments[0].click();", publish_btn)  # fallback nếu vẫn bị che
        print("✅ Đã publish khóa học sau khi chọn level.")

        # ===== VIEW COURSE =====
        backend_handle = driver.current_window_handle
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#wp-admin-bar-view a"))).click()
        driver.switch_to.window(driver.window_handles[-1])

        # Kiểm tra level hiển thị
        course_level_span = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".wp-block-learnpress-course-level .course-level"))
        )
        frontend_level = course_level_span.text.strip()

        # Mapping backend level values to frontend display text
        level_mapping = {
            "all": "All levels",
            "beginner": "Beginner",
            "intermediate": "Intermediate",
            "advanced": "Advanced",
        }

        expected_level = level_mapping.get(backend_value, backend_value).strip()

        if frontend_level.lower() == expected_level.lower():
            print("✅ PASS: Level hiển thị đúng")
        else:
            pytest.fail(f"❌ FAIL: Backend={backend_value}, Frontend={frontend_level}, Expected={expected_level}")
        time.sleep(5)

        # ===== Click vào "Edit Course" trong admin bar =====
        edit_course_btn = wait.until(EC.element_to_be_clickable((By.ID, "wp-admin-bar-edit")))
        edit_course_btn.click()
        print("✅ Đã click Edit Course để vào trang chỉnh sửa.")
        time.sleep(3)

        # ===== Scroll tới phần Curriculum =====
        curriculum = driver.find_element(By.ID, "lp-course-edit-curriculum")
        driver.execute_script("arguments[0].scrollIntoView(true);", curriculum)
        time.sleep(1)


        # ===== NHẬP FAKE STUDENTS =====
        students_input = wait.until(EC.presence_of_element_located((By.ID, "_lp_students")))
        fake_students = random.randint(1, 20)
        students_input.clear()
        students_input.send_keys(str(fake_students))

        # ===== CLICK PUBLISH (Fix intercept lỗi) =====
        publish_btn = wait.until(EC.presence_of_element_located((By.ID, "publish")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", publish_btn)
        time.sleep(1)  # chờ UI ổn định

        try:
            wait.until(EC.element_to_be_clickable((By.ID, "publish"))).click()
        except:
            # fallback nếu vẫn bị che → dùng JS click
            driver.execute_script("arguments[0].click();", publish_btn)

        print("✅ Đã update khóa học sau khi nhập fake students.")


        # ===== VIEW COURSE → KIỂM TRA STUDENTS =====
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#wp-admin-bar-view a"))).click()
        driver.switch_to.window(driver.window_handles[-1])

        student_div = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".course-count-student"))
        )
        text = student_div.text.strip()
        frontend_students = int("".join([c for c in text if c.isdigit()]))

        print(f"📊 Frontend hiển thị: {frontend_students} Students")
        if frontend_students >= fake_students:
            print("✅ PASS: Số học sinh hiển thị >= số fake")
        else:
            pytest.fail("❌ FAIL: Số học sinh hiển thị sai")
        time.sleep(5)

        # ===== Click vào "Edit Course" trong admin bar =====
        edit_course_btn = wait.until(EC.element_to_be_clickable((By.ID, "wp-admin-bar-edit")))
        edit_course_btn.click()
        print("✅ Đã click Edit Course để vào trang chỉnh sửa.")
        time.sleep(3)

        # ===== Scroll tới phần Curriculum =====
        curriculum = driver.find_element(By.ID, "lp-course-edit-curriculum")
        driver.execute_script("arguments[0].scrollIntoView(true);", curriculum)
        time.sleep(1)

        # ===== NHẬP RETAKE COURSE =====
        retake_input = wait.until(
            EC.presence_of_element_located((By.ID, "_lp_retake_count"))
        )
        retake_input.clear()
        retake_input.send_keys("1")
        print("✅ Đã điền giá trị 1 vào Retake Count")
        # (Tuỳ chọn) Cập nhật lại course sau khi thay đổi setting
        update_btn = driver.find_element(By.ID, "publish")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_btn)
        driver.execute_script("arguments[0].click();", update_btn)

        # =====: Click “View Course” ở admin bar =====
        view_course_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#wp-admin-bar-view a"))
        )
        view_course_link.click()
        print("✅ Đã mở trang View Course (frontend)")

        # ===== CLICK ENROLL COURSE (Start Now) =====
        start_now_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form.enroll-course button.lp-button.button-enroll-course"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_now_btn)
        time.sleep(1)

        start_now_btn.click()
        print("✅ Đã click vào nút Start Now (Enroll Course)")

         # ===== Bước 10: Click nút "Complete" trong Lesson =====
        complete_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.lp-btn-complete-item"))
        )
        complete_btn.click()
        print("✅ Student đã click Complete Lesson, popup hiện ra")

        # ===== Bước 11: Xác nhận "Yes" trong popup Complete lesson =====
        yes_btn_complete = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".lp-modal-footer .btn-yes"))
        )
        yes_btn_complete.click()
        print("✅ Student đã xác nhận Complete Lesson")
        time.sleep(2)

        # ===== Bước 12: Click nút "Finish course" =====
        finish_course_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form.form-button-finish-course button.lp-btn-finish-course"))
        )
        finish_course_btn.click()
        print("✅ Student đã click Finish course, popup hiện ra")

        # ===== Bước 13: Xác nhận "Yes" trong popup Finish course =====
        yes_btn_finish = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".lp-modal-footer .btn-yes"))
        )
        yes_btn_finish.click()
        print("🎉 Student đã hoàn thành khóa học thành công!")
        time.sleep(2)

        # ===== KIỂM TRA RETAKE BUTTON =====
        try:
            retake_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "form.lp-form-retake-course button.button-retake-course"))
            )
            if "Retake course" in retake_button.text:
                print(f"✅ PASS: Hiển thị button Retake: {retake_button.text}")
            else:
                pytest.fail(f"❌ FAIL: Button Retake hiển thị sai: {retake_button.text}")
        except:
            pytest.fail("❌ FAIL: Không tìm thấy button Retake course")

        # ===== Click vào "Edit Course" trong admin bar =====
        edit_course_btn = wait.until(EC.element_to_be_clickable((By.ID, "wp-admin-bar-edit")))
        edit_course_btn.click()
        print("✅ Đã click Edit Course để vào trang chỉnh sửa.")
        time.sleep(3)

        # ===== Scroll tới phần Curriculum =====
        curriculum = driver.find_element(By.ID, "lp-course-edit-curriculum")
        driver.execute_script("arguments[0].scrollIntoView(true);", curriculum)
        time.sleep(1)

        # ===== ĐIỀN MAX STUDENTS = 1 =====
        max_students_input = wait.until(
            EC.presence_of_element_located((By.ID, "_lp_max_students"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", max_students_input)
        time.sleep(1)

        max_students_input.clear()
        max_students_input.send_keys("1")
        print("✅ Đã điền Max Students = 1")

        # (Tuỳ chọn) Cập nhật lại course sau khi thay đổi setting
        update_btn = driver.find_element(By.ID, "publish")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_btn)
        driver.execute_script("arguments[0].click();", update_btn)

        # =====: Click “View Course” ở admin bar =====
        view_course_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#wp-admin-bar-view a"))
        )
        view_course_link.click()
        print("✅ Đã mở trang View Course (frontend)")

        # Lưu URL course frontend
        course_frontend_url = driver.current_url
        print(f"👉 URL course frontend: {course_frontend_url}")


        # ===== MỞ COURSE Ở TRÌNH DUYỆT MỚI ẨN DANH =====
        incognito_options = Options()
        incognito_options.add_argument("--incognito")
        incognito_options.add_argument("--start-maximized")

        new_driver = webdriver.Chrome(service=Service(), options=incognito_options)
        new_wait = WebDriverWait(new_driver, 10)

        # Mở URL course frontend đã lưu
        new_driver.get(course_frontend_url)
        print("✅ Đã mở course ở trình duyệt mới (ẩn danh)")

        # ===== KIỂM TRA COURSE FULL =====
        try:
            warning_msg = new_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.learn-press-message.warning"))
            )
            text_msg = warning_msg.text.strip()
            if text_msg == "The course is full of students.":
                print("✅ PASS: Hiển thị cảnh báo 'The course is full of students.'")
            else:
                pytest.fail(f"❌ FAIL: Thông báo khác: {text_msg}")
        except:
            pytest.fail("❌ FAIL: Không tìm thấy thông báo 'The course is full of students.'")
        time.sleep(5)
        

    finally:
        driver.quit()
