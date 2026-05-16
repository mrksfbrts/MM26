import streamlit as st
import pandas as pd
import json
import hashlib
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="MM 2026 Veikkaus", layout="wide", page_icon="⚽")

st.markdown("""
    <style>
        .stApp { background-color: #0a0f1c; color: #e0e0e0; }
        h1 { color: #00ff9d; font-size: 2.8rem; font-weight: 700; }
        h2, h3 { color: #00cc77; }
        .stButton>button { 
            background-color: #00cc77; 
            color: black; 
            border-radius: 12px; 
            height: 52px; 
            font-weight: bold;
            width: 100%;
        }
        .stButton>button:hover { background-color: #00ff9d; }
        .prediction-box {
            background-color: #1e3a2f;
            padding: 10px 14px;
            border-radius: 8px;
            display: inline-block;
            margin: 6px 0;
            font-weight: bold;
        }
        .result-box {
            background-color: #3a2f1e;
            padding: 10px 14px;
            border-radius: 8px;
            display: inline-block;
            margin: 6px 0;
            font-weight: bold;
        }
        div[data-baseweb="input"] {
            max-width: 420px !important;
        }
        .etusivu_text {
            text-align: center;
            font-size: 5.2rem;
            font-weight: 800;
            color: #00ff9d;
            margin-top: 160px;
            text-shadow: 0 0 30px rgba(0, 255, 157, 0.5);
        }
    </style>
""", unsafe_allow_html=True)

# ====================== TIEDOSTOT ======================
USERS_FILE = "users.json"
PREDICTIONS_FILE = "predictions.json"
RESULTS_FILE = "real_results.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_json(file_path, default):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        st.toast("💾 Tallennettu", icon="✅")
    except:
        st.error("Tallennus epäonnistui")

