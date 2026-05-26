import streamlit as st
import fitz  # PyMuPDF
import easyocr
import io
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator
import numpy as np

# --- واجهة النيون الأخضر ---
st.set_page_config(page_title="NovaTrans Pro - AI", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #2e3033; }
    h1 { color: #39ff14; text-align: center; text-shadow: 0 0 10px #39ff14; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ NovaTrans Pro - AI Vision")

# إعداد OCR (يتم تحميله مرة واحدة)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()
uploaded_file = st.file_uploader("📂 ارفع ملزمة (صور أو PDF):", type=["pdf", "jpg", "png"])

if uploaded_file:
    if st.button("🚀 معالجة وترجمة بصرية"):
        with st.spinner("جاري تحليل الصور والترجمة..."):
            # تحويل الملف إلى صورة (لأول صفحة كمثال)
            if uploaded_file.type == "application/pdf":
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                pix = doc.load_page(0).get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            else:
                img = Image.open(uploaded_file)
            
            # 1. استخراج النص ومكانه
            results = reader.readtext(np.array(img))
            
            # 2. الرسم فوق الصورة
            draw = ImageDraw.Draw(img)
            
            for (bbox, text, prob) in results:
                if prob > 0.3:  # دقة القراءة
                    # ترجمة
                    translated = GoogleTranslator(source='en', target='ar').translate(text)
                    
                    # تحديد إحداثيات الرسم
                    top_left = bbox[0]
                    # رسم مستطيل أبيض لتغطية النص الأصلي
                    draw.rectangle([bbox[0], bbox[2]], fill="white")
                    # كتابة الترجمة (يحتاج خط يدعم العربية)
                    draw.text(top_left, translated, fill="black")
            
            # عرض النتيجة
            st.image(img, caption="الملزمة المترجمة", use_column_width=True)
            
            # زر التحميل
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("📥 تحميل الصفحة المترجمة", buf.getvalue(), "translated_page.png")
