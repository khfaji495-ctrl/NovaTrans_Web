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
    return get_display(arabic_reshaper.reshape(text))

# ---------------- filter equations ----------------
def is_equation(text):
    return bool(re.search(r"[=<>±√∑∫]|\\d+\\/\\d+", text))

# ---------------- UI ----------------
uploaded_file = st.file_uploader("ارفع PDF", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    start = st.number_input("من صفحة", 1, len(doc), 1)
    end = st.number_input("إلى صفحة", 1, len(doc), len(doc))

    if st.button("ابدأ 😼"):
        output = io.BytesIO()
        new_doc = fitz.open()

        for i in range(start - 1, end):
            page = doc.load_page(i)

            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.show_pdf_page(page.rect, doc, i)

            blocks = page.get_text("blocks")

            for b in blocks:
                x0, y0, x1, y1, text = b[:5]
                text = text.strip()

                if not text or is_equation(text):
                    continue

                try:
                    ar = translator.translate_text(text, target_lang="AR").text
                    ar = fix_arabic(ar)
                except:
                    continue

                rect = fitz.Rect(x0, y0, x1, y1)

                # ---------------- 1) غطاء أبيض فوق النص الأصلي ----------------
                new_page.draw_rect(rect, color=None, fill=(1, 1, 1))

                # ---------------- 2) إعادة كتابة الإنجليزي ----------------
                new_page.insert_textbox(
                    rect,
                    text,
                    fontsize=10,
                    color=(0, 0, 0)
                )

                # ---------------- 3) الترجمة فوقه ----------------
                ar_rect = fitz.Rect(x0, y0 - 12, x1, y0)

                new_page.insert_textbox(
                    ar_rect,
                    ar,
                    fontsize=11,
                    color=(0.1, 0.6, 0.2)
                )

        new_doc.save(output)
        output.seek(0)

        st.success("تم إنشاء النسخة النهائية 😼🔥")

        st.download_button(
            "تحميل الملف",
            output,
            file_name="final_translated.pdf",
            mime="application/pdf"
        )
