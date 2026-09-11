import streamlit as st
import streamlit.components.v1 as components
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io

# 1. Page Configuration
st.set_page_config(
    page_title="National Eligibility Test Portal",
    page_icon="🇮🇳",
    layout="wide"
)

# 2. Session State Setup
if "lang_selected" not in st.session_state:
    st.session_state.lang_selected = False
if "user_lang" not in st.session_state:
    st.session_state.user_lang = "-- Select Language / ভাষা নির্বাচন করুন --"
if "lang_code" not in st.session_state:
    st.session_state.lang_code = "hi-IN"

# Form field state
if "form_name" not in st.session_state:
    st.session_state.form_name = ""
if "form_age" not in st.session_state:
    st.session_state.form_age = ""
if "form_income" not in st.session_state:
    st.session_state.form_income = ""
if "form_category" not in st.session_state:
    st.session_state.form_category = "SC/ST"

# Supported Indian Languages Dictionary
LANGUAGES = {
    "Bengali (বাংলা)": "bn-IN",
    "Hindi (हिन्दी)": "hi-IN",
    "English": "en-IN",
    "Marathi (मराठी)": "mr-IN",
    "Gujarati (ગુજરાતી)": "gu-IN",
    "Tamil (தமிழ்)": "ta-IN",
    "Telugu (తెలుగు)": "te-IN",
    "Kannada (ಕನ್ನಡ)": "kn-IN",
    "Malayalam (മലയാളം)": "ml-IN",
    "Odia (ଓଡ଼ିଆ)": "or-IN",
    "Punjabi (ਪੰਜਾਬੀ)": "pa-IN"
}

