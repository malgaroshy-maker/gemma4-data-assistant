import streamlit as st
import pandas as pd
from openai import OpenAI
import base64
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import json
import io
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.drawing.image import Image as OpenpyxlImage
import hashlib
import re
from translations import t

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
    captured_df = None
    try:
        import builtins
        import datetime, numpy, json, re, math

        safe_builtins = {
            k: v
            for k, v in builtins.__dict__.items()
            if k
            not in {
                "exec", "eval", "compile", "breakpoint",
                "exit", "quit", "input", "__import__",
            }
        }
        exec_globals = {
            "df": st.session_state.df,
            "pd": pd,
            "plt": plt,
            "sns": sns,
            "openpyxl": openpyxl,
            "datetime": datetime,
            "numpy": numpy,
            "np": numpy,
            "json": json,
            "re": re,
            "math": math,
            "dataframe_to_rows": dataframe_to_rows,
            "Image": OpenpyxlImage,
            "__builtins__": safe_builtins,
        }
        ar_ok = st.session_state.get("language") == "ar" and _ensure_arabic_matplotlib()
        if ar_ok:
            import arabic_reshaper
            from bidi.algorithm import get_display

            exec_globals["arabic_text"] = lambda text: get_display(
                arabic_reshaper.reshape(text)
            )
        from io import StringIO, BytesIO, IOBase
        import sys

        exec_globals["BytesIO"] = BytesIO
        exec_globals["StringIO"] = StringIO

        # Strip plt.show() — blocks in non-interactive (Agg) backend
        code_string = re.sub(r"plt\.show\(\s*\)", "", code_string)

        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()

        # Wrap print to capture DataFrame outputs
        original_print = print

        def wrapped_print(*args, **kwargs):
            nonlocal captured_df
            for arg in args:
                if isinstance(arg, pd.DataFrame):
                    captured_df = arg
            original_print(*args, **kwargs)

        exec_globals["print"] = wrapped_print

        # Execute the code
        try:
            exec(code_string, exec_globals)
        except (IndentationError, SyntaxError) as e:
            # Try to fix common indentation/syntax issues from AI-generated code
            lines = code_string.split("\n")
            fixed_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                fixed_lines.append(line)
                # If line ends with colon, ensure next non-blank line is properly indented
                if line.rstrip().endswith(":") and i + 1 < len(lines):
                    # Find the next non-blank line
                    j = i + 1
                    while j < len(lines) and lines[j].strip() == "":
                        j += 1
                    if j < len(lines):
                        next_nonblank = lines[j]
                        current_indent = len(line) - len(line.lstrip())
                        next_indent = len(next_nonblank) - len(next_nonblank.lstrip())
                        # If next non-blank line has same or less indent, insert pass
                        if next_indent <= current_indent:
                            indent = " " * (current_indent + 4)
                            fixed_lines.append(f"{indent}pass")
                    # Copy any blank lines between colon and next code
                    for k in range(i + 1, j if j < len(lines) else len(lines)):
                        fixed_lines.append(lines[k])
                i += 1
            code_string = "\n".join(fixed_lines)
            exec(code_string, exec_globals)

        # Capture text output
        output = redirected_output.getvalue().strip()
        sys.stdout = old_stdout

        # Check for plots — save each figure individually
        if plt.get_fignums():
            ar_ok = (
                st.session_state.get("language") == "ar" and _ensure_arabic_matplotlib()
            )
            fignums = list(plt.get_fignums())
            plot_b64_list = []
            for fig_num in fignums:
                figure = plt.figure(fig_num)
                if ar_ok:
                    figure.canvas.draw()
                    _process_figure_text(figure)
                    figure.canvas.draw()
                buf = BytesIO()
                plt.savefig(fig_num, format="png", bbox_inches="tight", dpi=100)
                buf.seek(0)
                plot_b64_list.append(base64.b64encode(buf.read()).decode("utf-8"))
            plt.close("all")
            plot_b64 = plot_b64_list[-1] if plot_b64_list else None

        # Detect Excel workbook created during execution (scan for xlsx ZIP magic bytes)
        excel_b64 = None
        for name, val in exec_globals.items():
            if isinstance(val, BytesIO):
                try:
                    val.seek(0)
                    if val.read(2) == b"PK":  # xlsx file signature (ZIP container)
                        val.seek(0)
                        excel_b64 = base64.b64encode(val.read()).decode("utf-8")
                        break
                except Exception:
                    pass

        # Detect any DataFrame created or modified during execution
        if "result_df" in exec_globals and isinstance(
            exec_globals["result_df"], pd.DataFrame
        ):
            st.session_state.last_tool_df = exec_globals["result_df"]
        elif captured_df is not None:
            st.session_state.last_tool_df = captured_df
        else:
            # Scan exec_globals for any new DataFrame
            skip = {
                "df",
                "pd",
                "plt",
                "sns",
                "openpyxl",
                "excel_bytes",
                "StringIO",
                "BytesIO",
                "IOBase",
                "sys",
                "old_stdout",
                "redirected_output",
                "print",
                "original_print",
                "wrapped_print",
            }
            for name, val in exec_globals.items():
                if name in skip:
                    continue
                if isinstance(val, pd.DataFrame):
                    st.session_state.last_tool_df = val
                    break

        return {
            "status": "success",
            "output": output or "Executed successfully.",
            "plot": plot_b64,
            "excel": excel_b64,
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
            "description": "Executes Python code to analyze 'df', draw charts, perform calculations, or generate Excel reports. CRITICAL: All modules are already pre-imported in the sandbox — NEVER write 'import' or 'from' statements. Pre-imported: df, pd, plt, sns, openpyxl, dataframe_to_rows, Image, datetime, numpy (as np), json, re, math, BytesIO, StringIO. For Excel reports: use openpyxl + dataframe_to_rows + Image. Save Excel to BytesIO named 'excel_bytes'. Example: 'wb = openpyxl.Workbook(); ws = wb.active; ws.title = \"Summary\"; for r in dataframe_to_rows(df, index=False, header=True): ws.append(r); excel_bytes = BytesIO(); wb.save(excel_bytes)'",
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
if "pending_image_b64" not in st.session_state:
    st.session_state.pending_image_b64 = None
if "pending_image_name" not in st.session_state:
    st.session_state.pending_image_name = None
if "language" not in st.session_state:
    st.session_state.language = "en"
if "arabic_initialized" not in st.session_state:
    st.session_state.arabic_initialized = False

# Initialize OpenAI client once (avoids recreation on every rerun)
DEFAULT_SERVER_URL = os.environ.get("SERVER_URL", "http://localhost:8080/v1")
DEFAULT_MODEL_NAME = os.environ.get("MODEL_NAME", "unsloth/gemma-4-e4b-it-gguf:Q4_K_XL")
client = OpenAI(base_url=DEFAULT_SERVER_URL, api_key="sk-no-key-required")

# ---------------------------------------------------------
# LANGUAGE & RTL
# ---------------------------------------------------------
lang = st.session_state.language
is_rtl = lang == "ar"


def _ensure_arabic_matplotlib():
    """Lazy-init Arabic matplotlib support on first Arabic request."""
    if st.session_state.arabic_initialized:
        return True
    if not is_rtl:
        return False

    try:
        import arabic_reshaper
        from bidi.algorithm import get_display

        has_support = True
    except ImportError:
        st.session_state.arabic_initialized = True
        return False

    # Search for Noto Sans Arabic dynamically (no hardcoded paths)
    import glob

    noto_paths = []
    user_font_dirs = [
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Microsoft\Windows\Fonts"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts"),
        os.path.expandvars(r"%WINDIR%\Fonts"),
    ]
    for d in user_font_dirs:
        if os.path.isdir(d):
            noto_paths.extend(glob.glob(os.path.join(d, "*NotoSansArabic*.ttf")))
            noto_paths.extend(glob.glob(os.path.join(d, "*NotoSansArabic*.otf")))

    font_found = False
    for font_path in noto_paths:
        if os.path.isfile(font_path):
            try:
                fm.fontManager.addfont(font_path)
                prop = fm.FontProperties(fname=font_path)
                family_name = prop.get_name()
                plt.rcParams["font.family"] = family_name
                plt.rcParams["font.sans-serif"] = [family_name] + plt.rcParams.get(
                    "font.sans-serif", []
                )
                font_found = True
                break
            except Exception:
                continue

    if not font_found:
        arabic_fonts = ["Arial", "Tahoma", "Segoe UI", "Times New Roman"]
        for font_name in arabic_fonts:
            try:
                font_path = fm.findfont(fm.FontProperties(family=font_name))
                if "DejaVu" not in font_path:
                    plt.rcParams["font.family"] = font_name
                    plt.rcParams["font.sans-serif"] = [font_name] + plt.rcParams.get(
                        "font.sans-serif", []
                    )
                    font_found = True
                    break
            except Exception:
                continue

    if not font_found:
        plt.rcParams["font.family"] = "sans-serif"

    st.session_state.arabic_initialized = True
    return has_support


