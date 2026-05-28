import streamlit as st
import fitz
import deepl
import io
from bidi.algorithm import get_display
import arabic_reshaper

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط المطور", layout="wide")

# 2. إعداد المترجم
auth_key = st.secrets.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key) if auth_key else None

def prepare_arabic_text(text):
    # معالجة الخط العربي لضمان ظهوره بشكل صحيح
    return get_display(arabic_reshaper.reshape(text))

uploaded_file = st.file_uploader("😸 ارفع ملف الملزمة (PDF)", type="pdf")

if uploaded_file and translator:
    if st.button("😸 ابدأ التخريج الذكي"):
        with st.spinner("🐈 سيد قط يطبق التخريج.."):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            
            for page in doc:
                blocks = page.get_text("blocks")
                # ترتيب الكتل من الأعلى للأسفل
                blocks.sort(key=lambda b: b[1]) 
                
                for b in blocks:
                    x0, y0, x1, y1, text, block_no, block_type = b
                    clean_text = " ".join(text.split())
                    
                    if clean_text and block_type == 0:
                        try:
                            res = translator.translate_text(clean_text, target_lang="AR")
                            proper_arabic = prepare_arabic_text(res.text)
                            
                            # استخدام insert_textbox للتحكم في مكان الترجمة
                            # نضعها تحت النص الأصلي مباشرة
                            rect = fitz.Rect(x0, y1, x1, y1 + 30)
                            page.insert_textbox(
                                rect, 
                                proper_arabic, 
                                fontsize=9, 
                                fontname="helv", # ملاحظة: الـ PDF يحتاج خط يدعم العربية
                                color=(0, 0, 1) # اللون أزرق لتمييز الترجمة
                            )
                        except:
                            continue
            
            output_pdf = io.BytesIO()
            doc.save(output_pdf)
            output_pdf.seek(0)
            st.success("✅ تم حفظ التنسيق مع الصور!")
            st.download_button("📥 تحميل الملزمة", output_pdf, "SayedQatt_Pro_Final.pdf")
