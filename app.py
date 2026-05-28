import streamlit as st
import fitz
import deepl
from bidi.algorithm import get_display
import arabic_reshaper
import io
import os

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

st.markdown('<p class="main-title">سيد قط </p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">سيد قط يترجم ملازمك الهندسية والطبية بدقة</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["😸  ترجم مع السيد قط " , "👨‍🏫 غرفة الدراسه"]) 

with tab1:
    try:
        auth_key = st.secrets["DEEPL_API_KEY"]
        translator = deepl.Translator(auth_key)
    except:
        st.error("⚠️ تأكد من إعداد مفتاح API في Secrets")
        st.stop()

    def prepare_arabic_text(text):
        return get_display(arabic_reshaper.reshape(text))

    uploaded_file = st.file_uploader(" 😸 ارسل ملف الملزمه للسيد قط", type="pdf")

    if uploaded_file is not None:
        uploaded_file.seek(0)
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        start = st.number_input("من صفحة:", 1, len(doc), 1)
        end = st.number_input("إلى صفحة:", 1, len(doc), start)

        if st.button("😸 ابدأ الترجمة مع سيد قط"):
            with st.spinner("🐈 سيد قط يترجم الآن.."):
                for i in range(start - 1, end):
                    page = doc.load_page(i)
                    
                    # تسجيل الخط
                    if os.path.exists("font.ttf"):
                        page.insert_font(fontfile="font.ttf", fontname="ArabicFont")
                    
                    blocks = page.get_text("blocks")
                    for i in range(start - 1, end):
                    page = doc.load_page(i)
                    if os.path.exists("font.ttf"):
                        page.insert_font(fontfile="font.ttf", fontname="ArabicFont")
                    
                    # استخدام get_text("dict") للوصول لكل سطر على حدة
                    data = page.get_text("dict")
                    for block in data["blocks"]:
                        if "lines" in block:
                            for line in block["lines"]:
                                line_text = "".join([span["text"] for span in line["spans"]])
                                
                                # إحداثيات السطر الحالي
                                rect = line["bbox"] 
                                x0, y0, x1, y1 = rect
                                
                                # شرط استثناء المعادلات
                                is_equation = any(char in line_text for char in ['=', '+', '-', '/', '*', '^', '∫', '∑'])
                                
                                if line_text.strip() and not is_equation:
                                    try:
                                        translated = translator.translate_text(line_text, target_lang="AR").text
                                        arabic = prepare_arabic_text(translated)
                                        
                                        # الرسم تحت السطر مباشرة
                                        # Y1 هو أسفل السطر، نكتب تحته مباشرة
                                        page.insert_text((x0, y1 + 2), arabic, fontsize=8, fontname="ArabicFont", color=(0, 0, 0))
                                    except:
                                        continue
                
                output = io.BytesIO()
                doc.save(output)
                output.seek(0)
                st.success("😼 تمت المهمة!")
                st.download_button("😸 تحميل الملزمة", output, "SayedQatt_Translated.pdf", "application/pdf")

with tab2:
    st.warning("⚠️ غرفة الدراسة تحت التطوير!")
