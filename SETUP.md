# Setup Instructions

## Prerequisites

- Python 3.7 or higher
- Gmail account (or other SMTP email provider)
- Internet connection for ESPN API access

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/brw32/nba-daily-digest.git
cd nba-daily-digest
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Email Setup

Edit `nba_digest_espn.py` and update these variables:

```python
SMTP_SERVER = "smtp.gmail.com"  # Your SMTP server
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password"  # See note below
RECIPIENT_EMAIL = "recipient@email.com"
```

**Gmail Users:** You need an "App Password", not your regular password:
1. Go to Google Account settings
2. Security → 2-Step Verification (must be enabled)
3. App passwords → Generate new app password
4. Use this 16-character password in the script

**Other Email Providers:**
- Outlook: `smtp-mail.outlook.com`, port 587
- Yahoo: `smtp.mail.yahoo.com`, port 587
- Custom SMTP: Contact your email provider

### 2. Player Tracking

Update the `TRACKED_PLAYERS` list with players you want to track:

```python
TRACKED_PLAYERS = [
    "LeBron James",
    "Stephen Curry",
    "Your Player Name Here",
]
```

**Important:** Use exact names as they appear on ESPN

### 3. Fantasy Scoring (Optional)

Customize scoring rules in the `SCORING` dictionary:

```python
SCORING = {
    'points': 1.0,      # 1 point per point scored
    'rebounds': 1.2,    # 1.2 points per rebound
    'assists': 1.5,     # 1.5 points per assist
    'steals': 3.0,      # 3 points per steal
    'blocks': 3.0,      # 3 points per block
    'turnovers': -1.0   # -1 point per turnover
}
```

## Running the Script

### Manual Execution

```bash
python nba_digest_espn.py
```

The script will:
1. Fetch yesterday's NBA games
2. Find your tracked players
3. Calculate fantasy scores
4. Send email digest

### Automated Daily Execution

#### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "NBA Daily Digest"
4. Trigger: Daily at 7:00 AM
5. Action: Start a program
   - Program: `C:\Python\python.exe` (your Python path)
   - Arguments: `C:\path\to\nba_digest_espn.py`
6. Finish

#### Mac/Linux (cron)

```bash
crontab -e
```

Add this line (runs at 7:00 AM daily):
```
0 7 * * * /usr/bin/python3 /path/to/nba_digest_espn.py
```

## Testing

1. **Test email configuration:**
   ```python
   # Add this to the bottom of nba_digest_espn.py
   send_email("Test", "This is a test email")
   ```

2. **Test with specific date:**
   - Modify the `date_str` in `get_yesterday_games()` to a known game day
   - Example: `date_str = "20241205"` for Dec 5, 2024

3. **Check for games:**
   ```python
   games = get_yesterday_games()
   print(f"Found {len(games)} games")
   ```

## Troubleshooting

### No email received
- Check spam folder
- Verify SMTP credentials
- Test SMTP connection manually
- Check firewall/antivirus blocking port 587

### No players found
- Verify player names match ESPN exactly
- Check that games occurred yesterday
- View ESPN API response: `print(games)` after `get_yesterday_games()`

### Wrong day's games
- Script uses Eastern Time (NBA standard)
- Run script after midnight ET for previous day's games
- For morning emails, schedule for 7:00 AM or later

### API errors
- ESPN API is free but may have rate limits
- Add retry logic if needed
- Check internet connection

## Security Notes

**NEVER commit credentials to GitHub:**
- Use environment variables: `os.getenv('EMAIL_PASSWORD')`
- Use a separate `config.py` (add to `.gitignore`)
- Use app passwords, not main account passwords

## Support

For issues or questions, check:
- ESPN API documentation
- Python smtplib documentation
- pytz timezone documentation

Built by Brian Wittig | github.com/brw32
