# ==================================
                        # إضافة الترجمة
                        # ==================================

                        new_y = y0 - 12

                        # مستطيل خفيف خلف الترجمة
                        rect = fitz.Rect(
                            x0,
                            new_y - 2,
                            x1,
                            new_y + 14
                        )

                        page.draw_rect(
                            rect,
                            color=(1,1,1),
                            fill=(1,1,1),
                            overlay=True
                        )

                        # كتابة العربي
                        page.insert_text(

                            (x0, new_y),

                            arabic_text,

                            fontsize=8,

                            fontname="helv",

                            color=(0, 0.7, 0),

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
                # تحميل
                # ======================================

                with open(output_path, "rb") as f:

                    st.success("😼 تمت الترجمة بنجاح!")

                    st.download_button(

                        label="😸 تحميل الملزمة",

                        data=f,

                        file_name="SayedQatt_Translated.pdf",

                        mime="application/pdf"

                    )

                os.remove(output_path)

            except Exception as e:

                st.error(str(e))
``
