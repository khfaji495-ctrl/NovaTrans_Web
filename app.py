import time # أضف هذه المكتبة في الأعلى

# ... داخل حلقة المعالجة ...
for line in lines:
    if line.strip():
        try:
            # إضافة تأخير بسيط (0.5 ثانية) لكي لا يتم حظرك من جوجل
            time.sleep(0.5) 
            
            translated = GoogleTranslator(source='en', target='ar').translate(line)
            proper_arabic = prepare_arabic_text(translated)
            
            # ... باقي كود الرسم ...
            
        except Exception as e:
            # في حال حدث خطأ (مثل حظر مؤقت)، تجاهله ولا توقف البرنامج
            continue
