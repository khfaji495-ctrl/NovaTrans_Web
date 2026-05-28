import streamlit as st
import fitz  # PyMuPDF
import deepl
import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from bidi.algorithm import get_display
import arabic_reshaper

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط ", layout="wide")

page_design = """
<style>
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
[data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #0e1117 0%, #16213e 100%); }
.main-title { color: #10b981; text-align: center; font-size: 3.5rem; font-weight: bold; margin-top: -50px; }
.sub-title { color: #cbd5e1; text-align: center; font-size: 1.2rem; margin-bottom: 30px; }
</style>
"""
st.markdown(page_design, unsafe_allow_html=True)

# 2. العنوان
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("cat_pixel.gif", use_container_width=True)

st.markdown('<p class="main-title">سيد قط </p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">سيد قط يترجم ملازمك الهندسية والطبية بدقة</p>', unsafe_allow_html=True)

# 3. إعداد المترجم
try:
    auth_key = st.secrets["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
except:
    st.error("⚠️ خطأ: تأكد من إضافة مفتاح API في إعدادات Secrets")
    st.stop()

def prepare_arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

# 4. الواجهة
uploaded_file = st.file_uploader(" 😸 ارسل ملف الملزمه للسيد قط", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages_doc = len(doc)
    c1, c2 = st.columns(2)
    start = c1.number_input("من صفحة:", 1, total_pages_doc, 1)
    end = c2.number_input("إلى صفحة:", 1, total_pages_doc, start)

    if st.button("😸 ابدأ الترجمة مع سيد قط"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer)
        
        try:
            pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
        except:
            st.warning("⚠️ ملف الخط (font.ttf) غير موجود.")

        page_range = range(start - 1, end)
        total_pages = len(page_range)

        for idx, i in enumerate(page_range):
            status_text.text(f"جاري معالجة الصفحة {idx + 1} من {total_pages}...")
            page = doc.load_page(i)
            
            # --- رسم الصور في مكانها الأصلي ---
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                img_data = pix.tobytes("png")
                # استخدام ImageReader لحل مشكلة TypeError
                img_reader = ImageReader(io.BytesIO(img_data))
                
                rects = page.get_image_rects(xref)
                if rects:
                    rect = rects[0]
                    # تحويل الإحداثيات لـ ReportLab
                    img_y = page.rect.height - rect.y1 
                    c.drawImage(img_reader, rect.x0, img_y, width=rect.width, height=rect.height)

            # --- ترجمة النصوص ---
            text = page.get_text()
            lines = text.split('\n')
            y = 750
            for line in lines:
                if line.strip():
                    if y < 100:
                        c.showPage()
                        y = 750
                    c.setFont("Helvetica", 10)
                    c.drawString(50, y, line[:80])
                    y -= 15
                    try:
                        result = translator.translate_text(line, target_lang="AR")
                        c.setFont("Arabic", 10)
                        c.drawString(50, y, prepare_arabic_text(result.text))
                        y -= 30
                    except:
                        continue
            c.showPage()
            progress_bar.progress((idx + 1) / total_pages)
            
        c.save()
        pdf_buffer.seek(0)
        st.success("😼سيد قط أتم المهمة بنجاح!")
        st.download_button("😸 تحميل الملزمة", data=pdf_buffer, file_name="SayedQatt_Translated.pdf", mime="application/pdf")
