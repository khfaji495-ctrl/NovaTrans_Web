import streamlit as st
import fitz  # PyMuPDF
from deep_translator import GoogleTranslator

# --- إعدادات الصفحة والواجهة النيون ---
st.set_page_config(page_title="NovaTrans Neon", layout="wide")

st.markdown("""
    <style>
    /* تنسيق الخلفية العامة */
    .stApp {
        background-color: #060911;
    }
    
    /* تنسيق العنوان الرئيسي بنمط النيون */
    .neon-title {
        color: #fff;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        font-size: 3rem;
        text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 40px #ff00ff;
        margin-bottom: 20px;
    }
    
    /* تنسيق الحقول والأزرار */
    .stButton>button {
        background: linear-gradient(45deg, #ff00ff, #00ffff);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        box-shadow: 0 0 10px #00ffff;
    }
    
    /* تنسيق صناديق النص */
    .stTextArea textarea {
        background-color: #1a1c24 !important;
        color: #00ffcc !important;
        border: 1px solid #00ffff !important;
    }
    
    h2, h3, p {
        color: #00ffff !important;
        text-shadow: 0 0 5px #00ffff;
    }
    </style>
    <h1 class="neon-title">✨ NovaTrans Neon Pro</h1>
""", unsafe_allow_html=True)

# --- واجهة التطبيق ---
uploaded_file = st.file_uploader("📂 ارفع ملف الـ PDF هنا", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    total_pages = len(doc)
    
    st.sidebar.markdown("### 🛠 إعدادات الترجمة")
    st.sidebar.write(f"إجمالي عدد الصفحات: {total_pages}")
    
    # تحديد نطاق الصفحات
    start_page = st.sidebar.number_input("من صفحة:", min_value=1, max_value=total_pages, value=1)
    end_page = st.sidebar.number_input("إلى صفحة:", min_value=1, max_value=total_pages, value=min(start_page, total_pages))

    if st.button("🚀 ابدأ الترجمة الآن"):
        if start_page > end_page:
            st.error("خطأ: يجب أن يكون رقم صفحة البداية أصغر من أو يساوي صفحة النهاية.")
        else:
            progress_bar = st.progress(0)
            translated_pages_content = ""
            
            for i in range(start_page - 1, end_page):
                page = doc.load_page(i)
                text = page.get_text()
                
                if text.strip():
                    try:
                        # الترجمة لكل صفحة
                        translated = GoogleTranslator(source='en', target='ar').translate(text)
                        translated_pages_content += f"--- الصفحة {i+1} ---\n{text}\n\n[الترجمة]:\n{translated}\n\n"
                    except Exception as e:
                        st.error(f"حدث خطأ في الصفحة {i+1}")
                
                # تحديث شريط التقدم
                progress_bar.progress((i - (start_page - 1) + 1) / (end_page - start_page + 1))

            st.success("✅ تمت العملية بنجاح!")
            
            # عرض النتائج في منطقة نصية كبيرة
            st.text_area("النتائج (الأصلي + الترجمة):", translated_pages_content, height=400)
            
            # زر التحميل
            st.download_button(
                label="📥 تحميل النص المترجم كـ Text",
                data=translated_pages_content,
                file_name="translated_document.txt",
                mime="text/plain"
            )
else:
    st.info("👋 مرحباً بك! يرجى رفع ملف PDF للبدء في الترجمة بنمط النيون.")
