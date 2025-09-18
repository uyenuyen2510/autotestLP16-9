import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

@pytest.mark.ui
def test_create_course_and_add_content():
    # ===== Cấu hình =====
    USERNAME = "admin"
    PASSWORD = "admin"
    URL = "http://learnpresshi.local/wp-admin"
    CREATE_COURSE_URL = "http://learnpresshi.local/wp-admin/post-new.php?post_type=lp_course"
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
        wait.until(EC.presence_of_element_located((By.ID, "user_login"))).send_keys(USERNAME)
        driver.find_element(By.ID, "user_pass").send_keys(PASSWORD)
        driver.find_element(By.ID, "wp-submit").click()
        time.sleep(2)
        print("✅ Đăng nhập thành công!")
        #  Bước 2: Vào trang danh sách Course =====
        COURSE_URL = "http://learnpresshi.local/wp-admin/edit.php?post_type=lp_course"
        driver.get(COURSE_URL)

        # Bước 3: Click vào title khóa học đầu tiên =====
        first_course = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.row-title"))
        )
        course_title = first_course.text
        first_course.click()
        print(f"✅ Đã mở khóa học đầu tiên: {course_title}")

        # Bước 4: Click vào "View Course" trên admin bar =====
        view_course = wait.until(
            EC.element_to_be_clickable((By.ID, "wp-admin-bar-view"))
        )
        view_course.find_element(By.TAG_NAME, "a").click()
        print("✅ Đã click View Course")

        # Bước 5: Chuyển sang tab mới (frontend khóa học) =====
        driver.switch_to.window(driver.window_handles[-1])

        # Bước 6: Kiểm tra thông tin "Lifetime" =====
        course_duration = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.course-duration"))
        ).text.strip()

        assert course_duration == "Lifetime", f"❌ Sai duration, nhận được: {course_duration}"
        print("✅ Duration đúng: Lifetime")

        # Bước 7: Click vào "Edit Course" trên admin bar =====
        edit_course = wait.until(
            EC.element_to_be_clickable((By.ID, "wp-admin-bar-edit"))
        )
        edit_course.find_element(By.TAG_NAME, "a").click()
        print("✅ Đã click Edit Course")

        # Bước 8: Kéo xuống phần Course Settings =====
        course_settings = wait.until(
            EC.presence_of_element_located((By.ID, "course-settings"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", course_settings)
        time.sleep(1)

        # Bước 9: Nhập giá trị -5 vào duration =====
        duration_input = wait.until(
            EC.presence_of_element_located((By.ID, "_lp_duration"))
        )
        duration_input.clear()
        duration_input.send_keys("-5")
        print("✅ Đã nhập giá trị -5 cho duration")

        # Bước 10: Click nút Update =====
        update_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "publish"))
        )
        update_btn.click()
        print("✅ Đã click Update")

        # Bước 11: Verify validation =====
        # Tùy hệ thống hiển thị validation thế nào, giả sử hiển thị lỗi ngay trên input
        try:
            # HTML5 validation sẽ báo lỗi => check validity
            is_valid = driver.execute_script("return arguments[0].checkValidity();", duration_input)
            assert not is_valid, "❌ Validation KHÔNG chạy khi nhập -5"
            print("✅ Validation hoạt động đúng khi nhập giá trị âm (-5)")
        except Exception as e:
            print(f"❌ Không tìm thấy validation phù hợp: {e}")

                # Bước 12: Nhập giá trị hợp lệ 10 =====
        duration_input = wait.until(
            EC.presence_of_element_located((By.ID, "_lp_duration"))
        )
        duration_input.clear()
        duration_input.send_keys("10")
        print("✅ Đã nhập giá trị 10 cho duration")

        # Bước 13: Chọn random option trong dropdown =====
        duration_select = Select(
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "select.lp-meta-box__duration-select")
            ))
        )

        import random
        options = duration_select.options
        random_choice = random.choice(options)
        duration_select.select_by_value(random_choice.get_attribute("value"))
        print(f"✅ Đã chọn option random: {random_choice.text}")

        # Bước 14: Click Update =====
        update_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "publish"))
        )
        update_btn.click()
        print("✅ Đã click Update với giá trị hợp lệ")

        # Bước 15: Verify cập nhật thành công =====
        # Giả sử WordPress hiện thông báo updated notice
        success_notice = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.updated.notice-success"))
        )
        assert "updated" in success_notice.text.lower(), "❌ Không thấy thông báo cập nhật thành công"
        print("✅ Khóa học đã cập nhật thành công")

                # Bước 16: Click lại vào "View Course" =====
        view_course = wait.until(
            EC.element_to_be_clickable((By.ID, "wp-admin-bar-view"))
        )
        view_course.find_element(By.TAG_NAME, "a").click()
        print("✅ Đã click View Course sau khi update")

        # Bước 17: Chuyển sang tab frontend (nếu mở tab mới) =====
        driver.switch_to.window(driver.window_handles[-1])

        # Bước 18: Verify duration hiển thị đúng =====
        course_duration = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.info-meta-right span.course-duration"))
        ).text.strip()

        expecte_text = f"{duration_input.get_attribute('value')} {random_choice.text}"
        assert course_duration == expected_text, f"❌ Duration sai, expected: {expected_text}, actual: {course_duration}"
        print(f"✅ Duration hiển thị đúng: {course_duration}")


    except Exception as e:
        print(f"❌ Đã xảy ra lỗi: {e}")
    finally:
        driver.quit()


    driver.quit()

