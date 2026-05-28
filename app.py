import streamlit as st
import fitz
import deepl
import io

# [إعدادات الصفحة وCSS تبقى كما هي...]

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    if st.button("😸 ابدأ الترجمة مع سيد قط"):
        # نفتح ملف PDF جديد لنحفظ فيه التعديلات
        output_pdf = fitz.open()
        
        with st.spinner(".... 🐈سيد قط يترجم الآن.."):
            for i in range(start - 1, end):
                page = doc.load_page(i)
                # إنشاء صفحة جديدة بنفس أبعاد الأصلية
                new_page = output_pdf.new_page(width=page.rect.width, height=page.rect.height)
                
                # نسخ الصفحة الأصلية كصورة (لضمان ظهور كل شيء)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                new_page.insert_image(page.rect, pixmap=pix)
                
                # إضافة النصوص
                blocks = sorted(page.get_text("blocks"), key=lambda b: b[1])
                for block in blocks:
                    if block[6] == 0:  # نص
                        text = block[4].strip()
                        if len(text) > 2:
                            x, y = block[0], block[1]
                            # إضافة الأصل
                            new_page.insert_text((x, y), text[:80], fontsize=10)
                            
                            # إضافة الترجمة تحت النص بمسافة بسيطة
                            try:
                                translated = translator.translate_text(text, target_lang="AR")
                                # ملاحظة: استخدم خطاً يدعم العربية إذا لزم الأمر
                                new_page.insert_text((x, y + 15), translated.text, fontsize=10)
                            except:
                                continue
            
            # حفظ وتحميل
            output_buffer = io.BytesIO()
            output_pdf.save(output_buffer)
            output_buffer.seek(0)
            st.success("😼 تم بنجاح!")
            st.download_button("تحميل الملزمة", data=output_buffer, file_name="Translated.pdf", mime="application/pdf")
