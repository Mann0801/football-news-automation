#!/usr/bin/env python3
"""
Football Daily Digest Agent
Sends match scores from the previous day for top leagues.
"""

import smtplib
import requests
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import (
    FOOTBALL_DATA_API_KEY,
    GMAIL_APP_PASSWORD,
    GMAIL_ADDRESS,
    RECIPIENT_EMAIL,
    LEAGUE_IDS,
    EMAIL_SUBJECT_PREFIX
)


def get_yesterday_date():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def fetch_match_scores(api_key, league_id, date):
    url = f"https://api.football-data.org/v4/competitions/{league_id}/matches"
    params = {
        "dateFrom": date,
        "dateTo": date,
        "status": "FINISHED"
    }
    headers = {"X-Auth-Token": api_key}
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json().get("matches", [])


def format_match_score(match):
    home_team = match["homeTeam"]["shortName"]
    away_team = match["awayTeam"]["shortName"]
    home_score = match["score"]["fullTime"]["home"]
    away_score = match["score"]["fullTime"]["away"]
    kickoff = match.get("utcDate", "")
    if kickoff:
        try:
            kickoff_time = datetime.fromisoformat(kickoff.replace("Z", "+00:00"))
            time_str = kickoff_time.strftime("%H:%M")
        except:
            time_str = ""
    else:
        time_str = ""
    
    return {
        "home": home_team,
        "away": away_team,
        "home_score": home_score if home_score is not None else 0,
        "away_score": away_score if away_score is not None else 0,
        "time": time_str
    }


def format_html_email(all_scores, date_str):
    league_emojis = {
        "Premier League": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "Champions League": "🏆",
        "La Liga": "🇪🇸"
    }
    
    league_colors = {
        "Premier League": "#3d195b",
        "Champions League": "#1a472a",
        "La Liga": "#ee8707"
    }
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #1a472a, #2d5a3f); color: white; padding: 30px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 24px; }}
            .header p {{ margin: 10px 0 0; opacity: 0.9; font-size: 14px; }}
            .content {{ padding: 20px; }}
            .league-section {{ margin-bottom: 30px; }}
            .league-title {{ font-size: 18px; font-weight: bold; color: white; margin-bottom: 15px; padding: 10px 15px; border-radius: 8px; }}
            .match-row {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; background: #f9f9f9; margin-bottom: 8px; border-radius: 6px; }}
            .team {{ font-size: 14px; font-weight: 500; color: #333; min-width: 100px; }}
            .team-home {{ text-align: left; }}
            .team-away {{ text-align: right; }}
            .score {{ font-size: 20px; font-weight: bold; color: #333; min-width: 60px; text-align: center; }}
            .score-wrapper {{ display: flex; align-items: center; justify-content: center; gap: 10px; flex: 1; }}
            .vs {{ font-size: 12px; color: #888; }}
            .time {{ font-size: 11px; color: #888; margin-top: 2px; text-align: center; }}
            .no-matches {{ color: #999; font-style: italic; text-align: center; padding: 20px; }}
            .footer {{ background: #f5f5f5; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚽ Football Match Results</h1>
                <p>{date_str}</p>
            </div>
            <div class="content">
    """
    
    for league_name, matches in all_scores.items():
        color = league_colors.get(league_name, "#1a472a")
        emoji = league_emojis.get(league_name, "⚽")
        html += f'<div class="league-section">'
        html += f'<div class="league-title" style="background: {color};"><span>{emoji}</span> {league_name}</div>'
        
        if matches:
            for match in matches:
                html += f'''
                <div class="match-row">
                    <div class="team team-home">{match["home"]}</div>
                    <div class="score-wrapper">
                        <span class="score">{match["home_score"]}</span>
                        <span class="vs">-</span>
                        <span class="score">{match["away_score"]}</span>
                    </div>
                    <div class="team team-away">{match["away"]}</div>
                </div>
                '''
        else:
            html += '<div class="no-matches">No matches played yesterday</div>'
        
        html += '</div>'
    
    html += f"""
            </div>
            <div class="footer">
                <p>⚽ Football Daily Digest | Powered by Football-Data.org</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


def send_email(subject, html_content, to_email):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = to_email
    
    part = MIMEText(html_content, "html")
    msg.attach(part)
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())


def validate_config():
    missing = []
    if not FOOTBALL_DATA_API_KEY or FOOTBALL_DATA_API_KEY == "your_football_data_key_here":
        missing.append("FOOTBALL_DATA_API_KEY")
    if not GMAIL_APP_PASSWORD or GMAIL_APP_PASSWORD == "your_gmail_app_password_here":
        missing.append("GMAIL_APP_PASSWORD")
    if not GMAIL_ADDRESS or GMAIL_ADDRESS == "your_email@gmail.com":
        missing.append("GMAIL_ADDRESS")
    
    if missing:
        print(f"❌ Missing configuration: {', '.join(missing)}")
        print("   Please update your .env file.")
        return False
    return True


def main():
    print("⚽ Football Daily Digest Agent")
    print("=" * 40)
    
    if not validate_config():
        return
    
    yesterday = get_yesterday_date()
    date_display = datetime.strptime(yesterday, "%Y-%m-%d").strftime("%B %d, %Y")
    
    print(f"📅 Fetching match results for: {date_display}")
    
    all_scores = {}
    
    try:
        for league_name, league_id in LEAGUE_IDS.items():
            print(f"🔍 Fetching {league_name}...")
            matches = fetch_match_scores(FOOTBALL_DATA_API_KEY, league_id, yesterday)
            scores = [format_match_score(m) for m in matches]
            all_scores[league_name] = scores
            print(f"   Found {len(scores)} matches")
        
        total_matches = sum(len(m) for m in all_scores.values())
        print(f"📊 Total matches: {total_matches}")
        
        print("📧 Creating email...")
        subject = f"{EMAIL_SUBJECT_PREFIX} Match Results - {date_display}"
        html_email = format_html_email(all_scores, date_display)
        
        print(f"📤 Sending email to: {RECIPIENT_EMAIL}")
        send_email(subject, html_email, RECIPIENT_EMAIL)
        
        print("✅ Success! Email sent.")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
