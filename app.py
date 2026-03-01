import os
import streamlit as st
from src.storage import (
    create_request, get_request, get_all_requests, update_request_response,
    update_request_files, create_user, get_user, get_all_users, verify_user,
    update_user_status, delete_user, get_user_requests,
    create_tutorial_request, get_tutorial_request, get_all_tutorial_requests, update_tutorial_request_response
)
from src.validation import validate_input, validate_signup, validate_tutorial_request


def _fmt_symptoms(d):
    """Format a symptom category dict for display.
    Boolean keys are converted to title-case labels; the special 'other' key
    is rendered as 'Other: <text>' when non-empty.
    """
    return [
        f"Other: {v}" if k == "other" else k.replace("_", " ").title()
        for k, v in d.items() if v
    ]


st.set_page_config(page_title="Automotive AI Diagnostics", layout="wide", page_icon="🚗")

# Passwords for expert and admin roles, loaded from environment variables
EXPERT_PASSWORD = os.environ.get("EXPERT_PASSWORD", "password123")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin456")

# ---------------------------------------------------------------------------
# Global CSS – automotive diagnostics database / workshop desk theme
# ---------------------------------------------------------------------------
st.markdown("""
<style>
/* ── Base ──────────────────────────────────────────────────────────────── */
.stApp {
    background: linear-gradient(160deg, #0c0c0e 0%, #111318 60%, #0c0c0e 100%);
    color: #c8c8c8;
}
.block-container { padding-top: 1.5rem; }

/* ── Typography ─────────────────────────────────────────────────────────── */
h1, h2, h3, h4 {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
    color: #e8820c !important;
}
p, label, span, div {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* ── Streamlit tabs ─────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #111318;
    border-bottom: 2px solid #e8820c;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    color: #888;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    letter-spacing: 0.3px;
    font-size: 0.85rem;
    background: #1a1a22;
    border: 1px solid #2a2a35;
    border-bottom: none;
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background: #1f1a0e !important;
    color: #e8820c !important;
    border-color: #e8820c !important;
}

/* ── Inputs ─────────────────────────────────────────────────────────────── */
input, textarea, select {
    background: rgba(255,255,255,0.05) !important;
    color: #e0e0e0 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}
input:focus, textarea:focus {
    border-color: #e8820c !important;
    box-shadow: 0 0 0 3px rgba(232,130,12,0.2) !important;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #e8820c 0%, #c96d00 100%);
    color: #fff !important;
    border: none;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-weight: 600;
    letter-spacing: 0.3px;
    border-radius: 8px;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(232,130,12,0.25);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #f0900f 0%, #d97800 100%);
    box-shadow: 0 6px 18px rgba(232,130,12,0.4);
    transform: translateY(-1px);
    color: #fff !important;
}

/* ── Alerts ──────────────────────────────────────────────────────────────── */
.stAlert {
    border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* ── Login / Signup card ─────────────────────────────────────────────────── */
.auth-card {
    border: 1px solid rgba(232,130,12,0.25);
    border-radius: 16px;
    padding: 40px 44px;
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(20px);
    max-width: 520px;
    margin: 0 auto;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(232,130,12,0.08);
}
.auth-header {
    text-align: center;
    padding-bottom: 20px;
    margin-bottom: 8px;
}
.auth-logo {
    font-size: 3rem;
    line-height: 1;
    margin-bottom: 14px;
    filter: drop-shadow(0 0 12px rgba(232,130,12,0.6));
}
.auth-header .title-lg {
    font-size: 1.6rem;
    color: #e8820c;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    letter-spacing: 3px;
    font-weight: 800;
    text-transform: uppercase;
}
.auth-header .subtitle {
    font-size: 0.72rem;
    color: #666;
    letter-spacing: 1.5px;
    margin-top: 6px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    text-transform: uppercase;
}
.obd-readout {
    border: 1px solid #2a2a35;
    background: #0a0a0f;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 0.7rem;
    color: #00c851;
    font-family: 'Courier New', Courier, monospace;
    margin: 16px 0;
    white-space: pre;
    overflow-x: auto;
}
.rudeness-warning {
    background: rgba(200,30,30,0.06);
    border: 1px solid rgba(139,26,26,0.5);
    border-left: 3px solid #c0392b;
    padding: 12px 16px;
    border-radius: 8px;
    color: #e07070;
    font-size: 0.78rem;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin: 16px 0;
    line-height: 1.5;
}

/* ── Fixed bottom-right admin button ────────────────────────────────────── */
.admin-access-fixed {
    position: fixed;
    bottom: 18px;
    right: 20px;
    z-index: 9999;
}
.admin-access-fixed a {
    background: rgba(10,10,20,0.85);
    border: 1px solid #3a3a4a;
    color: #555;
    padding: 5px 11px;
    border-radius: 6px;
    font-size: 10px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    text-decoration: none;
    letter-spacing: 0.5px;
}
.admin-access-fixed a:hover {
    border-color: #e8820c;
    color: #e8820c;
}

/* ── Expander ────────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background: #111318 !important;
    color: #c8c8c8 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Fixed admin button – always visible at bottom-right corner of every page.
# Clicking navigates to ?page=admin which renders the admin panel below.
# ---------------------------------------------------------------------------
st.markdown("""
<div class="admin-access-fixed">
    <a href="?page=admin">🔐 ADMIN</a>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page routing via query params
# ---------------------------------------------------------------------------
current_page = st.query_params.get("page", "main")


# ===========================================================================
# ADMIN PANEL  (accessed via the bottom-right 🔐 ADMIN button → ?page=admin)
# ===========================================================================
if current_page == "admin":
    st.markdown("""
    <div style="text-align:center; border-bottom: 2px solid #e8820c;
                padding-bottom:12px; margin-bottom:20px;">
        <span style="font-family:'Courier New',monospace; font-size:1.6rem;
                     color:#e8820c; letter-spacing:6px; font-weight:bold;">
            🔐 ADMIN CONTROL PANEL
        </span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Back to Main"):
        st.query_params.clear()
        st.rerun()

    if 'admin_logged_in' not in st.session_state:
        st.session_state['admin_logged_in'] = False

    if not st.session_state['admin_logged_in']:
        st.markdown("#### Administrator Login")
        adm_pw = st.text_input("Admin Password", type="password", key="admin_pw_input")
        if st.button("Login as Admin"):
            if adm_pw == ADMIN_PASSWORD:
                st.session_state['admin_logged_in'] = True
                st.rerun()
            else:
                st.error("Incorrect admin password.")
    else:
        st.success("Logged in as Administrator")
        if st.button("Logout Admin", key="admin_logout"):
            st.session_state['admin_logged_in'] = False
            st.rerun()

        st.markdown("---")

        # ── Stats ──────────────────────────────────────────────────────────
        all_requests = get_all_requests()
        all_users = get_all_users()

        total_req = len(all_requests)
        pending_cnt = sum(1 for r in all_requests.values() if r.get('status') == 'pending')
        completed_cnt = sum(1 for r in all_requests.values() if r.get('status') == 'completed')
        total_users = len(all_users)
        active_users = sum(1 for u in all_users.values() if u.get('status') == 'active')
        paused_users = sum(1 for u in all_users.values() if u.get('status') == 'paused')

        st.subheader("📊 Key Metrics")
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Total Requests", total_req)
        m2.metric("Pending", pending_cnt)
        m3.metric("Completed", completed_cnt)
        m4.metric("Total Members", total_users)
        m5.metric("Active", active_users)
        m6.metric("Paused", paused_users)

        st.markdown("---")

        # ── Member management ──────────────────────────────────────────────
        st.subheader("👥 Member Management")

        # Performance optimization: pre-fetch requests to avoid N+1 query inside loop
        requests_by_user = {}
        if all_requests:
            for r_id, r_data in all_requests.items():
                u_email = r_data.get('user_email', '').strip().lower()
                if u_email:
                    if u_email not in requests_by_user:
                        requests_by_user[u_email] = {}
                    requests_by_user[u_email][r_id] = r_data

        if all_users:
            for email, user in all_users.items():
                status_icon = "🟢" if user.get('status') == 'active' else "🔴"
                with st.expander(
                    f"{status_icon} {user.get('name', 'Unknown')}  —  {email}"
                ):
                    uc1, uc2 = st.columns(2)
                    with uc1:
                        st.write(f"**Name:** {user.get('name')}")
                        st.write(f"**Email:** {email}")
                        st.write(f"**Date of Birth:** {user.get('dob', 'N/A')}")
                    with uc2:
                        st.write(f"**Occupation:** {user.get('occupation', 'N/A')}")
                        st.write(f"**Status:** {user.get('status', 'N/A').upper()}")
                        st.write(f"**Registered:** {user.get('created_at', 'N/A')}")

                    # Request history for this user
                    user_reqs = requests_by_user.get(email.lower().strip(), {})
                    st.markdown(f"**Diagnostic Requests:** {len(user_reqs)}")
                    if user_reqs:
                        for rid, rdata in sorted(
                            user_reqs.items(),
                            key=lambda x: x[1].get('timestamp', ''),
                            reverse=True,
                        ):
                            rstatus = rdata.get('status', 'unknown')
                            ricon = "✅" if rstatus == 'completed' else "⏳"
                            st.markdown(
                                f"&nbsp;&nbsp;{ricon} `{rid[:8]}…` — "
                                f"{rdata.get('year', '')} {rdata.get('make', '')} "
                                f"{rdata.get('model', '')} — "
                                f"{rdata.get('timestamp', '')} — **{rstatus.upper()}**"
                            )

                    # Account actions
                    st.markdown("**Account Actions:**")
                    act_col1, act_col2 = st.columns(2)
                    with act_col1:
                        if user.get('status') == 'active':
                            if st.button("⏸ Pause Account", key=f"pause_{email}"):
                                update_user_status(email, 'paused')
                                st.success(f"Account paused for {email}.")
                                st.rerun()
                        else:
                            if st.button("▶ Reactivate Account", key=f"activate_{email}"):
                                update_user_status(email, 'active')
                                st.success(f"Account reactivated for {email}.")
                                st.rerun()
                    with act_col2:
                        if st.button(
                            "🗑 Delete Account", key=f"delete_{email}",
                            help="This permanently removes the account.",
                        ):
                            delete_user(email)
                            st.warning(f"Account deleted for {email}.")
                            st.rerun()
        else:
            st.info("No registered members yet.")

        st.markdown("---")

        # ── Recent Activity ────────────────────────────────────────────────
        st.subheader("📈 Recent Activity")
        if all_requests:
            sorted_requests = sorted(
                all_requests.items(),
                key=lambda x: x[1].get('timestamp', ''),
                reverse=True,
            )
            st.markdown("**Latest 10 Requests:**")
            for req_id, data in sorted_requests[:10]:
                sicon = "✅" if data.get('status') == 'completed' else "⏳"
                st.markdown(
                    f"{sicon} **{data.get('year', 'N/A')} {data.get('make', '?')} "
                    f"{data.get('model', '?')}** — {data.get('timestamp')} — "
                    f"Status: {data.get('status', '').upper()} — "
                    f"Member: {data.get('user_email', 'N/A')}"
                )
        else:
            st.info("No activity yet.")

        st.markdown("---")

        # ── All Requests ───────────────────────────────────────────────────
        st.subheader("🗂️ All Requests")
        if all_requests:
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                status_filter = st.selectbox(
                    "Filter by Status", ["All", "Pending", "Completed"]
                )
            with filter_col2:
                sort_order = st.selectbox("Sort by", ["Newest First", "Oldest First"])

            filtered = all_requests
            if status_filter != "All":
                filtered = {
                    k: v for k, v in all_requests.items()
                    if v.get('status') == status_filter.lower()
                }
            sorted_filtered = sorted(
                filtered.items(),
                key=lambda x: x[1].get('timestamp', ''),
                reverse=(sort_order == "Newest First"),
            )

            st.markdown(f"**Showing {len(sorted_filtered)} requests**")
            for req_id, data in sorted_filtered:
                sc = "🟢" if data.get('status') == 'completed' else "🟡"
                with st.expander(
                    f"{sc} {data.get('year', 'N/A')} {data.get('make', '?')} "
                    f"{data.get('model', '?')} — ID: {req_id[:12]}…"
                ):
                    st.write(f"**Request ID:** `{req_id}`")
                    st.write(f"**Member:** {data.get('user_email', 'N/A')}")
                    st.write(f"**Submitted:** {data.get('timestamp')}")
                    st.write(f"**Status:** {data.get('status', '').upper()}")
                    if data.get('status') == 'completed':
                        st.write(f"**Responded:** {data.get('response_timestamp')}")

                    st.markdown("**Vehicle:**")
                    vc1, vc2, vc3 = st.columns(3)
                    with vc1:
                        st.write(f"Make: {data.get('make')}")
                        st.write(f"Model: {data.get('model')}")
                        st.write(f"Year: {data.get('year')}")
                    with vc2:
                        st.write(f"Mileage: {data.get('mileage', 0)} km")
                        st.write(f"Engine: {data.get('engine_type')}")
                        if data.get('engine_capacity'):
                            st.write(f"Capacity: {data.get('engine_capacity')}")
                        if data.get('engine_code'):
                            st.write(f"Code: {data.get('engine_code')}")
                        if data.get('vin'):
                            st.write(f"VIN: {data.get('vin')}")
                    with vc3:
                        st.write(f"Transmission: {data.get('transmission_type')}")
                        st.write(f"Fuel: {data.get('fuel_type')}")
                        if data.get('last_service_date'):
                            st.write(f"Last Service: {data['last_service_date']}")
                    if data.get('obd_codes'):
                        st.write(f"**OBD Codes:** {data['obd_codes']}")

                    symptoms = data.get('symptoms', {})
                    if isinstance(symptoms, str):
                        st.markdown(f"**Symptoms:** {symptoms}")
                    else:
                        for cat, icon in [
                            ('power', '⚡'), ('tactile', '👋'), ('audible', '🔊'),
                            ('fuel', '⛽'), ('visual', '👁️'), ('temperature', '🌡️'),
                        ]:
                            active = _fmt_symptoms(symptoms.get(cat, {}))
                            if active:
                                st.markdown(f"**{icon} {cat.title()}:** {', '.join(active)}")
                        if symptoms.get('additional_details'):
                            st.markdown(f"**📝 Notes:** {symptoms['additional_details']}")

                    if data.get('status') == 'completed' and data.get('response'):
                        st.markdown("**✅ Expert Diagnosis:**")
                        st.info(data['response'])
        else:
            st.info("No requests to display.")

    # Stop rendering the rest of the page when in admin panel
    st.stop()


# ===========================================================================
# MAIN APP  (member login / signup then main tabs)
# ===========================================================================

st.title("🚗 Automotive Fault Diagnostics")

# ── Auth state ─────────────────────────────────────────────────────────────
if 'logged_in_user' not in st.session_state:
    st.session_state['logged_in_user'] = None

# ===========================================================================
# LOGIN / SIGNUP  (shown when not authenticated)
# ===========================================================================
if st.session_state['logged_in_user'] is None:

    # Branding card
    st.markdown("""
    <div class="auth-card">
        <div class="auth-header">
            <div class="auth-logo">🚗</div>
            <div class="title-lg">DSS Diagnostics</div>
            <div class="subtitle">Automotive Fault Database System v2.0</div>
        </div>
        <div class="obd-readout">SYSTEM READY...
SCAN TOOL CONNECTED
OBD-II INTERFACE: ACTIVE
DATABASE: ONLINE  |  EXPERTS: AVAILABLE
&gt; MEMBER LOGIN REQUIRED TO PROCEED_</div>
        <div class="rudeness-warning">
            ⚠️ <strong>Community Standards Warning</strong><br>
            Our experts are qualified professionals who volunteer their time.
            Any abusive, rude, or disrespectful behaviour toward experts
            <strong>will result in immediate account suspension.</strong>
            By creating an account you agree to treat all experts with respect.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Login / Signup toggle
    col_l, col_s = st.columns(2)
    with col_l:
        show_login = st.button("🔓 Member Login", use_container_width=True)
    with col_s:
        show_signup = st.button("📝 Create Account", use_container_width=True)

    if 'auth_mode' not in st.session_state:
        st.session_state['auth_mode'] = 'login'
    if show_login:
        st.session_state['auth_mode'] = 'login'
    if show_signup:
        st.session_state['auth_mode'] = 'signup'

    st.markdown("---")

    # ── LOGIN ──────────────────────────────────────────────────────────────
    if st.session_state['auth_mode'] == 'login':
        st.subheader("🔓 Member Login")
        st.markdown(
            "<div class='rudeness-warning'>⚠️ Reminder: Respectful communication "
            "with our experts is mandatory. Rude behaviour = account suspension.</div>",
            unsafe_allow_html=True,
        )
        with st.form("login_form"):
            login_email = st.text_input(
                "Email Address (your username)", placeholder="you@example.com"
            )
            login_pw = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login →")

        if login_btn:
            if not login_email or not login_pw:
                st.error("Please enter your email and password.")
            else:
                ok, msg = verify_user(login_email.strip(), login_pw)
                if ok:
                    user = get_user(login_email.strip())
                    st.session_state['logged_in_user'] = user
                    st.success(f"Welcome back, {user['name']}!")
                    st.rerun()
                else:
                    st.error(msg)

    # ── SIGNUP ─────────────────────────────────────────────────────────────
    else:
        st.subheader("📝 Create New Account")
        st.markdown(
            "<div class='rudeness-warning'>⚠️ <strong>Please read before signing up:</strong> "
            "Our experts are professionals. Any abusive or rude behaviour will result in "
            "<strong>immediate account suspension</strong>. By registering you agree to "
            "treat every expert with courtesy and respect at all times.</div>",
            unsafe_allow_html=True,
        )
        with st.form("signup_form"):
            su_name = st.text_input("Full Name *", placeholder="Jane Smith")
            su_email = st.text_input(
                "Email Address * (used as your login username)",
                placeholder="jane@example.com",
            )
            su_pw = st.text_input(
                "Password * (min 8 chars, must include a letter & number)",
                type="password",
            )
            su_pw2 = st.text_input("Confirm Password *", type="password")
            su_dob = st.date_input("Date of Birth *", value=None)
            su_occ = st.text_input(
                "Occupation *", placeholder="e.g. Fleet Manager, Car Enthusiast"
            )
            signup_btn = st.form_submit_button("Create Account →")

        if signup_btn:
            if su_pw != su_pw2:
                st.error("Passwords do not match.")
            else:
                errs = validate_signup(su_name, su_email, su_pw, su_dob, su_occ)
                if errs:
                    for e in errs:
                        st.error(e)
                else:
                    ok, msg = create_user(su_email, su_pw, su_name, su_dob, su_occ)
                    if ok:
                        st.success("✅ Account created! You can now log in.")
                        st.session_state['auth_mode'] = 'login'
                        st.rerun()
                    else:
                        st.error(msg)

    # Don't render the main app tabs while not logged in
    st.stop()


# ===========================================================================
# AUTHENTICATED – Main application tabs
# ===========================================================================

current_user = st.session_state['logged_in_user']

# Top bar: user info + logout
top_col1, top_col2 = st.columns([6, 1])
with top_col1:
    st.markdown(
        f"<span style='font-family:monospace; color:#e8820c;'>"
        f"👤 Logged in as: <strong>{current_user['name']}</strong> "
        f"({current_user['email']})</span>",
        unsafe_allow_html=True,
    )
with top_col2:
    if st.button("Logout"):
        st.session_state['logged_in_user'] = None
        st.rerun()

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "🚗 Submit Issue",
    "🔧 Expert Dashboard",
    "🔍 Check Status",
    "🎥 Custom Tutorial",
])

