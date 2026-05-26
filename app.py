import streamlit as st
import fitz
from deep_translator import GoogleTranslator
from fpdf import FPDF
import io

# --- التصميم والواجهة ---
st.set_page_config(page_title="NovaTrans", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #2e3033; }
    h1 { color: #39ff14; text-align: center; text-shadow: 0 0 10px #39ff14; }
    </style>
""", unsafe_allow_html=True)

st.title("NovaTrans")

uploaded_file = st.file_uploader("📂 ارفع ملزمة PDF:", type=["pdf"])

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    
    col1, col2 = st.columns(2)
    start_p = col1.number_input("من صفحة:", 1, total_pages, 1)
    end_p = col2.number_input("إلى صفحة:", 1, total_pages, start_p)

    if st.button("🚀 ابدأ المعالجة والترجمة"):
        with st.spinner("جاري الترجمة الذكية..."):
            pdf = FPDF()
            # إضافة الخط العربي (تأكد أن الملف في نفس المجلد)
            pdf.add_font("Amiri", "", "Amiri.ttf", uni=True)
            
            for i in range(start_p - 1, end_p):
                page = doc.load_page(i)
                text = page.get_text()
                
                if text.strip():
                    # ترجمة النص
                    translated = GoogleTranslator(source='auto', target='ar').translate(text)
                    
                    pdf.add_page()
                    # إضافة النص الإنجليزي (كخط لاتيني)
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, txt="Original Text:")
                    pdf.multi_cell(0, 10, txt=text[:1000].encode('latin-1', 'replace').decode('latin-1'))
                    
                    # إضافة الترجمة العربية (بخط Amiri)
                    pdf.set_font("Amiri", size=14)
                    pdf.multi_cell(0, 10, txt="الترجمة العربية:")
                    pdf.multi_cell(0, 10, txt=translated)
            
            # حفظ الملف في الذاكرة
            output = io.BytesIO(pdf.output(dest='S').encode('latin-1'))
            st.success("✅ تم الانتهاء بنجاح!")
            st.download_button("📥 تحميل PDF", output, "NovaTrans.pdf")
