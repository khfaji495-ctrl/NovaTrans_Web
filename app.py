import streamlit as st
import fitz
import deepl  # المكتبة الجديدة
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io

# الإعدادات
st.set_page_config(page_title="NovaTrans Pro", layout="wide")
st.title("NovaTrans Pro")

# إعداد مترجم DeepL
# تأكد من إضافة DEEPL_API_KEY في إعدادات Secrets في Streamlit Cloud
try:
    auth_key = st.secrets["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
except Exception as e:
    st.error("خطأ: لم يتم العثور على مفتاح API في الإعدادات.")

def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

uploaded_file = st.file_uploader("📂 ضع ملفك هنا", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    start = st.number_input("من صفحة:", 1, total_pages, 1)
    end = st.number_input("إلى صفحة:", 1, total_pages, start)

    if st.button("ترجمه باستخدام DeepL"):
        with st.spinner("جاري الترجمة الاحترافية..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.warning("تنبيه: ملف الخط غير موجود.")
            
       # حلقة الصفحات
            for i in range(start - 1, end):
                text = doc.load_page(i).get_text()
                if text.strip():
                    # ترجمة الصفحة كاملة دفعة واحدة (أسرع بكثير)
                    try:
                        result = translator.translate_text(text, target_lang="AR")
                        translated_text = result.text
                        
                        # تقسيم النص المترجم إلى أسطر ووضعه في الـ PDF
                        lines = translated_text.split('\n')
                        for line in lines:
                            if y < 100:
                                c.showPage()
                                y = 800
                            
                            proper_arabic = prepare_arabic_text(line)
                            c.setFont("Arabic", 12)
                            c.drawString(50, y, proper_arabic)
                            y -= 25
                    except Exception as e:
                        st.error(f"خطأ في الترجمة: {e}")
                            c.setFont("Helvetica", 12)
                            c.drawString(50, y, line[:60])
                            y -= 20
                            c.setFont("Arabic", 12)
                            c.drawString(50, y, proper_arabic)
                            y -= 40
                        except Exception as e:
                            continue
            
            c.save()
            pdf_buffer.seek(0)
            st.success("✅ تمت المعالجة بنجاح عبر DeepL!")
            st.download_button(
                label="📥 تحميل الملف المترجم PDF",
                data=pdf_buffer,
                file_name="NovaTrans_Translated.pdf",
                mime="application/pdf"
            )