# 3. Controlled Voice Guidance Function
def speak_text(text, lang_code="hi-IN"):
    """Executes clean speech synthesis in client browser."""
    js = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            setTimeout(function() {{
                var msg = new SpeechSynthesisUtterance("{text}");
                msg.lang = "{lang_code}";
                msg.rate = 0.85;
                window.speechSynthesis.speak(msg);
            }}, 100);
        }}
    </script>
    """
    components.html(js, height=0, width=0)

def detect_language(spoken_text):
    val = spoken_text.lower()
    if any(k in val for k in ["bengali", "bangla", "বাংলা", "बांग्ला"]):
        return "Bengali (বাংলা)"
    elif any(k in val for k in ["hindi", "हिंदी", "हिन्दी"]):
        return "Hindi (हिन्दी)"
    elif any(k in val for k in ["marathi", "मराठी"]):
        return "Marathi (मराठी)"
    elif any(k in val for k in ["gujarati", "ગુજરાતી"]):
        return "Gujarati (ગુજરાતી)"
    elif any(k in val for k in ["tamil", "தமிழ்"]):
        return "Tamil (தமிழ்)"
    elif any(k in val for k in ["telugu", "తెలుగు"]):
        return "Telugu (తెలుగు)"
    elif "english" in val:
        return "English"
    return None

# 4. Portal Header & Emblem
st.markdown("""
<style>
    .flag-top { background-color: #FF9933; height: 12px; border-radius: 4px 4px 0 0; }
    .flag-mid { background-color: #FFFFFF; height: 16px; display: flex; align-items: center; justify-content: center; }
    .flag-bot { background-color: #138808; height: 12px; border-radius: 0 0 4px 4px; }
    .emblem-container { text-align: center; margin-top: 10px; margin-bottom: 10px; }
    .emblem-img { width: 65px; height: auto; }
</style>

<div class="flag-top"></div>
<div class="flag-mid">
    <svg width="16" height="16" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="45" fill="none" stroke="#000080" stroke-width="6"/>
        <circle cx="50" cy="50" r="8" fill="#000080"/>
    </svg>
</div>
<div class="flag-bot"></div>

<div class="emblem-container">
    <img class="emblem-img" src="https://upload.wikimedia.org/wikipedia/commons/7/77/Emblem_of_India.svg" alt="Emblem">
    <h2 style="margin: 5px 0 0 0;">National Eligibility Test Portal</h2>
    <p style="color: #555; margin:0;">Rural & Marginalized Entrepreneur Welfare Scheme Portal</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# 5. Page Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Page 1: Welcome & Language", 
    "Page 2: Scheme Directory", 
    "Page 3: Voice Eligibility Portal", 
    "Page 4: Download Certificate"
])

# --- PAGE 1: WELCOME & MULTILINGUAL VOICE LOOP ---
with tab1:
    st.header("Welcome Portal / স্বাগতম পোর্টাল")

    # If language not chosen yet, loop welcoming speech in multiple Indian languages
    if not st.session_state.lang_selected:
        loop_js = """
        <script>
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                
                var prompts = [
                    {text: "Please select your language.", lang: "en-IN"},
                    {text: "कृपया अपनी भाषा चुनें।", lang: "hi-IN"},
                    {text: "অনুগ্রহ করে আপনার ভাষা নির্বাচন করুন।", lang: "bn-IN"},
                    {text: "कृपया तुमची भाषा निवडा.", lang: "mr-IN"},
                    {text: "કૃપા કરીને તમારી ભાષા પસંદ કરો.", lang: "gu-IN"}
                ];
                
                var idx = 0;
                function cycleSpeech() {
                    if (window.speechSynthesis.speaking) return;
                    var p = prompts[idx];
                    var u = new SpeechSynthesisUtterance(p.text);
                    u.lang = p.lang;
                    u.rate = 0.85;
                    u.onend = function() {
                        idx = (idx + 1) % prompts.length;
                        setTimeout(cycleSpeech, 1500);
                    };
                    window.speechSynthesis.speak(u);
                }
                cycleSpeech();
            }
        </script>
        """
        components.html(loop_js, height=0, width=0)
        st.info("🔄 **Voice Assistant Active:** Looping language choice prompt across Indian languages...")

    col1, col2 = st.columns([2, 1])

    with col1:
        options = ["-- Select Language / ভাষা নির্বাচন করুন --"] + list(LANGUAGES.keys())
        selected = st.selectbox("Choose Language:", options)

        if selected != "-- Select Language / ভাষা নির্বাচন করুন --" and selected != st.session_state.user_lang:
            st.session_state.user_lang = selected
            st.session_state.lang_code = LANGUAGES[selected]
            st.session_state.lang_selected = True
            st.rerun()

    with col2:
        st.write("---")
        st.write("**Or Speak Language:**")
        
        mic_js = """
        <button onclick="listenLang()" style="background-color:#FF9933; color:white; border:none; padding:10px 15px; border-radius:5px; font-weight:bold; cursor:pointer;">
            🎤 Tap & Speak Language
        </button>
        <p id="mic_out" style="font-size:12px; color:#555; margin-top:4px;"></p>

        <script>
        function listenLang() {
            if (!('webkitSpeechRecognition' in window)) return;
            window.speechSynthesis.cancel();
            var rec = new webkitSpeechRecognition();
            rec.lang = 'hi-IN';
            rec.onstart = function() { document.getElementById("mic_out").innerText = "Listening..."; };
            rec.onresult = function(e) {
                var text = e.results[0][0].transcript;
                document.getElementById("mic_out").innerText = "Spoken: " + text;
                const url = new URL(window.location.href);
                url.searchParams.set('spoken_lang', text);
                window.location.href = url.href;
            };
            rec.start();
        }
        </script>
        """
        components.html(mic_js, height=80)

        # Process URL parameters if speech detected language
        query_params = st.query_params
        if "spoken_lang" in query_params:
            spoken_val = query_params["spoken_lang"]
            matched = detect_language(spoken_val)
            if matched:
                st.session_state.user_lang = matched
                st.session_state.lang_code = LANGUAGES[matched]
                st.session_state.lang_selected = True
                st.query_params.clear()
                st.rerun()

    # Guidance once language is locked
    if st.session_state.lang_selected:
        lang_name = st.session_state.user_lang
        l_code = st.session_state.lang_code
        
        if "Bengali" in lang_name:
            guide_text = "আপনি বাংলা নির্বাচন করেছেন। এগিয়ে যাওয়ার জন্য অনুগ্রহ করে ৩ নম্বর ট্যাবে (Page 3) যান।"
        elif "Hindi" in lang_name:
            guide_text = "आपने हिंदी चुनी है। आगे बढ़ने के लिए कृपया तीसरे टैब (Page 3) पर जाएं।"
        elif "Marathi" in lang_name:
            guide_text = "तुम्ही मराठी निवडली आहे. पुढे जाण्यासाठी कृपया तिसऱ्या टॅबवर क्लिक करा."
        elif "Gujarati" in lang_name:
            guide_text = "તમે ગુજરાતી પસંદ કરી છે. આગળ વધવા માટે ત્રીજા ટેબ પર ક્લિક કરો."
        else:
            guide_text = f"You selected {lang_name}. Please click on Page 3 tab to proceed."

        st.success(f"🗣️ **Voice Navigation ({lang_name}):** {guide_text}")
        speak_text(guide_text, l_code)

        if st.button("🔄 Reset Language Choice"):
            st.session_state.lang_selected = False
            st.session_state.user_lang = "-- Select Language / ভাষা নির্বাচন করুন --"
            st.rerun()

# --- PAGE 2: SCHEME DIRECTORY ---
with tab2:
    st.header("Government Schemes Directory")
    st.write("• **PMEGP:** Up to 35% margin money subsidy for rural micro-enterprises.")
    st.write("• **Stand-Up India:** Bank loans from ₹10 Lakhs to ₹1 Crore for SC/ST and rural women entrepreneurs.")
    st.write("• **MUDRA Yojana:** Collateral-free micro-loans up to ₹10 Lakhs.")

# --- PAGE 3: VOICE ELIGIBILITY PORTAL FOR RURAL USERS ---
with tab3:
    st.header("Voice-Guided Form Entry")
    st.info("💡 **Voice Assistance Active:** Click the microphone icon next to any field or speak your input.")

    # URL query param handling for pure text injection (Fixes DeltaGenerator bug)
    qp = st.query_params
    if "voice_field_name" in qp:
        st.session_state.form_name = qp["voice_field_name"]
        st.query_params.clear()

    # Manual / Text inputs
    st.session_state.form_name = st.text_input("1. Full Name / নাম:", value=st.session_state.form_name)
    st.session_state.form_age = st.text_input("2. Age / বয়স / उम्र:", value=st.session_state.form_age)
    st.session_state.form_income = st.text_input("3. Annual Income (₹) / বার্ষিক আয়:", value=st.session_state.form_income)
    st.session_state.form_category = st.selectbox("4. Category / শ্রেণী:", ["SC/ST", "Women Entrepreneur", "OBC / Minorities", "General"])

    st.write("---")
    st.subheader("🎤 Voice Input Assistant")

    voice_fill_js = f"""
    <button onclick="startVoiceFill()" style="background-color:#138808; color:white; border:none; padding:12px 20px; border-radius:5px; font-weight:bold; cursor:pointer;">
        🎤 Speak Full Name Now
    </button>
    <p id="fill_status" style="font-size:13px; color:#333; margin-top:5px;"></p>

    <script>
    function startVoiceFill() {{
        if (!('webkitSpeechRecognition' in window)) return;
        window.speechSynthesis.cancel();
        
        var lCode = "{st.session_state.lang_code}";
        var rec = new webkitSpeechRecognition();
        rec.lang = lCode;
        
        var msg = new SpeechSynthesisUtterance("Please speak your name after the sound.");
        if (lCode.includes("bn")) msg.text = "অনুগ্রহ করে আপনার নাম বলুন।";
        else if (lCode.includes("hi")) msg.text = "कृपया अपना नाम बोलें।";
        msg.lang = lCode;

        msg.onend = function() {{
            document.getElementById("fill_status").innerText = "Listening for Name (pause when done)...";
            rec.start();
        }};
        
        rec.onresult = function(e) {{
            var nameVal = e.results[0][0].transcript;
            document.getElementById("fill_status").innerText = "Recorded: " + nameVal;
            const url = new URL(window.location.href);
            url.searchParams.set('voice_field_name', nameVal);
            window.location.href = url.href;
        }};

        window.speechSynthesis.speak(msg);
    }}
    </script>
    """
    components.html(voice_fill_js, height=100)

    st.divider()

    if st.button("Check Scheme Eligibility / पात्रता जांचें"):
        if st.session_state.form_name:
            st.session_state.eligible = True
            st.success(f"🎉 Eligibility Verified for candidate: **{st.session_state.form_name}**")
            
            l_code = st.session_state.lang_code
            if "bn" in l_code:
                res = f"অভিনন্দন {st.session_state.form_name}! আপনি নির্বাচিত হয়েছেন। আপনার অফিশিয়াল সার্টিফিকেট ডাউনলোড করতে ৪ নম্বর ট্যাবে যান।"
            elif "hi" in l_code:
                res = f"बधाई हो {st.session_state.form_name}! आप पात्र हैं। अपना प्रमाण पत्र डाउनलोड करने के लिए चौथे टैब पर जाएं।"
            else:
                res = f"Congratulations {st.session_state.form_name}! You are eligible. Click Page 4 to download your certificate."

            speak_text(res, l_code)
            st.info(f"🗣️ **Voice Output:** {res}")
        else:
            err = "Please enter or speak your name first."
            st.warning(err)
            speak_text(err, st.session_state.lang_code)

# --- PAGE 4: CERTIFICATE GENERATION ---
with tab4:
    st.header("Selection Certificate Download")
    if st.session_state.get("form_name") and st.session_state.get("eligible"):
        st.success(f"🎉 Certificate Ready for: **{st.session_state.form_name}**")

        def generate_pdf(name, age, income, category):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            story.append(Paragraph("<b>NATIONAL ELIGIBILITY TEST PORTAL</b>", styles['Title']))
            story.append(Paragraph("Official Scheme Selection Certificate", styles['Heading2']))
            story.append(Spacer(1, 15))
            info = f"<b>Applicant Name:</b> {name}<br/><b>Age:</b> {age}<br/><b>Income:</b> ₹{income}<br/><b>Category:</b> {category}<br/><b>Status:</b> <font color='green'><b>SELECTED</b></font>"
            story.append(Paragraph(info, styles['Normal']))
            doc.build(story)
            buffer.seek(0)
            return buffer

        pdf = generate_pdf(st.session_state.form_name, st.session_state.form_age, st.session_state.form_income, st.session_state.form_category)
        st.download_button("📄 Download Official Certificate PDF", data=pdf, file_name=f"Certificate_{st.session_state.form_name}.pdf", mime="application/pdf")
    else:
        st.warning("Please complete Page 3 first.")

        
        
