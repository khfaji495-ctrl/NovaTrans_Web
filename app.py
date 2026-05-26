import streamlit as st
import fitz  # PyMuPDF
import io
from deep_translator import GoogleTranslator
from bidi.algorithm import get_display
import arabic_reshaper

# --- إعدادات الواجهة ---
st.set_page_config(page_title="NovaTrans Pro", layout="wide")
st.markdown("<style>.stApp { background-color: #1e1e2e; color: #dcd7ba; }</style>", unsafe_allow_html=True)
st.title("✨ NovaTrans Pro - النسخة المحدثة")

def prepare_arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

uploaded_file = st.file_uploader("📂 ارفع ملف الـ PDF هنا", type="pdf")

if uploaded_file:
    # تحميل الملف في الذاكرة
    file_bytes = uploaded_file.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    
    if st.button("🚀 ترجم واحفظ PDF"):
        with st.spinner("جاري الترجمة والحفاظ على الصور..."):
            for page in doc:
                # استخراج النصوص وإحداثياتها
                blocks = page.get_text("blocks")
                for b in blocks:
                    # b[4] هو النص في كتلة النص
                    text = b[4].strip()
                    if text:
                        # ترجمة النص
                        translated = GoogleTranslator(source='auto', target='ar').translate(text[:500])
                        proper_arabic = prepare_arabic_text(translated)
                        
                        # إحداثيات الكتلة الحالية (x1, y1, x2, y2)
                        x0, y0, x1, y1 = b[0], b[1], b[2], b[3]
                        
                        # الكتابة تحت النص الأصلي مباشرة
                        # نستخدم y1 (نهاية النص الأصلي) لإضافة الترجمة
                        page.insert_text((x0, y1 + 10), proper_arabic, fontsize=10, fontname="helv", color=(0, 0, 0))

            # حفظ الملف الناتج في ذاكرة مؤقتة
            output_buffer = io.BytesIO()
            doc.save(output_buffer)
            output_buffer.seek(0)
            
            st.success("✅ تم الانتهاء! الصور والتنسيق محفوظان.")
            st.download_button("📥 تحميل الملف المترجم PDF", output_buffer, "NovaTrans_Translated.pdf")
