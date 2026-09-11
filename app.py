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
    st.session_state.user_lang = "Hindi (हिन्दी)"
if "lang_code" not in st.session_state:
    st.session_state.lang_code = "hi-IN"
if "last_spoken_msg" not in st.session_state:
    st.session_state.last_spoken_msg = ""

# Form state
if "form_name" not in st.session_state:
    st.session_state.form_name = ""
if "form_age" not in st.session_state:
    st.session_state.form_age = ""
if "form_income" not in st.session_state:
    st.session_state.form_income = ""
if "form_category" not in st.session_state:
    st.session_state.form_category = "SC/ST"

# Language Mapping Dictionary
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

# 3. Controlled Speech Engine (Prevents Overlap & Stuttering)
def speak_guaranteed(text, lang_code="hi-IN"):
    """Cancels any ongoing speech queue before speaking new text."""
    if st.session_state.last_spoken_msg != text:
        st.session_state.last_spoken_msg = text
        js_code = f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                setTimeout(function() {{
                    var msg = new SpeechSynthesisUtterance("{text}");
                    msg.lang = "{lang_code}";
                    msg.rate = 0.85;
                    window.speechSynthesis.speak(msg);
                }}, 200);
            }}
        </script>
        """
        components.html(js_code, height=0, width=0)

# 4. Header & Emblem
st.markdown("""
<style>
    .flag-top { background-color: #FF9933; height: 14px; border-radius: 4px 4px 0 0; }
    .flag-mid { 
        background-color: #FFFFFF; 
        height: 20px; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
    }
    .flag-bot { background-color: #138808; height: 14px; border-radius: 0 0 4px 4px; }
    .emblem-container { text-align: center; margin-top: 15px; margin-bottom: 10px; }
    .emblem-img { width: 75px; height: auto; }
</style>

<div class="flag-top"></div>
<div class="flag-mid">
    <svg width="18" height="18" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="50" r="45" fill="none" stroke="#000080" stroke-width="6"/>
        <circle cx="50" cy="50" r="8" fill="#000080"/>
        <g stroke="#000080" stroke-width="3">
            <line x1="50" y1="50" x2="50" y2="5"/><line x1="50" y1="50" x2="50" y2="95"/>
            <line x1="50" y1="50" x2="5" y2="50"/><line x1="50" y1="50" x2="95" y2="50"/>
            <line x1="50" y1="50" x2="18" y2="18"/><line x1="50" y1="50" x2="82" y2="82"/>
            <line x1="50" y1="50" x2="18" y2="82"/><line x1="50" y1="50" x2="82" y2="18"/>
            <line x1="50" y1="50" x2="33" y2="9"/><line x1="50" y1="50" x2="67" y2="91"/>
            <line x1="50" y1="50" x2="9" y2="33"/><line x1="50" y1="50" x2="91" y2="67"/>
            <line x1="50" y1="50" x2="9" y2="67"/><line x1="50" y1="50" x2="91" y2="33"/>
            <line x1="50" y1="50" x2="33" y2="91"/><line x1="50" y1="50" x2="67" y2="9"/>
        </g>
    </svg>
</div>
<div class="flag-bot"></div>

<div class="emblem-container">
    <img class="emblem-img" src="https://upload.wikimedia.org/wikipedia/commons/7/77/Emblem_of_India.svg" alt="State Emblem of India">
    <br/>
    <span style="font-size: 14px; font-weight: bold; color: #555;">सत्यमेव जयते | Satyameva Jayate</span>
    <h1 style="margin-top: 5px; margin-bottom: 0px;">National Eligibility Test Portal</h1>
    <p style="color: #666; font-weight: 500;">Rural & Marginalized Entrepreneur Welfare Scheme Portal</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# 5. Page Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Page 1: Welcome & Language", 
    "Page 2: Scheme Directory", 
    "Page 3: Voice Eligibility Portal", 
    "Page 4: Download Certificate"
])

