import streamlit as st
import fitz  # هذا هو الاسم البرمجي لمكتبة pymupdf
import deepl
import os
import io

# تأكد من إضافة 'pymupdf' في ملف requirements.txt
# استخدم مفتاح الـ API من Secrets
auth_key = os.environ.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key)

st.title("NovaTrans Pro - المترجم الاحترافي")

uploaded_file = st.file_uploader("ارفع الملف", type="pdf")

if uploaded_file and st.button("ترجمة"):
    # نفتح الملف كـ "وثيقة قابلة للتعديل"
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    for page in doc:
        # البحث عن كتل النصوص فقط
        blocks = page.get_text("blocks")
        for b in blocks:
            # b[4] هو النص الموجود داخل الـ PDF
            text = b[4]
            if text.strip():
                # ترجمة النص
                translated_text = translator.translate_text(text, target_lang="AR").text
                
                # إخفاء النص القديم برسم مستطيل أبيض فوقه
                page.add_redact_annot(b[:4], fill=(1, 1, 1))
                page.apply_redactions()
                
                # كتابة الترجمة فوق المستطيل الأبيض
                # ملاحظة: هذا يتطلب خطاً يدعم العربية مثل Arial.ttf
                page.insert_text(b[:2], translated_text, fontname="helv", fontsize=10)

    # حفظ الملف الناتج
    output_buffer = io.BytesIO()
    doc.save(output_buffer)
    st.download_button("تحميل الملف المترجم", output_buffer.getvalue(), "Translated.pdf")
