import streamlit as st
import fitz
import io
import base64
import google.generativeai as genai
from gtts import gTTS
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper

# إعدادات المساعد
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(layout="wide", page_title="سيد قط")

# تخزين الملف في الـ session_state لمنع اختفائه
if 'uploaded_pdf' not in st.session_state:
    st.session_state.uploaded_pdf = None

st.title("سيد قط 😸")
uploaded_file = st.file_uploader("ارفع الملزمة (PDF):", type="pdf")

if uploaded_file:
    st.session_state.uploaded_pdf = uploaded_file

tab1, tab2 = st.tabs(["😸 صفحة الترجمة والحفظ", "👨‍🏫 غرفة الدراسة الذكية"])

# --- تبويب الترجمة ---
with tab1:
    if st.session_state.uploaded_pdf:
        if st.button("ابدأ الترجمة"):
            # هنا يجب وضع كود الرسم (canvas) الخاص بك بدقة
            st.success("جاري المعالجة...")
            # أضف هنا كود الترجمة الذي كنت تستخدمه (مع تسجيل الخط العربي)
    else:
        st.warning("يرجى رفع الملف أولاً!")

# --- تبويب غرفة الدراسة ---
with tab2:
    if st.session_state.uploaded_pdf:
        # عرض الـ PDF
        pdf_data = st.session_state.uploaded_pdf.getvalue()
        base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
        st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500"></iframe>', unsafe_allow_html=True)
        
        user_q = st.text_input("اسأل سيد قط:")
        if user_q:
            response = model.generate_content(f"اشرح لي بلهجة عراقية: {user_q}")
            st.write(response.text)
            if st.button("🔊 اسمع الشرح"):
                tts = gTTS(text=response.text, lang='ar')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp, format='audio/mp3')
    else:
        st.info("يرجى رفع ملف في الأعلى.")