# --- PAGE 1: WELCOME & STABLE LANGUAGE SELECTION ---
with tab1:
    st.header("Welcome Portal / স্বাগতম পোর্টাল")

    col_select, col_mic = st.columns([2, 1])

    with col_select:
        options = ["-- Select Language / ভাষা নির্বাচন করুন --"] + list(LANGUAGES.keys())
        choice = st.selectbox("Choose Language:", options)

        if choice != "-- Select Language / ভাষা নির্বাচন করুন --":
            if st.session_state.user_lang != choice:
                st.session_state.user_lang = choice
                st.session_state.lang_code = LANGUAGES[choice]
                st.session_state.lang_selected = True
                st.session_state.last_spoken_msg = "" # Reset speech cache

    with col_mic:
        st.write("---")
        st.write("**Or Speak Language / মুখে বলুন:**")
        
        mic_html = """
        <button onclick="startListening()" style="background-color:#FF9933; color:white; border:none; padding:12px 20px; border-radius:5px; font-weight:bold; cursor:pointer;">
            🎤 Tap & Speak Language
        </button>
        <p id="speech_status" style="font-size:12px; color:#555; margin-top:5px;"></p>
        
        <script>
        function startListening() {
            var status = document.getElementById("speech_status");
            if (!('webkitSpeechRecognition' in window)) {
                status.innerText = "Speech recognition not supported.";
                return;
            }
            window.speechSynthesis.cancel(); // Silence voice while mic is listening
            var recognition = new webkitSpeechRecognition();
            recognition.lang = 'hi-IN';
            recognition.interimResults = false;
            
            recognition.onstart = function() { 
                status.innerText = "Listening... Speak language name now!"; 
            };
            
            recognition.onresult = function(event) {
                var transcript = event.results[0][0].transcript.toLowerCase();
                status.innerText = "Recognized: " + transcript;
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: transcript}, '*');
            };
            
            recognition.start();
        }
        </script>
        """
        spoken_val = components.html(mic_html, height=100)
        
        if spoken_val:
            val = str(spoken_val).lower()
            matched = None
            if "bengali" in val or "বাংলা" in val or "bangla" in val:
                matched = "Bengali (বাংলা)"
            elif "marathi" in val or "मराठी" in val:
                matched = "Marathi (मराठी)"
            elif "gujarati" in val or "ગુજરાતી" in val:
                matched = "Gujarati (ગૂજરાતી)"
            elif "tamil" in val or "தமிழ்" in val:
                matched = "Tamil (தமிழ்)"
            elif "telugu" in val or "తెలుగు" in val:
                matched = "Telugu (తెలుగు)"
            elif "hindi" in val or "हिंदी" in val or "हिन्दी" in val:
                matched = "Hindi (हिन्दी)"
            else:
                matched = "English"
                
            if st.session_state.user_lang != matched:
                st.session_state.user_lang = matched
                st.session_state.lang_code = LANGUAGES[matched]
                st.session_state.lang_selected = True
                st.session_state.last_spoken_msg = ""

    # Initial Welcome Prompt if Language not yet selected
    if not st.session_state.lang_selected:
        speak_guaranteed("Please select your language. कृपया अपनी भाषा चुनें। অনুগ্রহ করে আপনার ভাষা নির্বাচন করুন।", "hi-IN")
    else:
        lang_name = st.session_state.user_lang
        l_code = st.session_state.lang_code
        
        if "Bengali" in lang_name:
            guide = "আপনি বাংলা নির্বাচন করেছেন। এগিয়ে যাওয়ার জন্য অনুগ্রহ করে ৩ নম্বর ট্যাবে ক্লিক করুন।"
        elif "Hindi" in lang_name:
            guide = "आपने हिंदी चुनी है। आगे बढ़ने के लिए तीसरे टैब पर क्लिक करें।"
        elif "Marathi" in lang_name:
            guide = "तुम्ही मराठी निवडली आहे. पुढे जाण्यासाठी कृपया तिसऱ्या टॅबवर क्लिक करा."
        elif "Gujarati" in lang_name:
            guide = "તમે ગુજરાતી પસંદ કરી છે. આગળ વધવા માટે ત્રીજા ટેબ પર ક્લિક કરો."
        else:
            guide = f"You selected {lang_name}. Please click on Page 3 tab on top menu to proceed."

        st.success(f"🗣️ **Voice Direction ({lang_name}):** {guide}")
        speak_guaranteed(guide, l_code)

        if st.button("🔄 Change Language / भाषा बदलें"):
            st.session_state.lang_selected = False
            st.session_state.last_spoken_msg = ""
            st.rerun()

# --- PAGE 2: SCHEME DIRECTORY ---
with tab2:
    st.header("Government Schemes Directory")
    st.caption("Key welfare & micro-financing schemes available for rural entrepreneurs:")
    
    schemes = [
        {"name": "Prime Minister's Employment Generation Programme (PMEGP)", "detail": "Credit-linked subsidy program providing up to 35% margin money for rural micro-enterprises."},
        {"name": "Stand-Up India Scheme", "detail": "Bank loans between ₹10 Lakhs and ₹1 Crore for SC/ST and rural women entrepreneurs."},
        {"name": "Pradhan Mantri MUDRA Yojana (PMMY)", "detail": "Collateral-free loans up to ₹10 Lakhs for micro-businesses."}
    ]
    
    for s in schemes:
        st.subheader(s["name"])
        st.write(s["detail"])
        st.divider()

