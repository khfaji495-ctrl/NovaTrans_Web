import streamlit as st
from deep_translator import GoogleTranslator

st.title("NovaTrans Web")
text_input = st.text_area("أدخل النص المراد ترجمته:")

if st.button("ترجمة"):
    if text_input:
        # استخدام المكتبة الجديدة للترجمة
        translated = GoogleTranslator(source='auto', target='ar').translate(text_input)
        st.success("الترجمة:")
        st.write(translated)
    else:
        st.warning("يرجى كتابة نص أولاً!")