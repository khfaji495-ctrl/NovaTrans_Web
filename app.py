import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io
import google.generativeai as genai
from gtts import gTTS

# إعداد المساعد الذكي
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

# إعدادات الصفحة
st.set_page_config(page_title="سيد قط", layout="wide")

# (الـ CSS الخاص بك يبقى كما هو...)
st.markdown("""<style>[data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #0e1117 0%, #16213e 100%); }</style>""", unsafe_allow_html=True)

# إدارة الصفحات
if 'page' not in st.session_state:
    st.session_state.page = 'translator'

# --- صفحة الترجمة (كودك الأصلي) ---
if st.session_state.page == 'translator':
    st.title("سيد قط 😸")
    
    # [ضع هنا كود الترجمة الخاص بك كما هو...]
    if st.button("🚀 الدخول لغرفة الدراسة الذكية"):
        st.session_state.page = 'study_room'
        st.rerun()

# --- صفحة غرفة الدراسة (الفكرة الجديدة) ---
elif st.session_state.page == 'study_room':
    st.title("👨‍🏫 غرفة دراسة سيد قط")
    if st.button("⬅️ العودة للترجمة"):
        st.session_state.page = 'translator'
        st.rerun()
    
    user_q = st.text_input("اسأل المساعد الذكي عن فقرة في الملزمة:")
    if user_q:
        with st.spinner("سيد قط يشرح لك..."):
            # شرح ذكي
            response = model.generate_content(f"اشرح لي هذا بلهجة عراقية مبسطة: {user_q}")
            st.write(response.text)
            
            # تحويل الشرح لصوت
            if st.button("🔊 اسمع الشرح"):
                tts = gTTS(text=response.text, lang='ar')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp, format='audio/mp3')
