import streamlit as st
import fitz  # PyMuPDF
import deepl
import io
from bidi.algorithm import get_display
import arabic_reshaper

# 1. إعدادات المترجم
translator = deepl.Translator(st.secrets["DEEPL_API_KEY"])

def prepare_arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))
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
st.set_page_config(page_title="سيد قط ", layout="wide")

# كود CSS: إخفاء القائمة + الخلفية + التنسيق
page_design = """
<style>
/* إخفاء قائمة Streamlit وأدوات المطورين */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0e1117 0%, #16213e 100%);
}
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}
.main-title {
    color: #10b981;
    text-align: center;
    font-size: 3.5rem;
    font-weight: bold;
    margin-top: -50px;
}
.sub-title {
    color: #cbd5e1;
    text-align: center;
    font-size: 1.2rem;
    margin-bottom: 30px;
}
</style>
"""
st.markdown(page_design, unsafe_allow_html=True)

# 2. عرض الـ GIF والعنوان
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("cat_pixel.gif", use_container_width=True)

st.markdown('<p class="main-title">سيد قط </p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">سيد قط يترجم ملازمك الهندسية والطبية بدقة</p>', unsafe_allow_html=True)

# 3. إعداد مترجم DeepL
try:
    auth_key = st.secrets["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
except Exception as e:
    st.error("⚠️ خطأ: تأكد من إضافة مفتاح API في إعدادات Secrets باسم DEEPL_API_KEY")
    st.stop()

def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# 4. واجهة رفع الملفات
st.divider()
uploaded_file = st.file_uploader(" 😸 ارسل ملف الملزمه للسيد قط", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    
    c1, c2 = st.columns(2)
    with c1:
        start = st.number_input("من صفحة:", 1, total_pages, 1)
    with c2:
        end = st.number_input("إلى صفحة:", 1, total_pages, start)

    if st.button("😸 ابدأ الترجمة مع سيد قط"):
        with st.spinner(".... 🐈سيد قط يترجم الملزمة الآن.. يرجى الانتظار"):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.warning("⚠️ تنبيه: ملف الخط (font.ttf) غير موجود.")
            
            y = 800 
            for i in range(start - 1, end):
                text = doc.load_page(i).get_text()
                lines = text.split('\n')
                
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
                            proper_arabic = prepare_arabic_text(result.text)
                            
                            c.setFont("Arabic", 12)
                            c.drawString(50, y, proper_arabic)
                            y -= 40
                        except:
                            continue
            
            c.save()
            pdf_buffer.seek(0)
            st.success("😼سيد قط أتم المهمة بنجاح!")
            st.download_button(
                label="😸 تحميل الملزمة من سيد قط",
                data=pdf_buffer,
                file_name="SayedQatt_Translated.pdf",
                mime="application/pdf"
            )

# 2. الواجهة
uploaded_file = st.file_uploader("😸 ارسل ملف الملزمة للسيد قط", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    if st.button("😸 ابدأ الترجمة مع سيد قط"):
        output_pdf = fitz.open()
        
        with st.spinner("🐈 سيد قط يضيف الترجمة العربية.."):
            for i in range(len(doc)):
                page = doc.load_page(i)
                # إنشاء صفحة جديدة بنفس أبعاد الأصلية
                new_page = output_pdf.new_page(width=page.rect.width, height=page.rect.height)
                
                # وضع صورة الصفحة الأصلية كخلفية (لضمان بقاء كل شيء كما هو)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                new_page.insert_image(page.rect, pixmap=pix)
                
                # معالجة النصوص
                blocks = page.get_text("blocks")
                for block in blocks:
                    if block[6] == 0:  # نص
                        text = block[4].strip()
                        if len(text) > 3:
                            x0, y0 = block[0], block[1]
                            
                            # إضافة الترجمة العربية فوق النص الأصلي بمسافة 15 نقطة
                            # (لا نلمس النص الإنجليزي الموجود في صورة الخلفية)
                            try:
                                translated = translator.translate_text(text, target_lang="AR")
                                new_page.insert_text((x0, y0 - 5), # Y0-5 تجعل الترجمة فوق النص
                                                     prepare_arabic_text(translated.text), 
                                                     fontsize=10, color=(0, 0, 0))
                            except:
                                continue
            
            # حفظ الملف
            output_buffer = io.BytesIO()
            output_pdf.save(output_buffer)
            output_buffer.seek(0)
            
            st.success("😼 تم بنجاح! الترجمة فوق النص الأصلي.")
            st.download_button("تحميل الملزمة", data=output_buffer, file_name="Translated.pdf", mime="application/pdf")
