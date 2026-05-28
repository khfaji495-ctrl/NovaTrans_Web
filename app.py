```python
import streamlit as st
import fitz
import deepl
from bidi.algorithm import get_display
import arabic_reshaper
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
        "⚠️ خطأ: تأكد من إضافة مفتاح API باسم DEEPL_API_KEY داخل Secrets"
    )

    st.stop()

# -----------------------------------
# تجهيز النص العربي
# -----------------------------------

def prepare_arabic_text(text):

    reshaped_text = arabic_reshaper.reshape(text)

    return get_display(reshaped_text)

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

        # قراءة الملف مرة واحدة فقط
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
                "🐈 سيد قط يترجم الملزمة الآن... يرجى الانتظار"
            ):

                # المرور على الصفحات
                for i in range(start - 1, end):

                    page = doc.load_page(i)

                    text_dict = page.get_text("dict")

                    # المرور على البلوكات
                    for block in text_dict["blocks"]:

                        if "lines" in block:

                            # المرور على الأسطر
                            for line in block["lines"]:

                                line_text = ""

                                x0 = 0
                                y0 = 0

                                # جمع النص
                                for span in line["spans"]:

                                    line_text += span["text"] + " "

                                    x0 = span["bbox"][0]

                                    y0 = span["bbox"][1]

                                line_text = line_text.strip()

                                # إذا النص مو فارغ
                                if line_text:

                                    try:

                                        # ترجمة النص
                                        result = translator.translate_text(
                                            line_text,
                                            target_lang="AR"
                                        )

                                        arabic_text = prepare_arabic_text(
                                            result.text
                                        )

                                        # موضع النص العربي
                                        arabic_y = y0 - 10

                                        # مستطيل أبيض خلف الترجمة
                                        page.draw_rect(
                                            fitz.Rect(
                                                x0 - 2,
                                                arabic_y - 2,
                                                x0 + 320,
                                                arabic_y + 12
                                            ),
                                            fill=(1, 1, 1),
                                            overlay=True
                                        )

                                        # كتابة الترجمة
                                        page.insert_text(
                                            (x0, arabic_y + 8),
                                            arabic_text,
                                            fontsize=8,
                                            fontname="helv",
                                            color=(1, 0, 0),
                                            overlay=True
                                        )

                                    except:
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
                    "😼 سيد قط أتم المهمة بنجاح!"
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
```
