import random
import urllib.request
import urllib.parse
import os
from datetime import datetime
import pytz

# ===== TELEGRAM CONFIG =====
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ===== TEAMS =====
teams = {
    "MI": ("Mumbai Indians", "Hardik Pandya"),
    "CSK": ("Chennai Super Kings", "Ruturaj Gaikwad"),
    "RCB": ("Royal Challengers Bangalore", "Rajat Patidar"),
    "KKR": ("Kolkata Knight Riders", "Ajinkya Rahane"),
    "SRH": ("Sunrisers Hyderabad", "Pat Cummins"),
    "DC": ("Delhi Capitals", "Axar Patel"),
    "LSG": ("Lucknow Super Giants", "Rishabh Pant"),
    "GT": ("Gujarat Titans", "Shubman Gill"),
    "RR": ("Rajasthan Royals", "Riyan Parag"),
    "PBKS": ("Punjab Kings", "Shreyas Iyer")
}

# ===== SCHEDULE =====
schedule = [
    {"team1": "SRH", "team2": "KKR", "date": "2026-05-03"},
    {"team1": "GT", "team2": "PBKS", "date": "2026-05-03"},
    {"team1": "MI", "team2": "LSG", "date": "2026-05-04"},
    {"team1": "CSK", "team2": "SRH", "date": "2026-05-18"},
]

# ===== FUNCTIONS =====
def name_value(name):
    return sum(ord(ch) - 64 for ch in name.upper() if ch.isalpha())

def single_digit(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def send_telegram(msg):
    try:
        params = urllib.parse.urlencode({
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        })
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?{params}"
        urllib.request.urlopen(url)
    except Exception as e:
        print("Telegram Error:", e)

# ===== TODAY (IST TIMEZONE) =====
ist = pytz.timezone('Asia/Kolkata')
today = datetime.now(ist).strftime("%Y-%m-%d")

# ===== MAIN =====
found_match = False

for match in schedule:

    if match["date"] != today:
        continue

    found_match = True

    team1 = match["team1"]
    team2 = match["team2"]

    team1_full, captain1 = teams[team1]
    team2_full, captain2 = teams[team2]

    total1 = name_value(captain1)
    total2 = name_value(captain2)

    digit1 = single_digit(total1)
    digit2 = single_digit(total2)

    winner = random.choice([
        (team1_full, captain1, digit1),
        (team2_full, captain2, digit2)
    ])

    # ===== FORMAT DATE =====
    match_date = datetime.strptime(match["date"], "%Y-%m-%d").strftime("%A, %d %b %Y")

    # ===== MESSAGE =====
    message = f"""🏆 *IPL 2026 – Toss Prediction*

🗓 Date: {match_date}

🏏 Match
☆{team1_full} vs {team2_full}☆

👥 Captains:
👤 {captain1} → {total1} ➝ {digit1}
👤 {captain2} → {total2} ➝ {digit2}

━━━━━━━━━━━━━━━━━━━
🎯 Toss Winner
✨ *{winner[0].upper()}* ✨
━━━━━━━━━━━━━━━━━━━
"""

    send_telegram(message)

# ===== NO MATCH MESSAGE =====
if not found_match:
    send_telegram("❌ No IPL matches scheduled for today")