users = load_json(USERS_FILE, {})
predictions = load_json(PREDICTIONS_FILE, {})
real_results = load_json(RESULTS_FILE, {})

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# ====================== 48 OTTELUA ======================
matches = [
    {"id": 1, "date": "2026-06-11", "time": "03:00", "home": "Meksiko", "away": "Etelä-Afrikka", "group": "A"},
    {"id": 2, "date": "2026-06-11", "time": "20:00", "home": "Etelä-Korea", "away": "Tšekki", "group": "A"},
    {"id": 3, "date": "2026-06-12", "time": "03:00", "home": "Kanada", "away": "Bosnia ja Hertsegovina", "group": "B"},
    {"id": 4, "date": "2026-06-12", "time": "20:00", "home": "Brasilia", "away": "Marokko", "group": "B"},
    {"id": 5, "date": "2026-06-13", "time": "03:00", "home": "USA", "away": "Paraguay", "group": "C"},
    {"id": 6, "date": "2026-06-13", "time": "20:00", "home": "Argentiina", "away": "Chile", "group": "C"},
    {"id": 7, "date": "2026-06-14", "time": "03:00", "home": "Ranska", "away": "Australia", "group": "D"},
    {"id": 8, "date": "2026-06-14", "time": "20:00", "home": "Englanti", "away": "Iran", "group": "D"},
    {"id": 9, "date": "2026-06-15", "time": "03:00", "home": "Espanja", "away": "Nigeria", "group": "E"},
    {"id": 10, "date": "2026-06-15", "time": "20:00", "home": "Portugali", "away": "Ghana", "group": "E"},
    {"id": 11, "date": "2026-06-16", "time": "03:00", "home": "Saksa", "away": "Japani", "group": "F"},
    {"id": 12, "date": "2026-06-16", "time": "20:00", "home": "Uruguay", "away": "Italia", "group": "F"},
    {"id": 13, "date": "2026-06-17", "time": "03:00", "home": "Alankomaat", "away": "Saudi-Arabia", "group": "G"},
    {"id": 14, "date": "2026-06-17", "time": "20:00", "home": "Tanska", "away": "Senegal", "group": "G"},
    {"id": 15, "date": "2026-06-18", "time": "03:00", "home": "Belgia", "away": "Panama", "group": "H"},
    {"id": 16, "date": "2026-06-18", "time": "20:00", "home": "Kroatia", "away": "Kolumbia", "group": "H"},
    {"id": 17, "date": "2026-06-19", "time": "03:00", "home": "Meksiko", "away": "Etelä-Korea", "group": "A"},
    {"id": 18, "date": "2026-06-19", "time": "20:00", "home": "Tšekki", "away": "Etelä-Afrikka", "group": "A"},
    {"id": 19, "date": "2026-06-20", "time": "03:00", "home": "Kanada", "away": "Brasilia", "group": "B"},
    {"id": 20, "date": "2026-06-20", "time": "20:00", "home": "Marokko", "away": "Bosnia ja Hertsegovina", "group": "B"},
    {"id": 21, "date": "2026-06-21", "time": "03:00", "home": "USA", "away": "Argentiina", "group": "C"},
    {"id": 22, "date": "2026-06-21", "time": "20:00", "home": "Chile", "away": "Paraguay", "group": "C"},
    {"id": 23, "date": "2026-06-22", "time": "03:00", "home": "Ranska", "away": "Englanti", "group": "D"},
    {"id": 24, "date": "2026-06-22", "time": "20:00", "home": "Iran", "away": "Australia", "group": "D"},
    {"id": 25, "date": "2026-06-23", "time": "03:00", "home": "Espanja", "away": "Portugali", "group": "E"},
    {"id": 26, "date": "2026-06-23", "time": "20:00", "home": "Ghana", "away": "Nigeria", "group": "E"},
    {"id": 27, "date": "2026-06-24", "time": "03:00", "home": "Saksa", "away": "Uruguay", "group": "F"},
    {"id": 28, "date": "2026-06-24", "time": "20:00", "home": "Italia", "away": "Japani", "group": "F"},
    {"id": 29, "date": "2026-06-25", "time": "03:00", "home": "Alankomaat", "away": "Tanska", "group": "G"},
    {"id": 30, "date": "2026-06-25", "time": "20:00", "home": "Senegal", "away": "Saudi-Arabia", "group": "G"},
    {"id": 31, "date": "2026-06-26", "time": "03:00", "home": "Belgia", "away": "Kroatia", "group": "H"},
    {"id": 32, "date": "2026-06-26", "time": "20:00", "home": "Kolumbia", "away": "Panama", "group": "H"},
    {"id": 33, "date": "2026-06-27", "time": "03:00", "home": "Etelä-Afrikka", "away": "Etelä-Korea", "group": "A"},
    {"id": 34, "date": "2026-06-27", "time": "20:00", "home": "Meksiko", "away": "Tšekki", "group": "A"},
    {"id": 35, "date": "2026-06-28", "time": "03:00", "home": "Bosnia ja Hertsegovina", "away": "Brasilia", "group": "B"},
    {"id": 36, "date": "2026-06-28", "time": "20:00", "home": "Kanada", "away": "Marokko", "group": "B"},
    {"id": 37, "date": "2026-06-29", "time": "03:00", "home": "Paraguay", "away": "Argentiina", "group": "C"},
    {"id": 38, "date": "2026-06-29", "time": "20:00", "home": "USA", "away": "Chile", "group": "C"},
    {"id": 39, "date": "2026-06-30", "time": "03:00", "home": "Australia", "away": "Englanti", "group": "D"},
    {"id": 40, "date": "2026-06-30", "time": "20:00", "home": "Ranska", "away": "Iran", "group": "D"},
    {"id": 41, "date": "2026-07-01", "time": "03:00", "home": "Nigeria", "away": "Portugali", "group": "E"},
    {"id": 42, "date": "2026-07-01", "time": "20:00", "home": "Espanja", "away": "Ghana", "group": "E"},
    {"id": 43, "date": "2026-07-02", "time": "03:00", "home": "Japani", "away": "Uruguay", "group": "F"},
    {"id": 44, "date": "2026-07-02", "time": "20:00", "home": "Saksa", "away": "Italia", "group": "F"},
    {"id": 45, "date": "2026-07-03", "time": "03:00", "home": "Saudi-Arabia", "away": "Tanska", "group": "G"},
    {"id": 46, "date": "2026-07-03", "time": "20:00", "home": "Alankomaat", "away": "Senegal", "group": "G"},
    {"id": 47, "date": "2026-07-04", "time": "03:00", "home": "Panama", "away": "Kroatia", "group": "H"},
    {"id": 48, "date": "2026-07-04", "time": "20:00", "home": "Belgia", "away": "Kolumbia", "group": "H"},
]

def get_countdown(match):
    match_time = datetime.strptime(f"{match['date']} {match['time']}", "%Y-%m-%d %H:%M")
    lock_time = match_time - timedelta(minutes=15)
    time_left = lock_time - datetime.now()
    if time_left.total_seconds() <= 0:
        return "🔴 Lukittu", False
    hours, rem = divmod(int(time_left.total_seconds()), 3600)
    minutes, _ = divmod(rem, 60)
    return f"⏳ {hours}t {minutes:02d}min jäljellä", True

