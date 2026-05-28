import streamlit as st
import fitz
import deepl
from bidi.algorithm import get_display
import arabic_reshaperimport streamlit as st
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

# كود CSS: إخفاء القائمة + الخلفية + التنسيق
page_design = """
<style>
/* إخفاء قائمة Streamlit وأدوات المطورين */
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
        with st.spinner(".... 🐈سيد قط يترجم الملزمة الآن.. يرجى الانتظار"):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.warning("⚠️ تنبيه: ملف الخط (font.ttf) غير موجود.")
            
            y = 800 
            for i in range(start - 1, end):
                text = doc.load_page(i).get_text()
                lines = text.split('\n')
                
                for line in lines:
                    if line.strip():
                        if y < 100:
                            c.showPage()
                            y = 800
                        
                        c.setFont("Helvetica", 12)
                        c.drawString(50, y, line[:80])
                        y -= 20
                        
                        try:
                            result = translator.translate_text(line, target_lang="AR")
                            proper_arabic = prepare_arabic_text(result.text)
                            
                            c.setFont("Arabic", 12)
                            c.drawString(50, y, proper_arabic)
                            y -= 40
                        except:
                            continue
            
            c.save()
            pdf_buffer.seek(0)
            st.success("😼سيد قط أتم المهمة بنجاح!")
            st.download_button(
                label="😸 تحميل الملزمة من سيد قط",
                data=pdf_buffer,
                file_name="SayedQatt_Translated.pdf",
                mime="application/pdf"
            )

import io

# -----------------------------------
# إعداد الصفحة
# -----------------------------------

st.set_page_config(
    page_title="سيد قط",
    layout="wide"
)

# -----------------------------------
# CSS
# -----------------------------------

page_design = """
<style>

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

# -----------------------------------
# الصورة والعنوان
# -----------------------------------

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.image("cat_pixel.gif", use_container_width=True)

st.markdown(
    '<p class="main-title">سيد قط</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">سيد قط يترجم ملازمك الهندسية والطبية بدقة</p>',
    unsafe_allow_html=True
)

# -----------------------------------
# إعداد DeepL
# -----------------------------------

try:

    auth_key = st.secrets["DEEPL_API_KEY"]

    translator = deepl.Translator(auth_key)

except Exception:

    st.error(
        "⚠️ تأكد من إضافة DEEPL_API_KEY داخل Secrets"
    )

    st.stop()

# -----------------------------------
# تجهيز النص العربي
# -----------------------------------

def prepare_arabic_text(text):

    reshaped_text = arabic_reshaper.reshape(text)

    return get_display(reshaped_text)

# -----------------------------------
# كشف المعادلات
# -----------------------------------

def is_math_or_formula(text):

    math_symbols = [
        "=",
        "÷",
        "×",
        "∫",
        "√",
        "∑",
        "π",
        "∞",
        "≈",
        "≠",
        "^"
    ]

    symbol_count = sum(
        text.count(symbol)
        for symbol in math_symbols
    )

    letters_count = sum(
        c.isalpha()
        for c in text
    )

    digits_count = sum(
        c.isdigit()
        for c in text
    )

    # معادلات حقيقية
    if symbol_count >= 2 and letters_count < 5:
        return True

    # إذا الأرقام أكثر من الأحرف
    if digits_count > letters_count and symbol_count > 0:
        return True

    # معادلات قصيرة
    if len(text) < 15 and symbol_count > 0:
        return True

    return False

# -----------------------------------
# رفع الملف
# -----------------------------------

st.divider()

uploaded_file = st.file_uploader(
    "😸 ارسل ملف الملزمة للسيد قط",
    type="pdf"
)

# -----------------------------------
# عند رفع الملف
# -----------------------------------

if uploaded_file is not None:

    try:

        # قراءة الملف
        pdf_bytes = uploaded_file.getvalue()

        # فتح الـ PDF
        doc = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        total_pages = len(doc)

        # اختيار الصفحات
        c1, c2 = st.columns(2)

        with c1:

            start = st.number_input(
                "من صفحة:",
                1,
                total_pages,
                1
            )

        with c2:

            end = st.number_input(
                "إلى صفحة:",
                1,
                total_pages,
                start
            )

        # -----------------------------------
        # زر الترجمة
        # -----------------------------------

        if st.button("😸 ابدأ الترجمة مع سيد قط"):

            with st.spinner(
                "🐈 سيد قط يترجم الملزمة الآن..."
            ):

                # تحميل الخط العربي
                first_page = doc[0]

                first_page.insert_font(
                    fontname="Arabic",
                    fontfile="font.ttf"
                )

                # -----------------------------------
                # المرور على الصفحات
                # -----------------------------------

                for i in range(start - 1, end):

                    page = doc.load_page(i)

                    text_dict = page.get_text("dict")

                    for block in text_dict["blocks"]:

                        if "lines" not in block:
                            continue

                        for line in block["lines"]:

                            line_text = ""

                            x0 = 0
                            y0 = 0
                            x1 = 0
                            y1 = 0

                            font_size = 10

                            for span in line["spans"]:

                                line_text += span["text"] + " "

                                x0 = span["bbox"][0]
                                y0 = span["bbox"][1]
                                x1 = span["bbox"][2]
                                y1 = span["bbox"][3]

                                font_size = span["size"]

                            line_text = line_text.strip()

                            # تجاهل النصوص الفارغة
                            if not line_text:
                                continue

                            # تجاهل المعادلات
                            if is_math_or_formula(line_text):
                                continue

                            # تجاهل النصوص القصيرة
                            if len(line_text) < 4:
                                continue

                            try:

                                # -----------------------------------
                                # الترجمة
                                # -----------------------------------

                                result = translator.translate_text(
                                    line_text,
                                    target_lang="AR"
                                )

                                arabic_text = prepare_arabic_text(
                                    result.text
                                )

                                # -----------------------------------
                                # حذف النص الأصلي
                                # -----------------------------------

                                rect = fitz.Rect(
                                    x0,
                                    y0,
                                    x1,
                                    y1
                                )

                                page.add_redact_annot(
                                    rect,
                                    fill=(1, 1, 1)
                                )

                                page.apply_redactions()

                                # -----------------------------------
                                # إعادة كتابة الإنكليزي
                                # -----------------------------------

                                page.insert_text(
                                    (x0, y0 + 8),
                                    line_text,
                                    fontsize=font_size,
                                    fontname="helv",
                                    color=(0, 0, 0),
                                    overlay=True
                                )

                                # -----------------------------------
                                # كتابة الترجمة العربية
                                # -----------------------------------

                                shape = page.new_shape()

                                shape.insert_text(
                                    (x0, y0 - 6),
                                    arabic_text,
                                    fontsize=font_size + 2,
                                    fontname="Arabic",
                                    color=(1, 0, 0)
                                )

                                shape.commit()

                            except Exception:
                                continue

                # -----------------------------------
                # حفظ الملف
                # -----------------------------------

                output = io.BytesIO()

                doc.save(
                    output,
                    garbage=4,
                    deflate=True
                )

                output.seek(0)

                doc.close()

                # -----------------------------------
                # التحميل
                # -----------------------------------

                st.success(
                    "😼 تمت الترجمة بنجاح!"
                )

                st.download_button(
                    label="😸 تحميل الملزمة",
                    data=output,
                    file_name="SayedQatt_Translated.pdf",
                    mime="application/pdf"
                )

    except Exception as e:

        st.error("حدث خطأ أثناء معالجة الملف")

        st.write(e)
