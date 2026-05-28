import streamlit as st
import fitz
import deepl
import io
import re
import arabic_reshaper
from bidi.algorithm import get_display

st.set_page_config(page_title="سيد قط", layout="wide")

translator = deepl.Translator(st.secrets["DEEPL_API_KEY"])

# ---------------- Arabic fix ----------------
def fix_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# ---------------- detect equations ----------------
def is_equation(text):
    return bool(re.search(r"[=<>±√∑∫]|\\d+\\/\\d+", text))

# ---------------- spacing cleaner ----------------
def clean_blocks(blocks):
    return sorted(blocks, key=lambda b: (b[1], b[0]))  # ترتيب حسب Y ثم X

# ---------------- UI ----------------
uploaded_file = st.file_uploader("ارفع PDF", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    start = st.number_input("من صفحة", 1, len(doc), 1)
    end = st.number_input("إلى صفحة", 1, len(doc), len(doc))

    if st.button("ابدأ الترجمة 😼"):
        output = io.BytesIO()
        new_doc = fitz.open()

        for i in range(start - 1, end):
            page = doc.load_page(i)

            # 🔥 نفس الصفحة (يحافظ على الصور والتنسيق)
            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.show_pdf_page(page.rect, doc, i)

            blocks = clean_blocks(page.get_text("blocks"))

            last_y = 0

            for b in blocks:
                x0, y0, x1, y1, text = b[:5]
                text = text.strip()

                if not text or is_equation(text):
                    continue

                # يمنع التداخل بين الفقرات
                if abs(y0 - last_y) < 15:
                    continue
                last_y = y0

                try:
                    translated = translator.translate_text(text, target_lang="AR").text
                    translated = fix_arabic(translated)
                except:
                    continue

                # ---------------- ENGLISH (تحت) ----------------
                new_page.insert_text(
                    (x0, y0 + 12),
                    text,
                    fontsize=10,
                    color=(0, 0, 0),
                )

                # ---------------- ARABIC (فوق) ----------------
                new_page.insert_text(
                    (x0, y0),
                    translated,
                    fontsize=11,
                    fontname="helv",  # أو arabic font لو متوفر
                    color=(0.1, 0.5, 0.2),
                )

        new_doc.save(output)
        output.seek(0)

        st.success("تمت المعالجة بنجاح 😼")

        st.download_button(
            "تحميل الملف",
            output,
            file_name="translated.pdf",
            mime="application/pdf"
        )
