import streamlit as st
import fitz
import deepl
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="المترجم سيد قط", layout="wide")

# CSS لإخفاء القائمة والتنسيق
page_design = """
<style>
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
[data-testid="stAppViewContainer"] {background: linear-gradient(180deg, #0e1117 0%, #16213e 100%);}
.main-title {color: #10b981; text-align: center; font-size: 3.5rem; font-weight: bold; margin-top: -50px;}
.sub-title {color: #cbd5e1; text-align: center; font-size: 1.2rem; margin-bottom: 30px;}
</style>
"""
st.markdown(page_design, unsafe_allow_html=True)

# العنوان
st.image("cat_pixel.gif", width=200)
st.markdown('<p class="main-title">المترجم سيد قط</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">سيد قط يترجم ملازمك الهندسية والطبية بدقة</p>', unsafe_allow_html=True)

# مترجم DeepL
try:
    auth_key = st.secrets["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
except:
    st.error("⚠️ خطأ في مفتاح API")
    st.stop()

# 4. واجهة رفع الملفات
uploaded_file = st.file_uploader("📂 اسحب ملف الملزمة هنا (PDF)", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    if st.button("🚀 ابدأ الترجمة مع سيد قط"):
        with st.spinner("سيد قط يترجم الملزمة.. يرجى الانتظار"):
            pdf_buffer = io.BytesIO()
            doc_pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            
            # تسجيل الخط العربي (تأكد أن الملف font.ttf موجود في نفس المجلد)
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
                style_ar = ParagraphStyle('ArabicStyle', fontName='Arabic', fontSize=12, leading=16, alignment=1)
                style_en = ParagraphStyle('EnglishStyle', fontName='Helvetica', fontSize=10, leading=12, alignment=0)
            except:
                st.warning("⚠️ خط ملف الخط (font.ttf) غير موجود.")
                style_ar = styles["Normal"]
                style_en = styles["Normal"]

            story = []
            for i in range(len(doc)):
                text = doc.load_page(i).get_text()
                if text.strip():
                    # ترجمة الفقرة كاملة لزيادة السرعة
                    translated = translator.translate_text(text, target_lang="AR").text
                    story.append(Paragraph(text, style_en))
                    story.append(Spacer(1, 12))
                    story.append(Paragraph(translated, style_ar))
                    story.append(Spacer(1, 24))

            doc_pdf.build(story)
            pdf_buffer.seek(0)
            st.success("✅ سيد قط أتم المهمة!")
            st.download_button("📥 تحميل الملزمة", pdf_buffer, "SayedQatt_Translated.pdf", "application/pdf")
