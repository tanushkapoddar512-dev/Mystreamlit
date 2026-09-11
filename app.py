import streamlit as st
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

# 2. Header Section: Indian Flag & Emblem Title
st.markdown("""
<style>
    .flag-top { background-color: #FF9933; height: 12px; border-radius: 4px 4px 0 0; }
    .flag-mid { background-color: #FFFFFF; height: 12px; display: flex; align-items: center; justify-content: center; }
    .flag-bot { background-color: #138808; height: 12px; border-radius: 0 0 4px 4px; }
    .emblem-title { text-align: center; margin-top: 10px; margin-bottom: 20px; }
</style>
<div class="flag-top"></div>
<div class="flag-mid"></div>
<div class="flag-bot"></div>
""", unsafe_allow_html=True)

st.markdown("<div class="emblem-title">", unsafe_allow_html=True)
st.caption("सत्यमेव जयते | Satyameva Jayate")
st.title("National Eligibility Test Portal")
st.write("**AI Scheme-Based Matching for Marginalized Entrepreneurs**")
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# 3. Page Navigation (4 Distinct Pages/Tabs)
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
            ["English", "Hindi (हिन्दी)", "Bengali (বাংলা)", "Tamil (தமிழ்)", "Telugu (తెలుగు)", "Marathi (मराठी)", "Gujarati (ગુજરાતી)"]
        )
    
    with col2:
        st.write("---")
        if st.button("🔊 Play Voice Welcome / आवाज सुनें"):
            if "Hindi" in selected_lang:
                st.success("🗣️ Voice Assistant: नेशनल एलिजिबिलिटी टेस्ट पोर्टल में आपका स्वागत है। कृपया अपनी भाषा चुनें।")
            else:
                st.success("🗣️ Voice Assistant: Welcome to national eligibility test portal please select your preferred language.")

    st.info("💡 **Voice Guidance Mode Active:** The voice assistant will guide illiterate and first-time users through every option upon selection.")

# --- PAGE 2: SCHEME DIRECTORY ---
with tab2:
    st.header("Government Schemes Directory")
    st.caption("Overview of key financial and developmental assistance schemes in simple one-line details:")
    
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
    st.write("Enter your details below or use the assistant prompt.")
    
    # Session state for user inputs
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "user_category" not in st.session_state:
        st.session_state.user_category = "SC/ST"

    col_input, col_mic = st.columns([3, 1])
    with col_input:
        st.session_state.user_name = st.text_input("Enter your name / अपना नाम दर्ज करें:", value=st.session_state.user_name)
    with col_mic:
        st.write("---")
        if st.button("🎤 Voice Input Assistant"):
            st.info("🗣️ Voice Guide: Please enter your name or say it in the mic symbol.")

    st.session_state.user_category = st.selectbox(
        "Select Category / श्रेणी चुनें:",
        ["SC/ST", "Women Entrepreneur", "OBC / Minorities", "General"]
    )
    
    if st.button("Check Eligibility"):
        if st.session_state.user_name:
            st.session_state.eligible = True
            st.success(f"Selected for schemes! Selected candidate: {st.session_state.user_name}")
            st.info("🗣️ Voice Assistant: Selected for these schemes! Please proceed to Page 4 to download your official PDF notice.")
        else:
            st.warning("Please enter your name first.")

# --- PAGE 4: RESULTS & PDF DOWNLOAD ---
with tab4:
    st.header("Selection Results & Notice Download")
    
    if st.session_state.get("user_name"):
        st.success(f"🎉 **Congratulations {st.session_state.user_name}!** You are selected for top government schemes.")
        
        # PDF Generator Function
        def generate_pdf(name, category):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            
            story = []
            story.append(Paragraph("<b>NATIONAL ELIGIBILITY TEST PORTAL</b>", styles['Title']))
            story.append(Paragraph("Official Scheme Selection Certificate", styles['Subtitle']))
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
        
  
