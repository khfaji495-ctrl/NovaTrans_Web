import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io
import base64

# 1. إعدادات الصفحة
st.set_page_config(page_title="NovaTrans Pro", layout="wide")

# دالة لتحويل الـ GIF إلى Base64 لضمان عمله كخلفية
def get_base64_gif(gif_file):
    with open(gif_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

gif_base64 = get_base64_gif("cat_pixel.gif")

# 2. كود CSS للخلفية المتحركة
page_design = f"""
<style>
/* تعيين الـ GIF كخلفية ثابتة */
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/gif;base64,{gif_base64}");
    background-size: 200px; /* تحكم بحجم تكرار القطة هنا */
    background-repeat: repeat;
    background-attachment: fixed;
}}

/* إضافة طبقة غامقة فوق الخلفية عشان الكلام يكون واضح */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.85); /* 0.85 تعني شفافية 85% */
    z-index: 0;
}}

/* التأكد من أن كل المحتوى فوق الخلفية */
div.block-container {{
    position: relative;
    z-index: 1;
}}

.main-title {{
    color: #10b981;
    text-align: center;
    font-size: 3.5rem;
    font-weight: bold;
    margin-top: 20px;
}}
.sub-title {{
    color: #cbd5e1;
    text-align: center;
    font-size: 1.2rem;
    margin-bottom: 30px;
}}
</style>
"""
st.markdown(page_design, unsafe_allow_html=True)

# 3. العنوان (بدون الـ st.image لأن الـ GIF أصبح الآن خلفية)
st.markdown('<p class="main-title">NovaTrans Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">مساعدك الذكي لترجمة الملازم الهندسية والتقنية</p>', unsafe_allow_html=True)

# ... (باقي كود الترجمة الخاص بك يبقى كما هو بدون تغيير)
