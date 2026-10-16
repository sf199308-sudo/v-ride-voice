import streamlit as st
import requests
import os

# 1. إعدادات الصفحة باسم البراند الفخم V-Ride AI
st.set_page_config(page_title="V-Ride AI - Voice", page_icon="📞", layout="centered")

# حظر الكلمات غير الآمنة لحمايتك والأمان
BANNED_WORDS = ["قتل", "تهديد", "خطف", "شرطة", "قنبلة", "فلوس", "ابتزاز", "سجن"]

# قراءة مفتاح Vapi AI السري بأمان من إعدادات الـ Secrets
VAPI_API_KEY = os.environ.get("VAPI_API_KEY")

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("⚙️ V-Ride Control")
    st.markdown("---")
    st.subheader("💳 حالة السيستم")
    st.success("📞 منصة الرن: Vapi AI جاهزة")

# 3. الواجهة الرئيسية لإطلاق المكالمات
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>📞 V-Ride AI Voice</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>سيستم الرن الذكي مباشرة على خطوط المحمول عبر Vapi</h3>", unsafe_allow_html=True)
st.markdown("---")

with st.container():
    st.subheader("🎯 بيانات المفاجأة التليفونية")
    phone_number = st.text_input("📱 رقم التليفون المستهدف (بكود الدولة مثلاً +201xxxxxxxx):", placeholder="+201xxxxxxxx")
    prompt_input = st.text_area("📝 اكتب سيناريو المقلب أو الحوار بالبلدي لـ جيميني وصوت ElevenLabs:", placeholder="مثال: اتصل بصاحبي وقوله الأوردر بتاعك وصل بس طلع قفص طماطم...")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 ابدأ الاتصال البشري الذكي الآن", use_container_width=True):
    if not phone_number or not prompt_input:
        st.warning("يا أسطى كمل بياناتك الأول، ما تسيبش خانة فاضية!")
    else:
        if any(word in prompt_input for word in BANNED_WORDS):
            st.error("⚠️ الطلب ده مخالف لشروط الأمان يا أسطى، ما ينفعش نكمله.")
        else:
            if not VAPI_API_KEY:
                st.error("⚠️ مفتاح VAPI_API_KEY ناقص في الـ Secrets! روح حطه في إعدادات Hugging Face عشان يرضى يرن.")
            else:
                with st.spinner("🧠 جاري برمجة العميل وإطلاق الصاروخ ليرن حالاً..."):
                    try:
                        # 🛠️ تعديل الرابط ليكون الـ Endpoint الصحيح لعمل مكالمة خارجة (Outbound Call)
                        url = "https://vapi.ai"
                        
                        headers = {
                            "Authorization": f"Bearer {VAPI_API_KEY}",
                            "Content-Type": "application/json"
                        }
                        
                        # نبعت البيانات لـ Vapi وهما بيشغلوا عقل جيميني وصوت ElevenLabs أوتوماتيك
                        payload = {
                            "customer": {
                                "number": phone_number
                            },
                            "assistant": {
                                "model": {
                                    "provider": "google",
                                    "model": "gemini-1.5-flash",
                                    "messages": [
                                        {
                                            "role": "system",
                                            "content": f"أنت شخص مصري تتحدث بالعامية الشعبية بطلاقة وصياعة خفيفة. نفذ هذا السيناريو بالظبط وتفاعل مع ردوده بشكل طبيعي وضاحك: {prompt_input}"
                                        }
                                    ]
                                },
                                "voice": {
                                    "provider": "elevenlabs",
                                    "voiceId": "21m00Tcm4TlvDq8ikWAM" # صوت ElevenLabs رايق بيفهم مصري
                                }
                            }
                        }
                        
                        api_response = requests.post(url, json=payload, headers=headers)
                        
                        # 👍 هنا تم تصحيح الشرط عشان يقبل الاستجابة الناجحة (200 أو 201)
                        if api_response.status_code in:
                            st.success("🎉 الصاروخ انطلق! التليفون بيرن دلوقتي على الموبايل والذكاء الاصطناعي بيتكلم لايف!")
                            st.toast("تمت العملية بنجاح!")
                        else:
                            st.error(f"حصلت مشكلة في السيرفر. كود: {api_response.status_code} - الرد: {api_response.text}")
                            
                    except Exception as e:
                        st.error(f"حصلت قفلة في السيستم! الخطأ: {e}")
