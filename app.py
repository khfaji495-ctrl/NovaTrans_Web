import streamlit as st
import fitz
import deepl
from bidi.algorithm import get_display
import arabic_reshaper
import io
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط", layout="wide")

# كود CSS للتصميم
page_design = """
<style>
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
[data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #0e1117 0%, #16213e 100%); }
.main-title { color: #10b981; text-align: center; font-size: 3.5rem; font-weight: bold; margin-top: -20px; }
.sub-title { color: #cbd5e1; text-align: center; font-size: 1.2rem; margin-bottom: 30px; }
</style>
"""
st.markdown(page_design, unsafe_allow_html=True)

# العنوان و الـ GIF الأساسي
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("cat_pixel.gif") # استدعاء مباشر

st.markdown('<p class="main-title">سيد قط </p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">سيد قط يترجم ملازمك الهندسية والطبية بدقة</p>', unsafe_allow_html=True)

# إعداد المترجم
try:
    translator = deepl.Translator(st.secrets["DEEPL_API_KEY"])
except:
    st.error("⚠️ تأكد من إعداد مفتاح API في Secrets باسم DEEPL_API_KEY")
    st.stop()

def prepare_arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

# 4. التبويبات
tab1, tab2 = st.tabs(["😸 ترجمة السيد قط", "👨‍🏫 غرفة الدراسة"])

with tab1:
    c1, c2 = st.columns([0.1, 1])
    with c1:
        st.image("cati-pixel.gif") # استدعاء مباشر بدون تحديد width لتجنب الخطأ
    with c2:
        st.subheader("ترجمة السيد قط")
        
    uploaded_file = st.file_uploader("ارسل ملفك الى سيد قط", type="pdf")
    if uploaded_file is not None:
        uploaded_file.seek(0)
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        
        start = st.number_input("من صفحة:", 1, len(doc), 1)
        end = st.number_input("إلى صفحة:", 1, len(doc), start)

        if st.button("ابدأ الترجمه مع السيد قط"):
            placeholder = st.empty()
            with placeholder.container():
                col_anim1, col_anim2 = st.columns([1, 4])
                with col_anim1:
                    st.image("cati-pixel.gif") # استدعاء مباشر
                with col_anim2:
                    st.markdown("<br><h3>سيد قط يترجم، يرجى الانتظار...</h3>", unsafe_allow_html=True)

            new_doc = fitz.open()
            for i in range(start - 1, end):
                page = doc.load_page(i)
                new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
                new_page.show_pdf_page(new_page.rect, doc, page.number)
                
                if os.path.exists("font.ttf"):
                    new_page.insert_font(fontfile="font.ttf", fontname="ArabicFont")
                
                for block in page.get_text("dict")["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            text = "".join([s["text"] for s in line["spans"]])
                            x0, y0 = line["bbox"][0], line["bbox"][1]
                            if text.strip() and len(text.strip()) > 3:
                                try:
                                    ar_text = prepare_arabic_text(translator.translate_text(text, target_lang="AR").text)
                                    new_page.insert_text((x0, y0 - 2), ar_text, fontsize=8, fontname="ArabicFont")
                                except: continue
            
            placeholder.empty()
            output = io.BytesIO()
            new_doc.save(output)
            st.download_button("تحميل ملزمة السيد قط ", output.getvalue(), "SayedQatt_Translated.pdf")

with tab2:
    st.header("👨‍🏫 غرفة الدراسة الذكية")
    st.warning("⚠️ هذه الميزة تحت التطوير حالياً، انتظرنا قريباً! 😸")
