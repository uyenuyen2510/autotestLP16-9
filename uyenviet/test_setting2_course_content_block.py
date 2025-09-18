import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
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

                # ===== Bước 3.5: Cấu hình course settings =====
        course_settings = driver.find_element(By.ID, "course-settings")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", course_settings)
        time.sleep(2)

        # ---- Checkbox "Block Expire Duration" (#_lp_block_expire_duration) ----
        block_expire_checkbox = driver.find_element(By.ID, "_lp_block_expire_duration")
        if not block_expire_checkbox.is_selected():
            driver.execute_script("arguments[0].click();", block_expire_checkbox)

            print("✅ Đã bật Block Expire Duration")
        else:
            print("ℹ️ Block Expire Duration đã được bật sẵn")

        # ---- Checkbox "Block Finished" (#_lp_block_finished) ----
        block_finished_checkbox = driver.find_element(By.ID, "_lp_block_finished")
        if block_finished_checkbox.is_selected():
            block_finished_checkbox.click()
            print("✅ Đã tắt Block Finished")
        else:
            print("ℹ️ Block Finished đã tắt sẵn")

        time.sleep(2)

        # ===== Điền giá trị duration =====
        duration_input = driver.find_element(By.ID, "_lp_duration")
        duration_input.clear()
        duration_input.send_keys("1")  # điền 1

        # ===== Chọn Minute(s) trong select =====
        from selenium.webdriver.support.ui import Select

        duration_select = Select(driver.find_element(By.CSS_SELECTOR, "select.lp-meta-box__duration-select"))
        duration_select.select_by_value("minute")  # chọn Minute(s)

        print("✅ Đã thiết lập duration = 1 Minute")


        # ---- Lưu thay đổi bằng Update course ----
        update_btn = driver.find_element(By.ID, "publish")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_btn)
        update_btn.click()
        print("💾 Đã lưu lại course settings")
        time.sleep(3)

         # ===== Bước 4: Click “View Course” ở admin bar =====
        view_course_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#wp-admin-bar-view a"))
        )
        view_course_link.click()
        print("✅ Đã mở trang View Course (frontend)")

        # Lưu URL course frontend
        course_frontend_url = driver.current_url
        print(f"👉 URL course frontend: {course_frontend_url}")

        # ===== Bước 5: Logout admin trước khi login student =====
        driver.get("http://learnpresshi.local/wp-login.php?action=logout")
        driver.get("http://learnpresshi.local/wp-login.php")
        time.sleep(5)

        # ===== Bước 6: Login bằng student =====
        driver.get("http://learnpresshi.local/wp-login.php")  # đảm bảo về trang login chuẩn

        username_input = wait.until(EC.element_to_be_clickable((By.ID, "user_login")))
        password_input = wait.until(EC.element_to_be_clickable((By.ID, "user_pass")))

        username_input.clear()
        password_input.clear()

        username_input.send_keys(STUDENT_USERNAME)

        # nếu send_keys không ăn thì dùng execute_script
        try:
            password_input.send_keys(STUDENT_PASSWORD)
        except:
            driver.execute_script("arguments[0].value = arguments[1];", password_input, STUDENT_PASSWORD)

        driver.find_element(By.ID, "wp-submit").click()
        time.sleep(2)
        print("✅ Đăng nhập student thành công!")


        # ===== Bước 7: Truy cập lại course frontend đã lưu =====
        driver.get(course_frontend_url)

        # ===== Bước 8: Click nút “Start Now” =====
        start_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.lp-button.button-enroll-course"))
        )
        start_btn.click()
        print("✅ Student đã click Start Now để enroll course")

        # 👉 Có thể thêm assert kiểm tra enroll thành công
        # Ví dụ: check xem xuất hiện nút "Continue" thay vì "Start Now"
        try:
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.lp-button"))
            )
            print("🎉 Student đã enroll thành công!")
        except:
            print("⚠️ Không tìm thấy nút xác nhận enroll.")
        time.sleep(60)

        # ===== Bước 14: Click lại vào Lesson icon =====
        try:
            lesson_icon = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span.course-item-ico.lp_lesson"))
            )
            lesson_icon.click()
            print("✅ Đã click vào Lesson icon")
            time.sleep(2)

            # ===== Bước 15: Kiểm tra thông báo protected content =====
            protected_message = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.learn-press-message.learn-press-content-protected-message.error"))
            )

            if "The content of this item has been blocked because the course has exceeded its duration." in protected_message.text:
                print("🎉 Test Passed block content khi hết duration: Sau khi hoàn thành, lesson hiển thị thông báo protected đúng!")
            else:
                pytest.fail("❌ Test Failed: Không hiển thị thông báo protected mong đợi.")

        except Exception as e:
            pytest.fail(f"❌ Test Failed: Không tìm thấy thông báo protected. Lỗi: {e}")

        # ===== Click icon <i class="lp-icon-times"></i> =====
        close_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.lp-icon-times")))
        driver.execute_script("arguments[0].click();", close_icon)
        print("✅ Đã click icon đóng (lp-icon-times).")
        time.sleep(2)

        # ===== Logout student =====
        driver.get("http://learnpresshi.local/wp-login.php?action=logout")
        time.sleep(2)

        # Xác nhận logout (nếu có màn hình confirm)
        try:
            confirm_logout = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "log out")))
            confirm_logout.click()
            print("✅ Đã xác nhận logout student.")
        except:
            print("⚠️ Không thấy màn hình confirm logout, có thể đã logout luôn.")

        time.sleep(2)

        # ===== Login lại bằng admin =====
        driver.get("http://learnpresshi.local/wp-login.php")
        wait.until(EC.presence_of_element_located((By.ID, "user_login"))).send_keys(ADMIN_USERNAME)
        driver.find_element(By.ID, "user_pass").send_keys(ADMIN_PASSWORD)
        driver.find_element(By.ID, "wp-submit").click()
        print("✅ Đã login lại bằng admin.")
        time.sleep(3)

        # ===== Sau khi login admin, mở lại trang frontend của course =====
        driver.get(course_frontend_url)
        time.sleep(3)

        # ===== Click vào "Edit Course" trong admin bar =====
        edit_course_btn = wait.until(EC.element_to_be_clickable((By.ID, "wp-admin-bar-edit")))
        edit_course_btn.click()
        print("✅ Đã click Edit Course để vào trang chỉnh sửa.")
        time.sleep(3)

        # ===== Kéo xuống phần Course Settings =====
        course_settings = wait.until(EC.presence_of_element_located((By.ID, "course-settings")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", course_settings)
        time.sleep(2)

        # ===== Checkbox "Block Expire Duration" (#_lp_block_expire_duration) =====
        block_expire_checkbox = driver.find_element(By.ID, "_lp_block_expire_duration")
        if block_expire_checkbox.is_selected():
            driver.execute_script("arguments[0].click();", block_expire_checkbox)
            print("✅ Đã tắt checkbox Block Expire Duration")

        # ===== Checkbox "Block Finished" (#_lp_block_finished) =====
        block_finished_checkbox = driver.find_element(By.ID, "_lp_block_finished")
        if not block_finished_checkbox.is_selected():
            driver.execute_script("arguments[0].click();", block_finished_checkbox)
            print("✅ Đã bật checkbox Block Finished")

        time.sleep(2)

        # (Tuỳ chọn) Cập nhật lại course sau khi thay đổi setting
        update_btn = driver.find_element(By.ID, "publish")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_btn)
        driver.execute_script("arguments[0].click();", update_btn)










        # ===== Bước 4: Click “View Course” ở admin bar =====
        view_course_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#wp-admin-bar-view a"))
        )
        view_course_link.click()
        print("✅ Đã mở trang View Course (frontend)")

        # Lưu URL course frontend
        course_frontend_url = driver.current_url
        print(f"👉 URL course frontend: {course_frontend_url}")

        # ===== Bước 5: Logout admin trước khi login student =====
        driver.get("http://learnpresshi.local/wp-login.php?action=logout")
        driver.get("http://learnpresshi.local/wp-login.php")
        time.sleep(5)

        # ===== Bước 6: Login bằng student =====
        driver.get("http://learnpresshi.local/wp-login.php")  # đảm bảo về trang login chuẩn

        username_input = wait.until(EC.element_to_be_clickable((By.ID, "user_login")))
        password_input = wait.until(EC.element_to_be_clickable((By.ID, "user_pass")))

        username_input.clear()
        password_input.clear()

        username_input.send_keys(STUDENT_USERNAME)

        # nếu send_keys không ăn thì dùng execute_script
        try:
            password_input.send_keys(STUDENT_PASSWORD)
        except:
            driver.execute_script("arguments[0].value = arguments[1];", password_input, STUDENT_PASSWORD)

        driver.find_element(By.ID, "wp-submit").click()
        time.sleep(2)
        print("✅ Đăng nhập student thành công!")


        # ===== Bước 7: Truy cập lại course frontend đã lưu =====
        driver.get(course_frontend_url)


        # ===== Bước 9: Click nút "Continue" để vào Lesson =====
        continue_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.course-btn-continue"))
        )
        continue_btn.click()
        print("✅ Student đã click Continue để vào bài học")
        time.sleep(2)

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

        # ===== Bước 14: Click lại vào Lesson icon =====
        try:
            lesson_icon = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span.course-item-ico.lp_lesson"))
            )
            lesson_icon.click()
            print("✅ Đã click vào Lesson icon")
            time.sleep(2)

            # ===== Bước 15: Kiểm tra thông báo protected content =====
            protected_message = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.learn-press-message.learn-press-content-protected-message.error"))
            )

            if "You finished this course. This content is protected." in protected_message.text:
                print("🎉 Test Passed: Sau khi hoàn thành, lesson hiển thị thông báo protected đúng!")
            else:
                pytest.fail("❌ Test Failed: Không hiển thị thông báo protected mong đợi.")

        except Exception as e:
            pytest.fail(f"❌ Test Failed: Không tìm thấy Lesson icon hoặc thông báo protected. Lỗi: {e}")


    finally:
        time.sleep(3)
        driver.quit()
