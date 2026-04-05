import streamlit as st
import pandas as pd
from openai import OpenAI
import base64
import os
import matplotlib.pyplot as plt
import seaborn as sns
import json
import io
import hashlib
import re

# ---------------------------------------------------------
# CONSTANTS & ASSETS
# ---------------------------------------------------------
DEMO_DATASETS = {
    "Employee Records": """Employee_ID,Name,Department,Role,Hire_Date,Base_Salary,Performance_Score
E-1001,Yasser Salem A.,Operations,Manager,2022-01-15,3500,4.2
E-1002,Mona Abdel D.,IT,Data Analyst,2023-05-10,2800,4.8
E-1003,Omar Zwai B.,Finance,Accountant,2021-11-20,3100,3.9
E-1004,Salma Taher A.,HR,Specialist,2024-02-01,2400,4.5
E-1005,Ahmed Ali C.,Sales,Lead,2020-09-12,2900,4.1
E-1006,Lina Hamed B.,IT,Systems Admin,2022-08-30,2700,3.7
E-1007,Tariq Dali B.,Operations,Analyst,2023-12-05,2600,4.0
E-1008,Nadia Fathi C.,Finance,Manager,2019-03-22,4200,4.9
E-1009,Khaled Omar D.,IT,Developer,2025-01-10,3300,4.6
E-1010,Rania Ashour A.,HR,Manager,2021-06-15,3800,4.3""",
    "Sales Transactions": """Order_ID,Product,Category,Price,Quantity,Region,Date
ORD-001,Laptop,Electronics,1200,1,North,2024-03-01
ORD-002,Mouse,Accessories,25,3,South,2024-03-02
ORD-003,Monitor,Electronics,350,2,East,2024-03-05
ORD-004,Keyboard,Accessories,80,1,West,2024-03-10
ORD-005,Chair,Furniture,250,4,North,2024-03-12
ORD-006,Desk,Furniture,500,1,East,2024-03-15
ORD-007,Headphones,Electronics,150,2,South,2024-03-20
ORD-008,Smartphone,Electronics,800,1,West,2024-03-22""",
    "Project Management": """Task_ID,Task_Name,Assignee,Priority,Status,Days_to_Complete
T-1,Define Scope,Mahamed,High,Completed,5
T-2,Gemma 4 Integration,Algaroshy,Critical,In Progress,10
T-3,UI/UX Design,User,Medium,In Progress,7
T-4,Testing & QA,Team,High,Pending,4
T-5,Deployment,System,Medium,Pending,2""",
    "Inventory Stock": """SKU,Product_Name,Category,Stock_Level,Unit_Price,Reorder_Point
INV-101,SSD 1TB,Hardware,45,120,20
INV-102,DDR5 RAM 16GB,Hardware,12,85,15
INV-103,4K Monitor,Display,8,450,10
INV-104,Mechanical Keyboard,Peripherals,30,75,10
INV-105,Webcam 1080p,Peripherals,55,60,20""",
    "Customer Feedback": """Feedback_ID,Customer_Name,Product,Rating,Comment,Date
F-001,John Doe,Laptop,5,Excellent performance!,2024-03-25
F-002,Jane Smith,Mouse,3,A bit too small for my hand.,2024-03-26
F-003,Bob Wilson,SSD 1TB,5,Super fast drive.,2024-03-27
F-004,Alice Brown,Monitor,4,Great colors but expensive.,2024-03-28""",
}


# ---------------------------------------------------------
# UI HELPERS (SVG ICONS)
# ---------------------------------------------------------
def get_icon_svg(icon_name, size=20, color="currentColor"):
    icons = {
        "chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>',
        "settings": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.1a2 2 0 0 1-1-1.72v-.51a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>',
        "upload": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
        "brain": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.54Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-2.54Z"/></svg>',
        "activity": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        "sparkles": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3 1.912 5.813a2 2 0 0 0 1.275 1.275L21 12l-5.813 1.912a2 2 0 0 0-1.275 1.275L12 21l-1.912-5.813a2 2 0 0 0-1.275-1.275L3 12l5.813-1.912a2 2 0 0 0 1.275-1.275L12 3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/></svg>',
        "info": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>',
    }
    return icons.get(icon_name, "")


