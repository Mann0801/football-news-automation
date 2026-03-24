# Football Daily Digest

Automated daily email summarizing football news from Premier League, Champions League, and La Liga.

## Prerequisites

- Python 3.7+
- Gmail account with 2FA enabled
- NewsAPI free account

## Setup

### 1. Get NewsAPI Key

1. Go to [newsapi.org](https://newsapi.org)
2. Click "Get API Key"
3. Copy your API key

### 2. Setup Gmail App Password

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if not already enabled
3. Go to **App passwords** (search for it in the search bar)
4. Select "Mail" and "Other (Custom name)"
5. Enter "Football Digest" and click Generate
6. Copy the 16-character password

### 3. Configure the Script

```bash
cd football-digest
cp .env.example .env
```

Edit `.env`:
```
NEWS_API_KEY=your_newsapi_key_here
GMAIL_APP_PASSWORD=your_16_char_app_password
GMAIL_ADDRESS=your_email@gmail.com
RECIPIENT_EMAIL=your_email@gmail.com
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Test It

```bash
python football_digest.py
```

You should receive an email shortly.

## Schedule Daily (Linux/Mac)

### Option A: Cron

```bash
crontab -e
```

Add this line:
```
0 7 * * * /usr/bin/python3 /full/path/to/football-digest/football_digest.py >> /full/path/to/football-digest/digest.log 2>&1
```

### Option B: Task Scheduler (macOS)

1. Open System Settings → General → Login Items & Extensions → Scheduled Apps (or search "Schedule")
2. Click "+" and select the python3 executable
3. Add arguments: `/full/path/to/football-digest/football_digest.py`
4. Set frequency to daily at 7:00 AM

### Option C: Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task → Name it "Football Daily Digest"
3. Trigger: Daily at 7:00 AM
4. Action: Start a program
5. Program: `python`
6. Arguments: `football_digest.py`
7. Start in: `C:\path\to\football-digest\`

## Project Structure

```
football-digest/
├── football_digest.py    # Main script
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── .env.example          # Template for credentials
└── README.md             # This file
```

## Troubleshooting

### "Authentication failed" error
- Make sure you used **App Password**, not your regular Gmail password
- Verify 2FA is enabled on your Google account

### "NewsAPI key not valid"
- Check your API key at [newsapi.org](https://newsapi.org)
- Free tier only works on localhost (127.0.0.1)

### No articles found
- NewsAPI free tier may have rate limits
- Check your internet connection
- Verify the date format in logs

### Gmail blocking
- Go to [myaccount.google.com/permissions](https://myaccount.google.com/permissions)
- Check if "Less secure app access" is needed (shouldn't be with App Password)

## Customization

### Change leagues in `config.py`:
```python
LEAGUES = {
    "Your League": ["team1", "team2", "league keyword"]
}
```

### Change email styling in `football_digest.py`:
Look for the `format_html_email` function and edit the HTML/CSS.

### Change timing:
Update the cron expression `0 7 * * *`:
- `0 8` = 8:00 AM
- `30 7` = 7:30 AM
- `0 7 * * 1-5` = Weekdays only at 7 AM