def get_special_bets_countdown():
    first_match = matches[0]
    match_time = datetime.strptime(f"{first_match['date']} {first_match['time']}", "%Y-%m-%d %H:%M")
    lock_time = match_time - timedelta(minutes=15)
    time_left = lock_time - datetime.now()
    if time_left.total_seconds() <= 0:
        return "🔴 Erikoiskohteet sulkeutuneet", False
    hours, rem = divmod(int(time_left.total_seconds()), 3600)
    minutes, _ = divmod(rem, 60)
    return f"⏳ {hours}t {minutes:02d}min jäljellä", True

special_bets = [
    {"id": "most_goals", "name": "1. Mikä maa tekee alkulohkoissa eniten maaleja?", "points": 8},
    {"id": "most_cards", "name": "2. Mikä maa saa alkulohkoissa eniten varoituksia?", "points": 8},
    {"id": "group_a", "name": "3a. Lohko A voittaja", "points": 5},
    {"id": "group_b", "name": "3b. Lohko B voittaja", "points": 5},
    {"id": "group_c", "name": "3c. Lohko C voittaja", "points": 5},
    {"id": "group_d", "name": "3d. Lohko D voittaja", "points": 5},
    {"id": "group_e", "name": "3e. Lohko E voittaja", "points": 5},
    {"id": "group_f", "name": "3f. Lohko F voittaja", "points": 5},
    {"id": "group_g", "name": "3g. Lohko G voittaja", "points": 5},
    {"id": "group_h", "name": "3h. Lohko H voittaja", "points": 5},
    {"id": "top_scorer", "name": "4. Paras maalintekijä", "points": 12},
    {"id": "top_scorer_goals", "name": "5. Millä maalimäärällä voitetaan maalintekijäkuninkuus?", "points": 5},
    {"id": "champion", "name": "6. Maailmanmestari", "points": 12},
]

def calculate_match_points(pred, real):
    if not pred or not real:
        return 0
    p_home, p_away = pred
    r_home, r_away = real
    if p_home == r_home and p_away == r_away:
        return 8
    if p_home == p_away and r_home == r_away:
        return 8 if p_home == r_home and p_away == r_away else 5
    p_winner = 1 if p_home > p_away else 2 if p_away > p_home else 0
    r_winner = 1 if r_home > r_away else 2 if r_away > r_home else 0
    if p_winner == r_winner and p_winner != 0:
        if (p_home == r_home) or (p_away == r_away):
            return 5
        else:
            return 3
    return 0

# ====================== SIDEBAR ======================
if st.session_state.logged_in_user:
    st.sidebar.success(f"👤 {st.session_state.logged_in_user}")
    if st.sidebar.button("Kirjaudu ulos"):
        st.session_state.logged_in_user = None
        st.rerun()

page = st.sidebar.radio("Valikko", [
    "Etusivu",
    "Kirjaudu / Rekisteröidy",
    "VEIKKAA OTTELUITA",
    "VEIKKAA ERIKOISKOHTEITA",
    "Veikkaustilanne",
    "Omat veikkaukset",
    "Kaikkien veikkaukset",
    "Admin"
])

# ====================== ETUSIVU ======================
if page == "Etusivu":
    st.markdown('<div class="etusivu_text">MM26 - Veikkauskisa</div>', unsafe_allow_html=True)

# ====================== KIRJAUTUMINEN ======================
if page == "Kirjaudu / Rekisteröidy":
    tab1, tab2 = st.tabs(["Kirjaudu sisään", "Luo uusi käyttäjä"])
    with tab1:
        st.subheader("Kirjaudu sisään")
        username = st.text_input("Käyttäjänimi", key="login_username")
        password = st.text_input("Salasana", type="password", key="login_password")
        if st.button("Kirjaudu sisään", key="login_btn"):
            if username in users and users[username].get("password") == hash_password(password):
                st.session_state.logged_in_user = username
                st.success(f"Tervetuloa, {username}!")
                st.rerun()
            else:
                st.error("Väärä käyttäjänimi tai salasana")
    with tab2:
        st.subheader("Luo uusi käyttäjä")
        new_user = st.text_input("Käyttäjänimi", key="reg_username")
        new_pass = st.text_input("Salasana", type="password", key="reg_password")
        new_pass2 = st.text_input("Toista salasana", type="password", key="reg_password2")
        if st.button("Rekisteröidy", key="reg_btn"):
            if not new_user or not new_pass:
                st.error("Käyttäjänimi ja salasana ovat pakollisia")
            elif new_user in users:
                st.error("Käyttäjänimi on jo käytössä")
            elif new_pass != new_pass2:
                st.error("Salasanat eivät täsmää")
            else:
                users[new_user] = {"password": hash_password(new_pass), "created": str(datetime.now())}
                save_json(USERS_FILE, users)
                st.success(f"Käyttäjä **{new_user}** luotu!")

