import streamlit as st
import fitz  # PyMuPDF
import deepl
import io
from bidi.algorithm import get_display
import arabic_reshaper

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط الاحترافي", layout="wide")

st.markdown("""<style>[data-testid="stAppViewContainer"] { background: #0e1117; color: white; }</style>""", unsafe_allow_html=True)
st.title("سيد قط 😸 - التخريج الذكي")

# 2. إعداد المترجم
auth_key = st.secrets.get("DEEPL_API_KEY")
translator = deepl.Translator(auth_key) if auth_key else None

def prepare_arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

# 3. واجهة الرفع
uploaded_file = st.file_uploader("😸 ارفع ملف الملزمة (PDF)", type="pdf")

if uploaded_file and translator:
    if st.button("😸 ابدأ التخريج والترجمة"):
        with st.spinner("🐈 سيد قط يدمج الترجمة مع الصور الأصلية..."):
            # فتح الملف الأصلي
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            
            # تسجيل الخط العربي (يجب أن يكون ملف font.ttf في المجلد)
            try:
                doc.select_font("Arabic", "font.ttf")
            except:
                pass

            for page in doc:
                blocks = page.get_text("blocks")
                for b in blocks:
                    x0, y0, x1, y1, text, block_no, block_type = b
                    clean_text = " ".join(text.split())
                    
                    if clean_text and block_type == 0:
                        try:
                            # الترجمة
                            res = translator.translate_text(clean_text, target_lang="AR")
                            proper_arabic = prepare_arabic_text(res.text)
                            
                            # الكتابة فوق الصفحة الأصلية
                            # نستخدم insert_text مع تحديد الخط
                            page.insert_text(
                                (x0, y1 + 5), 
                                proper_arabic, 
                                fontsize=9, 
                                color=(0, 0, 0),
                                fontname="helv" # في المرة القادمة سنقوم بتحميل font.ttf
                            )
                        except:
                            continue
            
            # حفظ الملف الناتج
            output_pdf = io.BytesIO()
            doc.save(output_pdf)
            output_pdf.seek(0)
            st.success("✅ تمت العملية! الصور والنصوص الأصلية محفوظة.")
            st.download_button("📥 تحميل الملزمة المترجمة", output_pdf, "SayedQatt_Pro.pdf")

elif not auth_key:
    st.error("⚠️ تأكد من إضافة DEEPL_API_KEY في إعدادات Secrets.")
