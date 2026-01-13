import streamlit as st

# Page Configuration
st.set_page_config(page_title="LexTransition AI", page_icon="⚖️", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #1E3A8A; text-align: center; }
    .sub-text { font-size: 18px; text-align: center; color: #555; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1E3A8A; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation with Icons
st.sidebar.title("⚖️ LexTransition AI")
st.sidebar.info("Offline Legal Assistant: Mapping IPC to BNS")
role = st.sidebar.radio("Go to:", ["🏠 Home", "🔄 Law Mapper", "🖼️ OCR Document Analysis", "📚 Grounded Fact-Check"])

# --- 1. HOME PAGE ---
if role == "🏠 Home":
    st.markdown('<p class="main-title">LexTransition AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">Bridging the gap between IPC (Old) and BNS (New) Laws</p>', unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 1. Transition Mapper\nMaps IPC sections to BNS equivalents instantly.")
    with col2:
        st.success("### 2. OCR Analysis\nExtracts text from legal notices and FIR photos.")
    with col3:
        with st.expander("### 3. Fact Checking"):
            st.write("Ensures 100% accuracy with PDF citations.")

# --- 2. LAW MAPPER ---
elif role == "🔄 Law Mapper":
    st.header("🔄 IPC to BNS Transition Mapper")
    st.write("Search for an old IPC section to find its new BNS counterpart.")
    
    search_query = st.text_input("Enter IPC Section (e.g., 420, 302, 378):")
    
    # Static Sample Logic
    if search_query == "420":
        st.warning("### Old Law: IPC Section 420 (Cheating)")
        st.success("### New Law: BNS Section 318")
        st.write("**Key Changes:** The punishment remains similar, but the section numbering and sub-clauses have been reorganized for better clarity under BNS.")
    elif search_query:
        st.error("Section not found in static database. AI Model will process this in the full version.")

# --- 3. OCR ANALYSIS ---
elif role == "🖼️ OCR Document Analysis":
    st.header("🖼️ Multimodal Document Analysis")
    st.write("Upload a photo of a legal document to extract and simplify text.")
    
    uploaded_file = st.file_uploader("Upload Image (FIR/Notice)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Document", width=400)
        if st.button("Extract & Explain"):
            st.info("OCR Engine (EasyOCR/Tesseract) is processing... [Static Demo]")
            st.code("Extracted Text: NOTICE UNDER SECTION 41A CrPC...")
            st.success("**Simplified Action Item:** The police want you to join the investigation. No immediate arrest, but you must appear at the station.")

# --- 4. FACT-CHECK ---
elif role == "📚 Grounded Fact-Check":
    st.header("📚 Grounded Fact-Checking")
    st.write("Ask a legal question to get answers with official citations.")
    
    user_question = st.text_input("Ask a legal question:")
    
    if st.button("Verify with Law PDFs"):
        st.write("Searching through BNS Official Gazette...")
        # Static Demo Response
        st.markdown("""
        > **Answer:** Under BNS, theft is defined under Section 303.
        > 
        > **Citation:** > - **Source:** BNS_Official_Gazette.pdf
        > - **Chapter:** XVII (Offences Against Property)
        > - **Page No:** 84
        """)