import streamlit as st
import fitz
import deepl
import tempfile
import os

from bidi.algorithm import get_display
import arabic_reshaper

# ======================================================
# إعداد الصفحة
# ======================================================

st.set_page_config(
    page_title="سيد قط",
    layout="wide"
)

# ======================================================
# تصميم CSS
# ======================================================

page_design = """
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

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
    margin-bottom:30px;
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
# DeepL API
# ======================================================

try:

    auth_key = st.secrets["DEEPL_API_KEY"]

    translator = deepl.Translator(auth_key)

except Exception:

    st.error("⚠️ أضف مفتاح DeepL داخل Secrets")

    st.stop()

# ======================================================
# تجهيز العربي
# ======================================================

def prepare_arabic(text):

    reshaped_text = arabic_reshaper.reshape(text)

    bidi_text = get_display(reshaped_text)

    return bidi_text

# ======================================================
# رفع الملف
# ======================================================

uploaded_file = st.file_uploader(
    "😸 ارفع الملزمة",
    type="pdf"
)

# ======================================================
# إذا تم رفع ملف
# ======================================================

if uploaded_file is not None:

    # فتح الـ PDF

    doc = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    total_pages = len(doc)

    # اختيار الصفحات

    c1, c2 = st.columns(2)

    with c1:

        start_page = st.number_input(
            "من صفحة",
            min_value=1,
            max_value=total_pages,
            value=1
        )

    with c2:

        end_page = st.number_input(
            "إلى صفحة",
            min_value=1,
            max_value=total_pages,
            value=total_pages
        )

    # ==================================================
    # زر الترجمة
    # ==================================================

    if st.button("😸 ابدأ الترجمة"):

        with st.spinner("🐈 سيد قط يترجم الآن..."):

            try:

                # ======================================
                # الصفحات
                # ======================================

                for page_num in range(
                    start_page - 1,
                    end_page
                ):

                    page = doc.load_page(page_num)

                    # استخراج البلوكات
                    blocks = page.get_text("blocks")

                    # ==================================
                    # كل بلوك
                    # ==================================

                    for block in blocks:

                        x0, y0, x1, y1, text, *_ = block

                        text = text.strip()

                        # تجاهل النصوص القصيرة
                        if len(text) < 3:
                            continue

                        # تنظيف
                        clean_text = text.replace("\n", " ")

                        # ==================================
                        # الترجمة
                        # ==================================
              try:

                            result = translator.translate_text(
                                clean_text,
                                target_lang="AR"
                            )

                            arabic_text = prepare_arabic(
                                result.text
                            )

                        except Exception:

                            continue

                        # ==================================
                        # مكان الترجمة
                        # ==================================

                        new_y = y0 - 10

                        # ==================================
                        # خلفية خفيفة
                        # ==================================

                        rect = fitz.Rect(
                            x0,
                            new_y - 2,
                            x1,
                            new_y + 12
                        )

                        page.draw_rect(
                            rect,
                            color=(1, 1, 1),
                            fill=(1, 1, 1),
                            overlay=True
                        )

                        # ==================================
                        # كتابة الترجمة
                        # ==================================

                        page.insert_text(

                            (x0, new_y),

                            arabic_text,

                            fontsize=8,

                            fontname="helv",

                            color=(0, 0.6, 0),

                            overlay=True

                        )

                # ======================================
                # حفظ الملف
                # ======================================

                temp_pdf = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                )

                output_path = temp_pdf.name

                doc.save(output_path)

                doc.close()

                # ======================================
                # تحميل الملف
                # ======================================

                with open(output_path, "rb") as f:

                    st.success("😼 تمت الترجمة بنجاح!")

                    st.download_button(

                        label="😸 تحميل الملزمة المترجمة",

                        data=f,

                        file_name="SayedQatt_Translated.pdf",

                        mime="application/pdf"

                    )

                # حذف الملف المؤقت
                os.remove(output_path)

            except Exception as e:

                st.error(f"حدث خطأ: {e}")
