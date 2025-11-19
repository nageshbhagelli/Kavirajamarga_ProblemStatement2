# app.py
import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from word_joiner import KannadaWordBuilder

# --- CONFIG ---
st.set_page_config(
    page_title="Kannada Word Builder",
    page_icon="✍️",
    layout="wide",
)

# --- LOAD SYSTEM ---
@st.cache_resource
def load_system():
    return KannadaWordBuilder()

builder = load_system()

# --- CSS (no HTML wrappers for widgets) ---
st.markdown(
    """
    <style>
    /* page container width */
    .block-container {
        max-width: 920px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    /* a "card" appearance by targeting Streamlit container/blocks */
    /* We target the generic vertical block that Streamlit creates for containers/columns.
       These selectors are reasonably stable across Streamlit versions. */
    .stApp > div > div > section .stBlock > div[role="region"] {
        background: #11151b;
        border-radius: 12px;
        padding: 0 22px;
        border: 1px solid #222831;
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }

    /* make text inputs visually card-like */
    .stTextInput > div > div > input {
        background-color: #1f2430 !important;
        color: #e6eef8 !important;
        border-radius: 10px !important;
        padding: 0 12px !important;
    }

    .center-btn {
    display: flex;
    justify-content: center;
}

    /* button style */
    .stButton > button {
        background-color: #ef4444 !important;
        color: white !important;
        padding: 0px 22px !important;     
        border-radius: 10px !important;
        font-weight: 600;
        border: none !important;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* sidebar bg */
    section[data-testid="stSidebar"] {
        background-color: #0f1520;
        padding: 5px;
    }

    /* success/result area */
    .stAlert {
        border-radius: 10px;
        padding: 5px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* caption/hint */
    .stCaption {
        color: #aab6c9;
    }

    /* Center footer */
.footer {
    text-align: center;
    opacity: 0.7;
    font-size: 0.9rem;
}

    /* small spacing tweaks */
    .css-1d391kg { margin-bottom: 8px; } /* form label -> small tweak */
    </style>
    """,
    unsafe_allow_html=True,
)

# --- HEADER ---
st.markdown("<h1 style='text-align:center;margin-bottom:0.2rem;'>✍️ Kannada Word Builder</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#9CA3AF;margin-top:0;'>AI-Powered Sandhi & Vibhakti Joiner</p>", unsafe_allow_html=True)
#st.markdown("---")

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.markdown("## 📊 System Stats")
    st.write(f"**Dictionary Size:** {len(builder.root_words)} words")
    st.write(f"**Rules:** {len(builder.sandhi_rules) + len(builder.samasa_rules)}")
    st.write(f"**Case Markers:** {len(builder.vibhakti_markers)}")
    st.markdown("---")
    st.success("Ready for Multimodal AI Hackathon 🚀")

# --------------------------------
# INPUT AREA (no raw HTML wrappers)
# --------------------------------
# Use a container so all widgets are in one Streamlit block (so the CSS card targets them together)
left_col, right_col, btn_col = st.columns([1.1, 1.1, 1.1], gap="small")

with left_col:
    word1 = st.text_input("Enter Word 1 (Root):", placeholder="e.g., ಮಹಾ").strip()
    if word1 and hasattr(builder, "hint_engine"):
        hints = builder.hint_engine.get_hints(word1)
        if hints:
            st.caption(f"💡 Hint: Try **{hints[0]['next_word']}** → {hints[0]['result']}")

with right_col:
    word2 = st.text_input("Enter Word 2 (Suffix):", placeholder="e.g., ಆತ್ಮ / ಅಲ್ಲಿ").strip()

with btn_col:
    st.markdown("<div style='height:27px'></div>", unsafe_allow_html=True)  # vertical align
    combine_btn = st.button("🚀 Combine Words", use_container_width=True)


# --------------------------------
# RESULT AREA
# --------------------------------
if combine_btn:
    # Keep the result UI within a single Streamlit container block
    with st.container():
        if not word1 or not word2:
            st.warning("Please enter both words.")
        else:
            output = builder.join_words(word1, word2)

            if output.get("status") == "success":
                st.success(f"✔ Result: **{output['result']}**")
                with st.expander("🔍 Rule Explanation", expanded=True):
                    st.write(f"**Rule Applied:** {output.get('rule', '—')}") 
                    st.markdown(f"**{word1} + {word2} → {output['result']}**")
            elif output.get("status") == "error":
                st.error(f"❌ Error: {output.get('msg', 'Unknown error')}")
            else:
                st.warning(output.get("msg", "Unexpected output"))
                st.write(f"**Result:** {output.get('result', '')}")

st.markdown("""
<div class='footer'>
Team Project for Modalapada Hackathon • Built with ❤️
</div>
""", unsafe_allow_html=True)
