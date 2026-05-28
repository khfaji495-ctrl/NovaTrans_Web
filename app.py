import streamlit as st
import fitz  # PyMuPDF
import deepl

# ... (باقي الإعدادات ثابتة) ...

if st.button("😸 أضف الترجمة فوق النص الأصلي"):
    with st.spinner("🐈 سيد قط يضيف الترجمة فوق النص..."):
        # نفتح الملف الأصلي
        doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
        
        for i in range(start - 1, end):
            page = doc.load_page(i)
            # استخراج النصوص مع مواقعها (BBOX)
            text_dict = page.get_text("dict")
            
            for block in text_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        # نأخذ النص وموقعه
                        line_text = "".join([span["text"] for span in line["spans"]])
                        if line_text.strip():
                            # ترجمة النص
                            result = translator.translate_text(line_text, target_lang="AR")
                            
                            # تحديد مكان الكتابة (فوق النص الأصلي بـ 12 نقطة)
                            x0, y0 = line["bbox"][0], line["bbox"][1]
                            
                            # إدراج الترجمة مباشرة فوق النص
                            page.insert_text(
                                (x0, y0 - 12), 
                                prepare_arabic_text(result.text), 
                                fontsize=9, 
                                color=(1, 0, 0) # اللون الأحمر للترجمة
                            )

        # حفظ الملف المعدل
        output_buffer = io.BytesIO()
        doc.save(output_buffer)
        output_buffer.seek(0)
        
        st.success("😼 تمت إضافة الترجمة فوق النص الأصلي!")
        st.download_button("📥 تحميل الملزمة المعدلة", output_buffer, "Original_With_Arabic.pdf", "application/pdf")
