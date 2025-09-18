from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains

# ===== Cấu hình =====
USERNAME = "admin"  # Thay bằng tên đăng nhập thật
PASSWORD = "admin"  # Thay bằng mật khẩu thật
URL = "http://learnpresshi.local/wp-admin"
CREATE_COURSE_URL = "http://learnpresshi.local/wp-admin/post-new.php?post_type=lp_course"

# ===== Setup ChromeDriver =====
options = Options()
options.add_argument("--start-maximized")
service = Service()  # Nếu bạn cần chỉ định đường dẫn driver thì thêm vào Service('path/to/chromedriver')
driver = webdriver.Chrome(service=service, options=options)
actions = ActionChains(driver)
try:
    # ===== Mở trang đăng nhập =====
    driver.get(URL)

    # ===== Điền username =====
    username_field = driver.find_element(By.ID, "user_login")
    username_field.send_keys(USERNAME)

    # ===== Điền password =====
    password_field = driver.find_element(By.ID, "user_pass")
    password_field.send_keys(PASSWORD)

    # ===== Nhấn nút đăng nhập =====
    login_button = driver.find_element(By.ID, "wp-submit")
    login_button.click()

    # ===== Chờ & Kiểm tra đăng nhập thành công =====
    time.sleep(3)
    if "Dashboard" in driver.title or "wp-admin" in driver.current_url:
        print("✅ Đăng nhập thành công!")
    else:
        print("❌ Đăng nhập thất bại!")

 # ===== Step 2: Tạo khóa học mới =====
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

 # ===== Step 3: Kiểm tra khóa học đã xuất bản =====
    # -- Tìm khung chứa URL khóa học đã xuất bản --
    edit_slug_box = driver.find_element(By.ID, "edit-slug-box")
    permalink_link = edit_slug_box.find_element(By.TAG_NAME, "a")
    course_url = permalink_link.get_attribute("href")

    print("✅ Khóa học đã xuất bản tại:", course_url)

    # -- Click để mở trang khóa học --
    permalink_link.click()
    time.sleep(3)

    # -- Kiểm tra có vào đúng trang không --
    if "khoa-hoc" in driver.current_url or "course" in driver.current_url:
        print("✅ Trang khóa học mở thành công:", driver.current_url)
    else:
        print("❌ Không mở được trang khóa học")

finally:
    # ===== Đóng trình duyệt sau vài giây =====
    time.sleep(5)
    driver.quit()
