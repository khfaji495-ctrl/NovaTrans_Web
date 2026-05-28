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
        st.error("⚠️ تأكد من إعداد مفتاح API في Secrets باسم DEEPL_API_KEY")
        st.stop()

    def prepare_arabic_text(text):
        return get_display(arabic_reshaper.reshape(text))

    uploaded_file = st.file_uploader(" 😸 ارسل ملف الملزمه للسيد قط", type="pdf")

    if uploaded_file is not None:
        uploaded_file.seek(0)
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        
        start = st.number_input("من صفحة:", 1, len(doc), 1)
        end = st.number_input("إلى صفحة:", 1, len(doc), start)

        if st.button("😸 ابدأ الترجمة مع سيد قط"):
            with st.spinner("🐈 سيد قط يترجم الآن.."):
                for i in range(start - 1, end):
                    page = doc.load_page(i)
                    
                    if os.path.exists("font.ttf"):
                        page.insert_font(fontfile="font.ttf", fontname="ArabicFont")
                    
                    data = page.get_text("dict")
                    for block in data.get("blocks", []):
                        if "lines" in block:
                            for line in block["lines"]:
                                line_text = "".join([span["text"] for span in line["spans"]])
                                rect = line["bbox"]
                                y1 = rect[3]
                                x0 = rect[0]
                                
                                is_equation = any(char in line_text for char in ['=', '+', '-', '/', '*', '^', '∫', '∑'])
                                
                                if line_text.strip() and not is_equation and len(line_text.strip()) > 3:
                                    try:
                                        translated = translator.translate_text(line_text, target_lang="AR").text
                                        arabic = prepare_arabic_text(translated)
                                        # إضافة خلفية بيضاء صغيرة للوضوح
                                        page.draw_rect([x0, y1, x0 + 250, y1 + 12], color=(1, 1, 1), fill=(1, 1, 1))
                                        page.insert_text((x0, y1 + 10), arabic, fontsize=8, fontname="ArabicFont", color=(0, 0, 0))
                                    except:
                                        continue
                
                output = io.BytesIO()
                doc.save(output)
                output.seek(0)
                st.success("😼 تمت المهمة!")
                st.download_button("😸 تحميل الملزمة", output, "SayedQatt_Translated.pdf", "application/pdf")

with tab2:
    st.warning("⚠️ غرفة الدراسة تحت التطوير!")
