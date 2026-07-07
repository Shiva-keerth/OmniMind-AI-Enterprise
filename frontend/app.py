import streamlit as st
import requests
from streamlit_option_menu import option_menu
from streamlit_agraph import agraph, Node, Edge, Config

# ══════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="OmniMind AI | Enterprise Knowledge",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os

# Backend API URL (Uses local for dev, or ENV for production)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api")

# ══════════════════════════════════════════════════════════════
# ELITE CSS — THE ULTIMATE MIX (OPTION 10)
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global Reset ── */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #1a202c 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* ── Hide Streamlit Defaults ── */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding-top: 2rem; max-width: 1400px; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070a10 0%, #0b0f19 100%) !important;
        border-right: 1px solid rgba(0, 242, 254, 0.15);
    }

    /* ── Glassmorphism Metric Cards ── */
    .metric-row { display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap; }
    .metric-card {
        flex: 1; min-width: 200px;
        background: rgba(11, 15, 25, 0.7);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .metric-card:hover {
        border-color: rgba(138, 43, 226, 0.6);
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(138, 43, 226, 0.2);
    }
    .metric-value {
        font-size: 36px; font-weight: 800;
        background: linear-gradient(135deg, #00f2fe, #4facfe, #8a2be2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .metric-label { font-size: 13px; text-transform: uppercase; letter-spacing: 2px; color: #a0aec0; font-weight: 600; }

    /* ── Hero Titles ── */
    .hero-title {
        font-size: 38px; font-weight: 800; line-height: 1.2;
        background: linear-gradient(135deg, #00f2fe, #4facfe, #8a2be2);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .hero-sub { font-size: 16px; color: #a0aec0; margin-bottom: 32px; }

    /* ── Professional Buttons ── */
    .stButton>button {
        background: linear-gradient(180deg, #2b6cb0 0%, #2c5282 100%);
        color: white;
        border: 1px solid #2a4365;
        border-radius: 8px;
        padding: 8px 24px;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(180deg, #3182ce 0%, #2b6cb0 100%);
        border: 1px solid #00f2fe;
        color: white;
        box-shadow: 0 6px 12px rgba(0, 242, 254, 0.2);
    }

    /* ── Streamlit Input Overrides ── */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(11, 15, 25, 0.8) !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
    }
    .stTextArea textarea:focus {
        border-color: #8a2be2 !important;
        box-shadow: 0 0 15px rgba(138, 43, 226, 0.3) !important;
    }
    
    /* ── Chat Interface ── */
    .chat-user {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.1), rgba(79, 172, 254, 0.05));
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 18px 18px 4px 18px;
        padding: 16px 20px;
        margin: 8px 0; margin-left: 15%;
        color: #e2e8f0;
    }
    .chat-ai {
        background: rgba(11, 15, 25, 0.6);
        border: 1px solid rgba(138, 43, 226, 0.2);
        border-radius: 18px 18px 18px 4px;
        padding: 16px 20px;
        margin: 8px 0; margin-right: 15%;
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 30px; margin-top: 10px;'>
            <div style='background: linear-gradient(135deg, #00f2fe 0%, #8a2be2 100%); width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 26px; box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);'>
                🧠
            </div>
            <div>
                <h2 style='margin: 0; font-size: 24px; font-weight: 800; line-height: 1.2; background: linear-gradient(135deg, #00f2fe, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>OmniMind AI</h2>
                <span style='color: #a0aec0; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>Enterprise Engine</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    selected_tab = option_menu(
        menu_title=None,
        options=["Global Dashboard", "Knowledge Ingestion", "Graph Visualizer", "Graph-RAG Chat"],
        icons=["grid-fill", "cloud-arrow-up-fill", "diagram-3-fill", "chat-right-dots-fill"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#00f2fe", "font-size": "18px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"5px 0", "border-radius": "8px", "color": "#cbd5e0"},
            "nav-link-selected": {"background-color": "rgba(0, 242, 254, 0.1)", "border-left": "4px solid #00f2fe", "color": "#ffffff", "font-weight": "600"},
        }
    )


# ══════════════════════════════════════════════════════════════
# TAB 1: GLOBAL DASHBOARD
# ══════════════════════════════════════════════════════════════
if selected_tab == "Global Dashboard":
    st.markdown('<div class="hero-title">Global Command Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Live metrics pinged directly from the Neo4j Enterprise Graph Database.</div>', unsafe_allow_html=True)

    with st.spinner("Pinging Neo4j Database..."):
        try:
            res = requests.get(f"{API_URL}/stats")
            res.raise_for_status()
            stats = res.json().get("data", {})
            projects = stats.get("projects", 0)
            employees = stats.get("employees", 0)
            actions = stats.get("action_items", 0)
        except Exception as e:
            st.error("Could not connect to backend.")
            projects, employees, actions = 0, 0, 0

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-value">{projects}</div>
            <div class="metric-label">Corporate Projects</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{employees}</div>
            <div class="metric-label">Employees Indexed</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{actions}</div>
            <div class="metric-label">Action Items Tracked</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">Active</div>
            <div class="metric-label">Neo4j Cluster</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Tip:** Go to the 'Knowledge Ingestion' tab and upload the dummy data to see these numbers grow in real-time!")

# ══════════════════════════════════════════════════════════════
# TAB 2: KNOWLEDGE INGESTION
# ══════════════════════════════════════════════════════════════
elif selected_tab == "Knowledge Ingestion":
    st.markdown('<div class="hero-title">Enterprise Knowledge Ingestion</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Upload meeting recordings or strategy documents to extract and index actionable intelligence into the Neo4j Graph.</div>', unsafe_allow_html=True)

    parser_mode = st.radio("Select Input Source:", ["Document Text (Strategy PDF, Notes)", "Audio Recording (Zoom Meeting)"], horizontal=True)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("### 1. Data Input")
        
        if "result_data" not in st.session_state:
            st.session_state.result_data = None
        
        if "Text" in parser_mode:
            meeting_text = st.text_area("Paste Corporate Document/Meeting Transcript:", height=300, key="meeting_text_input")
            if st.button("Extract & Index Intelligence", use_container_width=True):
                if not meeting_text:
                    st.warning("Please paste some text first!")
                else:
                    with st.spinner("Analyzing with Llama-3.3 and writing to Neo4j..."):
                        try:
                            res = requests.post(f"{API_URL}/extract/text", json={"text": meeting_text})
                            res.raise_for_status()
                            st.session_state.result_data = res.json().get("data")
                        except Exception as e:
                            st.error(f"Backend Error: {e}")
                            
        else:
            uploaded_file = st.file_uploader("Upload Audio Recording", type=["mp3", "wav", "m4a"])
            if st.button("Transcribe, Extract & Index", use_container_width=True):
                if not uploaded_file:
                    st.warning("Please upload an audio file first!")
                else:
                    with st.spinner("Transcribing with Whisper & Analyzing with Llama-3.3..."):
                        try:
                            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                            res = requests.post(f"{API_URL}/extract/audio", files=files)
                            res.raise_for_status()
                            st.session_state.result_data = res.json().get("data")
                        except Exception as e:
                            st.error(f"Backend Error: {e}")

        result_data = st.session_state.result_data

    with col2:
        st.markdown("### 2. Extracted Intelligence")
        
        if result_data:
            st.markdown(
                '<div style="padding: 16px; border-radius: 12px; background: rgba(0, 242, 254, 0.1); border: 1px solid #00f2fe; color: #ffffff; margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2);">'
                '✅ <b>SUCCESS:</b> Data extracted and successfully indexed into Neo4j Graph!'
                '</div>', 
                unsafe_allow_html=True
            )
            
            project_name = result_data.get("project_name", "Unknown")
            emps = result_data.get("employees_mentioned", [])
            emp_count = len(emps) if emps else 0
            
            st.markdown(f'''
                <div class="metric-row" style="margin-bottom: 15px;">
                    <div class="metric-card" style="padding: 15px;">
                        <h3 style="margin-top:0; color:#00f2fe; font-size:24px;">{project_name}</h3>
                        <p style="font-size: 12px; color: #a0aec0; margin:0;">PROJECT NAME</p>
                    </div>
                    <div class="metric-card" style="padding: 15px;">
                        <h3 style="margin-top:0; color:#00f2fe; font-size:24px;">{emp_count} Personnel</h3>
                        <p style="font-size: 12px; color: #a0aec0; margin:0;">EMPLOYEES INVOLVED</p>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            if emps:
                st.write("**Personnel:** " + ", ".join([f"`{e}`" for e in emps]))
            
            st.markdown("#### 📝 Action Items")
            action_items = result_data.get("action_items", [])
            if action_items:
                for item in action_items:
                    if isinstance(item, str):
                        assignee = "Unassigned"
                        task_desc = item
                        deadline = "None"
                    else:
                        assignee = item.get("assignee", "Unassigned")
                        task_desc = item.get("task_description", "Unknown Task")
                        deadline = item.get("deadline", "None")

                    st.markdown(f'''
                        <div style="background: rgba(11, 15, 25, 0.6); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #8a2be2;">
                            <b>Assignee:</b> {assignee}<br/>
                            <b>Task:</b> <span style="color:#e2e8f0;">{task_desc}</span><br/>
                            <b>Deadline:</b> <span style="color:#00f2fe;">{deadline}</span>
                        </div>
                    ''', unsafe_allow_html=True)
            else:
                st.info("No action items detected.")
        else:
            st.markdown(
                '<div class="metric-card" style="text-align: center; color: #a0aec0; padding: 40px;">'
                '<i>Upload data and click Extract to see the real-time Neo4j ingestion results here.</i>'
                '</div>', 
                unsafe_allow_html=True
            )

# ══════════════════════════════════════════════════════════════
# TAB 3: GRAPH VISUALIZER
# ══════════════════════════════════════════════════════════════
elif selected_tab == "Graph Visualizer":
    st.markdown('<div class="hero-title">3D Knowledge Graph Visualizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Explore the interconnected web of Projects, Employees, and Tasks currently residing in Neo4j.</div>', unsafe_allow_html=True)
    
    with st.spinner("Fetching Graph Data from Neo4j..."):
        try:
            res = requests.get(f"{API_URL}/graph_data")
            res.raise_for_status()
            graph_data = res.json().get("data", {})
            nodes_data = graph_data.get("nodes", [])
            edges_data = graph_data.get("edges", [])
        except Exception as e:
            st.error("Failed to fetch graph data.")
            nodes_data, edges_data = [], []
            
    if not nodes_data:
        st.info("Graph is empty. Please go to Knowledge Ingestion and upload some transcripts!")
    else:
        st.markdown('''
            <div style="display: flex; gap: 20px; margin-bottom: 15px; padding: 10px 20px; background: rgba(11, 15, 25, 0.6); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 10px; width: fit-content;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 14px; height: 14px; background: #8a2be2; border-radius: 3px;"></div>
                    <span style="color: #cbd5e0; font-size: 14px; font-weight: 500;">Project</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 14px; height: 14px; background: #4facfe; border-radius: 3px;"></div>
                    <span style="color: #cbd5e0; font-size: 14px; font-weight: 500;">Employee</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 14px; height: 14px; background: #10b981; border-radius: 3px;"></div>
                    <span style="color: #cbd5e0; font-size: 14px; font-weight: 500;">Action Item</span>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        nodes = []
        edges = []
        
        # Build Nodes
        for n in nodes_data:
            # Color coding based on label
            color = "#00f2fe" # Default Cyan
            if n["label"] == "Project": color = "#8a2be2" # Purple
            elif n["label"] == "Employee": color = "#4facfe" # Blue
            elif n["label"] == "ActionItem": color = "#10b981" # Emerald Green
            
            nodes.append( Node(id=n["id"], label=n["title"], size=25, color=color, shape="box") )
            
        # Build Edges
        for e in edges_data:
            edges.append( Edge(source=e["source"], target=e["target"], type="CURVE_SMOOTH", color="#cbd5e1") )
            
        config = Config(
            width="100%",
            height=800,
            directed=True,
            nodeHighlightBehavior=True,
            highlightColor="#ffffff",
            **{
                "layout": {
                    "hierarchical": {
                        "enabled": True,
                        "direction": "LR",
                        "sortMethod": "directed",
                        "nodeSpacing": 150,
                        "levelSeparation": 350
                    }
                },
                "nodes": {
                    "font": {
                        "size": 14,
                        "color": "#ffffff",
                        "face": "sans-serif"
                    },
                    "borderWidth": 2,
                    "borderWidthSelected": 4
                },
                "edges": {
                    "font": {
                        "size": 11,
                        "color": "#00f2fe",
                        "strokeWidth": 4,
                        "strokeColor": "#0b0f19"
                    },
                    "smooth": {
                        "type": "cubicBezier",
                        "roundness": 0.6
                    }
                },
                "physics": {
                    "solver": "hierarchicalRepulsion",
                    "hierarchicalRepulsion": {
                        "centralGravity": 0.0,
                        "springLength": 250,
                        "springConstant": 0.01,
                        "nodeDistance": 250,
                        "damping": 0.09
                    }
                }
            }
        )
        
        # Render
        st.markdown('<div style="border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">', unsafe_allow_html=True)
        return_value = agraph(nodes=nodes, edges=edges, config=config)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 4: GRAPH-RAG CHAT
# ══════════════════════════════════════════════════════════════
elif selected_tab == "Graph-RAG Chat":
    st.markdown('<div class="hero-title">Corporate Knowledge Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Ask natural language questions to query the Neo4j Graph Database via LangChain.</div>', unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! I am the OmniMind Agent. I have full access to the Neo4j Enterprise Graph. You can ask me things like 'What action items is Sarah working on?'"}]

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("Ask the Graph Database a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(f'<div class="chat-user">{prompt}</div>', unsafe_allow_html=True)

        with st.spinner("Writing Cypher Query and searching Neo4j..."):
            try:
                res = requests.post(f"{API_URL}/chat", json={"question": prompt})
                res.raise_for_status()
                answer = res.json().get("answer", "No answer found.")
            except Exception as e:
                answer = f"Failed to connect to Graph-RAG backend: {e}"
                
        st.markdown(f'<div class="chat-ai">🤖 {answer}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": answer})