def _reshape_arabic(text):
    """Reshape and reorder Arabic text for matplotlib rendering."""
    if not isinstance(text, str):
        return text
    has_arabic = any(
        "\u0600" <= c <= "\u06ff" or "\u0750" <= c <= "\u077f" for c in text
    )
    if not has_arabic:
        return text
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display

        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text


def _process_figure_text(figure):
    """Process ALL text elements in a matplotlib figure for Arabic."""
    for ax in figure.get_axes():
        title = ax.get_title()
        if title:
            ax.set_title(_reshape_arabic(title))
        xlabel = ax.get_xlabel()
        if xlabel:
            ax.set_xlabel(_reshape_arabic(xlabel))
        ylabel = ax.get_ylabel()
        if ylabel:
            ax.set_ylabel(_reshape_arabic(ylabel))
        for tick in ax.get_xticklabels():
            txt = tick.get_text()
            if txt:
                tick.set_text(_reshape_arabic(txt))
        for tick in ax.get_yticklabels():
            txt = tick.get_text()
            if txt:
                tick.set_text(_reshape_arabic(txt))
        if ax.get_legend():
            for t in ax.get_legend().get_texts():
                txt = t.get_text()
                if txt:
                    t.set_text(_reshape_arabic(txt))
        for t in list(ax.texts):
            txt = t.get_text()
            if txt:
                t.set_text(_reshape_arabic(txt))
        for child in list(ax.get_children()):
            if hasattr(child, "get_text") and hasattr(child, "set_text"):
                txt = child.get_text()
                if txt and any("\u0600" <= c <= "\u06ff" for c in txt):
                    child.set_text(_reshape_arabic(txt))
    for t in list(figure.texts):
        txt = t.get_text()
        if txt:
            t.set_text(_reshape_arabic(txt))
    suptitle = figure._suptitle
    if suptitle:
        txt = suptitle.get_text()
        if txt:
            suptitle.set_text(_reshape_arabic(txt))


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