# ---------------------------------------------------------
# Define Tools / Agentic Functions for the AI
# ---------------------------------------------------------
def execute_python_code(code_string):
    """Executes python code and returns text output + any generated plot as base64."""
    plot_b64 = None
    try:
        exec_globals = {"df": st.session_state.df, "pd": pd, "plt": plt, "sns": sns}
        from io import StringIO, BytesIO
        import sys

        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()

        # Execute the code
        exec(code_string, exec_globals)

        # Capture text output
        output = redirected_output.getvalue().strip()
        sys.stdout = old_stdout

        # Check for plots
        if plt.get_fignums():
            buf = BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            plot_b64 = base64.b64encode(buf.read()).decode("utf-8")
            plt.clf()
            plt.close("all")

        # Update last_tool_df if created
        if "result_df" in exec_globals and isinstance(
            exec_globals["result_df"], pd.DataFrame
        ):
            st.session_state.last_tool_df = exec_globals["result_df"]
        elif "df" in exec_globals and isinstance(exec_globals["df"], pd.DataFrame):
            st.session_state.last_tool_df = exec_globals["df"]

        return {
            "status": "success",
            "output": output or "Executed successfully.",
            "plot": plot_b64,
        }
    except Exception as e:
        if "old_stdout" in locals():
            sys.stdout = old_stdout
        return {"status": "error", "message": str(e)}


tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "execute_python_code",
            "description": "Executes Python code to analyze 'df' or draw charts. 'df', 'pd', 'plt', 'sns' are available.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code_string": {"type": "string", "description": "Python code."}
                },
                "required": ["code_string"],
            },
        },
    }
]

# ---------------------------------------------------------
# MAIN APP CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Gemma Data Assistant",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "data_context" not in st.session_state:
    st.session_state.data_context = ""
if "df" not in st.session_state:
    st.session_state.df = None
if "current_sheet" not in st.session_state:
    st.session_state.current_sheet = None
if "last_tool_df" not in st.session_state:
    st.session_state.last_tool_df = None
if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None
if "last_image_hash" not in st.session_state:
    st.session_state.last_image_hash = None

# Initialize OpenAI client once (avoids recreation on every rerun)
DEFAULT_SERVER_URL = os.environ.get("SERVER_URL", "http://localhost:8080/v1")
DEFAULT_MODEL_NAME = os.environ.get("MODEL_NAME", "unsloth/gemma-4-e4b-it-gguf:Q4_K_XL")
client = OpenAI(base_url=DEFAULT_SERVER_URL, api_key="sk-no-key-required")

# ---------------------------------------------------------
# THEMED COLORS DEFINITION (FORCED DARK MODE)
# ---------------------------------------------------------
c = {
    "bg": "#0F172A",
    "sidebar_bg": "#1E293B",
    "text": "#F1F5F9",
    "primary": "#60A5FA",
    "secondary": "#93C5FD",
    "border": "#334155",
    "card_bg": "#1E293B",
    "sub_text": "#94A3B8",
}