# ====================== VEIKKAA OTTELUITA ======================
if page == "VEIKKAA OTTELUITA":
    if not st.session_state.logged_in_user:
        st.warning("Kirjaudu ensin sisään!")
    else:
        user = st.session_state.logged_in_user
        st.subheader(f"Veikkaukset - {user}")
        for m in matches:
            countdown_text, is_open = get_countdown(m)
            st.write(f"**{m['date']} klo {m['time']}**")
            st.markdown(f"**{m['home']} — {m['away']}** (Lohko {m['group']})")
            st.write(countdown_text)
            if not is_open:
                st.divider()
                continue
            col1, col2, col3, col4 = st.columns([1.5, 1.2, 1.2, 4])
            with col2:
                home_pred = st.number_input("Koti", min_value=0, value=0, key=f"h_{m['id']}_{user}", label_visibility="collapsed")
            with col3:
                away_pred = st.number_input("Vieras", min_value=0, value=0, key=f"a_{m['id']}_{user}", label_visibility="collapsed")
            if st.button("Tallenna veikkaus", key=f"save_{m['id']}_{user}"):
                if user not in predictions:
                    predictions[user] = {}
                predictions[user][str(m['id'])] = (home_pred, away_pred)
                save_json(PREDICTIONS_FILE, predictions)
            st.divider()

# ====================== VEIKKAA ERIKOISKOHTEITA ======================
if page == "VEIKKAA ERIKOISKOHTEITA":
    if not st.session_state.logged_in_user:
        st.warning("Kirjaudu ensin sisään!")
    else:
        user = st.session_state.logged_in_user
        st.subheader(f"Veikkaa erikoiskohteita - {user}")
        countdown_text, is_open = get_special_bets_countdown()
        st.write(countdown_text)
        if not is_open:
            st.error("Erikoiskohteiden veikkaus on päättynyt, kun kisat alkoivat.")
        else:
            for bet in special_bets:
                st.markdown(f"**{bet['name']}** ({bet['points']} pistettä)")
                col_input, col_button = st.columns([2.8, 1.2])
                with col_input:
                    key = f"special_{bet['id']}_{user}"
                    value = st.text_input("Vastaus", key=key, label_visibility="collapsed")
                with col_button:
                    if st.button("Tallenna", key=f"save_{bet['id']}"):
                        if user not in predictions:
                            predictions[user] = {}
                        if "special" not in predictions[user]:
                            predictions[user]["special"] = {}
                        predictions[user]["special"][bet["id"]] = value.strip()
                        save_json(PREDICTIONS_FILE, predictions)
                        st.success("✅ Tallennettu!")
                st.divider()

# ====================== VEIKKAUSTILANNE ======================
if page == "Veikkaustilanne":
    st.subheader("🏆 Veikkauskisan tilanne")
    leaderboard = []
    for player in users.keys():
        total_points = 0
        for m in matches:
            pred = predictions.get(player, {}).get(str(m['id']))
            real = real_results.get("matches", {}).get(str(m['id']))
            total_points += calculate_match_points(pred, real)
        user_special = predictions.get(player, {}).get("special", {})
        real_special = real_results.get("special", {})
        for bet in special_bets:
            if bet["id"] in user_special and bet["id"] in real_special:
                user_ans = str(user_special[bet["id"]]).lower().strip()
                real_list = [x.strip().lower() for x in str(real_special[bet["id"]]).split(",")]
                if user_ans in real_list and user_ans:
                    total_points += bet["points"]
        leaderboard.append({"Sijoitus": "", "Nimi": player, "Pisteet": total_points})
    
    if leaderboard:
        df = pd.DataFrame(leaderboard).sort_values("Pisteet", ascending=False).reset_index(drop=True)
        df.index = df.index + 1
        df["Sijoitus"] = df.index
        column_config = {
            "Sijoitus": st.column_config.NumberColumn(width=80, alignment="center"),
            "Nimi": st.column_config.TextColumn(width=200),
            "Pisteet": st.column_config.NumberColumn(width=100, alignment="center")
        }
        st.dataframe(df[["Sijoitus", "Nimi", "Pisteet"]], use_container_width=False, column_config=column_config, hide_index=True)
    else:
        st.info("Ei vielä tuloksia")

