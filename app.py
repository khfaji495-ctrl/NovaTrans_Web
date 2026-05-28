import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط", layout="wide")

# CSS التصميم
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #0e1117 0%, #16213e 100%); }
.main-title { color: #10b981; text-align: center; font-size: 3.5rem; font-weight: bold; margin-top: -50px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">سيد قط</p>', unsafe_allow_html=True)

# 2. التبويبات
tab1, tab2 = st.tabs(["😸 ترجم مع السيد قط", "👨‍🏫 غرفة الدراسة"])

with tab1:
    try:
        translator = deepl.Translator(st.secrets["DEEPL_API_KEY"])
    except:
        st.error("⚠️ تأكد من إضافة مفتاح DEEPL_API_KEY في الـ Secrets")
        st.stop()

    def prepare_arabic_text(text):
        return get_display(arabic_reshaper.reshape(text))

    uploaded_file = st.file_uploader("😸 ارسل ملف الملزمة للسيد قط", type="pdf")

    if uploaded_file is not None:
        # استخدام getvalue للحفاظ على الملف
        pdf_bytes = uploaded_file.getvalue()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        total_pages = len(doc)
        
        c1, c2 = st.columns(2)
        start = c1.number_input("من صفحة:", 1, total_pages, 1)
        end = c2.number_input("إلى صفحة:", 1, total_pages, start)

        if st.button("😸 ابدأ الترجمة مع سيد قط"):
            with st.spinner("🐈 سيد قط يترجم الملزمة الآن..."):
                pdf_buffer = io.BytesIO()
                c = canvas.Canvas(pdf_buffer)
                
                try:
                    pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
                except:
                    st.warning("⚠️ ملاحظة: ملف الخط (font.ttf) غير موجود، ستظهر النصوص كرموز.")

                y = 800
                for i in range(start - 1, end):
                    page_text = doc.load_page(i).get_text()
                    lines = page_text.split('\n')
                    
                    for line in lines:
                        if line.strip():
                            if y < 100:
                                c.showPage()
                                y = 800
                            
                            c.setFont("Helvetica", 12)
                            c.drawString(50, y, line[:80])
                            y -= 20
                            
                            try:
                                result = translator.translate_text(line, target_lang="AR")
                                c.setFont("Arabic", 12)
                                c.drawString(50, y, prepare_arabic_text(result.text))
                                y -= 40
                            except:
                                continue
                
                c.save()
                pdf_buffer.seek(0)
                st.success("😼 سيد قط أتم المهمة بنجاح!")
                st.download_button("📥 تحميل الملزمة المترجمة", pdf_buffer, "SayedQatt_Translated.pdf", "application/pdf")

with tab2:
    st.warning("⚠️ غرفة الدراسة الذكية تحت التطوير حالياً، انتظرنا قريباً! 😸")
