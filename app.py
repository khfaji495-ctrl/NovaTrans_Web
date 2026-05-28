import streamlit as st
import fitz
import deepl
from bidi.algorithm import get_display
import arabic_reshaper
import io
from groq import Groq

# إعداد المساعد الجديد (Groq)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط ", layout="wide")

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

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("cat_pixel.gif", use_container_width=True)

st.markdown('<p class="main-title">سيد قط </p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">سيد قط يترجم ملازمك الهندسية والطبية بدقة</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["😸  ترجم مع السيد قط " , "👨‍🏫 غرفة الدراسه"]) 

with tab1:
    try:
        auth_key = st.secrets["DEEPL_API_KEY"]
        translator = deepl.Translator(auth_key)
    except Exception as e:
        st.error("⚠️ خطأ: تأكد من إضافة مفتاح API")
        st.stop()

    def prepare_arabic_text(text):
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)

    uploaded_file = st.file_uploader(" 😸 ارسل ملف الملزمه للسيد قط", type="pdf")

    if uploaded_file is not None:
        uploaded_file.seek(0)
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        total_pages = len(doc)
        
        c1, c2 = st.columns(2)
        with c1: start = st.number_input("من صفحة:", 1, total_pages, 1)
        with c2: end = st.number_input("إلى صفحة:", 1, total_pages, start)

        if st.button("😸 ابدأ الترجمة مع سيد قط"):
            with st.spinner(".... 🐈سيد قط يترجم الملزمة الآن.. يرجى الانتظار"):
                # التسجيل للخط
                try:
                    doc.insert_font(fontfile="font.ttf", fontname="ArabicFont")
                except:
                    st.warning("⚠️ ملف الخط (font.ttf) مفقود، قد لا تظهر العربية بشكل صحيح.")

                for i in range(start - 1, end):
                    page = doc.load_page(i)
                    blocks = page.get_text("blocks")
                    
                    for b in blocks:
                        text = b[4]
                        x0, y0, x1, y1 = b[:4]
                        
                        # كشف المعادلات البسيطة (إذا وجد رمز رياضي لا تترجم)
                        is_equation = any(char in text for char in ['=', '+', '-', '/', '*', '^', '\\', '∫', '∑'])
                        
                        if text.strip() and not is_equation:
                            try:
                                result = translator.translate_text(text, target_lang="AR")
                                proper_arabic = prepare_arabic_text(result.text)
                                # الكتابة فوق الصفحة الأصلية
                                page.insert_text((x0, y1), proper_arabic, fontsize=10, fontname="ArabicFont", color=(0, 0, 0))
                            except:
                                continue

                output_buffer = io.BytesIO()
                doc.save(output_buffer)
                doc.close()
                output_buffer.seek(0)
                
                st.success("😼سيد قط أتم المهمة بنجاح!")
                st.download_button("😸 تحميل الملزمة من سيد قط", output_buffer, "SayedQatt_Translated.pdf", "application/pdf")

with tab2:
    st.warning("⚠️ غرفة الدراسة الذكية تحت التطوير حالياً، انتظرنا قريباً! 😸")
