"""
NBA Daily Scoring Digest
Automated email delivery of fantasy basketball performance for tracked players

Fetches previous day's NBA games from ESPN API, calculates fantasy scores,
and sends formatted email digest.
"""

import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pytz
import time

# ===== CONFIGURATION =====
# TODO: Move these to a config file or environment variables

# Email settings
SMTP_SERVER = "smtp.gmail.com"  # Change to your SMTP server
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"  # Your email address
SENDER_PASSWORD = "your-app-password"  # Your email app password
RECIPIENT_EMAIL = "recipient@email.com"  # Digest recipient

# Player tracking list
# Add the players you want to track (use full names as they appear on ESPN)
TRACKED_PLAYERS = [
    "LeBron James",
    "Stephen Curry",
    "Giannis Antetokounmpo",
    "Luka Dončić",
    "Joel Embiid",
    "Jayson Tatum",
    "Kevin Durant",
    "Anthony Davis",
    # Add more players here
]

# Fantasy scoring rules
SCORING = {
    'points': 1.0,
    'rebounds': 1.2,
    'assists': 1.5,
    'steals': 3.0,
    'blocks': 3.0,
    'turnovers': -1.0
}

# ESPN API endpoint
ESPN_API_BASE = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"


def get_yesterday_games():
    """
    Fetch yesterday's NBA games from ESPN API
    Returns list of game data
    """
    # Get yesterday's date in Eastern Time (NBA operates on ET)
    et_tz = pytz.timezone('US/Eastern')
    now_et = datetime.now(et_tz)
    yesterday_et = now_et - timedelta(days=1)
    date_str = yesterday_et.strftime('%Y%m%d')
    
    url = f"{ESPN_API_BASE}/scoreboard?dates={date_str}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('events', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching games: {e}")
        return []


def extract_player_stats(game_data):
    """
    Extract statistics for tracked players from game data
    Returns dict of player stats
    """
    player_stats = {}
    
    # ESPN API structure: game -> competitions -> competitors -> team -> athletes
    try:
        for competition in game_data.get('competitions', []):
            for competitor in competition.get('competitors', []):
                team_name = competitor.get('team', {}).get('abbreviation', '')
                
                # Get roster with stats
                if 'roster' in competitor:
                    for athlete in competitor['roster']:
                        player_name = athlete.get('athlete', {}).get('displayName', '')
                        
                        if player_name in TRACKED_PLAYERS:
                            stats = athlete.get('stats', {})
                            player_stats[player_name] = {
                                'team': team_name,
                                'points': float(stats.get('points', 0)),
                                'rebounds': float(stats.get('rebounds', 0)),
                                'assists': float(stats.get('assists', 0)),
                                'steals': float(stats.get('steals', 0)),
                                'blocks': float(stats.get('blocks', 0)),
                                'turnovers': float(stats.get('turnovers', 0))
                            }
    except Exception as e:
        print(f"Error extracting player stats: {e}")
    
    return player_stats


def calculate_fantasy_score(stats):
    """
    Calculate fantasy score based on player stats and scoring rules
    """
    score = 0.0
    for stat, value in stats.items():
        if stat in SCORING and stat != 'team':
            score += value * SCORING[stat]
    return round(score, 1)


def format_digest(player_stats, game_count, game_date):
    """
    Format player statistics into readable email digest
    """
    if not player_stats:
        return f"No games found for tracked players on {game_date}"
    
    # Calculate fantasy scores
    for player, stats in player_stats.items():
        stats['fantasy_pts'] = calculate_fantasy_score(stats)
    
    # Sort by fantasy points
    sorted_players = sorted(player_stats.items(), 
                          key=lambda x: x[1]['fantasy_pts'], 
                          reverse=True)
    
    # Build email content
    lines = []
    lines.append(f"NBA Daily Digest - {datetime.now().strftime('%B %d, %Y')}")
    lines.append(f"Games from: {game_date}")
    lines.append("")
    lines.append("=" * 60)
    lines.append(f"Yesterday's Games: {game_count}")
    lines.append("=" * 60)
    lines.append("")
    lines.append("YOUR PLAYERS - FANTASY PERFORMANCE")
    lines.append("")
    lines.append("-" * 60)
    lines.append(f"{'Player':<20} {'Team':<5} {'PTS':>4} {'REB':>4} {'AST':>4} {'STL':>4} {'BLK':>4} {'FAN PTS':>8}")
    lines.append("-" * 60)
    
    total_fantasy = 0.0
    for player, stats in sorted_players:
        lines.append(
            f"{player:<20} {stats['team']:<5} "
            f"{int(stats['points']):>4} {int(stats['rebounds']):>4} "
            f"{int(stats['assists']):>4} {int(stats['steals']):>4} "
            f"{int(stats['blocks']):>4} {stats['fantasy_pts']:>8.1f}"
        )
        total_fantasy += stats['fantasy_pts']
    
    lines.append("-" * 60)
    lines.append("")
    lines.append("TEAM SUMMARY")
    lines.append("=" * 60)
    lines.append(f"Total Fantasy Points:     {total_fantasy:.1f}")
    lines.append(f"Average per Player:       {total_fantasy/len(player_stats):.1f}")
    lines.append(f"Top Performer:            {sorted_players[0][0]} ({sorted_players[0][1]['fantasy_pts']:.1f} pts)")
    
    # Count high performers
    high_performers = sum(1 for _, stats in player_stats.items() 
                         if stats['fantasy_pts'] >= 50)
    lines.append(f"Games with 50+ pts:       {high_performers} of {len(player_stats)} players")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def send_email(subject, body):
    """
    Send email digest via SMTP
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        print(f"Email sent successfully to {RECIPIENT_EMAIL}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def main():
    """
    Main execution function
    """
    print("NBA Daily Digest - Starting...")
    print(f"Timestamp: {datetime.now()}")
    
    # Get yesterday's games
    games = get_yesterday_games()
    
    if not games:
        print("No games found for yesterday")
        return
    
    print(f"Found {len(games)} games")
    
    # Extract player stats from all games
    all_player_stats = {}
    for game in games:
        game_stats = extract_player_stats(game)
        all_player_stats.update(game_stats)
    
    if not all_player_stats:
        print("No tracked players found in yesterday's games")
        return
    
    print(f"Found stats for {len(all_player_stats)} tracked players")
    
    # Format digest
    et_tz = pytz.timezone('US/Eastern')
    yesterday_et = datetime.now(et_tz) - timedelta(days=1)
    game_date = yesterday_et.strftime('%B %d, %Y')
    
    digest_body = format_digest(all_player_stats, len(games), game_date)
    
    # Send email
    subject = f"NBA Daily Digest - {game_date}"
    send_email(subject, digest_body)
    
    print("NBA Daily Digest - Complete")


if __name__ == "__main__":
    main()
