from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

# Khởi động trình duyệt Edge 123
edge_options = webdriver.EdgeOptions()
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)

# Truy cập vào trang web
driver.get("http://qldt.actvn.edu.vn/CMCSoft.IU.Web.Info/Login.aspx")

# Tìm phần tử của form đăng nhập
username_input = driver.find_element(By.ID, "txtUserName")  # ID của ô nhập tên tài khoản
password_input = driver.find_element(By.ID, "txtPassword")  # ID của ô nhập mật khẩu

# Điền thông tin đăng nhập
username_input.send_keys("CT07N0134")
password_input.send_keys("07/04/2004")

# Nhấn nút đăng nhập
login_button = driver.find_element(By.ID, "btnSubmit")  # ID của nút đăng nhập
login_button.click()
# Chuyển đổi ngữ cảnh sang hộp thoại thông báo
alert = driver.switch_to.alert

# Bấm vào nút "OK"
alert.accept()
home_button = driver.find_element(By.LINK_TEXT, "Trang chủ")
home_button.click()
pla_button = driver.find_element(By.LINK_TEXT, "Thông tin cá nhân (SV)")
pla_button.click()

time.sleep(1)
score_button = driver.find_element(By.LINK_TEXT, "Tra cứu điểm")
score_button.click()

# Xác định bảng điểm chi tiết
table = driver.find_element(By.ID, "tblStudentMark")
rows = table.find_elements(By.TAG_NAME, "tr")

# Khởi tạo tổng TKHP
total_tkhp = 0
total_tc = 0
total_gpa = 0

# Hàm tính GPA
def calculate_gpa(tkhp):
    gpa_scale = {
        9: 4,
        8.5: 3.8,
        7.8: 3.5,
        7: 3,
        6.3: 2.4,
        5.5: 2,
        4.8: 1.5,
        4: 1,
        0: 0
    }
    for key in sorted(gpa_scale.keys(), reverse=True):
        if tkhp >= key:
            return gpa_scale[key]
    return 0

# Duyệt qua từng hàng (bỏ qua hàng tiêu đề đầu tiên)
for row in rows[1:]:
    # Lấy tất cả các ô (cột) trong hàng
    cols = row.find_elements(By.TAG_NAME, "td")
    
    # Kiểm tra số lượng cột có đúng không
    if len(cols) >= 14:
    # Lấy tên môn học từ cột thứ 2 (giả sử cột tên môn học là cột thứ 2)
        ten_mon_hoc = cols[2].text.strip()    
    # Kiểm tra nếu tên môn học không phải là "Giáo dục thể chất..."
        if not ten_mon_hoc.startswith("Giáo dục thể chất"):
            # Lấy điểm TKHP từ cột cuối cùng (giả sử cột TKHP là cột thứ 14)
            try:
                tkhp = float(cols[13].text)
                tc = float(cols[3].text)
                gpa = calculate_gpa(tkhp)
                total_gpa += gpa * tc
                total_tkhp += tkhp * tc
                total_tc += tc
            except ValueError:
                print(f"Lỗi: Không thể chuyển đổi giá trị '{cols[13].text}' thành số")
    else:
        row_html = row.get_attribute("outerHTML")
        print(f"Hàng không đủ cột (có {len(cols)} cột):\n{row_html}\n")

pla = int(input("Nhập số môn còn thiếu: "))
for i in range(1, pla + 1):
    print(f"Nhập môn thứ {i}")
    tc = float(input("Nhập số tín chỉ: "))
    tkhp = float(input("Nhập điểm TKHP: "))
    gpa = calculate_gpa(tkhp)
    total_gpa += gpa * tc
    total_tkhp += tkhp * tc
    total_tc += tc

# Hiển thị số lượng môn học và tổng TKHP
print(f"Số môn học: {len(rows) - 2 + pla}")
print(f"Tổng TC: {total_tc}")
print(f"Tổng TKHP: {total_tkhp}")
print(f"Điểm TBC: {total_tkhp / total_tc}")
phuc = total_gpa / total_tc
print(f"Điểm GPA: {phuc}")

# Xếp loại GPA
gpa_classification = {
    3.6: "xuất sắc",
    3.2: "giỏi",
    2.5: "khá",
    2: "Trung bình",
    1: "Yếu",
    0: "Kém"
}
for key in sorted(gpa_classification.keys(), reverse=True):
    if phuc >= key:
        gpa = gpa_classification[key]
        break

print(f"Xếp loại: {gpa}")
remaining_tc = 122 - total_tc
print(f"Số tín chỉ còn lại: {remaining_tc}")
print(f"Điểm cần đạt/tc để được loại xuất sắc: {(122 * 3.6 - total_gpa) / remaining_tc}")
print(f"Điểm cần đạt/tc để được loại giỏi: {(122 * 3.2 - total_gpa) / remaining_tc}")

input("Nhấn Enter để đóng trình duyệt...")
# Sau khi hoàn thành, đóng trình duyệt
# driver.quit()