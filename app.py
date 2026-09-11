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

# 2. Header Section: Indian Flag with Ashoka Chakra & National Emblem
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

<!-- Tricolor Flag with Ashoka Chakra -->
<div class="flag-top"></div>
<div class="flag-mid">
    <svg width="18" height="18" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="50" r="45" fill="none" stroke="#000080" stroke-width="6"/>
        <circle cx="50" cy="50" r="8" fill="#000080"/>
        <g stroke="#000080" stroke-width="3">
            <!-- 24 Spokes of Ashoka Chakra -->
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

<!-- National Emblem (Ashok Stambha) -->
<div class="emblem-container">
    <img class="emblem-img" src="https://upload.wikimedia.org/wikipedia/commons/7/77/Emblem_of_India.svg" alt="State Emblem of India">
    <br/>
    <span style="font-size: 14px; font-weight: bold; color: #555;">सत्यमेव जयते | Satyameva Jayate</span>
    <h1 style="margin-top: 5px; margin-bottom: 0px;">National Eligibility Test Portal</h1>
    <p style="color: #666; font-weight: 500;">AI Scheme-Based Matching for Marginalized Entrepreneurs</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Helper Function for Real Browser Text-to-Speech
def speak_text(text, lang_code="hi-IN"):
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{text}");
        msg.lang = "{lang_code}";
        msg.rate = 0.9;
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0, width=0)

# 3. Page Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "Page 1: Welcome Portal", 
    "Page 2: Scheme Directory", 
    "Page 3: Eligibility Test", 
    "Page 4: Download Notice"
])

# --- PAGE 1: WELCOME & VOICE ASSISTANT ---
with tab1:
    st.header("Welcome to National Eligibility Test Portal")
    st.write("This portal is built for all citizens, including learned and visually/text-assisted entrepreneurs.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_lang = st.selectbox(
            "Select Your Preferred Language / अपनी पसंदीदा भाषा चुनें:",
            ["Hindi (हिन्दी)", "English", "Bengali (বাংলা)", "Tamil (தமிழ்)", "Telugu (తెలుగు)", "Marathi (मराठी)"]
        )
    
    with col2:
        st.write("---")
        if st.button("🔊 Play Voice Welcome / आवाज सुनें"):
            if "Hindi" in selected_lang:
                speech_msg = "नेशनल एलिजिबिलिटी टेस्ट पोर्टल में आपका स्वागत है। कृपया अपनी पात्रता जांचें।"
                st.success(f"🗣️ Speaking: {speech_msg}")
                speak_text(speech_msg, "hi-IN")
            else:
                speech_msg = "Welcome to National Eligibility Test Portal. Please check your scheme eligibility."
                st.success(f"🗣️ Speaking: {speech_msg}")
                speak_text(speech_msg, "en-IN")

    st.info("💡 **Voice Guidance Active:** Tap the voice button above to hear spoken instructions from your device speaker.")

# --- PAGE 2: SCHEME DIRECTORY ---
with tab2:
    st.header("Government Schemes Directory")
    st.caption("Overview of key financial and developmental assistance schemes:")
    
    schemes = [
        {"name": "Prime Minister's Employment Generation Programme (PMEGP)", "detail": "Credit-linked subsidy program providing up to 35% margin money for micro-enterprises."},
        {"name": "Stand-Up India Scheme", "detail": "Bank loans between ₹10 Lakhs and ₹1 Crore for SC/ST and women entrepreneurs for greenfield enterprises."},
        {"name": "Pradhan Mantri MUDRA Yojana (PMMY)", "detail": "Collateral-free loans up to ₹10 Lakhs for non-farm micro-enterprises under Shishu, Kishore, and Tarun."},
        {"name": "Credit Guarantee Scheme for Micro & Small Enterprises (CGTMSE)", "detail": "Provides collateral-free credit guarantees to financial institutions lending up to ₹2 Crores to MSEs."}
    ]
    
    for s in schemes:
        with st.container():
            st.subheader(s["name"])
            st.write(s["detail"])
            st.divider()

# --- PAGE 3: ELIGIBILITY TEST PORTAL ---
with tab3:
    st.header("Interactive Eligibility Portal")
    
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "user_category" not in st.session_state:
        st.session_state.user_category = "SC/ST"

    col_input, col_mic = st.columns([3, 1])
    with col_input:
        st.session_state.user_name = st.text_input("Enter your name / अपना नाम दर्ज करें:", value=st.session_state.user_name)
    with col_mic:
        st.write("---")
        if st.button("🎤 Voice Assistant"):
            msg = "कृपया अपना नाम दर्ज करें"
            st.info(f"🗣️ {msg}")
            speak_text(msg, "hi-IN")

    st.session_state.user_category = st.selectbox(
        "Select Category / श्रेणी चुनें:",
        ["SC/ST", "Women Entrepreneur", "OBC / Minorities", "General"]
    )
    
    if st.button("Check Eligibility"):
        if st.session_state.user_name:
            st.session_state.eligible = True
            st.success(f"Selected for schemes! Selected candidate: {st.session_state.user_name}")
            voice_notice = f"बधाई हो {st.session_state.user_name}, आप सरकारी योजनाओं के लिए चुने गए हैं। कृपया पेज 4 से नोटिस डाउनलोड करें।"
            speak_text(voice_notice, "hi-IN")
        else:
            st.warning("Please enter your name first.")

# --- PAGE 4: RESULTS & PDF DOWNLOAD ---
with tab4:
    st.header("Selection Results & Notice Download")
    
    if st.session_state.get("user_name"):
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
        st.warning("No eligibility record found. Please complete the Eligibility Test on Page 3 first.")
        
        
            
