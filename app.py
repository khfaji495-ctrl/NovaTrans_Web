import streamlit as st
import fitz  # PyMuPDF
import deepl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io

# [الإعدادات السابقة كما هي...]
# (تأكد من بقاء تعريفات الـ UI والـ CSS في مكانها)

if st.button("😸 ابدأ الترجمة مع سيد قط"):
    # إضافة شريط التقدم
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner(".... 🐈سيد قط يترجم الملزمة الآن.. يرجى الانتظار"):
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer)
        
        try:
            pdfmetrics.registerFont(TTFont('Arabic', 'font.ttf'))
        except:
            st.warning("⚠️ تنبيه: ملف الخط (font.ttf) غير موجود.")
        
        page_range = range(start - 1, end)
        total_pages = len(page_range)

        for idx, i in enumerate(page_range):
            # تحديث شريط التقدم
            progress_bar.progress((idx + 1) / total_pages)
            status_text.text(f"جاري معالجة الصفحة {idx + 1} من {total_pages}...")
            
            page = doc.load_page(i)
            
            # --- 1. إضافة الصور في مكانها ---
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                img_data = pix.tobytes("png")
                
                # الحصول على موقع الصورة في الصفحة
                rects = page.get_image_rects(xref)
                if rects:
                    rect = rects[0]
                    # تحويل إحداثيات fitz إلى إحداثيات reportlab (التي تبدأ من الأسفل)
                    img_x = rect.x0
                    img_y = page.rect.height - rect.y1 
                    
                    c.drawImage(io.BytesIO(img_data), img_x, img_y, width=rect.width, height=rect.height)

            # --- 2. معالجة النصوص ---
            text = page.get_text()
            lines = text.split('\n')
            y = 800 
            
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
                    except:
                        continue
            c.showPage() # الانتقال لصفحة جديدة في الـ PDF الجديد بعد كل صفحة أصلية
            
        c.save()
        pdf_buffer.seek(0)
        progress_bar.empty()
        status_text.empty()
        st.success("😼سيد قط أتم المهمة بنجاح!")
        # [زر التحميل كما هو...]
