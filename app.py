# -------------------------
# كتابة النص العربي داخل الـ PDF
# -------------------------

try:

    # كتابة النص
    page.draw_rect(
        fitz.Rect(x0, new_y - 2, x0 + width, new_y + 10),
        fill=(1, 1, 1),
        overlay=True
    )

    page.insert_text(
        (x0, new_y),
        arabic_text,
        fontsize=8,
        fontname="helv",
        color=(0, 0.6, 0),
        overlay=True
    )

    # حفظ الملف
    temp_pdf = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    output_path = temp_pdf.name

    doc.save(output_path)
    doc.close()

    # زر التحميل
    with open(output_path, "rb") as f:

        st.success("😼 تمت الترجمة بنجاح!")

        st.download_button(
            label="😸 تحميل الملزمة",
            data=f,
            file_name="SayedQatt_Translated.pdf",
            mime="application/pdf"
        )

    # حذف الملف المؤقت
    os.remove(output_path)

except Exception as e:

    st.error(f"خطأ: {str(e)}")
