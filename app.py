import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import time
import base64
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

st.set_page_config(page_title="Tra cứu mã vạch Hải Quan", layout="centered")
st.title("📦 Tra cứu mã vạch container Hải Quan")

# Input form
with st.form("form"):
    st.write("Nhập thông tin tờ khai để tra cứu")
    ma_dn = st.text_input("Mã doanh nghiệp", "0316841383")
    so_to_khai = st.text_input("Số tờ khai", "107082808930")
    ma_hq = st.text_input("Mã hải quan", "02CI")
    ngay_khai = st.date_input("Ngày tờ khai")
    submitted = st.form_submit_button("🔍 Tra cứu")

if submitted:
    with st.spinner("Đang tra cứu, vui lòng chờ..."):
        # Setup headless Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.get("https://pus1.customs.gov.vn/BarcodeContainer/BarcodeContainer.aspx")

            # Điền form
            driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtMaDN").send_keys(ma_dn)
            driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtSoToKhai").send_keys(so_to_khai)
            driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtMaHaiQuan").send_keys(ma_hq)
            driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtNgayTKhai").send_keys(ngay_khai.strftime("%d/%m/%Y"))

            # Lấy captcha
            captcha_img = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_imgCaptcha")
            captcha_img.screenshot("captcha.png")
            captcha_text = pytesseract.image_to_string(Image.open("captcha.png")).strip()
            driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtCaptcha").send_keys(captcha_text)

            # Submit form
            driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnTraCuu").click()
            time.sleep(3)

            # Chụp màn hình kết quả
            driver.save_screenshot("result.png")
            st.success("✅ Tra cứu thành công!")
            st.image("result.png", caption="Kết quả tờ khai")

        except Exception as e:
            st.error(f"❌ Lỗi: {e}")
        finally:
            driver.quit()
            if os.path.exists("captcha.png"): os.remove("captcha.png")
