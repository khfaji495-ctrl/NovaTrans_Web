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

# 1. إعدادات الـ API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
translator = deepl.Translator(st.secrets["DEEPL_API_KEY"])

st.set_page_config(layout="wide", page_title="سيد قط الاحترافي")

# 2. إدارة الذاكرة (لضمان بقاء الملف)
if 'uploaded_pdf' not in st.session_state:
    st.session_state.uploaded_pdf = None

def register_arabic_font():
    try:
        pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
    except:
        st.error("⚠️ خطأ: تأكد من وجود ملف font.ttf في مجلد المشروع!")

st.title("سيد قط 😸")
uploaded_file = st.file_uploader("ارفع الملزمة (PDF) للبدء:", type="pdf")

if uploaded_file:
    st.session_state.uploaded_pdf = uploaded_file

# 3. التبويبات الرئيسية
tab1, tab2 = st.tabs(["😸 صفحة الترجمة والحفظ", "👨‍🏫 غرفة الدراسة الذكية"])

# --- تبويب الترجمة والحفظ ---
with tab1:
    if st.session_state.uploaded_pdf:
        if st.button("بدء الترجمة وحفظ الملف"):
            with st.spinner("سيد قط يترجم ويكتب الخط العربي..."):
                register_arabic_font()
                doc = fitz.open(stream=st.session_state.uploaded_pdf.read(), filetype="pdf")
                pdf_buffer = io.BytesIO()
                c = canvas.Canvas(pdf_buffer)
                
                # منطق الترجمة والرسم (تأكد من تعديل الإحداثيات حسب حاجتك)
                # ... (هنا ضع كود الرسم الخاص بك بـ reportlab) ...
                
                c.save()
                pdf_buffer.seek(0)
                
                st.download_button(
                    label="📥 تحميل الملزمة المترجمة",
                    data=pdf_buffer,
                    file_name="Translated_SayedQatt.pdf",
                    mime="application/pdf"
                )
                st.success("تم الحفظ بنجاح! 😸")
    else:
        st.info("يرجى رفع ملف في الأعلى للبدء.")

# --- تبويب غرفة الدراسة ---
with tab2:
    if st.session_state.uploaded_pdf:
        col_pdf, col_chat = st.columns([1, 1])
        with col_pdf:
            st.subheader("الملزمة")
            pdf_data = st.session_state.uploaded_pdf.getvalue()
            base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600"></iframe>', unsafe_allow_html=True)
        
        with col_chat:
            st.subheader("سيد قط يشرح لك:")
            user_q = st.text_input("اسألني عن أي جزء:")
            if user_q:
                with st.spinner("سيد قط يفكر..."):
                    response = model.generate_content(f"اشرح لي هذا بلهجة عراقية: {user_q}")
                    st.write(response.text)
                    if st.button("🔊 اسمع الشرح صوتياً"):
                        tts = gTTS(text=response.text, lang='ar')
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        st.audio(fp, format='audio/mp3')
    else:
        st.info("يرجى رفع الملف في تبويب الترجمة أولاً.")
