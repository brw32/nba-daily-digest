# NBA Daily Scoring Digest

Automatically sends an email digest with the top 3 scorers from each NBA game (preseason and regular season) every morning at 7am Eastern Time.

## 🏀 What You'll Receive

Each morning at 7am ET, you'll get an email like this:

```
NBA SCORING DIGEST - October 13, 2025
============================================================

PRESEASON GAMES
------------------------------------------------------------

MIA 115 @ ATL 120 (Preseason)

ATL Top Scorers:
  1. Trae Young - 28 pts
  2. Dejounte Murray - 24 pts
  3. Clint Capela - 16 pts

MIA Top Scorers:
  1. Tyler Herro - 22 pts
  2. Bam Adebayo - 19 pts
  3. Jimmy Butler - 18 pts

SAS 125 @ IND 118 (Preseason)

IND Top Scorers:
  1. Tyrese Haliburton - 26 pts
  2. Myles Turner - 20 pts
  3. Bennedict Mathurin - 17 pts

SAS Top Scorers:
  1. Victor Wembanyama - 31 pts
  2. Devin Vassell - 23 pts
  3. Keldon Johnson - 19 pts

REGULAR SEASON GAMES
------------------------------------------------------------

BOS 120 @ NYK 115 (Regular Season)

NYK Top Scorers:
  1. Jalen Brunson - 32 pts
  2. Julius Randle - 24 pts
  3. RJ Barrett - 19 pts

BOS Top Scorers:
  1. Jayson Tatum - 35 pts
  2. Jaylen Brown - 27 pts
  3. Derrick White - 16 pts

============================================================
This digest is automatically generated daily at 7:00 AM ET
```

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)

Run the setup script:
```bash
bash setup_nba_digest.sh
```

Follow the prompts to:
1. Install required packages
2. Configure your Gmail credentials
3. Test the script
4. Schedule daily emails at 7am ET

### Option 2: Manual Setup

#### Step 1: Install Requirements
```bash
pip3 install requests pytz
```

#### Step 2: Configure Email Credentials

You need a Gmail account to send emails. For security, use a Gmail App Password:

1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to https://myaccount.google.com/apppasswords
4. Create app password for "Mail"
5. Save the 16-character password

Set environment variables:
```bash
export SENDER_EMAIL='your-email@gmail.com'
export EMAIL_PASSWORD='your-app-password'
```

#### Step 3: Test the Script
```bash
python3 nba_digest.py
```

#### Step 4: Schedule Daily Execution

Add to crontab (runs at 7am ET):
```bash
crontab -e
```

Add this line:
```
0 11 * * * cd /path/to/script && source .env && python3 nba_digest.py >> nba_digest.log 2>&1
```

Note: 11:00 UTC = 7:00am ET (accounting for DST)

## 📋 Files Included

- **nba_digest.py** - Main Python script that fetches games and sends emails
- **setup_nba_digest.sh** - Automated setup script
- **README.md** - This documentation file

## 🔧 How It Works

1. **Daily Trigger**: Cron job runs at 7am ET every day
2. **Fetch Games**: Retrieves all NBA games from yesterday using NBA Stats API
3. **Get Scores**: Fetches box scores for each game
4. **Extract Top 3**: Identifies the 3 highest scorers per game
5. **Format Email**: Creates formatted digest separating preseason/regular season
6. **Send Email**: Delivers digest to cardbazaar32@gmail.com

## 🎯 Features

✅ Separate sections for preseason and regular season games  
✅ Top 3 scorers from EACH TEAM in each game  
✅ Player names and point totals clearly organized by team  
✅ Final scores for each game  
✅ Automatic daily delivery at 7am ET  
✅ Error handling and logging  

## 🔍 Monitoring

### Check if it's running:
```bash
crontab -l
```

### View logs:
```bash
tail -f nba_digest.log
```

### Test manually:
```bash
python3 nba_digest.py
```

## ⚠️ Troubleshooting

### No email received?

1. **Check cron job is active**:
   ```bash
   crontab -l | grep nba_digest
   ```

2. **Check logs**:
   ```bash
   cat nba_digest.log
   ```

3. **Verify credentials**:
   ```bash
   source .env
   echo $SENDER_EMAIL
   ```

4. **Test manually**:
   ```bash
   python3 nba_digest.py
   ```

### Email authentication errors?

- Make sure you're using a Gmail App Password, not your regular password
- Verify 2-Step Verification is enabled on your Google account
- Check that "Less secure app access" is NOT enabled (use App Passwords instead)

### No games shown?

- This is normal on off-days when no NBA games are played
- Preseason has fewer games than regular season
- The script fetches games from yesterday, so check the date

### API errors?

The NBA Stats API may occasionally be unavailable. The script will:
- Log the error
- Send a notification email
- Automatically retry the next day

## 🔐 Security Notes

- Email credentials are stored in `.env` file with restricted permissions (600)
- Never commit `.env` file to version control
- Use Gmail App Passwords, never your main password
- The script only reads NBA public data (no authentication required)

## 📅 NBA Season Information

- **Preseason**: October 4-20, 2025
- **Regular Season**: October 21, 2025 - April 12, 2026
- **Playoffs**: April 15 - June 2026

The digest will automatically include games from whichever portion of the season is active.

## 🛠️ Customization

### Change email time:
Edit the cron schedule (currently `0 11 * * *` for 7am ET)

### Change recipient:
Edit `RECIPIENT_EMAIL` in `nba_digest.py`

### Show more/fewer scorers per team:
Change `scorers[:3]` in the `parse_top_scorers()` function to show more or fewer players per team

### Add more stats:
Modify the API request in `get_box_score()` to include additional stats like rebounds, assists, etc.

## 📞 Support

For issues with:
- **NBA data**: Check https://stats.nba.com/
- **Gmail sending**: Check https://support.google.com/mail/
- **Cron scheduling**: Run `man cron` or check system logs

## 📜 License

This script is for personal use. NBA data is owned by the NBA.

---

**Enjoy your daily NBA scoring digest!** 🏀
