import streamlit as st
import fitz
from deep_translator import GoogleTranslator

st.title("✨ NovaTrans Neon")

uploaded_file = st.file_uploader("ارفع ملزمة الـ PDF:", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    page_num = st.number_input("اختر رقم الصفحة للترجمة:", min_value=1, max_value=len(doc), value=1)
    
    if st.button("ترجم الصفحة المحددة"):
        with st.spinner("جاري ترجمة الصفحة..."):
            # استخراج النص من صفحة واحدة فقط
            page = doc.load_page(page_num - 1)
            text = page.get_text()
            
            if text.strip():
                # ترجمة الصفحة الواحدة
                translated = GoogleTranslator(source='en', target='ar').translate(text)
                
                # عرض النتائج في عمودين
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("الأصلي")
                    st.write(text)
                with col2:
                    st.subheader("الترجمة")
                    st.write(translated)
            else:
                st.warning("هذه الصفحة لا تحتوي على نص قابل للقراءة!")
