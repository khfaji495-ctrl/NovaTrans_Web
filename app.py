import streamlit as st
import fitz
from deep_translator import GoogleTranslator
from io import BytesIO

# ---------------------------
# إعداد الصفحة
# ---------------------------

st.set_page_config(
    page_title="NovaTrans Web",
    page_icon="😺",
    layout="wide"
)

# ---------------------------
# تصميم
# ---------------------------

page_design = """
<style>
.stApp {
    background: linear-gradient(180deg, #0e1117 0%, #16213e 100%);
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-size: 18px;
}

.stButton>button:hover {
    background-color: #ff2e2e;
}
</style>
"""

st.markdown(page_design, unsafe_allow_html=True)

# ---------------------------
# العنوان
# ---------------------------

st.title("😺 NovaTrans Web")
st.write("ترجمة ملفات PDF مع الحفاظ على الصور والتنسيق")

# ---------------------------
# رفع الملف
# ---------------------------

uploaded_file = st.file_uploader(
    "😺 ارسل ملف الملازمة",
    type=["pdf"]
)

if uploaded_file:

    # فتح الملف لمعرفة عدد الصفحات
    pdf_data = uploaded_file.getvalue()
    temp_doc = fitz.open(stream=pdf_data, filetype="pdf")

    total_pages = len(temp_doc)

    c1, c2 = st.columns(2)

    with c1:
        start = st.number_input(
            "من صفحة:",
            min_value=1,
            max_value=total_pages,
            value=1
        )

    with c2:
        end = st.number_input(
            "إلى صفحة:",
            min_value=1,
            max_value=total_pages,
            value=total_pages
        )

    # ---------------------------
    # زر الترجمة
    # ---------------------------

    if st.button("😺 ابدأ الترجمة مع سيد قط"):

        with st.spinner("🐈 سيد قط يترجم الملازمة الآن..."):

            try:

                # فتح الملف الأصلي
                doc = fitz.open(stream=pdf_data, filetype="pdf")

                # المرور على الصفحات
                for i in range(start - 1, end):

                    page = doc.load_page(i)

                    text_dict = page.get_text("dict")

                    # المرور على البلوكات
                    for block in text_dict["blocks"]:

                        if "lines" in block:

                            # المرور على السطور
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
                                        translated = GoogleTranslator(
                                            source='auto',
                                            target='ar'
                                        ).translate(line_text)

                                        # إضافة الترجمة فوق النص الأصلي
                                        page.insert_text(
                                            (x0, y0 - 12),
                                            translated,
                                            fontsize=9,
                                            fontname="helv",
                                            color=(1, 0, 0)
                                        )

                                    except:
                                        pass

                # حفظ الملف
                output_buffer = BytesIO()

                doc.save(output_buffer)

                output_buffer.seek(0)

                st.success("✅ تمت الترجمة بنجاح")

                st.download_button(
                    label="📥 تحميل الملف المترجم",
                    data=output_buffer,
                    file_name="translated.pdf",
                    mime="application/pdf"
                )

            except Exception as e:

                st.error("حدث خطأ أثناء الترجمة")
                st.code(str(e))
