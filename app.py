import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط ", layout="wide")

# كود CSS
page_design = """
<style>

/* إخفاء القائمة */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0e1117 0%, #16213e 100%);
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

.main-title {
    color: #10b981;
    text-align: center;
    font-size: 3.5rem;
    font-weight: bold;
    margin-top: -50px;
}

.sub-title {
    color: #cbd5e1;
    text-align: center;
    font-size: 1.2rem;
    margin-bottom: 30px;
}

</style>
"""

st.markdown(page_design, unsafe_allow_html=True)

# 2. عرض الـ GIF والعنوان
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("cat_pixel.gif", use_container_width=True)

st.markdown('<p class="main-title">سيد قط </p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">سيد قط يترجم ملازمك الهندسية والطبية بدقة</p>', unsafe_allow_html=True)

# 3. إعداد مترجم DeepL
try:
    auth_key = st.secrets["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
except Exception as e:
    st.error("⚠️ خطأ: تأكد من إضافة مفتاح API في إعدادات Secrets باسم DEEPL_API_KEY")
    st.stop()

def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# 4. واجهة رفع الملفات
st.divider()
uploaded_file = st.file_uploader(" 😸 ارسل ملف الملزمه للسيد قط", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    
    c1, c2 = st.columns(2)
    with c1:
        start = st.number_input("من صفحة:", 1, total_pages, 1)
    with c2:
        end = st.number_input("إلى صفحة:", 1, total_pages, start)


if st.button("😸 ابدأ الترجمة مع سيد قط"):

    with st.spinner("🐈 سيد قط يترجم الملزمة الآن..."):

        try:

            # فتح ملف الـ PDF
            doc = fitz.open(
                stream=uploaded_file.read(),
                filetype="pdf"
            )

            # المرور على الصفحات
            for i in range(start - 1, end):

                page = doc.load_page(i)

                # استخراج النصوص مع الإحداثيات
                blocks = page.get_text("blocks")

                for block in blocks:

                    x0, y0, x1, y1, text, *_ = block

                    text = text.strip()

                    if not text:
                        continue

                    try:

                        # ترجمة النص
                        result = translator.translate_text(
                            text,
                            target_lang="AR"
                        )

                        arabic_text = prepare_arabic_text(
                            result.text
                        )

                        # رسم خلفية بيضاء فوق النص
                        page.draw_rect(
                            fitz.Rect(x0, y0, x1, y1 + 15),
                            fill=(1, 1, 1),
                            overlay=True
                        )

                        # إعادة النص الإنكليزي
                        page.insert_text(
                            (x0, y0 + 10),
                            text,
                            fontsize=8,
                            color=(0, 0, 0),
                            overlay=True
                        )

                        # كتابة الترجمة العربية تحته
                        page.insert_text(
                            (x0, y0 + 22),
                            arabic_text,
                            fontsize=8,
                            color=(0, 0.5, 0),
                            overlay=True
                        )

                    except Exception:
                        continue

            # حفظ الملف النهائي
            pdf_bytes = doc.write()

            doc.close()

            st.success("😼 تمت الترجمة بنجاح!")

            st.download_button(
                label="😸 تحميل الملزمة",
                data=pdf_bytes,
                file_name="SayedQatt_Translated.pdf",
                mime="application/pdf"
            )

        except Exception as e:

            st.error("حدث خطأ أثناء الترجمة")
            st.write(e)
