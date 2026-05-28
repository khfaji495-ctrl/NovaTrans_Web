import streamlit as st
import fitz  # PyMuPDF
import deepl
import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط الاحترافي", layout="wide")

# إعداد المترجم
auth_key = st.secrets.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key) if auth_key else None

def prepare_arabic_text(text):
    # الدالة المسؤولة عن معالجة الحروف العربية لتظهر متصلة
    return get_display(arabic_reshaper.reshape(text))

st.title("سيد قط 😸 - التخريج الذكي")
uploaded_file = st.file_uploader("ارفع ملف الملزمة (PDF)", type="pdf")

if uploaded_file and translator:
    if st.button("😸 ابدأ المعالجة الآن"):
        with st.spinner("🐈 سيد قط يحلل ويترجم.."):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            # تسجيل الخط العربي (تأكد من وجود font.ttf في المجلد)
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.error("⚠️ خطأ: تأكد من وجود ملف font.ttf في المجلد!")
                st.stop()

            for i in range(len(doc)):
                page = doc.load_page(i)
                # ضبط حجم صفحة الـ PDF الناتج
                c.setPageSize((page.rect.width, page.rect.height))
                
                # استخراج كتل النصوص بإحداثياتها
                blocks = page.get_text("blocks")
                
                for b in blocks:
                    x0, y0, x1, y1, text, block_no, block_type = b
                    clean_text = " ".join(text.split())
                    
                    if clean_text and block_type == 0:
                        try:
                            # الترجمة
                            res = translator.translate_text(clean_text, target_lang="AR")
                            proper_arabic = prepare_arabic_text(res.text)
                            
                            # رسم النص المترجم
                            # (page.rect.height - y1) هي المعادلة التي تحول إحداثيات PDF إلى إحداثيات الرسم
                            c.setFont("Arabic", 9)
                            c.drawString(x0, page.rect.height - y1, proper_arabic)
                        except:
                            continue
                
                c.showPage() # انتقال لصفحة جديدة في الملف الناتج
            
            c.save()
            pdf_buffer.seek(0)
            st.success("✅ تم الانتهاء بنجاح!")
            st.download_button("📥 تحميل الملزمة المترجمة", pdf_buffer, "SayedQatt_Final.pdf")
