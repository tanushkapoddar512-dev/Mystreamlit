import io
from flask import Flask, render_template_string, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

app = Flask(__name__)

# Sample Database of Schemes (One-line summaries)
SCHEMES_DATABASE = [
    {
        "id": "pmegp",
        "name": "Prime Minister's Employment Generation Programme (PMEGP)",
        "summary": "Credit-linked subsidy program providing up to 35% margin money for establishing micro-enterprises in manufacturing and service sectors.",
        "category": "General / SC / ST / OBC / Women / Rural"
    },
    {
        "id": "standup_india",
        "name": "Stand-Up India Scheme",
        "summary": "Bank loans between ₹10 Lakhs and ₹1 Crore for SC/ST and women entrepreneurs setting up greenfield ventures.",
        "category": "SC / ST / Women"
    },
    {
        "id": "mudra",
        "name": "Pradhan Mantri MUDRA Yojana (PMMY)",
        "summary": "Collateral-free loans up to ₹10 Lakhs for non-corporate, non-farm small/micro enterprises divided into Shishu, Kishore, and Tarun categories.",
        "category": "Micro-Enterprises / All Categories"
    },
    {
        "id": "cgtsme",
        "name": "Credit Guarantee Scheme for Micro & Small Enterprises (CGTMSE)",
        "summary": "Provides collateral-free credit guarantees to financial institutions lending up to ₹2 Crores to eligible MSEs.",
        "category": "Micro & Small Enterprises"
    }
]

