import streamlit as st
from PIL import Image
import pytesseract
import requests
from io import BytesIO
import datetime

st.set_page_config(page_title="Tra cứu mã vạch Hải Quan", layout="centered")
st.title("📦 Tra cứu mã vạch container Hải Quan")

# Input form
with st.form("form"):
    st.write("Nhập thông tin tờ khai để tra cứu")
    ma_dn = st.text_input("Mã doanh nghiệp", "0316841383")
    so_to_khai = st.text_input("Số tờ khai", "107082808930")
    ma_hq = st.text_input("Mã hải quan", "02CI")
    ngay_khai = st.date_input("Ngày tờ khai", datetime.date.today())
    submitted = st.form_submit_button("🔍 Tra cứu")

if submitted:
    with st.spinner("Đang tra cứu, vui lòng chờ..."):
        try:
            # Gửi yêu cầu GET để lấy trang chứa captcha
            session = requests.Session()
            response = session.get("https://pus1.customs.gov.vn/BarcodeContainer/BarcodeContainer.aspx")
            response.raise_for_status()

            # Trích xuất ảnh captcha từ trang
            # (Ở đây bạn cần sử dụng BeautifulSoup để phân tích HTML và tìm URL của ảnh captcha)
            # Giả sử bạn đã có URL của ảnh captcha:
            captcha_url = "https://pus1.customs.gov.vn/BarcodeContainer/CaptchaImage.aspx"

            captcha_response = session.get(captcha_url)
            captcha_image = Image.open(BytesIO(captcha_response.content))

            # Hiển thị ảnh captcha cho người dùng nhập tay nếu cần
            st.image(captcha_image, caption="Mã captcha")
            captcha_text = pytesseract.image_to_string(captcha_image).strip()

            # Gửi yêu cầu POST với dữ liệu tờ khai và captcha
            payload = {
                'ctl00$ContentPlaceHolder1$txtMaDN': ma_dn,
                'ctl00$ContentPlaceHolder1$txtSoToKhai': so_to_khai,
                'ctl00$ContentPlaceHolder1$txtMaHaiQuan': ma_hq,
                'ctl00$ContentPlaceHolder1$txtNgayTKhai': ngay_khai.strftime("%d/%m/%Y"),
                'ctl00$ContentPlaceHolder1$txtCaptcha': captcha_text,
                'ctl00$ContentPlaceHolder1$btnTraCuu': 'Tra cứu'
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            post_response = session.post("https://pus1.customs.gov.vn/BarcodeContainer/BarcodeContainer.aspx", data=payload, headers=headers)
            post_response.raise_for_status()

            # Phân tích kết quả và hiển thị mã vạch
            # (Bạn cần sử dụng BeautifulSoup để trích xuất ảnh mã vạch từ HTML)
            # Giả sử bạn đã trích xuất được ảnh mã vạch:
            barcode_image_url = "https://pus1.customs.gov.vn/BarcodeContainer/GeneratedBarcode.aspx"

            barcode_response = session.get(barcode_image_url)
            barcode_image = Image.open(BytesIO(barcode_response.content))
            st.success("✅ Tra cứu thành công!")
            st.image(barcode_image, caption="Kết quả mã vạch")

        except Exception as e:
            st.error(f"❌ Lỗi: {e}")
