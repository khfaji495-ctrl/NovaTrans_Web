import streamlit as st
import fitz
import deepl
import io
import base64
import google.generativeai as genai
from gtts import gTTS
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper

# إعدادات المساعد والترجمة
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash') # استخدمت فلاش لأنه أسرع وأذكى في قراءة الملفات
translator = deepl.Translator(st.secrets["DEEPL_API_KEY"])

st.set_page_config(layout="wide", page_title="سيد قط الاحترافي")

def prepare_arabic(text):
    return get_display(arabic_reshaper.reshape(text))

# عرض الـ PDF
def display_pdf(file):
    base64_pdf = base64.b64encode(file.getvalue()).decode('utf-8')
    st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600"></iframe>', unsafe_allow_html=True)

st.title("سيد قط 😸")
uploaded_file = st.file_uploader("ارفع الملزمة (PDF):", type="pdf")

tab1, tab2 = st.tabs(["😸 صفحة الترجمة والحفظ", "👨‍🏫 غرفة الدراسة الذكية"])

# --- تبويب الترجمة والحفظ ---
with tab1:
    if uploaded_file:
        if st.button("بدء الترجمة وحفظ الملف"):
            with st.spinner("سيد قط يعمل على الحفظ..."):
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                pdf_buffer = io.BytesIO()
                c = canvas.Canvas(pdf_buffer)
                
                # [هنا يوضع كود الرسم الذي اتفقنا عليه]
                # بعد انتهاء الرسم:
                c.save()
                pdf_buffer.seek(0)
                
                # زر التحميل المباشر
                st.download_button(
                    label="📥 تحميل الملزمة المترجمة النهائية",
                    data=pdf_buffer,
                    file_name="Translated_SayedQatt.pdf",
                    mime="application/pdf"
                )
                st.success("تم تجهيز الملف للتحميل! 😸")

# --- تبويب غرفة الدراسة ---
with tab2:
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        with col1:
            display_pdf(uploaded_file)
        with col2:
            user_q = st.text_input("اسأل سيد قط عن أي فقرة:")
            if user_q:
                response = model.generate_content(f"اشرح لي هذا بلهجة عراقية: {user_q}")
                st.write(response.text)
                if st.button("🔊 اسمع الشرح"):
                    tts = gTTS(text=response.text, lang='ar')
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    st.audio(fp, format='audio/mp3')
    else:
        st.info("يرجى رفع ملف في الأعلى.")
