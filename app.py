import streamlit as st
import fitz
import deepl
from bidi.algorithm import get_display
import arabic_reshaper
import io
import os

# إعدادات الصفحة
st.set_page_config(page_title="سيد قط", layout="wide")

# المترجم
translator = deepl.Translator(st.secrets["DEEPL_API_KEY"])

def prepare_arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

# واجهة المستخدم
st.title("😸 سيد قط للترجمة")

tab1, tab2 = st.tabs(["😸 ترجمة الملفات", "👨‍🏫 غرفة الدراسة"])

with tab1:
    uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")
    if uploaded_file is not None:
        uploaded_file.seek(0)
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        
        if st.button("ابدأ الترجمة"):
            new_doc = fitz.open()
            for page in doc:
                new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
                new_page.show_pdf_page(new_page.rect, doc, page.number)
                
                if os.path.exists("font.ttf"):
                    new_page.insert_font(fontfile="font.ttf", fontname="ArabicFont")
                
                for block in page.get_text("dict")["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            text = "".join([s["text"] for s in line["spans"]])
                            x0, y1 = line["bbox"][0], line["bbox"][3]
                            if text.strip() and len(text.strip()) > 3:
                                try:
                                    ar_text = prepare_arabic_text(translator.translate_text(text, target_lang="AR").text)
                                    new_page.insert_text((x0, y1 + 10), ar_text, fontsize=9, fontname="ArabicFont")
                                except: continue
            
            output = io.BytesIO()
            new_doc.save(output)
            st.download_button("تحميل الملزمة المترجمة", output.getvalue(), "SayedQatt_Translated.pdf")

with tab2:
    st.header("👨‍🏫 غرفة الدراسة الذكية")
    st.write("هنا يمكنك مراجعة ملاحظاتك وطرح أسئلة على سيد قط حول الملزمة.")
    user_query = st.text_input("اسأل سيد قط عن محتوى الملزمة:")
    if user_query:
        st.info(f"سيد قط يحلل سؤالك: {user_query} ... (قريباً سيتم ربط الذكاء الاصطناعي هنا!)")
