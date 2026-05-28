import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io

st.set_page_config(page_title="سيد قط", layout="wide")

# تصميم بسيط
st.markdown("<style>.main-title { color: #10b981; text-align: center; }</style>", unsafe_allow_html=True)
st.markdown('<p class="main-title">سيد قط للترجمة</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["😸 الترجمة", "👨‍🏫 غرفة الدراسة"])

with tab1:
    # إعداد المترجم
    try:
        translator = deepl.Translator(st.secrets["DEEPL_API_KEY"])
    except:
        st.error("تأكد من DEEPL_API_KEY")
        st.stop()

    uploaded_file = st.file_uploader("ارفع الملف", type="pdf")

    if uploaded_file:
        pdf_bytes = uploaded_file.getvalue()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        if st.button("بدء الترجمة"):
            with st.spinner("سيد قط يشتغل..."):
                buffer = io.BytesIO()
                c = canvas.Canvas(buffer)
                
                # محاولة تسجيل الخط
                try:
                    pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
                    has_font = True
                except:
                    has_font = False
                    st.warning("تحذير: ملف الخط غير موجود، قد لا تظهر الترجمة العربية.")

                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    lines = text.split('\n')
                    
                    y = 800
                    for line in lines:
                        if line.strip():
                            # ترجمة
                            try:
                                translated = translator.translate_text(line, target_lang="AR").text
                                if has_font:
                                    c.setFont("Arabic", 12)
                                    c.drawString(50, y, get_display(arabic_reshaper.reshape(translated)))
                                else:
                                    c.setFont("Helvetica", 12)
                                    c.drawString(50, y, "Text Translated (Arabic Font Missing)")
                                y -= 20
                            except:
                                continue
                    c.showPage()
                
                c.save()
                buffer.seek(0)
                st.success("تم!")
                st.download_button("تحميل الملف", buffer, "translated.pdf")

with tab2:
    st.warning("⚠️ غرفة الدراسة تحت التطوير")
