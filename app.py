import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io
import base64
from groq import Groq
from gtts import gTTS

# إعداد المساعد الجديد (Groq)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 1. إعدادات الصفحة
st.set_page_config(page_title="سيد قط ", layout="wide")

# كود CSS: إخفاء القائمة + الخلفية + التنسيق
page_design = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #0e1117 0%, #16213e 100%); }
[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
.main-title { color: #10b981; text-align: center; font-size: 3.5rem; font-weight: bold; margin-top: -50px; }
.sub-title { color: #cbd5e1; text-align: center; font-size: 1.2rem; margin-bottom: 30px; }
</style>
"""
st.markdown(page_design, unsafe_allow_html=True)

# 2. عرض الـ GIF والعنوان
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("cat_pixel.gif", use_container_width=True)

st.markdown('<p class="main-title">سيد قط </p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">سيد قط يترجم ملازمك الهندسية والطبية بدقة</p>', unsafe_allow_html=True)

# إدارة ذاكرة الملف
if 'uploaded_pdf' not in st.session_state:
    st.session_state.uploaded_pdf = None

# التبويبات الجديدة
tab1, tab2 = st.tabs(["😸 الترجمة", "👨‍🏫 غرفة الدراسة"])

with tab1:
    # 3. إعداد مترجم DeepL
    try:
        auth_key = st.secrets["DEEPL_API_KEY"]
        translator = deepl.Translator(auth_key)
    except Exception as e:
        st.error("⚠️ خطأ: تأكد من إضافة مفتاح API في إعدادات Secrets باسم DEEPL_API_KEY")
        st.stop()

    def prepare_arabic_text(text):
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)

    # 4. واجهة رفع الملفات
    st.divider()
    uploaded_file = st.file_uploader(" 😸 ارسل ملف الملزمه للسيد قط", type="pdf")

    if uploaded_file is not None:
        st.session_state.uploaded_pdf = uploaded_file
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        total_pages = len(doc)
        
        c1, c2 = st.columns(2)
        with c1: start = st.number_input("من صفحة:", 1, total_pages, 1)
        with c2: end = st.number_input("إلى صفحة:", 1, total_pages, start)

        if st.button("😸 ابدأ الترجمة مع سيد قط"):
            with st.spinner(".... 🐈سيد قط يترجم الملزمة الآن.. يرجى الانتظار"):
                pdf_buffer = io.BytesIO()
                c = canvas.Canvas(pdf_buffer)
                try:
                    pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
                except:
                    st.warning("⚠️ تنبيه: ملف الخط (font.ttf) غير موجود.")
                
                y = 800 
                for i in range(start - 1, end):
                    text = doc.load_page(i).get_text()
                    lines = text.split('\n')
                    for line in lines:
                        if line.strip():
                            if y < 100:
                                c.showPage()
                                y = 800
                            c.setFont("Helvetica", 12)
                            c.drawString(50, y, line[:80])
                            y -= 20
                            try:
                                result = translator.translate_text(line, target_lang="AR")
                                proper_arabic = prepare_arabic_text(result.text)
                                c.setFont("Arabic", 12)
                                c.drawString(50, y, proper_arabic)
                                y -= 40
                            except: continue
                c.save()
                pdf_buffer.seek(0)
                st.success("😼سيد قط أتم المهمة بنجاح!")
                st.download_button("😸 تحميل الملزمة من سيد قط", pdf_buffer, "SayedQatt_Translated.pdf", "application/pdf")

with tab2:
    uploaded_file_study = st.file_uploader("📥 ارفع الملزمة هنا لغرفة الدراسة", type="pdf", key="study_pdf")
    
    if uploaded_file_study:
        # قراءة النص
        doc = fitz.open(stream=uploaded_file_study.read(), filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
            
        sub_tab1, sub_tab2 = st.tabs(["📄 محتوى الملزمة", "💬 مناقشة المساعد"])
        
        with sub_tab1:
            st.text_area("نص الملزمة المستخرج:", value=full_text[:10000], height=400)
            
        with sub_tab2:
            user_q = st.text_input("سيد قط، اشرح لي هذه النقطة:")
            if user_q:
                with st.spinner("سيد قط يحلل الملزمة..."):
                    try:
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": "أنت مساعد ذكي عراقي أصيل اسمه سيد قط. تحكي بلهجة أهل العراق (مثل: شونك، هسة، تدلل، عيوني). شرحك علمي لكن بلهجة عراقية بسيطة ومفهومة. لا تستخدم اللهجة المصرية أبداً."},
                                {"role": "user", "content": f"نص الملزمة: {full_text[:5000]} \n\n سؤالك: {user_q}"}
                            ]
                        )
                        answer = response.choices[0].message.content
                        st.markdown(f"**سيد قط:** {answer}")
                        
                        # تفعيل الصوت تلقائياً للشرح العراقي
                        st.subheader("🔊 استمع للشرح بالعراقي:")
                        tts = gTTS(text=answer, lang='ar')
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        st.audio(fp, format='audio/mp3')
                        
                    except Exception as e:
                        st.error(f"خطأ: {e}")