rtl_css = (
    """
    /* RTL: Root direction */
    .stApp { direction: rtl !important; }

    /* RTL: Sidebar */
    [data-testid="stSidebar"] { direction: rtl !important; text-align: right !important; border-right: none !important; border-left: 1px solid #334155 !important; }
    [data-testid="stSidebar"] .stMarkdown p { text-align: right !important; }
    [data-testid="stSidebar"] label { text-align: right !important; }

    /* RTL: Chat messages */
    .stChatMessage { direction: rtl !important; text-align: right !important; }
    [data-testid="stChatMessageContent"] { direction: rtl !important; text-align: right !important; }
    [data-testid="stChatMessageContent"] p { direction: rtl !important; text-align: right !important; }

    /* RTL: Headers */
    .main-header, .sub-header { direction: rtl !important; text-align: right !important; }

    /* RTL: Step cards */
    .step-card { direction: rtl !important; text-align: right !important; }
    .step-card h3 { text-align: right !important; }

    /* RTL: Feature tips */
    .feature-tip { direction: rtl !important; text-align: right !important; border-left: none !important; border-right: 4px solid #60A5FA !important; }
    .feature-tip b { text-align: right !important; }

    /* RTL: Tables */
    .stMarkdown table { direction: rtl !important; text-align: right !important; }
    .stMarkdown table th, .stMarkdown table td { text-align: right !important; }

    /* RTL: Form elements */
    [data-baseweb="select"] { direction: rtl !important; }
    .stTextInput > div { direction: rtl !important; }
    .stTextArea > div { direction: rtl !important; }
    [role="textbox"] { direction: rtl !important; text-align: right !important; }

    /* RTL: Metrics */
    [data-testid="stMetric"] { direction: rtl !important; text-align: right !important; }
    [data-testid="stMetricValue"] { text-align: right !important; }
    [data-testid="stMetricLabel"] { text-align: right !important; }

    /* RTL: Expanders */
    .streamlit-expanderHeader { direction: rtl !important; text-align: right !important; }

    /* RTL: Columns and flex containers */
    [data-testid="column"] > div { direction: rtl !important; text-align: right !important; }
    div[data-testid="stHorizontalBlock"] > div { direction: rtl !important; }

    /* RTL: Download button */
    .stDownloadButton { direction: rtl !important; }

    /* RTL: Info/warning/error alerts */
    [data-testid="stAlertContainer"] { direction: rtl !important; text-align: right !important; }

    /* RTL: Code blocks */
    .stCode { direction: ltr !important; text-align: left !important; }
    .stCode pre { direction: ltr !important; text-align: left !important; }
"""
    if is_rtl
    else ""
)

