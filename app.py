import streamlit as st
import fitz  # PyMuPDF
import deepl
import os
import arabic_reshaper
from bidi.algorithm import get_display

auth_key = os.environ.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key)

st.title("NovaTrans - المترجم المباشر")

uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")

if uploaded_file and st.button("ترجمة"):
    # فتح الملف الأصلي مباشرة
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    for page in doc:
        # 1. إيجاد النصوص في الصفحة
        text_instances = page.get_text("dict")["blocks"]
        
        for block in text_instances:
            if "lines" in block:
                for line in block["lines"]:
                    # استخراج النص من السطر
                    raw_text = "".join([span["text"] for span in line["spans"]])
                    
                    if raw_text.strip():
                        # ترجمة
                        try:
                            res = translator.translate_text(raw_text, target_lang="AR").text
                            bidi_text = get_display(arabic_reshaper.reshape(res))
                            
                            # رسم مستطيل أبيض لتغطية النص الأصلي (اختياري)
                            # page.draw_rect(line["bbox"], color=(1, 1, 1), fill=(1, 1, 1))
                            
                            # كتابة الترجمة العربية في مكان النص الأصلي
                            page.insert_text(line["bbox"][:2], bidi_text, fontname="helv", fontsize=10, color=(0, 0, 0))
                        except:
                            continue
                            
    # حفظ الملف المعدل
    output_buffer = io.BytesIO()
    doc.save(output_buffer)
    st.success("✅ تمت المعالجة!")
    st.download_button("تحميل", output_buffer.getvalue(), "Translated.pdf")
