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

# 2. Continuous Voice Navigation Helper (Auto-Speak)
def announce_voice(text, lang_code="hi-IN"):
    js_code = f"""
    <script>
        window.speechSynthesis.cancel(); // Stop any ongoing speech
        var msg = new SpeechSynthesisUtterance("{text}");
        msg.lang = "{lang_code}";
        msg.rate = 0.85; // Natural spoken speed
        msg.pitch = 1.0;
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0, width=0)

# 3. Header Section: Flag, Ashoka Chakra, and State Emblem
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

# Session State Initializers
if "first_visit" not in st.session_state:
    st.session_state.first_visit = True

# --- AUTOMATIC INITIAL WELCOME (MAPS STYLE AUTO-START) ---
if st.session_state.first_visit:
    welcome_prompt = "नेशनल एलिजिबिलिटी टेस्ट पोर्टल में आपका स्वागत है। आगे बढ़ने के लिए अपनी भाषा का चयन करें, फिर पेज 3 पर जाएं।"
    announce_voice(welcome_prompt, "hi-IN")
    st.session_state.first_visit = False

# 4. Page Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Page 1: Welcome & Navigation", 
    "Page 2: Scheme Directory", 
    "Page 3: Eligibility Test", 
    "Page 4: Download Notice"
])

# --- PAGE 1: WELCOME & VOICE GUIDANCE ---
with tab1:
    st.header("Welcome & Voice Guide")
    st.info("🔊 **Google Maps Style Voice Guide:** The voice assistant will guide you continuously through every action.")
    
    selected_lang = st.selectbox(
        "Select Your Preferred Language / अपनी पसंदीदा भाषा चुनें:",
        ["Hindi (हिन्दी)", "English", "Bengali (বাংলা)", "Tamil (தமிழ்)", "Marathi (मराठी)"]
    )
    
    # Speak dynamic instructions when language changes
    if "Hindi" in selected_lang:
        nav_msg = "आपने हिंदी चुनी है। अब आगे बढ़ने के लिए ऊपर दिए गए तीसरे टैब 'Page 3: Eligibility Test' पर क्लिक करें।"
        announce_voice(nav_msg, "hi-IN")
        st.success(f"🗣️ **Voice Direction:** {nav_msg}")
    else:
        nav_msg = "You selected English. To proceed, please tap on the 3rd tab at the top named Page 3 Eligibility Test."
        announce_voice(nav_msg, "en-IN")
        st.success(f"🗣️ **Voice Direction:** {nav_msg}")

    if st.button("🔊 Re-play Voice Navigation Guidance"):
        if "Hindi" in selected_lang:
            announce_voice("आगे बढ़ने के लिए पेज 3 एलिजिबिलिटी टेस्ट वाले बटन पर टैप करें।", "hi-IN")
        else:
            announce_voice("Please tap on Page 3 Eligibility Test on the top menu to proceed.", "en-IN")

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
    st.write("Follow the spoken directions to complete your eligibility check:")
    
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    col_input, col_mic = st.columns([3, 1])
    with col_input:
        st.session_state.user_name = st.text_input("Enter your name / अपना नाम दर्ज करें:", value=st.session_state.user_name)
    with col_mic:
        st.write("---")
        if st.button("🎤 Voice Assistant Prompt"):
            msg = "अपना नाम दर्ज करें, फिर नीचे दिए गए Check Eligibility बटन पर क्लिक करें।"
            st.info(f"🗣️ {msg}")
            announce_voice(msg, "hi-IN")

    st.session_state.user_category = st.selectbox(
        "Select Category / श्रेणी चुनें:",
        ["SC/ST", "Women Entrepreneur", "OBC / Minorities", "General"]
    )
    
    if st.button("Check Eligibility"):
        if st.session_state.user_name:
            st.session_state.eligible = True
            st.success(f"Selected for schemes! Selected candidate: {st.session_state.user_name}")
            
            # Step-by-Step Voice Direction after checking
            next_step_voice = f"बधाई हो {st.session_state.user_name}! आप सरकारी योजनाओं के लिए पात्र हैं। अब अपना पीडीएफ प्रमाणपत्र डाउनलोड करने के लिए ऊपर दिए गए चौथे टैब Page 4 Download Notice पर क्लिक करें।"
            announce_voice(next_step_voice, "hi-IN")
            st.info(f"🗣️ **Voice Navigation:** {next_step_voice}")
        else:
            err_msg = "कृपया आगे बढ़ने के लिए पहले अपना नाम लिखें।"
            st.warning(err_msg)
            announce_voice(err_msg, "hi-IN")

# --- PAGE 4: RESULTS & PDF DOWNLOAD ---
with tab4:
    st.header("Selection Results & Notice Download")
    
    if st.session_state.get("user_name"):
        st.success(f"🎉 **Congratulations {st.session_state.user_name}!** You are selected for top government schemes.")
        
        # Turn-by-turn voice prompt on page load
        download_voice = "सर्टिफिकेट तैयार है। लाल रंग के Download Official Notice PDF बटन पर क्लिक करके अपना नोटिस डाउनलोड करें।"
        announce_voice(download_voice, "hi-IN")
        st.info(f"🗣️ **Voice Navigation:** {download_voice}")
        
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
        no_rec_msg = "कोई रिकॉर्ड नहीं मिला। पहले पेज 3 पर जाएं और अपनी पात्रता जांचें।"
        st.warning(no_rec_msg)
        announce_voice(no_rec_msg, "hi-IN")
