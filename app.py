import streamlit as st
import fitz
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io

# ... (نفس إعدادات CSS والـ UI السابقة) ...

    if st.button("🚀 ابدأ الترجمة مع سيد قط"):
        with st.spinner("سيد قط يضبط المسافات.. يرجى الانتظار"):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer)
            
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
            except:
                st.warning("⚠️ ملف الخط غير موجود.")
            
            y = 750  # بدأنا من مستوى أعلى قليلاً
            for i in range(start - 1, end):
                text = doc.load_page(i).get_text()
                lines = text.split('\n')
                
                for line in lines:
                    if line.strip():
                        if y < 50: # صفحة جديدة إذا وصلنا للقاع
                            c.showPage()
                            y = 750
                        
                        # نص إنجليزي
                        c.setFont("Helvetica", 10)
                        c.drawString(50, y, line[:100])
                        y -= 15 # تقليل المسافة بين العربي والإنجليزي
                        
                        try:
                            result = translator.translate_text(line, target_lang="AR")
                            # المعالجة الدقيقة للنص العربي
                            proper_arabic = get_display(arabic_reshaper.reshape(result.text))
                            
                            c.setFont("Arabic", 10)
                            c.rightDrawString(550, y, proper_arabic) # استخدام rightDrawString للمحاذاة لليمين
                            y -= 25 # مسافة معقولة للسطر التالي
                        except:
                            continue
            
            c.save()
            pdf_buffer.seek(0)
            st.success("✅ سيد قط أتم المهمة!")
            # ... (باقي زر التحميل) ...
