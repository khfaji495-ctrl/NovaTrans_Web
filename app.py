import streamlit as st
import base64

# ... (دالة get_base64_gif وكود CSS المحدث)

page_design = f"""
<style>
/* الخلفية ثابتة وتغطي الشاشة */
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/gif;base64,{gif_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* طبقة تغميق */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.7); /* تغميق أكثر لتوضيح النصوص */
    z-index: 0;
}}

/* هذا التعديل يحل مشكلة صعود النصوص واختفاء الأزرار */
div.block-container {{
    position: relative;
    z-index: 1;
    padding-top: 100px; /* دفع المحتوى للأسفل قليلاً */
    background: rgba(0, 0, 0, 0.3);
    border-radius: 20px;
    margin-top: 50px;
}}

.main-title {{
    color: #10b981;
    text-align: center;
    font-size: 3.0rem;
    font-weight: bold;
    margin-bottom: 10px;
}}
.sub-title {{
    color: #cbd5e1;
    text-align: center;
    font-size: 1.1rem;
    margin-bottom: 40px;
}}
</style>
"""
st.markdown(page_design, unsafe_allow_html=True)

# ... (بقية كودك من st.markdown('<p class="main-title">... وحتى النهاية)
