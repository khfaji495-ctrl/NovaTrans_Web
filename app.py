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

page_design = """
<style>

/* إخفاء قائمة Streamlit */
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

    pdf_bytes = uploaded_file.getvalue()

    doc = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    total_pages = len(doc)
    
    c1, c2 = st.columns(2)
    with c1:
        start = st.number_input("من صفحة:", 1, total_pages, 1)
    with c2:
        end = st.number_input("إلى صفحة:", 1, total_pages, start)


if st.button("😺 ابدأ الترجمة مع سيد قط"):

    with st.spinner("🐈 سيد قط يترجم الملزمة الآن..."):

        try:

            pdf_bytes = uploaded_file.getvalue()

            doc = fitz.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

            # المرور على الصفحات
            for i in range(start - 1, end):

                page = doc.load_page(i)

                text_dict = page.get_text("dict")

             for block in text_dict["blocks"]:

    if "lines" in block:

        for line in block["lines"]:

            line_text = ""

            x0 = 0
            y0 = 0

            for span in line["spans"]:

                line_text += span["text"] + " "

                x0 = span["bbox"][0]
                y0 = span["bbox"][1] - 10

            if line_text.strip():

                try:

                    result = translator.translate_text(
                        line_text,
                        target_lang="AR"
                    )

                    arabic_text = prepare_arabic_text(result.text)

                    page.draw_rect(
                        fitz.Rect(
                            x0 - 2,
                            y0 - 14,
                            x0 + 300,
                            y0 + 2
                        ),
                        color=(1, 1, 1),
                        fill=(1, 1, 1)
                    )

                    page.insert_text(
                        (x0, y0 - 3),
                        arabic_text,
                        fontsize=9,
                        color=(1, 0, 0)
                    )

                except:
                    pass

                                result = translator.translate_text(
                                    line_text,
                                    target_lang="AR"
                                )

                                arabic_text = prepare_arabic_text(result.text)

                                page.insert_text(
                                    (x0, y0 - 12),
                                    arabic_text,
                                    fontsize=10,
                                    color=(1, 0, 0)
                                )

            output = io.BytesIO()
            doc.save(output, garbage=4, deflate=True)
            output.seek(0)

            st.success("😺 تمت الترجمة بنجاح!")

            st.download_button(
                label="📥 تحميل الملف المترجم",
                data=output,
                file_name="translated.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error("حدث خطأ أثناء الترجمة")
            st.exception(e)
