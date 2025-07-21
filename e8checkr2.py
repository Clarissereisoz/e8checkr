import streamlit as st
from PIL import Image
import base64
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
# (plus any other imports like pandas, matplotlib, etc.)

# === LOGIN SETUP ===
USERNAME = "admin"
PASSWORD = "letmein"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:
    st.markdown("## 🔐 Login to E8Checkr")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful! 🎉")
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")
    st.stop()  # ⛔ Stop the rest of the script if not logged in

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()


st.markdown(
    """
    <style>
    /* Set background color */
    .stApp {
        background-color: #fff8e1;
    }

    /* Optional: make text a bit darker for contrast */
    .stMarkdown, .stText, .stTitle {
        color: #111 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --- Load logo image ---
image = Image.open("e8checkr_logo.jpg")

# --- Centered Logo with Markdown & Base64 Encoding ---
def get_base64_image(img):
    with open(img, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_data = get_base64_image("e8checkr_logo.jpg")

# --- Display logo centered and larger ---
st.markdown(
    f"""
    <div style='text-align: center; margin-bottom: 40px;'>
        <img src='data:image/jpg;base64,{img_data}' width='700'/>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Title and Intro ---

st.markdown("""
Welcome! This tool checks if your system is compliant with 8 key controls from the Australian Government's **Essential Eight** framework.
Just answer the questions below and get your compliance score!
""")

st.sidebar.title("📋 Navigation")
st.sidebar.markdown("✔️ Run Checks\n📈 View Summary\n⬇️ Download Report")



controls = [
    ("Is application control enabled on all workstations?", "Application Control"),
    ("Are all applications patched within 2 weeks of security updates?", "Patch Applications"),
    ("Are Microsoft Office macros blocked or restricted?", "MS Office Macros"),
    ("Are internet-facing applications hardened (e.g. Flash, ads, Java disabled)?", "Application Hardening"),
    ("Are admin privileges restricted to only those who need them?", "Admin Privileges"),
    ("Are operating systems patched within 30 days of release?", "Patch Operating Systems"),
    ("Is multi-factor authentication enabled for all admin accounts?", "MFA"),
    ("Are backups performed regularly and tested?", "Backups"),
]

st.markdown("### ✅ Answer the following compliance checks:")

responses = {}
for question, control in controls:
    responses[control] = st.radio(f"• {question}", ["Yes", "No"], key=control)

if st.button("🔍 Run Compliance Check"):
    compliant = 0
    results = []

    for control in controls:
        question, control_name = control
        status = "Compliant" if responses[control_name] == "Yes" else "Non-Compliant"
        if status == "Compliant":
            compliant += 1
        results.append({
            "Control": control_name,
            "Status": status
        })

    df = pd.DataFrame(results)

    st.markdown("---")
    st.subheader("📊 Compliance Summary")
    st.dataframe(df)

    # Progress bar
    st.markdown("### 📈 Compliance Progress")
    progress = compliant / len(controls)
    st.progress(progress)


    # Show the percentage (nicely formatted)
    percent = int(progress * 100)
    st.markdown(f"**Your compliance score is: {percent}%**")

    # Bar chart
    st.markdown("### 📉 Compliant vs Non-Compliant")
    summary_counts = df["Status"].value_counts()
    fig, ax = plt.subplots()
    summary_counts.plot(kind="bar", color=["green", "red"], ax=ax)
    ax.set_ylabel("Number of Controls")
    ax.set_title("Compliance Breakdown")
    st.pyplot(fig)

    # Score summary
    st.write(f"**You passed {compliant} out of {len(controls)} controls.**")

    if compliant == 8:
        st.success("🎉 Perfect! Fully compliant with all Essential Eight Level 1 controls.")
    elif compliant >= 6:
        st.info("👍 Good effort. A few more controls to tighten.")
    elif compliant >= 4:
        st.warning("⚠️ Moderate risk. Recommend review.")
    else:
        st.error("🚨 High risk! Major gaps in compliance.")

    # CSV download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV Report",
        data=csv,
        file_name="e8checkr_compliance_report.csv",
        mime="text/csv"
    )

    # Placeholder for PDF button
    st.markdown("🚧 PDF export feature coming soon... (Use CSV for now)")

    st.markdown(
    """
    <hr style='margin-top: 40px;'>
    <div style='text-align: center; color: #888; font-size: 0.85rem;'>
        🔐 <i>Clarisse's E8Checkr</i> | Capstone Project | IOD Cyber Security Program | © 2025
    </div>
    """,
    unsafe_allow_html=True
)

