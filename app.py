import streamlit as st
import fitz
import easyocr
import io
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display

# إعدادات الواجهة النيون الأخضر
st.set_page_config(page_title="NovaTrans Pro - AI", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #2e3033; }
    h1 { color: #39ff14; text-align: center; text-shadow: 0 0 10px #39ff14; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ NovaTrans Pro - AI Vision")

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

uploaded_file = st.file_uploader("📂 ارفع ملزمة (صور أو PDF):", type=["pdf", "jpg", "png"])

if uploaded_file:
    if st.button("🚀 معالجة وترجمة بصرية"):
        with st.spinner("جاري التحليل والترجمة الذكية..."):
            # تحويل الملف إلى صورة
            if uploaded_file.type == "application/pdf":
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                pix = doc.load_page(0).get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            else:
                img = Image.open(uploaded_file)
            
            results = reader.readtext(np.array(img))
            draw = ImageDraw.Draw(img)
            
            # تحميل خط عربي (تأكد من وجود font.ttf في المستودع)
            try:
                font = ImageFont.truetype("font.ttf", 20)
            except:
                font = ImageFont.load_default()

            for (bbox, text, prob) in results:
                if prob > 0.2:
                    # 1. الترجمة
                    translated = GoogleTranslator(source='en', target='ar').translate(text)
                    
                    # 2. معالجة النص العربي (الربط والاتجاه)
                    reshaped_text = arabic_reshaper.reshape(translated)
                    bidi_text = get_display(reshaped_text)
                    
                    # 3. الرسم فوق النص الأصلي
                    x0, y0 = bbox[0]
                    x1, y1 = bbox[2]
                    draw.rectangle([x0, y0, x1, y1], fill="white")
                    
                    # 4. كتابة الترجمة
                    draw.text((x0, y0), bidi_text, fill="black", font=font)
            
            st.image(img, caption="النتيجة بعد الترجمة البصرية", use_column_width=True)
            
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("📥 تحميل الصورة المترجمة", buf.getvalue(), "translated.png")
