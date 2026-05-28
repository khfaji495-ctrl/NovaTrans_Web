import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io
from groq import Groq
from gtts import gTTS

# إعداد المساعد (Groq)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط", layout="wide")

# كود CSS
page_design = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #0e1117 0%, #16213e 100%); }
.main-title { color: #10b981; text-align: center; font-size: 3.5rem; font-weight: bold; margin-top: -50px; }
.sub-title { color: #cbd5e1; text-align: center; font-size: 1.2rem; margin-bottom: 30px; }
</style>
"""
st.markdown(page_design, unsafe_allow_html=True)

# 2. العنوان
st.markdown('<p class="main-title">سيد قط</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">سيد قط يترجم ملازمك الهندسية والطبية بدقة</p>', unsafe_allow_html=True)

# التبويبات
tab1, tab2 = st.tabs(["😸 ترجم مع السيد قط", "👨‍🏫 غرفة الدراسة"])

with tab1:
    try:
        translator = deepl.Translator(st.secrets["DEEPL_API_KEY"])
    except:
        st.error("تأكد من إضافة DEEPL_API_KEY")
        st.stop()

    def prepare_arabic_text(text):
        return get_display(arabic_reshaper.reshape(text))

    uploaded_file = st.file_uploader("😸 ارسل ملف الملزمة للسيد قط", type="pdf")

    if uploaded_file:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        start = st.number_input("من صفحة:", 1, len(doc), 1)
        end = st.number_input("إلى صفحة:", 1, len(doc), start)

        if st.button("😸 ابدأ الترجمة مع سيد قط"):
            with st.spinner("سيد قط يترجم الآن..."):
                pdf_buffer = io.BytesIO()
                c = canvas.Canvas(pdf_buffer)
                # ... (باقي منطق الترجمة الخاص بك) ...
                c.save()
                pdf_buffer.seek(0)
                st.success("تمت المهمة!")
                st.download_button("تحميل الملف", pdf_buffer, "translated.pdf")

with tab2:
    st.warning("⚠️ غرفة الدراسة الذكية تحت التطوير حالياً، انتظرنا قريباً! 😸")
