if st.button("😺 ابدأ الترجمة مع سيد قط"):

    with st.spinner("🐈 سيد قط يترجم الملازمة الآن..."):

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
                                y0 = span["bbox"][1]

        except Exception as e:
            st.error(f"حدث خطأ أثناء الترجمة: {e}")
