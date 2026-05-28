import streamlit as st
import fitz
import deepl
import io
import re

st.set_page_config(page_title="سيد قط", layout="wide")

# ---------------- DeepL ----------------
translator = deepl.Translator(st.secrets["DEEPL_API_KEY"])

# ---------------- تنظيف المعادلات ----------------
def is_equation(text):
    return bool(re.search(r"[=<>±√∑∫]|\\d+\\/\\d+", text))

# ---------------- تقسيم النص ----------------
def split_text(text, max_len=90):
    words = text.split()
    lines = []
    temp = ""

    for w in words:
        if len(temp + " " + w) < max_len:
            temp += " " + w
        else:
            lines.append(temp)
            temp = w
    if temp:
        lines.append(temp)

    return lines

# ---------------- واجهة ----------------
uploaded_file = st.file_uploader("ارفع PDF", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    start = st.number_input("من صفحة", 1, len(doc), 1)
    end = st.number_input("إلى صفحة", 1, len(doc), len(doc))

    if st.button("ابدأ 😼"):
        output = io.BytesIO()
        new_doc = fitz.open()

        for page_num in range(start - 1, end):
            page = doc.load_page(page_num)

            # 🔥 نحافظ على نفس الصفحة (صور + تنسيق)
            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.show_pdf_page(page.rect, doc, page_num)

            blocks = page.get_text("blocks")

            for b in blocks:
                text = b[4].strip()
                x0, y0, x1, y1 = b[:4]

                if not text or is_equation(text):
                    continue

                try:
                    translated = translator.translate_text(text, target_lang="AR").text
                except:
                    continue

                # ---------------- الإنجليزية ----------------
                new_page.insert_text(
                    (x0, y0),
                    text,
                    fontsize=10,
                    color=(0, 0, 0),
                )

                # ---------------- العربية فوقه ----------------
                new_page.insert_text(
                    (x0, y0 - 12),
                    translated,
                    fontsize=11,
                    color=(0.1, 0.6, 0.3),
                )

        new_doc.save(output)
        output.seek(0)

        st.success("تمت المعالجة 😼")

        st.download_button(
            "تحميل الملف المعدل",
            output,
            file_name="translated_overlay.pdf",
            mime="application/pdf"
        )