st.markdown(
    f"""
<style>
    .stApp {{ background-color: {c["bg"]}; color: {c["text"]} !important; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; }}
    .stApp p, .stApp span, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {{ color: {c["text"]} !important; }}
    [data-testid="stSidebar"] {{ background-color: {c["sidebar_bg"]}; border-right: 1px solid {c["border"]}; }}
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label {{ color: {c["text"]} !important; }}
    .main-header {{ font-size: 3rem; font-weight: 800; color: {c["primary"]} !important; letter-spacing: -0.04em; margin-bottom: 0; }}
    .sub-header {{ font-size: 1.2rem; color: {c["sub_text"]} !important; margin-bottom: 2rem; }}
    .stMetric {{ background-color: {c["card_bg"]}; border: 1px solid {c["border"]}; border-radius: 12px; padding: 1rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
    .stMetric [data-testid="stMetricValue"], .stMetric [data-testid="stMetricLabel"] {{ color: {c["text"]} !important; }}
    .stChatMessage {{ border-radius: 16px; border: 1px solid {c["border"]}; background-color: {c["card_bg"]}; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
    [data-testid="stChatMessageContent"] p {{ color: {c["text"]} !important; }}
    .streamlit-expanderHeader {{ color: {c["primary"]} !important; font-weight: 600 !important; }}
    @keyframes pulse {{ 0% {{ opacity: 0.5; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.5; }} }}
    .skeleton {{ background: {c["border"]}; border-radius: 4px; height: 16px; margin: 8px 0; animation: pulse 1.5s infinite ease-in-out; }}
    .hero-container {{ text-align: center; padding: 3rem 2rem; background: {c["card_bg"]}; border-radius: 24px; border: 1px solid {c["border"]}; margin-bottom: 2rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); }}
    .step-card {{ background: {c["bg"]}; padding: 1.5rem; border-radius: 16px; border: 1px solid {c["border"]}; text-align: left; height: 100%; }}
    .step-card h3 {{ color: {c["primary"]} !important; margin-top: 0; }}
    .stMarkdown table {{ color: {c["text"]} !important; background-color: {c["card_bg"]}; }}
    .feature-tip {{ background: {c["bg"]}; padding: 1rem; border-radius: 12px; border-left: 4px solid {c["primary"]}; margin: 10px 0; }}
    .feature-tip b {{ color: {c["primary"]} !important; }}
</style>
""",
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    st.caption("Gemma 4 | 128K Context Window")
    est_tokens = len(st.session_state.data_context) // 4
    st.progress(
        min(est_tokens / 128000, 1.0), text=f"Context: {est_tokens:,} / 128k tokens"
    )

    with st.expander("Server Settings"):
        server_url = st.text_input("Server URL", value=DEFAULT_SERVER_URL)
        model_name = st.text_input("Model Name", value=DEFAULT_MODEL_NAME)
        st.info(
            "💡 **Multimodal Note:** To use Voice/Vision, you MUST start your server with the `--mmproj` flag pointing to the Gemma 4 multimodal projector file."
        )
        if st.button("🔌 Check Connection", use_container_width=True):
            try:
                temp_client = OpenAI(base_url=server_url, api_key="sk-no-key-required")
                models = temp_client.models.list()
                st.success(f"Connected! {len(models.data)} models found.")
            except Exception as e:
                st.error(str(e))

    st.divider()
    st.header("🧠 Reasoning Depth")
    reasoning_effort = st.select_slider(
        "Depth", options=["Quick", "Standard", "Deep Analysis"], value="Standard"
    )

    st.divider()
    st.header("📂 Upload Data")
    uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])

    # Fast Context Toggle
    use_fast_context = st.sidebar.checkbox(
        "⚡ Fast Context (Recommended)",
        value=True,
        help="Only sends the first 100 rows to speed up model processing.",
    )

    if uploaded_file:
        if uploaded_file.name.endswith(".xlsx"):
            xls = pd.ExcelFile(uploaded_file)
            selected_sheet = st.selectbox("Sheet:", options=xls.sheet_names)
        else:
            selected_sheet = "CSV_Data"

        if (
            st.session_state.df is None
            or st.session_state.current_sheet != selected_sheet
        ):
            try:
                with st.spinner("Loading..."):
                    df = (
                        pd.read_csv(uploaded_file)
                        if uploaded_file.name.endswith(".csv")
                        else pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                    )
                    for col in df.columns:
                        if df[col].dtype == "object":
                            df[col] = df[col].astype(str)
                    (
                        st.session_state.df,
                        st.session_state.current_sheet,
                        st.session_state.messages,
                    ) = (df, selected_sheet, [])

                    data_info = f"Dataset: {uploaded_file.name}\nRows: {len(df)} | Cols: {len(df.columns)}\n\nSchema:\n"
                    for col, dtype in df.dtypes.items():
                        data_info += f"- {col}: {dtype}\n"

                    num_cols = df.select_dtypes(include=["number"])
                    if not num_cols.empty:
                        data_info += (
                            "\nStats:\n"
                            + pd.concat(
                                [
                                    num_cols.describe(),
                                    pd.DataFrame(num_cols.sum()).T.set_index(
                                        pd.Index(["sum"])
                                    ),
                                ]
                            ).to_markdown()
                            + "\n"
                        )

                    st.session_state.data_context = (
                        data_info
                        + f"\nData Preview ({'Top 100' if use_fast_context else 'Top 2000'} rows):\n"
                        + df.head(100 if use_fast_context else 2000).to_markdown(
                            index=False
                        )
                    )
                st.success("Data Loaded!")
            except Exception as e:
                st.error(str(e))

    if st.session_state.df is not None:
        st.divider()
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        if st.button("❌ Reset All", type="primary", use_container_width=True):
            st.session_state.df = None
            st.session_state.data_context = ""
            st.rerun()

    st.divider()
    st.markdown(
        f"""<div style='text-align: center; padding: 10px; border-top: 1px solid {c["border"]};'>
        <p style='font-size: 0.8rem; color: {c["sub_text"]};'>Developed by</p>
        <p style='font-weight: bold; color: {c["primary"]}; margin-top: -10px;'>Mahamed Algaroshy</p>
        <p style='font-size: 0.75rem; color: {c["sub_text"]}; line-height: 1.2;'>Electrical Engineer & AI Enthusiast</p>
    </div>""",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# MAIN APP BODY
# ---------------------------------------------------------
if st.session_state.df is None:
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown(f'<h1 class="main-header">Gemma Frontier</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">The Future of Private, Local Data Intelligence.</p>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="step-card"><h3>{get_icon_svg("settings", 24, c["primary"])} 1. Connect</h3><p>Ensure llama-server is active on port 8080.</p></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="step-card"><h3>{get_icon_svg("upload", 24, c["primary"])} 2. Ingest</h3><p>Upload files or choose a demo dataset below.</p></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="step-card"><h3>{get_icon_svg("sparkles", 24, c["primary"])} 3. Unleash</h3><p>Chat, visualize, and analyze with multi-modal AI.</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br><h3>🚀 Quick-Start Demos</h3>", unsafe_allow_html=True)
    demo_cols = st.columns(len(DEMO_DATASETS))
    for i, (name, data) in enumerate(DEMO_DATASETS.items()):
        if demo_cols[i].button(f"Load {name}", use_container_width=True):
            st.session_state.df = pd.read_csv(io.StringIO(data))
            st.session_state.current_sheet = name
            st.session_state.data_context = (
                f"Demo: {name}\n" + st.session_state.df.to_markdown()
            )
            st.rerun()

    st.markdown("<br><h3>💡 Pro Tips for Showcase</h3>", unsafe_allow_html=True)
    st.markdown(
        f"""
    <div class="feature-tip"><b>🗣️ Voice Analysis:</b> Click the mic and say "Which department has the highest performance?"</div>
    <div class="feature-tip"><b>🎨 Agentic Visuals:</b> Ask "Draw a correlation heatmap of numeric columns" and watch code execute.</div>
    <div class="feature-tip"><b>👁️ Vision context:</b> Upload a screenshot of an external chart and ask "Compare this image with my data".</div>
    <div class="feature-tip"><b>🧮 Precise Math:</b> Ask for complex budget impacts; Gemma uses pre-calculated Pandas stats for 100% accuracy.</div>
    <div class="feature-tip"><b>📊 Sentiment Analysis:</b> (Load Feedback) Ask "What is the general sentiment of these comments?"</div>
    <div class="feature-tip"><b>📉 Predictive Insights:</b> Ask "Based on current task speeds, when will the project be finished?"</div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(
        f'<h1 class="main-header">📊 Data Workspace</h1>', unsafe_allow_html=True
    )
    st.markdown(
        f'<p class="sub-header">Working on <b>{st.session_state.current_sheet}</b></p>',
        unsafe_allow_html=True,
    )

    with st.expander(f"🔍 Preview Data & Export"):
        c1, c2, c3 = st.columns([1, 1, 1])
        c1.metric("Rows", len(st.session_state.df))
        c2.metric("Cols", len(st.session_state.df.columns))
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            st.session_state.df.to_excel(writer, index=False)
        c3.download_button(
            label="💾 Export Excel",
            data=buffer.getvalue(),
            file_name=f"gemma_transformed.xlsx",
            use_container_width=True,
        )
        st.dataframe(st.session_state.df.head(100), use_container_width=True)

    st.divider()
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "thought" in message and message["thought"]:
                with st.expander("🤔 View AI Reasoning"):
                    st.markdown(message["thought"])

            st.markdown(message["content"])

            # Show PERSISTED tool results (charts, code, etc.)
            if "tool_results" in message:
                for res in message["tool_results"]:
                    if res.get("code"):
                        with st.expander("📝 View Generated Code", expanded=False):
                            st.code(res["code"], language="python")
                    if res.get("plot"):
                        st.image(base64.b64decode(res["plot"]))
                    if res.get("output") and res["output"] != "Executed successfully.":
                        st.info(res["output"])
                    if res.get("df_preview") is not None:
                        st.markdown("### 📋 Result Table")
                        st.dataframe(
                            pd.read_json(res["df_preview"]), use_container_width=True
                        )

    input_col, mic_col = st.columns([0.9, 0.1])
    with input_col:
        prompt = st.chat_input("Ask about your data...")
    with mic_col:
        audio_bytes = st.audio_input("🎙️", label_visibility="collapsed")
    uploaded_image = st.file_uploader(
        "🖼️ Add context image", type=["png", "jpg", "jpeg"]
    )

    # Check if this is a new image using hash
    image_is_new = False
    if uploaded_image:
        image_content = uploaded_image.getvalue()
        image_hash = hashlib.md5(image_content).hexdigest()
        if image_hash != st.session_state.get("last_image_hash"):
            image_is_new = True
            st.session_state.last_image_hash = image_hash
            # Reset file uploader position so we can read it again later
            uploaded_image.seek(0)

    # Handle Audio: Transcribe locally using SpeechRecognition
    transcribed_text = None
    if audio_bytes:
        import speech_recognition as sr
        import tempfile

        audio_content = audio_bytes.getvalue()
        audio_hash = hashlib.md5(audio_content).hexdigest()

        if audio_hash != st.session_state.get("last_audio_hash"):
            st.session_state.last_audio_hash = audio_hash

            # Save audio to temp WAV file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_content)
                tmp_path = tmp.name

            try:
                recognizer = sr.Recognizer()
                with sr.AudioFile(tmp_path) as source:
                    audio_data = recognizer.record(source)
                transcribed_text = recognizer.recognize_google(audio_data)
                st.success(f'🎤 Transcribed: "{transcribed_text}"')
            except sr.UnknownValueError:
                st.warning("🎤 Could not understand audio. Please try again.")
            except sr.RequestError as e:
                st.error(f"🎤 Speech service error: {e}")
            except Exception as e:
                st.error(f"🎤 Error: {str(e)}")
            finally:
                import os

                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

    if prompt or transcribed_text or (uploaded_image and image_is_new):
        st.session_state.last_tool_df = None
        user_content = []
        # Use transcribed text if available, otherwise use typed prompt
        active_prompt = (
            transcribed_text if transcribed_text else (prompt if prompt else "")
        )
        display_prompt = active_prompt
        if transcribed_text:
            display_prompt = f"🎤 {transcribed_text}"

        # Image MUST come before text per Gemma 4 multimodal spec
        if uploaded_image and image_is_new:
            display_prompt = f"🖼️ [Image: {uploaded_image.name}]" + (
                f"\n{display_prompt}" if display_prompt else ""
            )
            # Reset position before reading
            uploaded_image.seek(0)
            b64_img = base64.b64encode(uploaded_image.read()).decode("utf-8")
            user_content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{b64_img}"},
                }
            )

        if active_prompt:
            user_content.append({"type": "text", "text": active_prompt})

        if not active_prompt:
            user_content.append({"type": "text", "text": "Analyze media."})

        st.session_state.messages.append(
            {"role": "user", "content": display_prompt, "api_content": user_content}
        )
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            thought_container, answer_placeholder = st.empty(), st.empty()
            answer_placeholder.markdown(
                '<div class="skeleton"></div><div class="skeleton" style="width:70%"></div>',
                unsafe_allow_html=True,
            )

            api_messages = [
                {
                    "role": "system",
                    "content": f"<|think|>\nYou are an expert data analyst. Use tool calls for charts. Data Context:\n{st.session_state.data_context}",
                }
            ]
            for m in st.session_state.messages:
                api_messages.append(
                    {"role": m["role"], "content": m.get("api_content", m["content"])}
                )

            try:
                temp = {"Quick": 0.3, "Standard": 0.6, "Deep Analysis": 0.9}[
                    reasoning_effort
                ]
                stream = client.chat.completions.create(
                    model=model_name,
                    messages=api_messages,
                    tools=tools_schema,
                    tool_choice="auto",
                    stream=True,
                    temperature=temp,
                )
                (
                    is_thinking,
                    thought_content,
                    final_content,
                    tool_calls,
                    thought_expander,
                ) = (False, "", "", {}, None)

                for chunk in stream:
                    delta = chunk.choices[0].delta
                    if delta.tool_calls:
                        for tc in delta.tool_calls:
                            if tc.index not in tool_calls:
                                tool_calls[tc.index] = {
                                    "id": tc.id,
                                    "function": {
                                        "name": tc.function.name,
                                        "arguments": "",
                                    },
                                }
                            if tc.function.arguments:
                                tool_calls[tc.index]["function"]["arguments"] += (
                                    tc.function.arguments
                                )
                        continue
                    if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                        if not thought_expander:
                            thought_expander = thought_container.expander(
                                "🤔 View AI Reasoning", expanded=True
                            )
                            thought_placeholder = thought_expander.empty()
                        thought_content += delta.reasoning_content
                        thought_placeholder.markdown(thought_content + "▌")
                        continue
                    if delta.content:
                        if "<think>" in delta.content:
                            is_thinking = True
                        if "</think>" in delta.content:
                            is_thinking = False
                            continue
                        if is_thinking:
                            if not thought_expander:
                                thought_expander = thought_container.expander(
                                    "🤔 View AI Reasoning", expanded=True
                                )
                                thought_placeholder = thought_expander.empty()
                            thought_content += delta.content
                            thought_placeholder.markdown(thought_content + "▌")
                        else:
                            final_content += delta.content
                            answer_placeholder.markdown(final_content + "▌")

                answer_placeholder.markdown(final_content)

                turn_tool_results = []
                if tool_calls:
                    for tc in tool_calls.values():
                        st.info("⚙️ Calling Tool...")
                        raw_args = tc["function"]["arguments"]
                        # Extract valid JSON object from potentially malformed output
                        match = re.search(r"\{.*\}", raw_args, re.DOTALL)
                        if match:
                            args = json.loads(match.group(0))
                        else:
                            args = json.loads(raw_args)
                        code = (
                            args.get("code_string", "")
                            .replace(" plt.", "\nplt.")
                            .replace(" sns.", "\nsns.")
                        )
                        st.code(code, language="python")

                        # Execute and capture results
                        res = execute_python_code(code)

                        # Prepare for persistence
                        tool_res_entry = {
                            "code": code,
                            "output": res.get("output"),
                            "plot": res.get("plot"),
                        }
                        if st.session_state.last_tool_df is not None:
                            # Save a small preview of the dataframe if one was created/modified
                            tool_res_entry["df_preview"] = (
                                st.session_state.last_tool_df.head(20).to_json()
                            )
                            st.markdown("### 📋 Result Preview")
                            st.dataframe(st.session_state.last_tool_df.head(10))

                        turn_tool_results.append(tool_res_entry)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": final_content,
                        "thought": thought_content,
                        "tool_results": turn_tool_results,
                    }
                )
                st.rerun()
            except Exception as e:
                error_str = str(e)
                if "audio input is not supported" in error_str or "mmproj" in error_str:
                    st.error(
                        "🚨 **Multimodal Error**: The server rejected your audio/image input."
                    )
                    st.warning(
                        "To fix this, you must restart your `llama-server` with the `--mmproj` flag. Example:\n`llama-server -m model.gguf --mmproj projector.gguf`"
                    )
                else:
                    st.error(f"Server Error: {error_str}")
