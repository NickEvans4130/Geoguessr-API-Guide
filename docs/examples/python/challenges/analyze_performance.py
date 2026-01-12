"""
Analyze Challenge Performance

Compares your score to the leaderboard and shows your ranking.

Usage:
    python analyze_performance.py

Requirements:
    pip install requests
"""

import requests
import os
import statistics


def analyze_performance(challenge_token, cookie):
    """
    Analyze your performance on a challenge.

    Args:
        challenge_token (str): The challenge token/ID
        cookie (str): Your _ncfa cookie value

    Returns:
        dict: Performance statistics
    """
    try:
        # Get your profile
        profile_response = requests.get(
            'https://www.geoguessr.com/api/v3/profiles',
            cookies={'_ncfa': cookie}
        )
        profile_response.raise_for_status()
        profile = profile_response.json()
        my_user_id = profile['user']['id']

        # Get leaderboard
        leaderboard_url = f'https://www.geoguessr.com/api/v3/results/highscores/{challenge_token}'
        leaderboard_response = requests.get(leaderboard_url, cookies={'_ncfa': cookie})
        leaderboard_response.raise_for_status()
        data = leaderboard_response.json()

        # Find your entry
        my_entry = None
        my_rank = None

        for index, item in enumerate(data['items']):
            if item['game']['player']['id'] == my_user_id:
                my_entry = item
                my_rank = index + 1
                break

        if not my_entry:
            print('❌ You have not played this challenge yet.')
            return None

        my_score = int(my_entry['game']['player']['totalScore']['amount'])
        total_players = len(data['items'])

        # Calculate statistics
        scores = [int(item['game']['player']['totalScore']['amount']) for item in data['items']]
        top_score = scores[0]
        avg_score = statistics.mean(scores)
        median_score = statistics.median(scores)

        # Calculate percentile
        percentile = ((total_players - my_rank + 1) / total_players) * 100

        # Display results
        print(f"\n📊 Your Performance Analysis\n")
        print(f"Your Rank: #{my_rank} of {total_players}")
        print(f"Your Score: {my_score:,}")
        print(f"Percentile: Top {percentile:.1f}%")

        print(f"\n📈 Comparison:")
        diff_top = top_score - my_score
        diff_avg = round(avg_score) - my_score
        diff_median = median_score - my_score

        print(f"Top Score: {top_score:,} ({diff_top:+,})")
        print(f"Average Score: {round(avg_score):,} ({diff_avg:+,})")
        print(f"Median Score: {median_score:,} ({diff_median:+,})")

        # Show nearby players
        print(f"\n👥 Nearby Players:")
        start = max(0, my_rank - 3)
        end = min(total_players, my_rank + 2)

        for index in range(start, end):
            item = data['items'][index]
            rank = index + 1
            player = item['game']['player']
            score = int(player['totalScore']['amount'])
            indicator = '👉' if player['id'] == my_user_id else '  '

            print(f"{indicator} #{rank} {player['nick']}: {score:,}")

        return {
            'rank': my_rank,
            'score': my_score,
            'total_players': total_players,
            'percentile': percentile,
            'top_score': top_score,
            'avg_score': avg_score,
            'median_score': median_score
        }

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

    # Example challenge token
    challenge_token = input("Enter challenge token (or URL): ").strip()

    # Extract token from URL if full URL provided
    if '/' in challenge_token:
        challenge_token = challenge_token.split('/')[-1]

    # Analyze performance
    stats = analyze_performance(challenge_token, cookie)

    if stats:
        print("\n✅ Analysis complete!")


if __name__ == '__main__':
    main()
