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

# 2. Session State Initialization
if "lang_selected" not in st.session_state:
    st.session_state.lang_selected = False
if "user_lang" not in st.session_state:
    st.session_state.user_lang = "English"

# 3. Speech Utilities
def speak_single(text, lang_code="en-IN"):
    """Plays a single spoken audio prompt without looping."""
    js = f"""
    <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance("{text}");
        msg.lang = "{lang_code}";
        msg.rate = 0.85;
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js, height=0, width=0)

def start_language_loop():
    """Loops bilingual request every 3 seconds until a language is chosen."""
    js_loop = """
    <script>
        window.speechSynthesis.cancel();
        
        function playLoopPrompt() {
            if (window.langSelected === true) return;
            
            window.speechSynthesis.cancel();
            
            var msgEn = new SpeechSynthesisUtterance("Please select your preferred language.");
            msgEn.lang = "en-IN";
            msgEn.rate = 0.9;
            
            var msgHi = new SpeechSynthesisUtterance("कृपया अपनी पसंदीदा भाषा चुनें।");
            msgHi.lang = "hi-IN";
            msgHi.rate = 0.9;
            
            window.speechSynthesis.speak(msgEn);
            msgEn.onend = function() {
                if (!window.langSelected) {
                    window.speechSynthesis.speak(msgHi);
                }
            };
        }

        // Initial trigger
        playLoopPrompt();
        
        // Loop every 3 seconds after speech finishes
        if (!window.promptInterval) {
            window.promptInterval = setInterval(function() {
                if (!window.speechSynthesis.speaking && !window.langSelected) {
                    playLoopPrompt();
                }
            }, 3000);
        }
    </script>
    """
    components.html(js_loop, height=0, width=0)

def stop_language_loop():
    """Stops the continuous looping prompt."""
    js_stop = """
    <script>
        window.langSelected = true;
        if (window.promptInterval) {
            clearInterval(window.promptInterval);
        }
        window.speechSynthesis.cancel();
    </script>
    """
    components.html(js_stop, height=0, width=0)

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
    <p style="color: #666; font-weight: 500;">AI Scheme-Based Matching for Marginalized Entrepreneurs</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# 5. Page Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Page 1: Welcome & Navigation", 
    "Page 2: Scheme Directory", 
    "Page 3: Eligibility Test", 
    "Page 4: Download Notice"
])

# --- PAGE 1: WELCOME & VOICE CONTROL ---
with tab1:
    st.header("Welcome Portal")
    
    # Trigger 3-second loop if user hasn't confirmed language yet
    if not st.session_state.lang_selected:
        start_language_loop()
        st.info("🔄 **Voice Assistant Loop Active:** Repeating *'Please select your preferred language / कृपया अपनी पसंदीदा भाषा चुनें'* every 3 seconds...")

    col_select, col_mic = st.columns([2, 1])

    with col_select:
        options = ["-- Choose Language --", "English", "Hindi (हिन्दी)"]
        choice = st.selectbox("Select Language / भाषा चुनें:", options)

        if choice != "-- Choose Language --":
            st.session_state.user_lang = choice
            st.session_state.lang_selected = True
            stop_language_loop()

    with col_mic:
        st.write("---")
        st.write("**Or Speak Your Language:**")
        
        mic_html = """
        <button onclick="startListening()" style="background-color:#FF9933; color:white; border:none; padding:10px 15px; border-radius:5px; font-weight:bold; cursor:pointer;">
            🎤 Tap Mic & Say Language
        </button>
        <p id="speech_status" style="font-size:12px; color:#555; margin-top:5px;"></p>
        
        <script>
        function startListening() {
            var status = document.getElementById("speech_status");
            if (!('webkitSpeechRecognition' in window)) {
                status.innerText = "Speech recognition not supported in browser.";
                return;
            }
            var recognition = new webkitSpeechRecognition();
            recognition.lang = 'en-IN';
            recognition.interimResults = false;
            
            recognition.onstart = function() { 
                status.innerText = "Listening for 'English' or 'Hindi'..."; 
            };
            
            recognition.onresult = function(event) {
                var transcript = event.results[0][0].transcript.toLowerCase();
                status.innerText = "You said: " + transcript;
                
                if (transcript.includes("hindi") || transcript.includes("हिन्दी")) {
                    window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'Hindi'}, '*');
                } else {
                    window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'English'}, '*');
                }
            };
            
            recognition.start();
        }
        </script>
        """
        spoken_lang = components.html(mic_html, height=90)
        
        if spoken_lang:
            if "hindi" in str(spoken_lang).lower():
                st.session_state.user_lang = "Hindi (हिन्दी)"
            else:
                st.session_state.user_lang = "English"
            st.session_state.lang_selected = True
            stop_language_loop()

    # Step-by-step voice guidance after selection
    if st.session_state.lang_selected:
        if "Hindi" in st.session_state.user_lang:
            guide_text = "आपने हिंदी चुनी है। आगे बढ़ने के लिए ऊपर दिए गए तीसरे टैब Page 3 Eligibility Test पर क्लिक करें।"
            st.success(f"🗣️ **Voice Navigation (Hindi):** {guide_text}")
            speak_single(guide_text, "hi-IN")
        else:
            guide_text = "You have selected English. To proceed, please click on Page 3 Eligibility Test on the top menu bar."
            st.success(f"🗣️ **Voice Navigation (English):** {guide_text}")
            speak_single(guide_text, "en-IN")

        if st.button("🔄 Reset Language Choice"):
            st.session_state.lang_selected = False
            st.rerun()

# --- PAGE 2: SCHEME DIRECTORY ---
with tab2:
    st.header("Government Schemes Directory")
    st.caption("Overview of key financial assistance schemes for micro-entrepreneurs:")
    
    schemes = [
        {"name": "Prime Minister's Employment Generation Programme (PMEGP)", "detail": "Credit-linked subsidy program providing up to 35% margin money for micro-enterprises."},
        {"name": "Stand-Up India Scheme", "detail": "Bank loans between ₹10 Lakhs and ₹1 Crore for SC/ST and women entrepreneurs."},
        {"name": "Pradhan Mantri MUDRA Yojana (PMMY)", "detail": "Collateral-free loans up to ₹10 Lakhs for non-farm micro-enterprises."}
    ]
    
    for s in schemes:
        st.subheader(s["name"])
        st.write(s["detail"])
        st.divider()

# --- PAGE 3: ELIGIBILITY TEST PORTAL ---
with tab3:
    st.header("Interactive Eligibility Portal")
    
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    st.session_state.user_name = st.text_input("Enter your name / अपना नाम दर्ज करें:", value=st.session_state.user_name)

    st.session_state.user_category = st.selectbox(
        "Select Category / श्रेणी चुनें:",
        ["SC/ST", "Women Entrepreneur", "OBC / Minorities", "General"]
    )
    
    if st.button("Check Eligibility"):
        if st.session_state.user_name:
            st.session_state.eligible = True
            st.success(f"Selected for schemes! Selected candidate: {st.session_state.user_name}")
            
            # Step-by-Step Guidance in the selected language
            if "Hindi" in st.session_state.user_lang:
                res_voice = f"बधाई हो {st.session_state.user_name}! आप पात्र हैं। अपना नोटिस डाउनलोड करने के लिए ऊपर दिए गए चौथे टैब Page 4 Download Notice पर जाएं।"
                speak_single(res_voice, "hi-IN")
            else:
                res_voice = f"Congratulations {st.session_state.user_name}! You are eligible. Please click on Page 4 Download Notice on the top menu to get your certificate."
                speak_single(res_voice, "en-IN")
        else:
            if "Hindi" in st.session_state.user_lang:
                err = "कृपया आगे बढ़ने के लिए अपना नाम दर्ज करें।"
                speak_single(err, "hi-IN")
            else:
                err = "Please enter your name to proceed."
                speak_single(err, "en-IN")
            st.warning(err)

# --- PAGE 4: RESULTS & PDF DOWNLOAD ---
with tab4:
    st.header("Selection Results & Notice Download")
    
    if st.session_state.get("user_name") and st.session_state.get("eligible"):
        st.success(f"🎉 **Congratulations {st.session_state.user_name}!** You are selected for top government schemes.")
        
        def generate_pdf(name, category):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            
            story = []
            story.append(Paragraph("<b>NATIONAL ELIGIBILITY TEST PORTAL</b>", styles['Title']))
            story.append(Paragraph("Official Scheme Selection Certificate", styles['Heading2']))
            story.append(Spacer(1, 15))
            
            info = f"<b>Applicant Name:</b> {name}<br/><b>Category:</b> {category}<br/><b>Status:</b> <font color='green'><b>SELECTED</b></font>"
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

        pdf_file = generate_pdf(st.session_state.user_name, st.session_state.user_category)
        
        st.download_button(
            label="📄 Download Official Notice PDF",
            data=pdf_file,
            file_name=f"Selection_Notice_{st.session_state.user_name}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("No record found. Please complete Page 3 first.")
        
