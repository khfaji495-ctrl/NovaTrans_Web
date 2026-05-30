import streamlit as st
import streamlit.components.v1 as components

# إضافة كود التحقق من Google AdSense
def inject_adsense_meta():
    adsense_meta = """
    <meta name="google-adsense-account" content="ca-pub-1676304062422955">
    """
    components.html(f"{adsense_meta}", height=0)

# استدعاء الدالة في بداية الكود
inject_adsense_meta()

# ... هنا يكمل باقي كود تطبيقك الخاص بالترجمة ...
