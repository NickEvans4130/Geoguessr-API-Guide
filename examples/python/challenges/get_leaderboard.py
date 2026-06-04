"""
Get Challenge Leaderboard

Retrieves and displays the leaderboard for a specific challenge.

Usage:
    python get_leaderboard.py

Requirements:
    pip install requests
"""

import requests
import os
from datetime import datetime


def get_challenge_leaderboard(challenge_token, cookie):
    """
    Fetch and display challenge leaderboard.

    Args:
        challenge_token (str): The challenge token/ID
        cookie (str): Your _ncfa cookie value

    Returns:
        list: List of leaderboard entries
    """
    try:
        url = f'https://www.geoguessr.com/api/v3/results/highscores/{challenge_token}'

        response = requests.get(url, cookies={'_ncfa': cookie})
        response.raise_for_status()

        data = response.json()

        # Extract and format leaderboard
        leaderboard = []
        for index, item in enumerate(data['items']):
            player = item['game']['player']
            leaderboard.append({
                'rank': index + 1,
                'username': player['nick'],
                'score': int(player['totalScore']['amount']),
                'is_pro': player['isProUser'],
                'country': player['countryCode'],
                'played_at': datetime.fromisoformat(
                    item['game']['created'].replace('Z', '+00:00')
                ).strftime('%Y-%m-%d %H:%M:%S')
            })

        # Display results
        print(f"\n🏆 Challenge Leaderboard ({len(data['items'])} players)\n")
        print(f"{'Rank':<6} {'Username':<20} {'Score':<10} {'Pro':<5} {'Country'}")
        print("-" * 60)

        for entry in leaderboard[:20]:  # Show top 20
            pro_indicator = "✓" if entry['is_pro'] else " "
            print(f"{entry['rank']:<6} {entry['username']:<20} "
                  f"{entry['score']:<10,} {pro_indicator:<5} {entry['country']}")

        # Statistics
        total_players = len(leaderboard)
        avg_score = sum(p['score'] for p in leaderboard) / total_players
        top_score = leaderboard[0]['score'] if leaderboard else 0

        print(f"\n📊 Statistics:")
        print(f"Total Players: {total_players}")
        print(f"Average Score: {avg_score:,.0f}")
        print(f"Top Score: {top_score:,}")
        print(f"Winner: {leaderboard[0]['username']}")

        return leaderboard

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return None


def main():
    # Get credentials from environment variables
    cookie = os.getenv('GEOGUESSR_COOKIE')
    if not cookie:
        print("❌ Error: GEOGUESSR_COOKIE environment variable not set")
        print("Set it with: export GEOGUESSR_COOKIE='your_cookie_value'")
        return

    # Example challenge token (replace with your own)
    challenge_token = input("Enter challenge token (or URL): ").strip()

    # Extract token from URL if full URL provided
    if '/' in challenge_token:
        challenge_token = challenge_token.split('/')[-1]

    # Fetch leaderboard
    leaderboard = get_challenge_leaderboard(challenge_token, cookie)

    if leaderboard:
        print("\n✅ Successfully retrieved leaderboard!")


if __name__ == '__main__':
    main()