# Combined HTML Template with Inline Tailwinds CSS & Speech Web APIs
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>National Eligibility Test & AI Scheme Matching Portal</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    .flag-saffron { background-color: #FF9933; height: 16px; }
    .flag-white { background-color: #FFFFFF; height: 20px; display: flex; justify-content: center; align-items: center; }
    .flag-green { background-color: #138808; height: 16px; }
  </style>
</head>
<body class="bg-slate-100 text-slate-800 font-sans min-h-screen">

  <!-- Header Section -->
  <header class="w-full shadow-md bg-white sticky top-0 z-50">
    <!-- Top Indian Flag with Ashoka Chakra -->
    <div class="w-full">
      <div class="flag-saffron"></div>
      <div class="flag-white">
        <svg class="w-5 h-5 text-blue-900" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="6"/>
          <g stroke="currentColor" stroke-width="2">
            <line x1="50" y1="5" x2="50" y2="95"/><line x1="5" y1="50" x2="95" y2="50"/>
            <line x1="18" y1="18" x2="82" y2="82"/><line x1="18" y1="82" x2="82" y2="18"/>
            <line x1="8" y1="31" x2="92" y2="69"/><line x1="8" y1="69" x2="92" y2="31"/>
            <line x1="31" y1="8" x2="69" y2="92"/><line x1="31" y1="92" x2="69" y2="8"/>
          </g>
        </svg>
      </div>
      <div class="flag-green"></div>
    </div>

    <!-- National Emblem Representative Header -->
    <div class="text-center py-3 border-b bg-amber-50/30">
      <div class="inline-block p-1 bg-amber-100 rounded-full border border-amber-300 mb-1">
        <span class="text-xs font-bold text-amber-900 uppercase tracking-widest px-2">सत्यमेव जयते | Satyameva Jayate</span>
      </div>
      <h1 class="text-xl md:text-2xl font-black text-slate-900">National Eligibility Test Portal</h1>
      <p class="text-xs md:text-sm text-slate-600">AI-Powered Government Scheme Matching for Marginalized Entrepreneurs</p>
    </div>

    <!-- Navigation Tabs -->
    <nav class="flex justify-center bg-slate-800 text-white text-sm font-medium">
      <button onclick="switchPage('page1')" class="px-4 py-2 hover:bg-slate-700 border-b-2 border-amber-400">Page 1: Welcome</button>
      <button onclick="switchPage('page2')" class="px-4 py-2 hover:bg-slate-700">Page 2: Scheme Directory</button>
      <button onclick="switchPage('page3')" class="px-4 py-2 hover:bg-slate-700">Page 3: Eligibility Test</button>
    </nav>
  </header>

  <main class="max-w-4xl mx-auto p-4 md:p-6">

    <!-- PAGE 1: Welcome & Voice Assistant -->
    <section id="page1" class="space-y-6 bg-white p-6 rounded-xl shadow border">
      <div class="text-center space-y-4">
        <h2 class="text-2xl font-bold text-slate-900">Welcome / स्वागत है</h2>
        <p class="text-slate-600 text-sm">Dedicated assistant for both learned users and visually impaired/illiterate citizens.</p>
        
        <button onclick="playWelcomePrompt()" class="bg-amber-500 hover:bg-amber-600 text-white font-bold py-3 px-6 rounded-full shadow-lg transition transform active:scale-95 flex items-center justify-center gap-2 mx-auto">
          🔊 Click/Tap to Play Voice Welcome
        </button>
      </div>

      <div class="max-w-md mx-auto pt-4">
        <label for="language-select" class="block text-sm font-bold text-slate-700 mb-2">
          Select Preferred Language / अपनी पसंदीदा भाषा चुनें:
        </label>
        <select id="language-select" onchange="onLanguageChanged(this.value)" class="w-full p-3 border-2 border-slate-300 rounded-lg focus:border-amber-500 focus:outline-none">
          <option value="en-IN">English</option>
          <option value="hi-IN">हिन्दी (Hindi)</option>
          <option value="bn-IN">বাংলা (Bengali)</option>
          <option value="ta-IN">தமிழ் (Tamil)</option>
          <option value="te-IN">తెలుగు (Telugu)</option>
          <option value="mr-IN">मराठी (Marathi)</option>
          <option value="gu-IN">ગુજરાતી (Gujarati)</option>
        </select>
      </div>
    </section>

    <!-- PAGE 2: Schemes Directory (One-line Details) -->
    <section id="page2" class="hidden space-y-4 bg-white p-6 rounded-xl shadow border">
      <h2 class="text-2xl font-bold text-slate-900 border-b pb-2">Government Schemes Directory</h2>
      <p class="text-xs text-slate-500">Overview of available Central and State assistance programs in simple one-line descriptions:</p>
      
      <div class="space-y-3">
        {% for scheme in schemes %}
        <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
          <span class="text-xs font-semibold px-2 py-0.5 rounded bg-blue-100 text-blue-800 float-right">{{ scheme.category }}</span>
          <h3 class="font-bold text-slate-800 text-base mb-1">{{ scheme.name }}</h3>
          <p class="text-sm text-slate-600">{{ scheme.summary }}</p>
        </div>
        {% endfor %}
      </div>
    </section>

    <!-- PAGE 3: Interactive Eligibility Portal -->
    <section id="page3" class="hidden space-y-6 bg-white p-6 rounded-xl shadow border">
      <h2 class="text-2xl font-bold text-slate-900 border-b pb-2">Eligibility Verification Form</h2>

      <form id="eligibility-form" action="/download-notice" method="POST" class="space-y-4">
        
        <!-- Field 1: Name -->
        <div>
          <label class="block text-sm font-semibold text-slate-700 mb-1">Entrepreneur Name / उद्यमी का नाम:</label>
          <div class="flex gap-2">
            <input type="text" id="applicant_name" name="applicant_name" required placeholder="Type name or use mic" class="flex-1 p-3 border rounded-lg focus:ring-2 focus:ring-amber-500">
            <button type="button" onclick="promptAndListen('applicant_name', 'Please enter your name or say it in the mic symbol', 'कृपया अपना नाम दर्ज करें या माइक में बोलें')" class="bg-amber-500 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-1 hover:bg-amber-600">
              🎤 Voice
            </button>
          </div>
        </div>

        <!-- Field 2: Enterprise Type -->
        <div>
          <label class="block text-sm font-semibold text-slate-700 mb-1">Category / वर्ग:</label>
          <select id="category" name="category" class="w-full p-3 border rounded-lg">
            <option value="SC/ST">Scheduled Caste / Scheduled Tribe (SC/ST)</option>
            <option value="Women Entrepreneur">Women Entrepreneur</option>
            <option value="OBC / Minorities">OBC / Minorities</option>
            <option value="General">General Category</option>
          </select>
        </div>

        <!-- Submission Trigger -->
        <button type="submit" onclick="playSelectionSuccessMessage(event)" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 rounded-lg shadow transition">
          Check Eligibility & Download PDF Notice
        </button>
      </form>
    </section>

  </main>

  <script>
    const synth = window.speechSynthesis;

    function switchPage(pageId) {
      ['page1', 'page2', 'page3'].forEach(id => {
        document.getElementById(id).classList.add('hidden');
      });
      document.getElementById(pageId).classList.remove('hidden');
    }

    function speakText(text, lang = 'hi-IN') {
      if (synth.speaking) synth.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang;
      synth.speak(utterance);
    }

    function playWelcomePrompt() {
      const selectedLang = document.getElementById('language-select').value;
      const eng = "Welcome to national eligibility test portal please select your preferred language";
      const hin = "नेशनल एलिजिबिलिटी टेस्ट पोर्टल में आपका स्वागत है, कृपया अपनी पसंदीदा भाषा चुनें";

      if (selectedLang.startsWith('hi')) {
        speakText(hin, 'hi-IN');
      } else {
        speakText(eng, 'en-IN');
      }
    }

    function onLanguageChanged(lang) {
      const guideText = lang.startsWith('hi') 
        ? "आपने हिंदी भाषा चुनी है। अब voice assistant आपकी सहायता करेगा।" 
        : "You have selected your preferred language. Voice assistance is now active.";
      speakText(guideText, lang);
    }

    function promptAndListen(inputId, engPrompt, hinPrompt) {
      const selectedLang = document.getElementById('language-select').value;
      const promptText = selectedLang.startsWith('hi') ? hinPrompt : engPrompt;

      speakText(promptText, selectedLang);

      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert("Speech Recognition API not supported in this browser.");
        return;
      }

      const recognition = new SpeechRecognition();
      recognition.lang = selectedLang;

      // Start speech recognition after voice prompt ends
      setTimeout(() => {
        recognition.start();
      }, 3500);

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById(inputId).value = transcript;
        speakText(`Captured: ${transcript}`, selectedLang);
      };
    }

    function playSelectionSuccessMessage(e) {
      const selectedLang = document.getElementById('language-select').value;
      const msg = selectedLang.startsWith('hi') 
        ? "बधाई हो! आप इन योजनाओं के लिए चुने गए हैं। आधिकारिक पीडीएफ नोटिस डाउनलोड हो रहा है।" 
        : "Selected for these schemes! Downloading official PDF notice.";
      speakText(msg, selectedLang);
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, schemes=SCHEMES_DATABASE)

@app.route("/download-notice", methods=["POST"])
def download_notice():
    applicant_name = request.form.get("applicant_name", "Entrepreneur")
    category = request.form.get("category", "General")

    # Generate Dynamic PDF in Memory using ReportLab
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    story = []

    # Document Header
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Heading1'], alignment=1, textColor=colors.HexColor('#1E293B'))
    story.append(Paragraph("<b>NATIONAL ELIGIBILITY TEST PORTAL</b>", header_style))
    story.append(Paragraph("<font size=10 color='#475569'>Official Selection Notice for Marginalized Entrepreneur Schemes</font>", ParagraphStyle('Sub', parent=header_style, alignment=1)))
    story.append(Spacer(1, 15))

    # Applicant Information Block
    info_text = f"<b>Applicant Name:</b> {applicant_name}<br/><b>Category:</b> {category}<br/><b>Status:</b> <font color='green'><b>ELIGIBLE / SELECTED</b></font>"
    story.append(Paragraph(info_text, styles['Normal']))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Selected for these schemes:</b>", styles['Heading2']))
    story.append(Spacer(1, 10))

    # Filter/Select schemes dynamically
    table_data = [["Scheme Name", "Assistance Focus"]]
    for scheme in SCHEMES_DATABASE:
        table_data.append([scheme["name"], scheme["summary"]])

    table = Table(table_data, colWidths=[200, 320])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F59E0B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))

    story.append(table)
    doc.build(story)

    pdf_buffer.seek(0)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Scheme_Selection_Notice_{applicant_name.replace(' ', '_')}.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
  
