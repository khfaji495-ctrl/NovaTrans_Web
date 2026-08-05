import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="رسالة خاصة جداً", page_icon="❤️", layout="centered"
)

# تصميم وتنسيق CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #faf5f5;
    }
    h1 {
        color: #d9534f;
        text-align: center;
        font-family: 'Tahoma', sans-serif;
    }
    .love-text {
        font-size: 18px;
        color: #333333;
        text-align: center;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .message-box {
        font-size: 20px;
        color: #b30059;
        text-align: center;
        padding: 15px;
        background-color: #fff0f5;
        border-radius: 10px;
        border: 2px dashed #ffb6c1;
        margin-top: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# العنوان الرئيسي
st.markdown("<h1>إلى أغلى ما أملك ❤️</h1>", unsafe_allow_html=True)
st.write(
    "<p style='text-align: center; color: #666;'>تصميم خاص لعيونك وحدك</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

# رسالة الصفا والترضية العامة
st.markdown(
    """
<div class="love-text">
<b>أحياناً العتب يكون بقدر الحب، وأنا ما عندي أغلى منكِ بهالدنيا.</b><br>
هذه الصفحة سويتها خصيصاً حتى أثبت لكِ أن زعلك ما يهون علي ابداً، وأن كل محاولة مني هي حتى تبقى ضحكتك منورة حياتي.
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("### 🎮 فقرة التحدي والرضوة:")
st.write(
    "كل ما تجمعين قلب، راح تطلع لك رسالة خاصة من قلبي.. خلينا نشوف للنهاية:"
)

# قائمة العبارات (فارغة، يمكنك كتابة ما تحب بين علامتي التنصيص لكل قلب)
love_messages = [
    " زعل الدنيا بكفه وزعل اميرتي بكفه ثانيه",
    "احب ابتسامتج ما احب اشوفج زعلانه",
    "احبج هواي فدا عيونج اني",
    "يلا يلا اميرتي الحلوه راح ترضى عني ",
    "يلا اخير قلب هذا ام خدود",
]

# إدارة حالة النقاط في التطبيق
if "score" not in st.session_state:
  st.session_state.score = 0

st.write(f"🌟 عدد القلوب المجمعة: **{st.session_state.score} / 5**")

col1, col2 = st.columns(2)

with col1:
  if st.button("اضغطي هنا لجمع قلب 💖"):
    if st.session_state.score < len(love_messages):
      st.session_state.score += 1
      st.rerun()

with col2:
  if st.button("إعادة اللعبة 🔄"):
    st.session_state.score = 0
    st.rerun()

# عرض العبارة الخاصة بكل مرحلة بناءً على عدد القلوب التي جمعتها
if st.session_state.score > 0:
  current_msg = love_messages[st.session_state.score - 1]
  st.markdown(
      f'<div class="message-box">💖 {current_msg}</div>',
      unsafe_allow_html=True,
  )

# إذا جمعت كل القلوب (العدد 5)
if st.session_state.score >= len(love_messages):
  st.balloons()
  st.markdown(
      "<h3 style='color: #28a745; text-align: center; margin-top:20px;'>لقد"
      " جمعتِ كَلبي كله، ولا زعل بعد اليوم! 🎉❤️</h3>",
      unsafe_allow_html=True,
  )

st.markdown("---")

# السؤال النهائي التفاعلي
st.write(
    "<h4 style='text-align: center;'>سامحتني اميرتي ؟</h4>",
    unsafe_allow_html=True,
)

answer_col1, answer_col2 = st.columns(2)

with answer_col1:
  if st.button("نعم مسامحتك ❤️"):
    st.balloons()
    st.success(
        "يا بعد عيوني ، الله لا يحرمني منج ومن حنانج  ولا يكتب زعل بيننا ابداً! ✨"
    )

with answer_col2:
  if st.button("لا بعدني زعلانة 😤"):
    st.warning(
        "محاولة ذكية، بس هذا الخيار مرفوض جملة وتفصيلاً! يلا اضغطي على الزر"
        " الأول 😉"
