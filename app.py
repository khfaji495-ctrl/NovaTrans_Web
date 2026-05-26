import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io

# الإعدادات
st.set_page_config(page_title="NovaTrans Pro", layout="wide")
st.title("NovaTrans Pro - ترجمة مزدوجة")

# إعداد مترجم DeepL
try:
    auth_key = st.secrets["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
except Exception as e:
    st.error("خطأ: تأكد من إضافة مفتاح API في الإعدادات.")
    st.stop()

def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

uploaded_file = st.file_uploader("📂 ضع ملفك هنا", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    start = st.number_input("من صفحة:", 1, total_pages, 1)
    end = st.number_input("إلى صفحة:", 1, total_pages, start)

    if st.button("ابدأ الترجمة المزدوجة"):
        with st.spinner("جاري المعالجة..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
                pdfmetrics.registerFont(TTFont('English', 'Helvetica'))
            except:
                st.warning("تنبيه: ملف الخط غير موجود.")
            
            y = 800 
            for i in range(start - 1, end):
                text = doc.load_page(i).get_text()
                lines = text.split('\n')
                
                for line in lines:
                    if line.strip():
                        if y < 100:
                            c.showPage()
                            y = 800
                        
                        # كتابة النص الإنجليزي
                        c.setFont("English", 12)
                        c.drawString(50, y, line[:80]) # النص الإنجليزي
                        y -= 20
                        
                        # ترجمة السطر
                        try:
                            result = translator.translate_text(line, target_lang="AR")
                            proper_arabic = prepare_arabic_text(result.text)
                            
                            # كتابة الترجمة العربية
                            c.setFont("Arabic", 12)
                            c.drawString(50, y, proper_arabic)
                            y -= 40 # مسافة أكبر بعد كل جملة
                        except:
                            continue
            
            c.save()
            pdf_buffer.seek(0)
            st.success("✅ تمت المعالجة!")
            st.download_button(
                label="📥 تحميل الملف المترجم PDF",
                data=pdf_buffer,
                file_name="NovaTrans_Dual.pdf",
                mime="application/pdf"
            )
