}
import streamlit as st
import fitz
import deepl
import tempfile
import os

from bidi.algorithm import get_display
import arabic_reshaper

# ======================================================
# إعدادات الصفحة
# ======================================================

st.set_page_config(
    page_title="سيد قط",
    layout="wide"
)

# ======================================================
# CSS
# ======================================================

page_design = """
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0e1117 0%, #16213e 100%);
}

.main-title{
    color:#10b981;
    text-align:center;
    font-size:3.5rem;
    font-weight:bold;
}

.sub-title{
    color:#cbd5e1;
    text-align:center;
    font-size:1.2rem;
}

</style>
"""

st.markdown(page_design, unsafe_allow_html=True)

# ======================================================
# العنوان
# ======================================================

st.markdown(
    '<p class="main-title">سيد قط</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">سيد قط يترجم ملازمك الهندسية والطبية</p>',
    unsafe_allow_html=True
)

# ======================================================
# DeepL
# ======================================================

try:

    auth_key = st.secrets["DEEPL_API_KEY"]

    translator = deepl.Translator(auth_key)

except:

    st.error("أضف DEEPL_API_KEY داخل secrets")

    st.stop()

# ======================================================
# تجهيز العربي
# ======================================================

def prepare_arabic(text):

    reshaped = arabic_reshaper.reshape(text)

    bidi_text = get_display(reshaped)

    return bidi_text

# ======================================================
# رفع الملف
# ======================================================

uploaded_file = st.file_uploader(
    "😸 ارفع الملزمة",
    type="pdf"
)

# ======================================================
# الترجمة
# ======================================================

if uploaded_file is not None:

    doc = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    total_pages = len(doc)

    c1, c2 = st.columns(2)

    with c1:

        start_page = st.number_input(
            "من صفحة",
            1,
            total_pages,
            1
        )

    with c2:

        end_page = st.number_input(
            "إلى صفحة",
            1,
            total_pages,
            start_page
        )

    # ==================================================
    # بدء الترجمة
    # ==================================================

    if st.button("😸 ابدأ الترجمة"):

        with st.spinner("🐈 سيد قط يعمل الآن..."):

            try:

                for page_num in range(
                    start_page - 1,
                    end_page
                ):

                    page = doc.load_page(page_num)

                    blocks = page.get_text("blocks")

                    for block in blocks:

                        x0, y0, x1, y1, text, *_ = block

                        text = text.strip()

                        if len(text) < 3:
                            continue

                        # ==================================
                        # تنظيف النص
                        # ==================================

                        clean_text = text.replace("\n", " ")

                        # ==================================
                        # ترجمة
                        # ==================================

                        try:

                            result = translator.translate_text(
                                clean_text,
                                target_lang="AR"
                            )

                            arabic_text = prepare_arabic(
                                result.text
                            )

                        except:

                            continue
