import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io
import re

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(page_title="سيد قط", layout="wide")

page_design = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0e1117 0%, #16213e 100%);
}

.main-title {
    color: #10b981;
    text-align: center;
    font-size: 3.5rem;
    font-weight: bold;
}

.sub-title {
    color: #cbd5e1;
    text-align: center;
    font-size: 1.2rem;
    margin-bottom: 20px;
}
</style>
"""
st.markdown(page_design, unsafe_allow_html=True)

# -----------------------------
# UI
# -----------------------------
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.image("cat_pixel.gif", use_container_width=True)

st.markdown('<p class="main-title">سيد قط</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ترجمة الملازم مع الحفاظ على التنسيق</p>', unsafe_allow_html=True)

# -----------------------------
# DeepL
# -----------------------------
try:
    translator = deepl.Translator(st.secrets["DEEPL_API_KEY"])
except:
    st.error("أضف مفتاح DeepL API")
    st.stop()

# -----------------------------
# Arabic fix
# -----------------------------
def prepare_arabic_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# -----------------------------
# تنظيف النص (تجاهل المعادلات)
# -----------------------------
def is_equation(line):
    return bool(re.search(r"[=<>±∑∫√]|\\|\\(|\\)|\\d+\\/\\d+", line))

# -----------------------------
# تقسيم ذكي لتقليل التداخل
# -----------------------------
def split_text(text, max_len=90):
    words = text.split()
    lines = []
    current = ""

    for w in words:
        if len(current + " " + w) <= max_len:
            current += " " + w
        else:
            lines.append(current.strip())
            current = w
    if current:
        lines.append(current.strip())
    return lines

# -----------------------------
# Upload
# -----------------------------
uploaded_file = st.file_uploader("😸 ارسل ملف الملزمة", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)

    c1, c2 = st.columns(2)
    with c1:
        start = st.number_input("من صفحة:", 1, total_pages, 1)
    with c2:
        end = st.number_input("إلى صفحة:", 1, total_pages, start)

    if st.button("ابدأ الترجمة 😼"):
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer)

        try:
            pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            arabic_font = "Arabic"
        except:
            arabic_font = "Helvetica"

        y = 800

        for i in range(start - 1, end):
            page = doc.load_page(i)

            # يحافظ على الصور (تقريبياً)
            blocks = page.get_text("blocks")

            for b in blocks:
                text = b[4].strip()

                if not text:
                    continue

                # تجاهل المعادلات
                if is_equation(text):
                    continue

                for line in split_text(text):

                    if y < 120:
                        c.showPage()
                        y = 800

                    # النص الإنجليزي
                    c.setFont("Helvetica", 11)
                    c.drawString(50, y, line[:120])
                    y -= 18

                    try:
                        translated = translator.translate_text(line, target_lang="AR").text
                        ar = prepare_arabic_text(translated)

                        # الترجمة فوقه
                        c.setFont(arabic_font, 12)
                        c.drawString(50, y, ar[:120])
                        y -= 30

                    except:
                        continue

                y -= 10

        c.save()
        pdf_buffer.seek(0)

        st.success("تمت الترجمة بنجاح 😼")

        st.download_button(
            "تحميل الملف",
            pdf_buffer,
            file_name="translated.pdf",
            mime="application/pdf"
        )