# ====================== OMAT VEIKKAUKSET ======================
if page == "Omat veikkaukset":
    if not st.session_state.logged_in_user:
        st.warning("Kirjaudu ensin sisään!")
    else:
        user = st.session_state.logged_in_user
        st.subheader(f"Omat veikkaukset - {user}")
        st.write("### Otteluveikkaukset")
        for m in matches:
            pred = predictions.get(user, {}).get(str(m['id']))
            real = real_results.get("matches", {}).get(str(m['id']))
            st.write(f"**{m['home']} — {m['away']}**")
            if pred:
                st.markdown(f'<div class="prediction-box">Veikkaus: {pred[0]}–{pred[1]}</div>', unsafe_allow_html=True)
            else:
                st.write("Ei veikkausta")
            if real:
                points = calculate_match_points(pred, real)
                st.markdown(f'<div class="result-box">Tulos: {real[0]}–{real[1]} (+{points} pistettä)</div>', unsafe_allow_html=True)
            st.divider()

        st.write("### Erikoiskohteet")
        user_special = predictions.get(user, {}).get("special", {})
        real_special = real_results.get("special", {})
        for bet in special_bets:
            value = user_special.get(bet["id"], "Ei veikkausta")
            real_val = real_special.get(bet["id"])
            st.write(f"**{bet['name']}**")
            st.markdown(f'<div class="prediction-box">Veikkaus: {value}</div>', unsafe_allow_html=True)
            if real_val:
                user_ans = str(value).lower().strip()
                real_list = [x.strip().lower() for x in str(real_val).split(",")]
                points = bet["points"] if user_ans in real_list and user_ans else 0
                st.markdown(f'<div class="result-box">Toteutunut: {real_val} (+{points} pistettä)</div>', unsafe_allow_html=True)
            st.divider()

# ====================== KAIKKIEN VEIKKAUKSET ======================
if page == "Kaikkien veikkaukset":
    st.subheader("📋 Kaikkien osallistujien veikkaukset")
    if not real_results.get("matches") and not real_results.get("special"):
        st.info("Admin ei ole vielä syöttänyt tuloksia.")
    else:
        st.write("### Ottelut")
        for m in matches:
            real = real_results.get("matches", {}).get(str(m['id']))
            if not real: continue
            st.write(f"**{m['home']} — {m['away']}**")
            st.markdown(f'<div class="result-box">Tulos: {real[0]}–{real[1]}</div>', unsafe_allow_html=True)
            for player in sorted(users.keys()):
                pred = predictions.get(player, {}).get(str(m['id']))
                if pred:
                    points = calculate_match_points(pred, real)
                    st.write(f"**{player}**: {pred[0]}–{pred[1]} (+{points}p)")
                else:
                    st.write(f"**{player}**: ei veikkausta")
            st.divider()

        st.write("### Erikoiskohteet")
        real_special = real_results.get("special", {})
        for bet in special_bets:
            real_val = real_special.get(bet["id"])
            if not real_val: continue
            st.write(f"**{bet['name']}**")
            st.markdown(f'<div class="result-box">Toteutunut: {real_val}</div>', unsafe_allow_html=True)
            for player in sorted(users.keys()):
                value = predictions.get(player, {}).get("special", {}).get(bet["id"], "Ei veikkausta")
                user_ans = str(value).lower().strip()
                real_list = [x.strip().lower() for x in str(real_val).split(",")]
                points = bet["points"] if user_ans in real_list and user_ans else 0
                st.write(f"**{player}**: {value} (+{points}p)")
            st.divider()

# ====================== ADMIN ======================
if page == "Admin":
    pw = st.text_input("Admin-salasana", type="password")
    if pw == "admin123":
        st.success("✅ Admin auki")
        tab1, tab2 = st.tabs(["Ottelutulokset", "Erikoiskohteet"])
        with tab1:
            for m in matches:
                st.write(f"{m['home']} — {m['away']}")
                c1, c2 = st.columns(2)
                with c1: h = st.number_input("Koti", min_value=0, key=f"rh_{m['id']}")
                with c2: a = st.number_input("Vieras", min_value=0, key=f"ra_{m['id']}")
                if st.button("Tallenna tulos", key=f"save_match_{m['id']}"):
                    if "matches" not in real_results:
                        real_results["matches"] = {}
                    real_results["matches"][str(m['id'])] = (h, a)
                    save_json(RESULTS_FILE, real_results)
                st.divider()
        with tab2:
            for bet in special_bets:
                st.write(f"**{bet['name']}**")
                val = st.text_input("Hyväksytyt vastaukset (pilkulla eroteltuna)", key=f"admin_{bet['id']}")
                if st.button("Tallenna", key=f"save_admin_{bet['id']}"):
                    if "special" not in real_results:
                        real_results["special"] = {}
                    real_results["special"][bet["id"]] = val
                    save_json(RESULTS_FILE, real_results)
    elif pw:
        st.error("Väärä admin-salasana")

