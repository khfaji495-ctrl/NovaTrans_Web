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

# دالة لتحويل الـ GIF
def get_base64_gif(gif_file):
    with open(gif_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

gif_base64 = get_base64_gif("cat_pixel.gif")

# 2. كود CSS معدل: يجعل الـ GIF يغطي الشاشة بالكامل ويحافظ على ظهور العناصر
page_design = f"""
<style>
/* تعيين الـ GIF كخلفية ثابتة تغطي الشاشة بالكامل */
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/gif;base64,{gif_base64}");
    background-size: cover; /* هذا يغطي الشاشة بالكامل */
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* طبقة تغميق لضمان وضوح النصوص */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.85);
    z-index: 0;
}}

/* هذا هو السر: جعل كل عناصر Streamlit تظهر فوق الخلفية */
div.block-container {{
    position: relative;
    z-index: 1;
    background: rgba(0, 0, 0, 0.2); /* إضافة لمسة شفافية بسيطة خلف العناصر */
    padding: 2rem;
    border-radius: 15px;
}}

.main-title {{
    color: #10b981;
    text-align: center;
    font-size: 3.5rem;
    font-weight: bold;
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

# 3. واجهة الموقع
st.markdown('<p class="main-title">NovaTrans Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">مساعدك الذكي لترجمة الملازم الهندسية والتقنية</p>', unsafe_allow_html=True)

# ... (باقي كود الترجمة الخاص بك يبقى كما هو في الأسفل)
