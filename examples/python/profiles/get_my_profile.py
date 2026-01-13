"""
Get My Profile

Retrieves and displays your own GeoGuessr profile information.

Usage:
    python get_my_profile.py

Requirements:
    pip install requests
"""

import requests
import os
from datetime import datetime


def get_my_profile(cookie):
    """
    Fetch and display your GeoGuessr profile.

    Args:
        cookie (str): Your _ncfa cookie value

    Returns:
        dict: Your profile data
    """
    try:
        response = requests.get(
            'https://www.geoguessr.com/api/v3/profiles',
            cookies={'_ncfa': cookie}
        )
        response.raise_for_status()

        profile = response.json()
        user = profile['user']

        # Display profile information
        print(f"\n👤 Your Profile\n")
        print(f"Username: {user['nick']}")
        print(f"User ID: {user['id']}")
        print(f"Country: {user['countryCode'].upper()}")

        created_date = datetime.fromisoformat(user['created'].replace('Z', '+00:00'))
        print(f"Created: {created_date.strftime('%Y-%m-%d')}")
        print(f"Pro User: {'✅ Yes' if user['isProUser'] else '❌ No'}")
        print(f"Verified: {'✅ Yes' if user['isVerified'] else '❌ No'}")

        print(f"\n📊 Progress:")
        progress = user['progress']
        print(f"Level: {progress['level']}")
        print(f"XP: {progress['xp']:,}")
        print(f"Next Level: {progress['nextLevel']} ({progress['nextLevelXp']:,} XP)")
        xp_to_next = progress['nextLevelXp'] - progress['xp']
        print(f"XP to Next Level: {xp_to_next:,}")

        if 'competitive' in user and user['competitive']:
            comp = user['competitive']
            print(f"\n🏆 Competitive:")
            print(f"Rating: {comp['rating']}")
            if 'division' in comp and comp['division']:
                print(f"Division: {comp['division'].get('type', 'N/A')}")
            print(f"On Leaderboard: {'✅ Yes' if comp.get('onLeaderboard') else '❌ No'}")

        print(f"\n🌍 Achievements:")
        if 'streakProgress' in user:
            streak = user['streakProgress']
            print(f"Streak Badges: Bronze {streak['bronze']}, Silver {streak['silver']}, "
                  f"Gold {streak['gold']}, Platinum {streak['platinum']}")

        if 'explorerProgress' in user:
            explorer = user['explorerProgress']
            print(f"Explorer Badges: Bronze {explorer['bronze']}, Silver {explorer['silver']}, "
                  f"Gold {explorer['gold']}, Platinum {explorer['platinum']}")

        return profile

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if e.response.status_code == 401:
            print("Note: Your cookie may be invalid or expired")
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

    # Fetch profile
    profile = get_my_profile(cookie)

    if profile:
        print("\n✅ Profile retrieved successfully!")


if __name__ == '__main__':
    main()
