import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="NovaTrans Pro", layout="wide")

# 2. عرض القط (استخدام الرابط المباشر من GitHub لضمان الظهور)
st.image("https://raw.githubusercontent.com/khfaji495-ctrl/NovaTrans_Web/main/cat_pixel.gif", width=250)

st.title("🐱 NovaTrans Pro - المترجم الذكي")

# 3. إعداد المترجم
try:
    auth_key = st.secrets["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
except:
    st.error("خطأ: تأكد من إضافة مفتاح API في إعدادات Secrets.")
    st.stop()

def prepare_arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

# 4. واجهة المستخدم
uploaded_file = st.file_uploader("📂 اسحب ملف الملزمة هنا", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    
    col1, col2 = st.columns(2)
    start = col1.number_input("من صفحة:", 1, total_pages, 1)
    end = col2.number_input("إلى صفحة:", 1, total_pages, start)

    if st.button("🚀 ابدأ الترجمة"):
        with st.spinner("القط يقوم بالترجمة... مياو! 🐱"):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            # محاولة تسجيل الخط
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.warning("⚠️ ملاحظة: ملف الخط (font.ttf) غير موجود.")
            
            y = 800
            for i in range(start - 1, end):
                text = doc.load_page(i).get_text()
                for line in text.split('\n'):
                    if line.strip():
                        if y < 100:
                            c.showPage()
                            y = 800
                        c.setFont("Helvetica", 12)
                        c.drawString(50, y, line[:80])
                        y -= 20
                        try:
                            res = translator.translate_text(line, target_lang="AR")
                            c.setFont("Arabic", 12)
                            c.drawString(50, y, prepare_arabic_text(res.text))
                            y -= 40
                        except:
                            continue
            c.save()
            pdf_buffer.seek(0)
            st.success("✅ تمت المعالجة!")
            st.download_button("📥 تحميل الملف المترجم", pdf_buffer, "NovaTrans_Result.pdf", "application/pdf")
