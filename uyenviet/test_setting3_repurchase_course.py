import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


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

        # ===== Click bật checkbox Allow Course Repurchase =====
        repurchase_checkbox = driver.find_element(By.ID, "_lp_allow_course_repurchase")
        if not repurchase_checkbox.is_selected():
            repurchase_checkbox.click()
            print("✅ Đã bật Allow Course Repurchase.")
        else:
            print("ℹ️ Checkbox Allow Course Repurchase đã được bật sẵn.")

        time.sleep(2)

        # ===== Tìm và click vào tab Pricing =====
        pricing_tab = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.price_options.price_tab a[href='#price_course_data']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pricing_tab)
        pricing_tab.click()
        print("✅ Đã click vào tab Pricing.")
        time.sleep(2)

        import random

        # ===== Sinh giá random từ 20-100 =====
        random_price = random.randint(20, 100)

        # ===== Tìm ô nhập Regular Price và điền giá =====
        regular_price_input = wait.until(
            EC.presence_of_element_located((By.ID, "_lp_regular_price"))
        )
        regular_price_input.clear()
        regular_price_input.send_keys(str(random_price))
        print(f"✅ Đã điền Regular Price: {random_price}")
        time.sleep(2)

        # ===== Sinh giá Sale Price nhỏ hơn Regular Price =====
        sale_price = random.randint(1, random_price - 1)

        # ===== Tìm ô nhập Sale Price và điền giá =====
        sale_price_input = wait.until(
            EC.presence_of_element_located((By.ID, "_lp_sale_price"))
        )
        sale_price_input.clear()
        sale_price_input.send_keys(str(sale_price))
        print(f"✅ Đã điền Sale Price: {sale_price} (nhỏ hơn Regular Price: {random_price})")
        time.sleep(2)


        # ===== Cập nhật lại khóa học =====
        update_btn = driver.find_element(By.ID, "publish")  # nút Publish đổi thành Update
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_btn)
        update_btn.click()
        print("✅ Đã lưu cập nhật Course Settings.")
        time.sleep(3)

        # ===== Click vào menu View Course trên admin bar =====
        view_course_link = wait.until(
            EC.element_to_be_clickable((By.ID, "wp-admin-bar-view"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_course_link)
        view_course_link.click()
        print("✅ Đã click View Course, chuyển sang trang khóa học.")
        time.sleep(3)

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

        # ===== Tìm và click vào nút Buy Now =====
        buy_now_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form.purchase-course button.button-purchase-course"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_now_button)
        buy_now_button.click()
        print("✅ Đã click vào nút Buy Now.")
        time.sleep(3)

        # ===== Tìm và click nút Place Order tại trang Checkout =====
        place_order_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "learn-press-checkout-place-order"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", place_order_btn)
        place_order_btn.click()
        print("✅ Đã click vào nút Place Order.")
        time.sleep(5)

        # ===== Bước 7: Truy cập lại course frontend đã lưu =====
        driver.get(course_frontend_url)


        # ===== Bước 9: Click nút "Continue" để vào Lesson =====
        continue_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.course-btn-continue"))
        )
        continue_btn.click()
        print("✅ đã click Continue để vào bài học")
        time.sleep(2)

        # ===== Bước 10: Click nút "Complete" trong Lesson =====
        complete_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.lp-btn-complete-item"))
        )
        complete_btn.click()
        print("✅ đã click Complete Lesson, popup hiện ra")

        # ===== Bước 11: Xác nhận "Yes" trong popup Complete lesson =====
        yes_btn_complete = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".lp-modal-footer .btn-yes"))
        )
        yes_btn_complete.click()
        print("✅ đã xác nhận Complete Lesson")
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
        print("🎉 đã hoàn thành khóa học thành công!")
        time.sleep(2)

        # ===== Kiểm tra sự tồn tại của nút Buy Now =====
        try:
            buy_now_button = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.course-buttons form.purchase-course button.button-purchase-course"))
            )
            assert buy_now_button.is_displayed(), "❌ Sai: Nút Buy Now không hiển thị."
            print("✅ Đúng: Nút Buy Now hiển thị trên trang khóa học -> repurchase oke.")
        except Exception:
            pytest.fail("❌ Sai: Không tìm thấy nút Buy Now trên trang khóa học -> repurchase not oke.")

        # ===== Tìm và click vào nút Buy Now =====
        buy_now_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form.purchase-course button.button-purchase-course"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_now_button)
        buy_now_button.click()
        print("✅ Đã click vào nút Buy Now.")
        time.sleep(3)

        # ===== Tìm và click nút Place Order tại trang Checkout =====
        place_order_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "learn-press-checkout-place-order"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", place_order_btn)
        place_order_btn.click()
        print("✅ Đã click vào nút Place Order.")
        time.sleep(5)

        # ===== Bước 7: Truy cập lại course frontend đã lưu =====
        driver.get(course_frontend_url)

        # ===== Bước 9: Kiểm tra tiến độ học khóa học =====
        try:
            progress_text = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.course-progress__number span.number"))
            ).text.strip()

            print(f"📊 Tiến độ khóa học hiện tại: {progress_text} -> Reset course progress ok")

            assert progress_text.startswith("0"), f"❌ Sai: Tiến độ khóa học không phải 0%, mà là {progress_text} -> Reset course progress not oke."
            print("✅ Đúng: Tiến độ khóa học là 0% (student chưa học gì) -> Reset course progress ok.")
        except Exception:
            pytest.fail("❌ Không tìm thấy tiến độ khóa học để kiểm tra.")

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

        # ===== Kéo xuống Course Settings =====
        course_settings = driver.find_element(By.ID, "course-settings")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", course_settings)
        time.sleep(2)

        # ===== Chọn Keep course progress trong Repurchase Option =====
        repurchase_select = wait.until(
            EC.presence_of_element_located((By.ID, "_lp_course_repurchase_option"))
        )
        select = Select(repurchase_select)
        select.select_by_value("keep")  # chọn option "Keep course progress"
        print("✅ Đã chọn Keep course progress trong Repurchase Option.")
        time.sleep(2)

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

        # ===== Tìm và click vào nút Buy Now =====
        buy_now_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form.purchase-course button.button-purchase-course"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_now_button)
        buy_now_button.click()
        print("✅ Đã click vào nút Buy Now.")
        time.sleep(3)

        # ===== Tìm và click nút Place Order tại trang Checkout =====
        place_order_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "learn-press-checkout-place-order"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", place_order_btn)
        place_order_btn.click()
        print("✅ Đã click vào nút Place Order.")
        time.sleep(5)

        # ===== Bước 7: Truy cập lại course frontend đã lưu =====
        driver.get(course_frontend_url)

        # ===== Bước XX: Kiểm tra course progress =====
        try:
            progress_number = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.course-progress__number span.number"))
            )
            progress_text = progress_number.text.strip().replace("%", "")
            print(f"📊 Course progress hiển thị: {progress_text}%")

            if progress_text == "100":
                print("✅ PASS: Course progress = 100%")
            else:
                print("❌ FAIL: Course progress khác 100%")
                assert False, f"Expected 100% but got {progress_text}%"
        except Exception as e:
            print(f"❌ Không tìm thấy course progress: {e}")
            assert False, "Course progress element not found"



    except Exception as e:
        print(f"❌ Đã xảy ra lỗi: {e}")
    finally:
        driver.quit()
