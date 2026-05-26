import arabic_reshaper
from bidi.algorithm import get_display

# دالة لتجهيز النص العربي للطباعة بشكل صحيح
def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# داخل حلقة التكرار (loop) عند طباعة النص في PDF:
translated_line = GoogleTranslator(source='en', target='ar').translate(line)
# تحويل النص العربي
proper_arabic = prepare_arabic_text(translated_line)

# ثم اطبع النص:
c.drawString(x, y, proper_arabic)
