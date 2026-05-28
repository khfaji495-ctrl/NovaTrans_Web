import streamlit as st
import fitz  # PyMuPDF
import deepl
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط", layout="wide")

# ... (نفس كود CSS الخاص بك) ...

# 2. إعداد المترجم
try:
    auth_key = st.secrets["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
except:
    st.error("⚠️ خطأ: تأكد من إضافة مفتاح API في إعدادات Secrets")
    st.stop()

# 3. الواجهة
uploaded_file = st.file_uploader("😸 ارسل ملف الملزمة للسيد قط", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages_doc = len(doc)
    c1, c2 = st.columns(2)
    start = c1.number_input("من صفحة:", 1, total_pages_doc, 1)
    end = c2.number_input("إلى صفحة:", 1, total_pages_doc, start)

    if st.button("😸 ابدأ الترجمة مع سيد قط"):
        output_pdf = fitz.open()  # إنشاء ملف جديد
        progress_bar = st.progress(0)
        
        with st.spinner("🐈 سيد قط يترجم الملزمة الآن..."):
            page_range = range(start - 1, end)
            for idx, i in enumerate(page_range):
                page = doc.load_page(i)
                # إنشاء صفحة جديدة بنفس أبعاد الأصلية
                new_page = output_pdf.new_page(width=page.rect.width, height=page.rect.height)
                
                # إدراج صورة الصفحة الأصلية (لضمان بقاء الصور والتنسيق)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                new_page.insert_image(page.rect, pixmap=pix)
                
                # إضافة النصوص
                blocks = sorted(page.get_text("blocks"), key=lambda b: b[1])
                for block in blocks:
                    if block[6] == 0:  # إذا كان نصاً
                        text = block[4].strip()
                        if len(text) > 3:
                            x, y = block[0], block[1]
                            
                            # كتابة النص الإنجليزي (الأصلي)
                            new_page.insert_text((x, y), text[:80], fontsize=9, color=(0.5, 0.5, 0.5))
                            
                            # كتابة الترجمة العربية أسفله مباشرة
                            try:
                                translated = translator.translate_text(text, target_lang="AR")
                                # ملاحظة: PyMuPDF يعرض العربية بشكل جيد إذا كان النص Unicode
                                new_page.insert_text((x, y + 15), translated.text, fontsize=9, color=(0, 0, 0))
                            except:
                                continue
                
                progress_bar.progress((idx + 1) / len(page_range))
            
            # حفظ الملف في الذاكرة
            output_buffer = io.BytesIO()
            output_pdf.save(output_buffer)
            output_buffer.seek(0)
            
            st.success("😼 تم بنجاح!")
            st.download_button("😸 تحميل الملزمة", data=output_buffer, file_name="SayedQatt_Translated.pdf", mime="application/pdf")