font_family = (
    "'Noto Sans Arabic', 'Segoe UI', system-ui, -apple-system, sans-serif"
    if is_rtl
    else "'Segoe UI', system-ui, -apple-system, sans-serif"
)

font_import = (
    """
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;500;600;700&display=swap');
"""
    if is_rtl
    else ""
)

st.markdown(
    f"""
<style>
    {font_import}
    .stApp {{ background-color: {c["bg"]}; color: {c["text"]} !important; font-family: {font_family}; }}
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
    {rtl_css}
</style>
""",
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    # Language selector at the top
    lang_options = {"en": "🇬🇧 English", "ar": "🇸🇦 العربية"}
    selected_lang = st.selectbox(
        t("language_label", lang=lang),
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=list(lang_options.keys()).index(lang),
        key="lang_selector",
    )
    if selected_lang != lang:
        st.session_state.language = selected_lang
        st.rerun()

    st.header(t("config_header", lang=lang))

    st.caption(t("context_window_caption", lang=lang))
    est_tokens = len(st.session_state.data_context) // 4
    ctx_tokens = st.session_state.get("current_ctx_tokens", est_tokens)
    total_est = est_tokens + ctx_tokens
    st.progress(
        min(total_est / 128000, 1.0),
        text=t("context_meter", lang=lang, est=f"{total_est:,}"),
    )
    if total_est > 96000:
        st.warning(f"⚠️ Context nearing limit ({total_est:,} / 128K tokens). Older messages will be dropped.")

    with st.expander(t("server_settings", lang=lang)):
        server_url = st.text_input(
            t("server_url_label", lang=lang), value=DEFAULT_SERVER_URL
        )
        model_name = st.text_input(
            t("model_name_label", lang=lang), value=DEFAULT_MODEL_NAME
        )
        st.markdown(t("multimodal_note", lang=lang))
        if st.button(t("check_connection", lang=lang), use_container_width=True):
            try:
                temp_client = OpenAI(base_url=server_url, api_key="sk-no-key-required")
                models = temp_client.models.list()
                st.success(t("connected", lang=lang, count=len(models.data)))
            except Exception as e:
                st.error(str(e))

    st.divider()
    st.header(t("reasoning_header", lang=lang))
    reasoning_options = {
        "en": {
            "Quick": "Quick",
            "Standard": "Standard",
            "Deep Analysis": "Deep Analysis",
        },
        "ar": {"Quick": "سريع", "Standard": "قياسي", "Deep Analysis": "تحليل عميق"},
    }
    reasoning_map = reasoning_options[lang]
    reasoning_display = st.select_slider(
        t("reasoning_depth", lang=lang),
        options=list(reasoning_map.keys()),
        format_func=lambda x: reasoning_map[x],
        value="Standard",
    )
    reasoning_effort = reasoning_display  # Keep English keys for code logic

    st.divider()
    st.header(t("upload_header", lang=lang))
    uploaded_file = st.file_uploader(
        t("file_uploader_label", lang=lang), type=["csv", "xlsx"]
    )

    # Fast Context Toggle
    use_fast_context = st.sidebar.checkbox(
        t("fast_context", lang=lang),
        value=True,
        help=t("fast_context_help", lang=lang),
    )

    if uploaded_file:
        if uploaded_file.name.endswith(".xlsx"):
            xls = pd.ExcelFile(uploaded_file)
            selected_sheet = st.selectbox(
                t("sheet_label", lang=lang), options=xls.sheet_names
            )
        else:
            selected_sheet = "CSV_Data"

        if (
            st.session_state.df is None
            or st.session_state.current_sheet != selected_sheet
        ):
            try:
                with st.spinner(t("loading", lang=lang)):
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
                st.success(t("data_loaded", lang=lang))
            except Exception as e:
                st.error(str(e))

    if st.session_state.df is not None:
        st.divider()
        if st.button(t("clear_chat", lang=lang), use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        if st.button(
            t("reset_all", lang=lang), type="primary", use_container_width=True
        ):
            st.session_state.df = None
            st.session_state.data_context = ""
            st.rerun()

    st.divider()
    st.markdown(
        f"""<div style='text-align: center; padding: 10px; border-top: 1px solid {c["border"]};'>
        <p style='font-size: 0.8rem; color: {c["sub_text"]};'>{t("developed_by", lang=lang)}</p>
        <p style='font-weight: bold; color: {c["primary"]}; margin-top: -10px;'>Mahamed Algaroshy</p>
        <p style='font-size: 0.75rem; color: {c["sub_text"]}; line-height: 1.2;'>{t("engineer_title", lang=lang)}</p>
    </div>""",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# MAIN APP BODY
# ---------------------------------------------------------
if st.session_state.df is None:
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown(
        f'<h1 class="main-header">{t("main_header", lang=lang)}</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p class="sub-header">{t("sub_header", lang=lang)}</p>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="step-card"><h3>{get_icon_svg("settings", 24, c["primary"])} {t("step1_title", lang=lang)}</h3><p>{t("step1_desc", lang=lang)}</p></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="step-card"><h3>{get_icon_svg("upload", 24, c["primary"])} {t("step2_title", lang=lang)}</h3><p>{t("step2_desc", lang=lang)}</p></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="step-card"><h3>{get_icon_svg("sparkles", 24, c["primary"])} {t("step3_title", lang=lang)}</h3><p>{t("step3_desc", lang=lang)}</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f"<br><h3>{t('quick_start_demos', lang=lang)}</h3>", unsafe_allow_html=True
    )
    demo_cols = st.columns(len(DEMO_DATASETS))
    for i, (name, data) in enumerate(DEMO_DATASETS.items()):
        if demo_cols[i].button(
            t("load_demo", lang=lang, name=name), use_container_width=True
        ):
            st.session_state.df = pd.read_csv(io.StringIO(data))
            st.session_state.current_sheet = name
            st.session_state.data_context = (
                f"Demo: {name}\n" + st.session_state.df.to_markdown()
            )
            st.rerun()

    st.markdown(f"<br><h3>{t('pro_tips', lang=lang)}</h3>", unsafe_allow_html=True)
    st.markdown(
        f"""
    <div class="feature-tip">{t("pro_tip_voice", lang=lang)}</div>
    <div class="feature-tip">{t("pro_tip_visuals", lang=lang)}</div>
    <div class="feature-tip">{t("pro_tip_vision", lang=lang)}</div>
    <div class="feature-tip">{t("pro_tip_math", lang=lang)}</div>
    <div class="feature-tip">{t("pro_tip_sentiment", lang=lang)}</div>
    <div class="feature-tip">{t("pro_tip_predictive", lang=lang)}</div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(
        f'<h1 class="main-header">{t("workspace_header", lang=lang)}</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p class="sub-header">{t("working_on", lang=lang)} <b>{st.session_state.current_sheet}</b></p>',
        unsafe_allow_html=True,
    )

    with st.expander(f"{t('preview_export', lang=lang)}"):
        c1, c2, c3 = st.columns([1, 1, 1])
        c1.metric(t("rows", lang=lang), len(st.session_state.df))
        c2.metric(t("cols", lang=lang), len(st.session_state.df.columns))
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            st.session_state.df.to_excel(writer, index=False)
        c3.download_button(
            label=t("export_excel", lang=lang),
            data=buffer.getvalue(),
            file_name=f"gemma_transformed.xlsx",
            use_container_width=True,
        )
        st.dataframe(st.session_state.df.head(100), use_container_width=True)

    st.divider()
    for midx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if "thought" in message and message["thought"]:
                with st.expander(t("view_reasoning", lang=lang)):
                    st.markdown(message["thought"])

            st.markdown(message["content"])

            # Show PERSISTED tool results (charts, code, etc.)
            if "tool_results" in message:
                for ridx, res in enumerate(message["tool_results"]):
                    if res.get("code"):
                        with st.expander(t("view_code", lang=lang), expanded=False):
                            st.code(res["code"], language="python")
                    if res.get("error"):
                        st.error(f"❌ Code execution error: {res['error']}")
                    if res.get("plot"):
                        st.image(base64.b64decode(res["plot"]))
                    if res.get("output") and res["output"] != t(
                        "executed_successfully", lang=lang
                    ):
                        st.info(res["output"])
                    if res.get("df_preview") is not None:
                        st.markdown(f"### {t('result_table', lang=lang)}")
                        st.dataframe(
                            pd.read_json(StringIO(res["df_preview"])), use_container_width=True
                        )
                    if res.get("excel"):
                        st.download_button(
                            label="📥 Download Excel Report",
                            data=base64.b64decode(res["excel"]),
                            file_name="gemma_report.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"dl_excel_{midx}_{ridx}",
                        )

    # Chat input row with integrated mic
    st.markdown(
        f"""
        <style>
        .voice-row {{
            display: flex;
            align-items: flex-end;
            gap: 6px;
            margin-bottom: 8px;
        }}
        .voice-row .chat-col {{
            flex: 1;
        }}
        .voice-row .mic-col {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2px;
        }}
        div[data-testid="stAudioInput"] {{
            margin: 0 !important;
            padding: 0 !important;
        }}
        div[data-testid="stAudioInput"] > div {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
        div[data-testid="stAudioInput"] button {{
            background: linear-gradient(135deg, #60A5FA, #3B82F6) !important;
            border: none !important;
            border-radius: 50% !important;
            width: 42px !important;
            height: 42px !important;
            min-width: 42px !important;
            padding: 0 !important;
            font-size: 1.2rem !important;
            box-shadow: 0 2px 8px rgba(96, 165, 250, 0.3) !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
        }}
        div[data-testid="stAudioInput"] button:hover {{
            box-shadow: 0 4px 16px rgba(96, 165, 250, 0.5) !important;
            transform: scale(1.08) !important;
        }}
        div[data-testid="stAudioInput"] button:active {{
            transform: scale(0.92) !important;
        }}
        .mic-label {{
            font-size: 0.65rem;
            color: #64748B;
            cursor: help;
            text-align: center;
            white-space: nowrap;
        }}
        </style>
        <div class="voice-row">
            <div class="chat-col"></div>
            <div class="mic-col">
                <span class="mic-label" title="{t("voice_requires_internet_help", lang=lang)}">🎙️ Voice</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    chat_col, mic_col = st.columns([0.92, 0.08])
    with chat_col:
        prompt = st.chat_input(t("chat_input", lang=lang))
    with mic_col:
        audio_bytes = st.audio_input(t("record_audio", lang=lang), label_visibility="collapsed")
    uploaded_image = st.file_uploader(
        t("image_uploader", lang=lang), type=["png", "jpg", "jpeg"]
    )

    # Check if this is a new image using hash — persist in session state
    image_is_new = False
    if uploaded_image:
        image_content = uploaded_image.getvalue()
        image_hash = hashlib.md5(image_content).hexdigest()
        if image_hash != st.session_state.get("last_image_hash"):
            image_is_new = True
            st.session_state.last_image_hash = image_hash
            uploaded_image.seek(0)
            st.session_state.pending_image_b64 = base64.b64encode(image_content).decode(
                "utf-8"
            )
            st.session_state.pending_image_name = uploaded_image.name

    # Handle Audio: Transcribe using native Gemma 4 ASR via llama-server
    # Stores transcribed text in session state — only sends when user clicks Send
    transcribed_text = None
    audio_ready_to_send = False
    if audio_bytes:
        import io

        audio_content = audio_bytes.getvalue()
        audio_hash = hashlib.md5(audio_content).hexdigest()

        if audio_hash != st.session_state.get("last_audio_hash"):
            st.session_state.last_audio_hash = audio_hash
            st.session_state.pending_audio_text = None

            try:
                asr_lang_name = {"en": "English", "ar": "Arabic"}.get(lang, "English")
                asr_prompt = (
                    f"Transcribe the following speech segment in {asr_lang_name} into {asr_lang_name} text.\n\n"
                    "Follow these specific instructions for formatting the answer:\n"
                    "* Only output the transcription, with no newlines.\n"
                    "* When transcribing numbers, write the digits, i.e. write 1.7 and not one point seven, and write 3 instead of three."
                )
                response = client.audio.transcriptions.create(
                    model="gemma4",
                    file=("audio.wav", io.BytesIO(audio_content), "audio/wav"),
                    language=lang,
                    prompt=asr_prompt,
                    response_format="json",
                )
                transcribed = response.text.strip()
                if transcribed:
                    st.session_state.pending_audio_text = transcribed
                    st.success(t("transcribed", lang=lang, text=transcribed))
                else:
                    st.warning(t("could_not_understand", lang=lang))
                    st.session_state.pending_audio_text = None
            except Exception as e:
                error_str = str(e)
                if "mmproj" in error_str.lower() or "audio input is not supported" in error_str.lower():
                    st.error(t("multimodal_error", lang=lang))
                    st.warning(t("multimodal_fix", lang=lang))
                elif "connect" in error_str.lower() or "timed out" in error_str.lower():
                    st.error(t("server_offline", lang=lang))
                else:
                    st.error(t("audio_error", lang=lang, error=error_str))
                st.session_state.pending_audio_text = None
        elif st.session_state.get("pending_audio_text"):
            transcribed_text = st.session_state.pending_audio_text

    # Show transcribed text with Send button if available
    if st.session_state.get("pending_audio_text") and not prompt:
        col_preview, col_send = st.columns([0.85, 0.15])
        with col_preview:
            st.info(f'🎤 "{st.session_state.pending_audio_text}"')
        with col_send:
            if st.button("▶️ " + t("send", lang=lang), key="send_audio_btn"):
                audio_ready_to_send = True
                st.session_state.pending_audio_text = None

    # Only trigger AI on explicit user action
    if prompt or audio_ready_to_send:
        st.session_state.last_tool_df = None
        user_content = []
        active_prompt = prompt if prompt else (transcribed_text or "")
        display_prompt = active_prompt
        if transcribed_text and not prompt:
            display_prompt = f"🎤 {transcribed_text}"

        # Image MUST come before text per Gemma 4 multimodal spec
        pending_b64 = st.session_state.get("pending_image_b64")
        pending_name = st.session_state.get("pending_image_name")
        if pending_b64:
            display_prompt = f"🖼️ [{t('image_prefix', lang=lang)}: {pending_name}]" + (
                f"\n{display_prompt}" if display_prompt else ""
            )
            user_content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{pending_b64}"},
                }
            )
            # Clear pending image after attaching
            st.session_state.pending_image_b64 = None
            st.session_state.pending_image_name = None

        if active_prompt:
            user_content.append({"type": "text", "text": active_prompt})

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

            # Language-aware system prompt
            lang_instruction = (
                "\nYou MUST respond in Arabic (العربية). Use Arabic for all explanations, labels, and responses."
                if lang == "ar"
                else ""
            )
            api_messages = [
                {
                    "role": "system",
                    "content": (
                        f"<|think|>\n"
                        f"You are an expert data analyst with access to a Python execution tool. Your job is to answer questions about the user's data.\n\n"
                        f"USE THE TOOL (execute_python_code) when the user asks for: charts, visualizations, tables, statistical summaries, filtering, grouping, calculations, or Excel reports (.xlsx). "
                        f"For conversational or knowledge questions, answer in plain text — do not generate code.\n\n"
                        f"CODE RULES:\n"
                        f"- All needed modules are pre-imported (pd, plt, sns, openpyxl, datetime, numpy as np, json, re, math, dataframe_to_rows, Image, BytesIO, StringIO). Do NOT write import statements.\n"
                        f"- Keep code under 50 lines unless building an Excel report\n"
                        f"- Handle edge cases: check for empty DataFrames, missing columns, division by zero (use try/except or .get())\n"
                        f"- Format numbers: use f\"{{value:,.0f}}\" for currency or df.round(2) for decimals\n"
                        f"- Chart titles and axis labels must be descriptive\n"
                        f"- Use f-strings, not string concatenation\n"
                        f"- NEVER call plt.show() — it is stripped automatically\n\n"
                        f"EXCEL REPORTS: When asked to create an Excel file:\n"
                        f"- Create an openpyxl Workbook, add sheets, embed charts via openpyxl.drawing.image.Image\n"
                        f"- Use dataframe_to_rows() to write DataFrames to sheets\n"
                        f"- Save the final BytesIO to variable 'excel_bytes' — the file will appear as a download automatically\n"
                        f"- ws.append() requires a LIST: ws.append(['text']) not ws.append('text')\n\n"
                        f"ERRORS: If a tool call fails, briefly explain why and offer to fix it. If data is empty or a column is missing, tell the user.\n\n"
                        f"Data Context:\n{st.session_state.data_context}{lang_instruction}"
                    ),
                }
            ]
            for m in st.session_state.messages:
                api_messages.append(
                    {"role": m["role"], "content": m.get("api_content", m["content"])}
                )

            # Context window management: prevent silent failures from overflow
            MAX_CTX_TOKENS = 96000  # Safe headroom under 128K
            total_tokens = sum(len(json.dumps(m)) // 4 for m in api_messages)
            while total_tokens > MAX_CTX_TOKENS and len(api_messages) > 3:
                # Drop oldest user/assistant pair (keep system message)
                if api_messages[1]["role"] == "user":
                    del api_messages[1:3]
                else:
                    del api_messages[1:2]
                total_tokens = sum(len(json.dumps(m)) // 4 for m in api_messages)
            # Final safety: if still over limit with only system + 1 message, truncate system
            if total_tokens > MAX_CTX_TOKENS and len(api_messages) > 1:
                api_messages[0]["content"] = api_messages[0]["content"][:MAX_CTX_TOKENS * 2]
            st.session_state.current_ctx_tokens = total_tokens

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
                                t("view_reasoning", lang=lang), expanded=True
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
                            parts = delta.content.split("</think>", 1)
                            if len(parts) > 1 and parts[1].strip():
                                delta.content = parts[1]
                            else:
                                continue
                        if is_thinking:
                            if not thought_expander:
                                thought_expander = thought_container.expander(
                                    t("view_reasoning", lang=lang), expanded=True
                                )
                                thought_placeholder = thought_expander.empty()
                            thought_content += delta.content
                            thought_placeholder.markdown(thought_content + "▌")
                        else:
                            final_content += delta.content
                            answer_placeholder.markdown(final_content + "▌")

                answer_placeholder.markdown(final_content)

                turn_tool_results = []

                # Fallback: If model outputs code as text (not via tool calls), extract and execute it
                code_block_pattern = re.compile(r"```python\s*\n(.*?)\n```", re.DOTALL)
                text_code_blocks = code_block_pattern.findall(final_content)
                if text_code_blocks and not tool_calls:
                    for block in text_code_blocks:
                        code = block.strip()
                        if code:
                            st.info(t("executing_text_code", lang=lang))
                            res = execute_python_code(code)
                            tool_res_entry = {
                                "code": code,
                                "output": res.get("output"),
                                "plot": res.get("plot"),
                                "excel": res.get("excel"),
                            }
                            if res.get("status") == "error":
                                tool_res_entry["error"] = res.get("message")
                            if st.session_state.last_tool_df is not None:
                                tool_res_entry["df_preview"] = (
                                    st.session_state.last_tool_df.head(20).to_json()
                                )
                            turn_tool_results.append(tool_res_entry)
                    # Remove code blocks from final_content since they'll be shown as results
                    final_content = code_block_pattern.sub("", final_content).strip()
                    answer_placeholder.markdown(final_content)

                if tool_calls:
                    for tc in tool_calls.values():
                        st.info(t("calling_tool", lang=lang))
                        raw_args = tc["function"]["arguments"]
                        try:
                            match = re.search(r"\{.*\}", raw_args, re.DOTALL)
                            if match:
                                args = json.loads(match.group(0))
                            else:
                                args = json.loads(raw_args)
                        except (json.JSONDecodeError, ValueError):
                            st.warning(f"⚠️ Could not parse tool call arguments:\n```\n{raw_args[:200]}\n```")
                            turn_tool_results.append({"code": raw_args[:200], "error": "JSON parse error in tool arguments"})
                            continue
                        code = (
                            re.sub(r"(?<!=)\s+plt\.", "\nplt.", args.get("code_string", ""))
                        )
                        code = re.sub(r"(?<!=)\s+sns\.", "\nsns.", code)
                        st.code(code, language="python")

                        # Execute and capture results
                        res = execute_python_code(code)

                        # Prepare for persistence
                        tool_res_entry = {
                            "code": code,
                            "output": res.get("output"),
                            "plot": res.get("plot"),
                            "excel": res.get("excel"),
                        }
                        if res.get("status") == "error":
                            tool_res_entry["error"] = res.get("message")
                            st.error(f"❌ Code execution error: {res.get('message')}")
                        if st.session_state.last_tool_df is not None:
                            # Save a small preview of the dataframe if one was created/modified
                            tool_res_entry["df_preview"] = (
                                st.session_state.last_tool_df.head(20).to_json()
                            )
                            st.markdown(f"### {t('result_preview', lang=lang)}")
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
                # Prevent session state bloat from base64 images/Excel
                if len(st.session_state.messages) > 50:
                    st.session_state.messages = st.session_state.messages[-50:]
                st.rerun()
            except Exception as e:
                error_str = str(e)
                # Save partial content so user doesn't lose streamed text
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": final_content if final_content.strip() else "(error processing response)",
                        "thought": thought_content,
                        "tool_results": turn_tool_results,
                    }
                )
                if len(st.session_state.messages) > 50:
                    st.session_state.messages = st.session_state.messages[-50:]
                if "audio input is not supported" in error_str or "mmproj" in error_str:
                    st.error(t("multimodal_error", lang=lang))
                    st.warning(t("multimodal_fix", lang=lang))
                else:
                    st.error(t("server_error", lang=lang, error=error_str))
                st.rerun()
