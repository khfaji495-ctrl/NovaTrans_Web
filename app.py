import streamlit as st
import fitz
import pytesseract
from PIL import Image
from deep_translator import GoogleTranslator
import io

st.set_page_config(page_title="NovaTrans", layout="wide")
st.markdown("<style>.stApp { background-color: #2e3033; } h1 { color: #39ff14; text-align: center; }</style>", unsafe_allow_html=True)
st.title("NovaTrans")

uploaded_file = st.file_uploader("📂 ارفع ملف PDF:", type=["pdf"])

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    if st.button("🚀 ترجمة"):
        with st.spinner("جاري المعالجة..."):
            full_text = ""
            for page in doc:
                # محاولة استخراج النص مباشرة (أسرع وأضمن)
                text = page.get_text()
                if not text.strip():
                    # إذا لم يوجد نص، نستخدم التعرّف البصري الخفيف
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text = pytesseract.image_to_string(img)
                
                # الترجمة
                translated = GoogleTranslator(source='auto', target='ar').translate(text[:1000])
                full_text += translated + "\n\n"
            
            st.text_area("الترجمة:", full_text, height=400)
            st.download_button("📥 تحميل النص", full_text, "NovaTrans.txt")