# ---------------------------------------------------------------------------
# TAB 1: CAR OWNER – Submit Issue
# ---------------------------------------------------------------------------
with tab1:
    st.header("Describe Your Car Issue")
    st.markdown("Get professional diagnostic advice from certified experts.")

    # Australian Market Vehicle Data
    AUSTRALIAN_MAKES = [
        "Select Make", "Abarth", "Alfa Romeo", "Aston Martin", "Audi", "Bentley", "BMW", "BYD", "Chery",
        "Chevrolet", "Chrysler", "Citroen", "Cupra", "Dacia", "Daewoo", "Daihatsu", "Dodge", "Ferrari",
        "Fiat", "Ford", "Genesis", "GWM", "Holden", "Honda", "Hyundai", "Infiniti", "Isuzu", "Jaguar",
        "Jeep", "Kia", "Lamborghini", "Land Rover", "LDV", "Lexus", "Mahindra", "Maserati", "Mazda",
        "McLaren", "Mercedes-Benz", "MG", "Mini", "Mitsubishi", "Nissan", "Opel", "Peugeot", "Porsche",
        "RAM", "Renault", "Rolls-Royce", "Skoda", "SsangYong", "Subaru", "Suzuki", "Tesla", "Toyota",
        "Volkswagen", "Volvo", "Other",
    ]

    MODELS_BY_MAKE = {
        "Abarth": ["Select Model", "500", "595", "695", "124 Spider", "Punto", "Other"],
        "Alfa Romeo": ["Select Model", "147", "156", "159", "Brera", "Giulia", "Giulietta", "GTV", "MiTo", "Spider", "Stelvio", "Tonale", "Other"],
        "Aston Martin": ["Select Model", "DB7", "DB9", "DB11", "DBS", "DBX", "Rapide", "Vantage", "Virage", "Vanquish", "Other"],
        "Audi": ["Select Model", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "e-tron", "e-tron GT", "Q2", "Q3", "Q4 e-tron", "Q5", "Q7", "Q8", "Q8 e-tron", "R8", "RS3", "RS4", "RS5", "RS6", "RS7", "S3", "S4", "S5", "S6", "S7", "S8", "TT", "Other"],
        "Bentley": ["Select Model", "Arnage", "Azure", "Bentayga", "Continental GT", "Continental GTC", "Flying Spur", "Mulsanne", "Other"],
        "BMW": ["Select Model", "1 Series", "2 Series", "3 Series", "4 Series", "5 Series", "6 Series", "7 Series", "8 Series", "i3", "i4", "i5", "i7", "iX", "iX1", "iX3", "M2", "M3", "M4", "M5", "M8", "X1", "X2", "X3", "X3 M", "X4", "X4 M", "X5", "X5 M", "X6", "X6 M", "X7", "Z3", "Z4", "Other"],
        "BYD": ["Select Model", "Atto 3", "Dolphin", "Han", "Seal", "Sea Lion 6", "Song", "Song Plus", "Tang", "Other"],
        "Chery": ["Select Model", "Omoda 5", "Tiggo 4", "Tiggo 7", "Tiggo 7 Pro", "Tiggo 8", "Tiggo 8 Pro", "Other"],
        "Chevrolet": ["Select Model", "Camaro", "Colorado", "Corvette", "Equinox", "Express", "Silverado", "Suburban", "Tahoe", "Trailblazer", "Traverse", "Other"],
        "Chrysler": ["Select Model", "300", "300C", "Grand Voyager", "Neon", "PT Cruiser", "Sebring", "Voyager", "Other"],
        "Citroen": ["Select Model", "Berlingo", "Boxer", "C1", "C2", "C3", "C3 Aircross", "C4", "C4 Cactus", "C5", "C5 Aircross", "C5 X", "C6", "Dispatch", "DS3", "DS4", "DS5", "Jumper", "Jumpy", "Relay", "SpaceTourer", "Xsara", "Other"],
        "Cupra": ["Select Model", "Ateca", "Born", "Formentor", "Leon", "Terramar", "Tavascan", "Other"],
        "Dacia": ["Select Model", "Duster", "Logan", "Sandero", "Spring", "Jogger", "Other"],
        "Daewoo": ["Select Model", "Kalos", "Lacetti", "Lanos", "Leganza", "Nubira", "Tacuma", "Other"],
        "Daihatsu": ["Select Model", "Charade", "Cuore", "Feroza", "Rocky", "Sirion", "Terios", "YRV", "Other"],
        "Dodge": ["Select Model", "Challenger", "Charger", "Durango", "Journey", "Neon", "Nitro", "Viper", "Other"],
        "Ferrari": ["Select Model", "296 GTB", "296 GTS", "458", "488 GTB", "488 Spider", "812 Competizione", "812 GTS", "812 Superfast", "California", "California T", "F12berlinetta", "F8 Spider", "F8 Tributo", "FF", "GTC4Lusso", "Portofino", "Portofino M", "Purosangue", "Roma", "SF90 Spider", "SF90 Stradale", "Other"],
        "Fiat": ["Select Model", "124 Spider", "500", "500C", "500L", "500X", "Bravo", "Doblo", "Ducato", "Freemont", "Grande Punto", "Linea", "Panda", "Punto", "Scudo", "Tipo", "Other"],
        "Ford": ["Select Model", "Bronco", "Bronco Sport", "Edge", "Escape", "Everest", "Explorer", "F-150", "Fiesta", "Focus", "Fusion", "Galaxy", "Kuga", "Maverick", "Mondeo", "Mustang", "Puma", "Ranger", "S-Max", "Territory", "Transit", "Transit Custom", "Other"],
        "Genesis": ["Select Model", "G70", "G80", "G90", "GV60", "GV70", "GV80", "Other"],
        "GWM": ["Select Model", "Haval H2", "Haval H6", "Haval H9", "Haval Jolion", "Tank 300", "Tank 500", "Ute", "Other"],
        "Holden": ["Select Model", "Astra", "Barina", "Calais", "Captiva", "Colorado", "Commodore", "Cruze", "Insignia", "Malibu", "Monaro", "Spark", "Statesman", "Trailblazer", "Trax", "Ute", "Other"],
        "Honda": ["Select Model", "Accord", "Accord Euro", "BR-V", "City", "Civic", "CR-V", "CR-Z", "e:NS1", "e:NP1", "e:NY1", "HR-V", "Integra", "Jazz", "Legend", "Odyssey", "Passport", "Pilot", "Ridgeline", "S2000", "WR-V", "ZR-V", "Other"],
        "Hyundai": ["Select Model", "Accent", "Elantra", "Getz", "i20", "i20 N", "i30", "i30 N", "i40", "IONIQ", "IONIQ 5", "IONIQ 6", "IONIQ 9", "Kona", "Kona Electric", "Palisade", "Santa Cruz", "Santa Fe", "Sonata", "Staria", "Tucson", "Venue", "Veloster", "Other"],
        "Infiniti": ["Select Model", "EX", "FX", "G", "M", "Q30", "Q50", "Q60", "Q70", "QX30", "QX50", "QX55", "QX60", "QX70", "QX80", "Other"],
        "Isuzu": ["Select Model", "D-Max", "MU-X", "Other"],
        "Jaguar": ["Select Model", "E-Pace", "F-Pace", "F-Type", "I-Pace", "S-Type", "XE", "XF", "XJ", "XJR", "XK", "Other"],
        "Jeep": ["Select Model", "Cherokee", "Commander", "Compass", "Gladiator", "Grand Cherokee", "Grand Cherokee L", "Patriot", "Renegade", "Wrangler", "Other"],
        "Kia": ["Select Model", "Carnival", "Ceed", "Cerato", "EV6", "EV9", "Mohave", "Niro", "Niro EV", "Picanto", "Pro Ceed", "Rio", "Seltos", "Sorento", "Soul", "Sportage", "Stinger", "Stonic", "Telluride", "Other"],
        "Lamborghini": ["Select Model", "Aventador", "Gallardo", "Huracan", "Revuelto", "Urus", "Other"],
        "Land Rover": ["Select Model", "Defender", "Discovery", "Discovery Sport", "Evoque", "Freelander", "Range Rover", "Range Rover Sport", "Range Rover Velar", "Other"],
        "LDV": ["Select Model", "D90", "Deliver 9", "G10", "Mifa 6", "Mifa 9", "T60", "T60 Max", "Other"],
        "Lexus": ["Select Model", "CT", "ES", "GS", "GX", "IS", "LC", "LS", "LX", "NX", "RC", "RC F", "RX", "RZ", "UX", "Other"],
        "Mahindra": ["Select Model", "Bolero", "Pik Up", "Scorpio", "Thar", "XUV300", "XUV400", "XUV700", "Other"],
        "Maserati": ["Select Model", "Ghibli", "GranCabrio", "GranTurismo", "Grecale", "Levante", "MC20", "Quattroporte", "Other"],
        "Mazda": ["Select Model", "2", "3", "6", "BT-50", "CX-3", "CX-30", "CX-5", "CX-60", "CX-70", "CX-80", "CX-90", "CX-9", "MX-5", "MX-30", "Other"],
        "McLaren": ["Select Model", "540C", "570GT", "570S", "600LT", "620R", "650S", "675LT", "720S", "765LT", "Artura", "GT", "MP4-12C", "Other"],
        "Mercedes-Benz": ["Select Model", "A-Class", "AMG GT", "B-Class", "C-Class", "CLA", "CLS", "E-Class", "EQA", "EQB", "EQC", "EQE", "EQS", "G-Class", "GLA", "GLB", "GLC", "GLE", "GLS", "S-Class", "SL", "SLC", "Sprinter", "V-Class", "Vito", "Other"],
        "MG": ["Select Model", "3", "4", "5", "6", "Cyberster", "HS", "HS PHEV", "Marvel R", "ZS", "ZS EV", "Other"],
        "Mini": ["Select Model", "Clubman", "Convertible", "Countryman", "Coupe", "Hatch", "John Cooper Works", "Paceman", "Roadster", "Other"],
        "Mitsubishi": ["Select Model", "3000GT", "ASX", "Carisma", "Colt", "Eclipse Cross", "Eclipse Cross PHEV", "Galant", "i-MiEV", "Lancer", "Mirage", "Outlander", "Outlander PHEV", "Pajero", "Pajero Sport", "Triton", "Other"],
        "Nissan": ["Select Model", "350Z", "370Z", "Altima", "Ariya", "Armada", "Frontier", "GT-R", "Juke", "Leaf", "Maxima", "Micra", "Murano", "Navara", "Note", "Pathfinder", "Patrol", "Pulsar", "Qashqai", "Sentra", "Skyline", "Tiida", "Titan", "X-Trail", "Z", "Other"],
        "Opel": ["Select Model", "Astra", "Corsa", "Grandland", "Insignia", "Mokka", "Zafira", "Other"],
        "Peugeot": ["Select Model", "108", "208", "308", "408", "508", "2008", "3008", "4008", "5008", "Boxer", "Expert", "Partner", "Rifter", "Traveller", "Other"],
        "Porsche": ["Select Model", "718 Boxster", "718 Cayman", "911", "Cayenne", "Cayenne E-Hybrid", "Macan", "Macan Electric", "Panamera", "Taycan", "Other"],
        "RAM": ["Select Model", "1500", "1500 Classic", "2500", "3500", "Other"],
        "Renault": ["Select Model", "Arkana", "Austral", "Captur", "Clio", "Duster", "Kadjar", "Kangoo", "Koleos", "Laguna", "Master", "Megane", "Scenic", "Trafic", "Zoe", "Other"],
        "Rolls-Royce": ["Select Model", "Cullinan", "Dawn", "Ghost", "Phantom", "Silver Shadow", "Silver Seraph", "Spectre", "Wraith", "Other"],
        "Skoda": ["Select Model", "Enyaq", "Fabia", "Kamiq", "Karoq", "Kodiaq", "Octavia", "Scala", "Superb", "Other"],
        "SsangYong": ["Select Model", "Actyon", "Korando", "Musso", "Rexton", "Tivoli", "Torres", "Other"],
        "Subaru": ["Select Model", "BRZ", "Crosstrek", "Forester", "Impreza", "Legacy", "Levorg", "Liberty", "Outback", "Solterra", "WRX", "WRX STI", "XV", "Other"],
        "Suzuki": ["Select Model", "Across", "Baleno", "Grand Vitara", "Ignis", "Jimny", "Kizashi", "S-Cross", "Splash", "Swift", "SX4", "Vitara", "Other"],
        "Tesla": ["Select Model", "Cybertruck", "Model 3", "Model S", "Model X", "Model Y", "Roadster", "Other"],
        "Toyota": ["Select Model", "86", "Aurion", "Avalon", "Camry", "C-HR", "Corolla", "Corolla Cross", "Dyna", "Fortuner", "GR86", "GR Corolla", "GR Supra", "HiAce", "Hilux", "Kluger", "LandCruiser", "LandCruiser 200", "LandCruiser 300", "Lite Ace", "Prado", "ProAce", "RAV4", "RAV4 PHEV", "Rukus", "Supra", "Tarago", "Yaris", "Yaris Cross", "Other"],
        "Volkswagen": ["Select Model", "Amarok", "Arteon", "Caddy", "Caravelle", "Crafter", "Golf", "ID.3", "ID.4", "ID.5", "Multivan", "Passat", "Polo", "T-Cross", "T-Roc", "Tiguan", "Tiguan Allspace", "Touareg", "Touran", "Transporter", "Other"],
        "Volvo": ["Select Model", "C30", "C40", "C70", "EX30", "EX40", "EX90", "S40", "S60", "S80", "S90", "V40", "V60", "V90", "XC40", "XC60", "XC70", "XC90", "Other"],
    }

    YEARS = ["Select Year"] + [str(year) for year in range(2025, 1979, -1)]

    st.subheader("📋 Vehicle Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        make = st.selectbox("Car Make", AUSTRALIAN_MAKES, index=0)
        if make in MODELS_BY_MAKE:
            model_options = MODELS_BY_MAKE[make]
        else:
            model_options = ["Select Model", "Other"]
        model = st.selectbox("Car Model", model_options, index=0)
        year_str = st.selectbox("Year", YEARS, index=0)
        year = int(year_str) if year_str != "Select Year" else 0

    with col2:
        mileage = st.number_input("Mileage (km/miles)", min_value=0, step=1000)
        vin = st.text_input("VIN (Optional)", placeholder="17-digit VIN")
        engine_type = st.selectbox("Engine Type (Cylinders)", ["2", "3", "4", "5", "6", "8", "10", "11", "12", "Rotary"])
        engine_capacity = st.text_input("Engine Capacity:", placeholder="e.g., 2.0L, 3500cc")
        engine_code = st.text_input("Engine Code (If known)", placeholder="e.g., 2GR-FE, EJ257")

    with col3:
        transmission_type = st.selectbox("Transmission", ["Automatic", "Manual", "CVT", "Semi-Automatic", "Unknown"])
        fuel_type = st.selectbox("Fuel Type", ["Petrol/Unleaded", "Diesel", "Hybrid", "Bio-Diesel", "Alcohol (E85/Methanol)"])
        last_service_date = st.text_input("Last Service Date (Optional)", placeholder="YYYY-MM-DD or e.g., 3 months ago")

    st.markdown("---")
    st.subheader("🔍 Symptom Categories")
    st.markdown("**Select at least one option in each category:**")

    # Power Symptoms
    st.markdown("**⚡ Power Symptoms**")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        power_loss = st.checkbox("Loss of power")
        power_intermittent = st.checkbox("Intermittent power loss")
    with col_p2:
        power_surge = st.checkbox("Power surges")
        power_more = st.checkbox("Increased power")
    with col_p3:
        power_hesitation = st.checkbox("Hesitation/lag")
        power_no_change = st.checkbox("No change")
    power_other = st.checkbox("Other", key="power_other")
    if power_other:
        power_other_text = st.text_input(
            "Describe other power symptoms", key="power_other_text",
            placeholder="Enter any other power symptoms not listed above...",
        )
    else:
        power_other_text = ""

    # Tactile Symptoms
    st.markdown("**👋 Tactile Symptoms**")
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        tactile_vibration = st.checkbox("Vibration")
        tactile_rough = st.checkbox("Rough engine performance")
    with col_t2:
        tactile_pulling = st.checkbox("Pulling to one side")
        tactile_shaking = st.checkbox("Shaking/trembling")
    with col_t3:
        tactile_jerking = st.checkbox("Jerking motion")
        tactile_hunting = st.checkbox("Hunting")
        tactile_stiff = st.checkbox("Stiff steering/pedals")
        tactile_no_change = st.checkbox("No change", key="tactile_no_change")
    tactile_other = st.checkbox("Other", key="tactile_other")
    if tactile_other:
        tactile_other_text = st.text_input(
            "Describe other tactile symptoms", key="tactile_other_text",
            placeholder="Enter any other tactile/physical symptoms not listed above...",
        )
    else:
        tactile_other_text = ""

    # Audible Symptoms
    st.markdown("**🔊 Audible Symptoms**")
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        audible_rattling = st.checkbox("Rattling")
        audible_knocking = st.checkbox("Knocking")
    with col_a2:
        audible_grinding = st.checkbox("Grinding")
        audible_squealing = st.checkbox("Squealing/squeaking")
    with col_a3:
        audible_humming = st.checkbox("Humming/buzzing")
        audible_clicking = st.checkbox("Clicking")
        audible_no_change = st.checkbox("No change", key="audible_no_change")
    audible_other = st.checkbox("Other", key="audible_other")
    if audible_other:
        audible_other_text = st.text_input(
            "Describe other audible symptoms", key="audible_other_text",
            placeholder="Enter any other sounds or noises not listed above...",
        )
    else:
        audible_other_text = ""

    # Fuel Symptoms
    st.markdown("**⛽ Fuel/Consumption Symptoms**")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        fuel_increased = st.checkbox("Increased fuel consumption")
        fuel_smell = st.checkbox("Fuel smell")
    with col_f2:
        fuel_decreased_mileage = st.checkbox("Decreased mileage/efficiency")
        fuel_leak = st.checkbox("Fuel leak")
    with col_f3:
        fuel_difficulty_starting = st.checkbox("Difficulty starting")
        fuel_stalling = st.checkbox("Engine stalling")
        fuel_no_change = st.checkbox("No change", key="fuel_no_change")
    fuel_other = st.checkbox("Other", key="fuel_other")
    if fuel_other:
        fuel_other_text = st.text_input(
            "Describe other fuel/consumption symptoms", key="fuel_other_text",
            placeholder="Enter any other fuel or consumption issues not listed above...",
        )
    else:
        fuel_other_text = ""

    # Visual Symptoms
    st.markdown("**👁️ Visual Symptoms**")
    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        visual_smoke_white = st.checkbox("White smoke")
        visual_smoke_black = st.checkbox("Black smoke")
    with col_v2:
        visual_smoke_blue = st.checkbox("Blue smoke")
        visual_warning_lights = st.checkbox("Warning lights on")
    with col_v3:
        visual_fluid_leak = st.checkbox("Fluid leaks")
        visual_corrosion = st.checkbox("Corrosion/rust")
        visual_no_change = st.checkbox("No change", key="visual_no_change")
    visual_other = st.checkbox("Other", key="visual_other")
    if visual_other:
        visual_other_text = st.text_input(
            "Describe other visual symptoms", key="visual_other_text",
            placeholder="Enter any other visual or observable symptoms not listed above...",
        )
    else:
        visual_other_text = ""

    # Temperature Symptoms
    st.markdown("**🌡️ Temperature Symptoms**")
    col_temp1, col_temp2, col_temp3 = st.columns(3)
    with col_temp1:
        temp_overheating = st.checkbox("Engine overheating")
        temp_running_hot = st.checkbox("Running hotter than normal")
    with col_temp2:
        temp_running_cold = st.checkbox("Running colder than normal")
        temp_ac_issues = st.checkbox("A/C not working properly")
    with col_temp3:
        temp_heater_issues = st.checkbox("Heater not working properly")
        temp_no_change = st.checkbox("No change", key="temp_no_change")
    temp_other = st.checkbox("Other", key="temp_other")
    if temp_other:
        temp_other_text = st.text_input(
            "Describe other temperature symptoms", key="temp_other_text",
            placeholder="Enter any other temperature-related symptoms not listed above...",
        )
    else:
        temp_other_text = ""

    with st.form("diagnostic_request_form"):
        st.markdown("---")
        st.subheader("📝 Additional Details")
        additional_symptoms = st.text_area(
            "Describe any additional symptoms or context", height=150,
            placeholder="Example: The rattling noise only happens when accelerating above 40mph. "
                        "The check engine light came on yesterday.",
        )
        obd_codes = st.text_input("OBD-II Codes (if known)", placeholder="P0300, P0420")
        uploaded_files = st.file_uploader(
            "Upload Photos/Videos/Audio of the issue", accept_multiple_files=True
        )

        st.markdown("### Payment")
        st.info("Consultation Fee: $20.00")
        submitted = st.form_submit_button("Pay & Submit Request")

    st.info(
        "📋 **What to expect from this service:**\n\n"
        "After payment, here is what you can expect:\n\n"
        "1. **Confirmation:** You will receive an email confirming your submission and unique Request ID.\n"
        "2. **Expert Clarification:** An expert may contact you via email to clarify or verify specific details of "
        "your reported issue before proceeding.\n"
        "3. **Diagnostic Flow:** You will receive a structured, step-by-step diagnostic guide tailored to your "
        "vehicle and symptoms, designed to guide you toward identifying the root cause.\n"
        "4. **Back-and-Forth Exchanges:** Your service includes up to **3 exchanges** with our expert team to "
        "refine and progress the diagnosis.\n"
        "5. **Service Goal:** Our aim is to guide you to the point of diagnosis — or as close as possible within "
        "your allotted consultation period.\n"
        "6. **Extended Consultations:** If you require additional expert time or actions beyond your initial "
        "package, extended consultation packages are available for purchase at any time.\n\n"
        "*Note: This is a guided remote diagnostic service. It does not include physical vehicle inspection, "
        "parts replacement, or on-site repairs.*"
    )

    if submitted:
        symptoms_data = {
            "power": {
                "loss_of_power": power_loss, "intermittent_power_loss": power_intermittent,
                "power_surges": power_surge, "increased_power": power_more,
                "hesitation_lag": power_hesitation, "no_change": power_no_change,
                "other": power_other_text,
            },
            "tactile": {
                "vibration": tactile_vibration, "rough_engine": tactile_rough,
                "pulling_to_side": tactile_pulling, "shaking": tactile_shaking,
                "jerking": tactile_jerking, "hunting": tactile_hunting,
                "stiff_controls": tactile_stiff, "no_change": tactile_no_change,
                "other": tactile_other_text,
            },
            "audible": {
                "rattling": audible_rattling, "knocking": audible_knocking,
                "grinding": audible_grinding, "squealing": audible_squealing,
                "humming": audible_humming, "clicking": audible_clicking,
                "no_change": audible_no_change, "other": audible_other_text,
            },
            "fuel": {
                "increased_consumption": fuel_increased, "fuel_smell": fuel_smell,
                "decreased_mileage": fuel_decreased_mileage, "fuel_leak": fuel_leak,
                "difficulty_starting": fuel_difficulty_starting, "stalling": fuel_stalling,
                "no_change": fuel_no_change, "other": fuel_other_text,
            },
            "visual": {
                "white_smoke": visual_smoke_white, "black_smoke": visual_smoke_black,
                "blue_smoke": visual_smoke_blue, "warning_lights": visual_warning_lights,
                "fluid_leak": visual_fluid_leak, "corrosion": visual_corrosion,
                "no_change": visual_no_change, "other": visual_other_text,
            },
            "temperature": {
                "overheating": temp_overheating, "running_hot": temp_running_hot,
                "running_cold": temp_running_cold, "ac_issues": temp_ac_issues,
                "heater_issues": temp_heater_issues, "no_change": temp_no_change,
                "other": temp_other_text,
            },
            "additional_details": additional_symptoms,
        }

        errors = validate_input(
            make, model, year, mileage, vin, engine_type, transmission_type,
            fuel_type, last_service_date, symptoms_data, obd_codes,
        )
        if errors:
            for error in errors:
                st.error(error)
        else:
            with st.spinner("Processing Payment..."):
                request_data = {
                    "make": make, "model": model, "year": year, "mileage": mileage,
                    "vin": vin, "engine_type": engine_type, "engine_capacity": engine_capacity,
                    "engine_code": engine_code, "transmission_type": transmission_type,
                    "fuel_type": fuel_type, "last_service_date": last_service_date,
                    "symptoms": symptoms_data, "obd_codes": obd_codes,
                    "has_files": bool(uploaded_files),
                    "user_email": current_user['email'],
                }
                req_id = create_request(request_data)
                st.success("Payment Successful! Your request has been submitted.")
                st.balloons()
                st.markdown(f"**Your Request ID is:** `{req_id}`")
                st.warning("Please save this ID to check your diagnosis status later.")


# ---------------------------------------------------------------------------
# TAB 2: EXPERT DASHBOARD
# ---------------------------------------------------------------------------
with tab2:
    st.header("Expert Dashboard")

    if 'expert_logged_in' not in st.session_state:
        st.session_state['expert_logged_in'] = False

    if not st.session_state['expert_logged_in']:
        password = st.text_input("Enter Expert Password", type="password")
        if st.button("Login"):
            if password == EXPERT_PASSWORD:
                st.session_state['expert_logged_in'] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    else:
        st.success("Logged in as Expert")
        if st.button("Logout"):
            st.session_state['expert_logged_in'] = False
            st.rerun()

        st.markdown("---")
        st.subheader("Pending Requests")

        all_requests = get_all_requests()
        if all_requests:
            pending_requests = {k: v for k, v in all_requests.items() if v.get('status') == 'pending'}

            if not pending_requests:
                st.info("No pending requests.")
            else:
                for req_id, data in pending_requests.items():
                    with st.expander(
                        f"{data.get('year', 'N/A')} {data.get('make', '?')} "
                        f"{data.get('model', '?')} - {req_id[:8]}..."
                    ):
                        st.write(f"**Request ID:** {req_id}")
                        st.write(f"**Submitted:** {data.get('timestamp')}")
                        st.write(f"**Member:** {data.get('user_email', 'N/A')}")

                        st.markdown("### 🚗 Vehicle Details")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Make/Model:** {data.get('make')} {data.get('model')}")
                            st.write(f"**Year:** {data.get('year')}")
                            st.write(f"**Mileage:** {data.get('mileage')}")
                        with col2:
                            st.write(f"**Engine:** {data.get('engine_type')}")
                            if data.get('engine_capacity'):
                                st.write(f"**Engine Capacity:** {data['engine_capacity']}")
                            if data.get('engine_code'):
                                st.write(f"**Engine Code:** {data['engine_code']}")
                            st.write(f"**Transmission:** {data.get('transmission_type', 'N/A')}")
                            st.write(f"**Fuel Type:** {data.get('fuel_type', 'N/A')}")
                        if data.get('last_service_date'):
                            st.write(f"**Last Service:** {data['last_service_date']}")
                        if data.get('obd_codes'):
                            st.write(f"**OBD Codes:** {data['obd_codes']}")

                        st.markdown("### 🔍 Reported Symptoms")
                        symptoms = data.get('symptoms', {})
                        if isinstance(symptoms, str):
                            st.markdown(f"**General Description:**\n>{symptoms}")
                        else:
                            for cat, icon in [
                                ('power', '⚡'), ('tactile', '👋'), ('audible', '🔊'),
                                ('fuel', '⛽'), ('visual', '👁️'), ('temperature', '🌡️'),
                            ]:
                                active = _fmt_symptoms(symptoms.get(cat, {}))
                                if active:
                                    st.markdown(f"**{icon} {cat.title()}:** {', '.join(active)}")
                            if symptoms.get('additional_details'):
                                st.markdown(f"**📝 Additional Details:**\n>{symptoms['additional_details']}")

                        if data.get('has_files'):
                            st.write("📎 *User uploaded files (placeholder)*")

                        with st.form(key=f"response_form_{req_id}"):
                            diagnosis = st.text_area(
                                "Expert Diagnosis & Recommendation", height=200,
                                placeholder="Enter your detailed diagnosis here...",
                            )
                            submit_diagnosis = st.form_submit_button("Send Diagnosis")
                            if submit_diagnosis:
                                if diagnosis:
                                    if update_request_response(req_id, diagnosis):
                                        st.success(f"Diagnosis sent for request {req_id}!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to update request.")
                                else:
                                    st.warning("Please enter a diagnosis.")
        else:
            st.info("No requests found.")

        st.markdown("---")
        st.subheader("Pending Tutorial Requests")
        all_tutorials = get_all_tutorial_requests()
        if all_tutorials:
            pending_tutorials = {k: v for k, v in all_tutorials.items() if v.get('status') == 'pending'}

            if not pending_tutorials:
                st.info("No pending tutorial requests.")
            else:
                for tut_id, data in pending_tutorials.items():
                    with st.expander(
                        f"Tutorial: {data.get('year', 'N/A')} {data.get('make', '?')} "
                        f"{data.get('model', '?')} - {tut_id[:8]}..."
                    ):
                        st.write(f"**Request ID:** {tut_id}")
                        st.write(f"**Submitted:** {data.get('timestamp')}")
                        st.write(f"**User Email:** {data.get('user_email', 'N/A')}")
                        st.markdown("### 🚗 Vehicle Details")
                        st.write(f"**Vehicle:** {data.get('year')} {data.get('make')} {data.get('model')}")
                        st.markdown("### 🎥 Tutorial Details")
                        st.write(f"**Description:** {data.get('description')}")
                        st.write(f"**Preferred Medium:** {data.get('medium')}")

                        with st.form(key=f"tutorial_response_form_{tut_id}"):
                            tutorial_response = st.text_area(
                                "Tutorial Content/Link", height=150,
                                placeholder="Provide the tutorial link or instructions here...",
                            )
                            submit_tutorial = st.form_submit_button("Send Tutorial")
                            if submit_tutorial:
                                if tutorial_response:
                                    if update_tutorial_request_response(tut_id, tutorial_response):
                                        st.success(f"Tutorial sent for request {tut_id}!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to update tutorial request.")
                                else:
                                    st.warning("Please enter the tutorial content or link.")
        else:
            st.info("No tutorial requests found.")


# ---------------------------------------------------------------------------
# TAB 3: CHECK STATUS
# ---------------------------------------------------------------------------
with tab3:
    st.header("Check Your Status")

    check_id = st.text_input("Enter your Request ID")

    if st.button("Check Status"):
        if check_id:
            clean_id = check_id.strip()
            req_data = get_request(clean_id)
            tut_data = get_tutorial_request(clean_id) if not req_data else None

            if req_data:
                st.subheader(f"Status: {req_data.get('status', 'Unknown').upper()}")

                st.markdown("### 🚗 Vehicle Details")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(
                        f"**Vehicle:** {req_data.get('year')} "
                        f"{req_data.get('make')} {req_data.get('model')}"
                    )
                    st.write(f"**Mileage:** {req_data.get('mileage')}")
                    st.write(f"**Engine:** {req_data.get('engine_type')}")
                    if req_data.get('engine_capacity'):
                        st.write(f"**Engine Capacity:** {req_data.get('engine_capacity')}")
                    if req_data.get('engine_code'):
                        st.write(f"**Engine Code:** {req_data.get('engine_code')}")
                with col2:
                    if req_data.get('transmission_type'):
                        st.write(f"**Transmission:** {req_data.get('transmission_type')}")
                    if req_data.get('fuel_type'):
                        st.write(f"**Fuel Type:** {req_data.get('fuel_type')}")
                    if req_data.get('last_service_date'):
                        st.write(f"**Last Service:** {req_data.get('last_service_date')}")

                st.markdown("### 🔍 Reported Symptoms")
                symptoms = req_data.get('symptoms', {})
                if isinstance(symptoms, str):
                    st.markdown(f"**Description:**\n>{symptoms}")
                else:
                    for cat, icon in [
                        ('power', '⚡'), ('tactile', '👋'), ('audible', '🔊'),
                        ('fuel', '⛽'), ('visual', '👁️'), ('temperature', '🌡️'),
                    ]:
                        active = _fmt_symptoms(symptoms.get(cat, {}))
                        if active:
                            st.markdown(f"**{icon} {cat.title()}:** {', '.join(active)}")
                    if symptoms.get('additional_details'):
                        st.markdown(f"**📝 Additional Details:**\n>{symptoms['additional_details']}")

                if req_data.get('status') == 'completed':
                    st.markdown("---")
                    st.subheader("✅ Expert Diagnosis")
                    st.info(req_data.get('response'))
                    st.caption(f"Responded on: {req_data.get('response_timestamp')}")
                else:
                    st.info(
                        "Your request is currently being reviewed by an expert. "
                        "Please check back later."
                    )
            elif tut_data:
                st.subheader(f"Tutorial Status: {tut_data.get('status', 'Unknown').upper()}")

                st.markdown("### 🚗 Vehicle Details")
                st.write(f"**Vehicle:** {tut_data.get('year')} {tut_data.get('make')} {tut_data.get('model')}")

                st.markdown("### 🎥 Tutorial Request Details")
                st.write(f"**Description:** {tut_data.get('description')}")
                st.write(f"**Preferred Medium:** {tut_data.get('medium')}")

                if tut_data.get('status') == 'completed':
                    st.markdown("---")
                    st.subheader("✅ Expert Tutorial Response")
                    st.info(tut_data.get('response'))
                    st.caption(f"Responded on: {tut_data.get('response_timestamp')}")
                else:
                    st.info(
                        "Your custom tutorial request is currently being prepared by an expert. "
                        "Please check back later."
                    )
            else:
                st.error("Request ID not found. Please check and try again.")


# ---------------------------------------------------------------------------
# TAB 4: CUSTOM TUTORIAL
# ---------------------------------------------------------------------------
with tab4:
    st.header("Request a Custom Tutorial")
    st.markdown("Need a specific walkthrough? Request a custom instructional video or guide made just for your vehicle.")

    with st.form("tutorial_form"):
        st.subheader("Vehicle Details")
        col1, col2, col3 = st.columns(3)
        with col1:
            tut_make = st.selectbox("Car Make", AUSTRALIAN_MAKES, key="tut_make")
        with col2:
            tut_models = MODELS_BY_MAKE.get(tut_make, ["Select Model"])
            tut_model = st.selectbox("Car Model", tut_models, key="tut_model")
        with col3:
            current_year = 2025
            years = [0] + list(range(current_year, 1979, -1))
            tut_year = st.selectbox("Year", years, format_func=lambda x: "Select Year" if x == 0 else str(x), key="tut_year")

        st.subheader("Tutorial Details")
        tut_desc = st.text_area("What do you need a tutorial for?", height=150, placeholder="e.g. How to replace the cabin air filter, How to check transmission fluid level...")

        st.subheader("Preferred Medium")
        tut_medium = st.radio(
            "What format would be most helpful?",
            options=["Video", "Images", "Text/Instructions", "Whatever is most useful"],
            index=0
        )

        tut_submitted = st.form_submit_button("Submit Request")

    if tut_submitted:
        errors = validate_tutorial_request(tut_make, tut_model, tut_year, tut_desc, tut_medium)
        if errors:
            for error in errors:
                st.error(error)
        else:
            with st.spinner("Submitting request..."):
                request_data = {
                    "make": tut_make,
                    "model": tut_model,
                    "year": tut_year,
                    "description": tut_desc,
                    "medium": tut_medium,
                    "user_email": current_user['email'],
                }
                req_id = create_tutorial_request(request_data)
                st.success("Tutorial Request Submitted!")
                st.balloons()
                st.markdown(f"**Your Tutorial Request ID is:** `{req_id}`")
                st.warning("Please save this ID to check your tutorial status later.")
