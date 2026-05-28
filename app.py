import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io
import base64
import google.generativeai as genai
from gtts import gTTS

# إعداد المساعد الذكي
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط ", layout="wide")

# كود CSS: إخفاء القائمة + الخلفية + التنسيق
page_design = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #0e1117 0%, #16213e 100%); }
[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
.main-title { color: #10b981; text-align: center; font-size: 3.5rem; font-weight: bold; margin-top: -50px; }
.sub-title { color: #cbd5e1; text-align: center; font-size: 1.2rem; margin-bottom: 30px; }
</style>
"""
st.markdown(page_design, unsafe_allow_html=True)

# 2. عرض الـ GIF والعنوان
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("cat_pixel.gif", use_container_width=True)

st.markdown('<p class="main-title">سيد قط </p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">سيد قط يترجم ملازمك الهندسية والطبية بدقة</p>', unsafe_allow_html=True)

# إدارة ذاكرة الملف
if 'uploaded_pdf' not in st.session_state:
    st.session_state.uploaded_pdf = None

# التبويبات الجديدة
tab1, tab2 = st.tabs(["😸 الترجمة", "👨‍🏫 غرفة الدراسة"])

with tab1:
    # 3. إعداد مترجم DeepL
    try:
        auth_key = st.secrets["DEEPL_API_KEY"]
        translator = deepl.Translator(auth_key)
    except Exception as e:
        st.error("⚠️ خطأ: تأكد من إضافة مفتاح API في إعدادات Secrets باسم DEEPL_API_KEY")
        st.stop()

    def prepare_arabic_text(text):
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)

    # 4. واجهة رفع الملفات
    st.divider()
    uploaded_file = st.file_uploader(" 😸 ارسل ملف الملزمه للسيد قط", type="pdf")

    if uploaded_file is not None:
        st.session_state.uploaded_pdf = uploaded_file
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        total_pages = len(doc)
        
        c1, c2 = st.columns(2)
        with c1: start = st.number_input("من صفحة:", 1, total_pages, 1)
        with c2: end = st.number_input("إلى صفحة:", 1, total_pages, start)

        if st.button("😸 ابدأ الترجمة مع سيد قط"):
            with st.spinner(".... 🐈سيد قط يترجم الملزمة الآن.. يرجى الانتظار"):
                pdf_buffer = io.BytesIO()
                c = canvas.Canvas(pdf_buffer)
                try:
                    pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
                except:
                    st.warning("⚠️ تنبيه: ملف الخط (font.ttf) غير موجود.")
                
                y = 800 
                for i in range(start - 1, end):
                    text = doc.load_page(i).get_text()
                    lines = text.split('\n')
                    for line in lines:
                        if line.strip():
                            if y < 100:
                                c.showPage()
                                y = 800
                            c.setFont("Helvetica", 12)
                            c.drawString(50, y, line[:80])
                            y -= 20
                            try:
                                result = translator.translate_text(line, target_lang="AR")
                                proper_arabic = prepare_arabic_text(result.text)
                                c.setFont("Arabic", 12)
                                c.drawString(50, y, proper_arabic)
                                y -= 40
                            except: continue
                c.save()
                pdf_buffer.seek(0)
                st.success("😼سيد قط أتم المهمة بنجاح!")
                st.download_button("😸 تحميل الملزمة من سيد قط", pdf_buffer, "SayedQatt_Translated.pdf", "application/pdf")

from groq import Groq

# إعداد المساعد باستخدام Groq (بديل سريع لـ Google)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

with tab2:
    if st.session_state.uploaded_pdf:
        st.write("---")
        user_q = st.text_input("اسأل سيد قط عن الملزمة:")
        
        if user_q and user_q.strip() != "":
            with st.spinner("سيد قط يحلل المعلومات..."):
                try:
                    # طلب الشرح من Llama 3 عبر Groq
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "أنت مساعد ذكي اسمه سيد قط، تشرح الملازم بلهجة عراقية بسيطة."},
                            {"role": "user", "content": f"اشرح لي هذا بلهجة عراقية: {user_q}"}
                        ],
                        model="llama3-8b-8192",
                    )
                    
                    response_text = chat_completion.choices[0].message.content
                    st.write(response_text)
                    
                    if st.button("🔊 اسمع الشرح"):
                        tts = gTTS(text=response_text, lang='ar')
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        st.audio(fp, format='audio/mp3')
                except Exception as e:
                    st.error(f"خطأ في الاتصال: {e}")
        else:
            st.write("بانتظار سؤالك يا بطل! 😸")
    else:
        st.info("يرجى رفع الملف في تبويب الترجمة أولاً.")
