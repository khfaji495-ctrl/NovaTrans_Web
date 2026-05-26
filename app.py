import streamlit as st
import fitz
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
import io

# --- الإعدادات والواجهة (ألوان مريحة للعين) ---
st.set_page_config(page_title="NovaTrans Pro", layout="wide")
st.markdown("""
    <style>
    /* خلفية التطبيق */
    .stApp { background-color: #262730; color: #E0E0E0; }
    
    /* العنوان: لون تركوازي هادئ بدلاً من الفوشيا */
    h1 { 
        color: #40E0D0; 
        text-align: center; 
        font-family: sans-serif;
        margin-bottom: 30px;
    }
    
    /* تنسيق زر التحميل والخيارات */
    div.stButton > button {
        background-color: #40E0D0;
        color: #262730;
        font-weight: bold;
        border: none;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ NovaTrans Pro")
# ... باقي الكود الخاص بك كما هو ...
