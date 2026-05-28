import streamlit as st
import fitz  # PyMuPDF
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط المطور", layout="wide")

# CSS لتجميل الواجهة
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #0e1117 0%, #16213e 100%); }
.main-title { color: #10b981; text-align: center; font-size: 3rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">سيد قط 😸 - التخريج الذكي</p>', unsafe_allow_html=True)

# 2. إعداد المترجم
auth_key = st.secrets.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key) if auth_key else None

def prepare_arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

# 3. واجهة الرفع
uploaded_file = st.file_uploader("😸 ارفع ملف الملزمة", type="pdf")

if uploaded_file and translator:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    start, end = st.columns(2)
    s_page = start.number_input("من صفحة:", 1, total_pages, 1)
    e_page = end.number_input("إلى صفحة:", 1, total_pages, s_page)

    if st.button("😸 ابدأ التخريج والترجمة"):
        with st.spinner("🐈 سيد قط يحلل ويترجم.."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.error("⚠️ ملف الخط (font.ttf) مفقود")

            for i in range(s_page - 1, e_page):
                page = doc.load_page(i)
                blocks = page.get_text("blocks") # الحصول على كتل النصوص بإحداثياتها
                
                c.showPage()
                # ضبط أبعاد الصفحة في الـ PDF الجديد
                c.setPageSize((page.rect.width, page.rect.height))
                
                for b in blocks:
                    x0, y0, x1, y1, text, block_no, block_type = b
                    clean_text = " ".join(text.split())
                    
                    if clean_text and block_type == 0:
                        # 1. رسم النص الإنجليزي في مكانه
                        c.setFont("Helvetica", 9)
                        c.drawString(x0, page.rect.height - y1, clean_text[:100])
                        
                        # 2. ترجمة ورسم العربي أسفل الإنجليزي (التخريج)
                        try:
                            res = translator.translate_text(clean_text, target_lang="AR")
                            proper_arabic = prepare_arabic_text(res.text)
                            c.setFont("Arabic", 9)
                            # رسم العربي في إحداثيات مدروسة لعدم التداخل
                            c.drawString(x0, page.rect.height - y1 - 12, proper_arabic)
                        except:
                            continue
            
            c.save()
            pdf_buffer.seek(0)
            st.success("✅ تمت العملية بنجاح!")
            st.download_button("📥 تحميل الملزمة المترجمة", pdf_buffer, "SayedQatt_Pro.pdf")
