import time
import pytest
from selenium import webdriver
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
        #  Bước 2: Vào trang danh sách Lesson =====
        LESSON_URL = "http://learnpresshi.local/wp-admin/edit.php?post_type=lp_lesson"
        driver.get(LESSON_URL)

        # Chờ nút "Add New" (class=page-title-action) xuất hiện và click
        add_lesson_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".page-title-action"))
        )
        add_lesson_btn.click()
        print("✅ Đã click nút Add New Lesson!")

        import random 
        # Viết tiêu đề bài học random ----
        random_number = random.randint(1000, 9999)  # Số ngẫu nhiên 4 chữ số
        title_field = driver.find_element(By.ID, "title")
        title_field.send_keys(f"Lesson Selenium Tự động {random_number}")
        print(f"✅ Đã nhập tiêu đề: Lesson Selenium Tự động {random_number}")


        # ---- Viết mô tả khóa học ----
        driver.switch_to.frame(driver.find_element(By.ID, "content_ifr"))  # Chuyển vào iframe mô tả
        body = driver.find_element(By.ID, "tinymce")
        body.send_keys("Đây là mô tả tự động cho bài học Selenium.")
        driver.switch_to.default_content()

        # ---- Click nút Publish ----
        publish_btn = driver.find_element(By.ID, "publish")
        publish_btn.click()

        time.sleep(3)
        print("✅ Tạo bài học thành công!")

        #Bước 3: Kéo xuống phần Lesson Settings =====
        lesson_settings = wait.until(
            EC.presence_of_element_located((By.ID, "lesson_settings"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", lesson_settings)
        print("✅ Đã kéo xuống phần Lesson Settings!")

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

        # Bước 6: Click random vào Preview (id="_lp_preview") =====
        preview_checkbox = wait.until(
            EC.presence_of_element_located((By.ID, "_lp_preview"))
        )

        # Random True/False
        if random.choice([True, False]):
            if not preview_checkbox.is_selected():
                preview_checkbox.click()
                print("✅ Đã bật Preview cho lesson.")
            else:
                print("ℹ️ Preview đã được bật sẵn.")
        else:
            if preview_checkbox.is_selected():
                preview_checkbox.click()
                print("✅ Đã tắt Preview cho lesson.")
            else:
                print("ℹ️ Preview đã tắt sẵn.")
        # ===== Bước 7: Thêm Material =====
        # 1. Click nút Add Material
        wait.until(EC.element_to_be_clickable((By.ID, "btn-lp--add-material"))).click()
        print("✅ Đã click Add Material!")

        # 2. Chờ nhóm material xuất hiện và lấy nhóm cuối cùng
        material_groups = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".lp-material--group"))
        )
        latest_group = material_groups[-1]  # Nhóm mới nhất

        # 3. Điền tiêu đề file Material random
        random_number = random.randint(1000, 9999)
        title_input = latest_group.find_element(By.CSS_SELECTOR, ".lp-material--field-title")
        title_input.clear()
        title_input.send_keys(f"Material {random_number}")
        print(f"✅ Đã nhập Material title: Material {random_number}")

        # 4. Upload file
        upload_input = latest_group.find_element(By.CSS_SELECTOR, ".lp-material--field-upload")
        upload_input.send_keys(r"C:\Users\LAPTOP\Downloads\iloveimg-compressed\test.doc")  # Đường dẫn tuyệt đối
        print("✅ Đã chọn file upload!")

        # 3. Xử lý alert OK
        WebDriverWait(driver, 10).until(EC.alert_is_present())  # Chờ alert xuất hiện
        alert = driver.switch_to.alert
        alert.accept()  # Bấm nút OK
        print("✅ Đã bấm OK alert.")

        # 5. Click Save field
        save_btn = latest_group.find_element(By.CSS_SELECTOR, ".button.lp-material-save-field")
        save_btn.click()
        print("✅ Đã lưu Material!")

        # Chờ alert xuất hiện
        WebDriverWait(driver, 10).until(EC.alert_is_present())

        # Chuyển qua alert và accept
        alert = driver.switch_to.alert
        alert.accept()
        print("✅ Click nút OK thêm material thành công.")

        # ===== Bước 8: Cập nhật Lesson =====
        update_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "publish"))
        )
        driver.execute_script("arguments[0].click();", update_btn)
        print("✅ Đã click nút Update Lesson.")

        # Chờ thông báo cập nhật thành công
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "notice-success")))
        print("✅ Cập nhật lesson thành công!")

        # ===== Bước 8: Quay lại danh sách Lesson =====
        driver.get(LESSON_URL)
        print("✅ Quay lại danh sách Lesson thành công!")

    except Exception as e:
        print(f"❌ Lỗi xảy ra: {e}")


        
    finally:
        # Đóng trình duyệt sau vài giây
        time.sleep(5)
        driver.quit()