# --- PAGE 3: VOICE-ASSISTED FORM FOR RURAL USERS ---
with tab3:
    st.header("Voice-Guided Eligibility Entry")
    st.info("💡 Tap the button below to fill details using your voice.")

    col_fields, col_voice_nav = st.columns([2, 1])

    with col_fields:
        st.session_state.form_name = st.text_input("1. Full Name / नाम:", value=st.session_state.form_name)
        st.session_state.form_age = st.text_input("2. Age / उम्र:", value=st.session_state.form_age)
        st.session_state.form_income = st.text_input("3. Annual Income (₹) / आय:", value=st.session_state.form_income)
        st.session_state.form_category = st.selectbox(
            "4. Category / श्रेणी:",
            ["SC/ST", "Women Entrepreneur", "OBC / Minorities", "General"]
        )

    with col_voice_nav:
        st.write("---")
        st.write("**Voice Fill Assistant:**")
        
        guided_mic_html = f"""
        <button onclick="startFormAssistant()" style="background-color:#138808; color:white; border:none; padding:12px 18px; border-radius:5px; font-weight:bold; cursor:pointer;">
            🎤 Speak Name
        </button>
        <p id="form_status" style="font-size:13px; color:#333; margin-top:8px;"></p>

        <script>
        function startFormAssistant() {{
            var status = document.getElementById("form_status");
            if (!('webkitSpeechRecognition' in window)) {{
                status.innerText = "Speech recognition not supported.";
                return;
            }}
            window.speechSynthesis.cancel();
            var lCode = "{st.session_state.lang_code}";
            var rec = new webkitSpeechRecognition();
            rec.lang = lCode;
            rec.interimResults = false;

            status.innerText = "Listening for Name...";
            rec.start();

            rec.onresult = function(e) {{
                var spoken = e.results[0][0].transcript;
                status.innerText = "Recorded: " + spoken;
                window.parent.postMessage({{type: 'streamlit:setComponentValue', value: spoken}}, '*');
            }};
        }}
        </script>
        """
        voice_input_result = components.html(guided_mic_html, height=100)
        
        if voice_input_result:
            st.session_state.form_name = str(voice_input_result)

    st.divider()

    if st.button("Check Scheme Eligibility / पात्रता जांचें"):
        if st.session_state.form_name:
            st.session_state.eligible = True
            st.success(f"🎉 Eligibility Verified for candidate: **{st.session_state.form_name}**")
            
            l_code = st.session_state.lang_code
            if "bn" in l_code:
                resp = f"অভিনন্দন {st.session_state.form_name}! আপনি মনোনীত হয়েছেন। আপনার সার্টিফিকেট ডাউনলোড করতে ৪ নম্বর ট্যাবে যান।"
            elif "hi" in l_code:
                resp = f"बधाई हो {st.session_state.form_name}! आप पात्र हैं। अपना प्रमाण पत्र डाउनलोड करने के लिए चौथे टैब पर जाएं।"
            else:
                resp = f"Congratulations {st.session_state.form_name}! You are eligible. Please click on Page 4 to download your notice."

            speak_guaranteed(resp, l_code)
            st.info(f"🗣️ **Voice Navigation:** {resp}")
        else:
            err = "Please enter or speak your name first."
            st.warning(err)
            speak_guaranteed(err, st.session_state.lang_code)

# --- PAGE 4: RESULTS & PDF DOWNLOAD ---
with tab4:
    st.header("Selection Certificate Download")
    
    if st.session_state.get("form_name") and st.session_state.get("eligible"):
        st.success(f"🎉 **Selection Verified:** {st.session_state.form_name}")
        
        l_code = st.session_state.lang_code
        if "bn" in l_code:
            dl_prompt = "আপনার সার্টিফিকেট প্রস্তুত। ডাউনলোড করতে নিচের ডাউনলোড বাটনে ক্লিক করুন।"
        elif "hi" in l_code:
            dl_prompt = "आपका प्रमाण पत्र तैयार है। डाउनलोड करने के लिए नीचे दिए गए बटन पर क्लिक करें।"
        else:
            dl_prompt = "Your certificate is ready. Click the download button below to save your official notice."

        speak_guaranteed(dl_prompt, l_code)
        st.info(f"🗣️ **Voice Direction:** {dl_prompt}")

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
            story.append(Spacer(1, 15))
            
            story.append(Paragraph("<b>Matched Government Schemes:</b>", styles['Heading2']))
            data = [
                ["Scheme Name", "Benefits Summary"],
                ["PMEGP", "Up to 35% subsidy for micro-enterprises"],
                ["Stand-Up India", "Bank loans up to ₹1 Crore"],
                ["PMMY (MUDRA)", "Collateral-free loans up to ₹10 Lakhs"]
            ]
            
            t = Table(data, colWidths=[150, 300])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FF9933')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))
            story.append(t)
            
            doc.build(story)
            buffer.seek(0)
            return buffer

        pdf_file = generate_pdf(
            st.session_state.form_name, 
            st.session_state.form_age, 
            st.session_state.form_income, 
            st.session_state.form_category
        )
        
        st.download_button(
            label="📄 Download Official Notice PDF",
            data=pdf_file,
            file_name=f"Selection_Notice_{st.session_state.form_name}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("No record found. Please complete Page 3 first.")
