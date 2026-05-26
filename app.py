import streamlit as st
import fitz
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# --- التصميم ---
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

    if st.button("🚀 ابدأ الترجمة"):
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        
        with st.spinner("جاري المعالجة..."):
            for i in range(start_p - 1, end_p):
                page = doc.load_page(i)
                text = page.get_text()
                
                if text.strip():
                    translated = GoogleTranslator(source='auto', target='ar').translate(text)
                    
                    # نكتب النص في الـ PDF (الإنجليزي الأصلي ثم العربي)
                    c.setFont("Helvetica", 12)
                    c.drawString(50, 750, f"Original Text (Page {i+1}):")
                    c.setFont("Helvetica", 10)
                    c.drawString(50, 730, text[:100]) # عرض جزء من النص
                    
                    c.setFont("Helvetica", 12)
                    c.drawString(50, 700, "الترجمة:")
                    c.setFont("Helvetica", 10)
                    c.drawString(50, 680, translated[:100])
                    
                c.showPage()
            
            c.save()
            st.success("✅ تم الانتهاء!")
            st.download_button("📥 تحميل ملف PDF", pdf_buffer.getvalue(), "NovaTrans.pdf")
