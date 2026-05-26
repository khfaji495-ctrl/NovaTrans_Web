import streamlit as st
import fitz
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io
import time  # استيراد مكتبة الوقت لإضافة التأخير

# --- الإعدادات والواجهة ---
st.set_page_config(page_title="NovaTrans Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #2e3033; }
    h1 { color: #39ff14; text-align: center; text-shadow: 0 0 10px #39ff14; }
    .stMarkdown, .stText, label { color: #ffffff !important; font-size: 18px !important; }
    .stButton>button { background-color: #39ff14 !important; color: #000000 !important; font-weight: bold; border: none; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ NovaTrans Pro")

def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

uploaded_file = st.file_uploader("📂 ارفع ملف الـ PDF هنا", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    
    start = st.number_input("من صفحة:", 1, total_pages, 1)
    end = st.number_input("إلى صفحة:", 1, total_pages, start)

    if st.button("🚀 ترجم واحفظ PDF"):
        # إعدادات التقدم
        total_to_process = end - start + 1
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("جاري المعالجة..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            
            y = 800
            for idx, page_num in enumerate(range(start - 1, end)):
                # تحديث شريط التقدم
                progress_bar.progress((idx + 1) / total_to_process)
                status_text.text(f"جاري ترجمة الصفحة {page_num + 1} من {end}...")
                
                text = doc.load_page(page_num).get_text()
                lines = text.split('\n')
                
                for line in lines:
                    if line.strip():
                        if y < 100:
                            c.showPage()
                            y = 800
                        
                        # إضافة تأخير بسيط لتجنب الحظر (TooManyRequests)
                        time.sleep(0.3)
                        
                        try:
                            translated = GoogleTranslator(source='en', target='ar').translate(line)
                            proper_arabic = prepare_arabic_text(translated)
                            
                            c.setFont("Helvetica", 12)
                            c.drawString(50, y, line[:80])
                            y -= 20
                            c.setFont("Arabic", 12)
                            c.drawString(50, y, proper_arabic)
                            y -= 40
                        except:
                            # في حال حدوث خطأ، نتخطى السطر الحالي ونكمل
                            continue
            
            c.save()
            pdf_buffer.seek(0)
            st.success("✅ تم الانتهاء بنجاح!")
            st.download_button("📥 تحميل الملف المترجم PDF", pdf_buffer, "NovaTrans_Translated.pdf")
