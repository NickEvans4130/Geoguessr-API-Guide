"""
Get Friends List

Retrieves and displays your complete friends list.

Usage:
    python get_friends_list.py

Requirements:
    pip install requests
"""

import requests
import os
from collections import Counter


def get_friends_list(cookie):
    """
    Fetch and display your friends list.

    Args:
        cookie (str): Your _ncfa cookie value

    Returns:
        list: List of friends
    """
    try:
        response = requests.get(
            'https://www.geoguessr.com/api/v3/social/friends',
            cookies={'_ncfa': cookie}
        )
        response.raise_for_status()

        friends = response.json()

        if len(friends) == 0:
            print('You have no friends yet. Add some friends to see them here!')
            return []

        # Display friends list
        print(f"\n👥 Your Friends ({len(friends)} total)\n")
        print(f"{'Username':<20} {'Level':<8} {'Country':<10} {'Pro':<5} {'Online'}")
        print('-' * 60)

        for friend in friends:
            username = friend['nick'][:19]
            level = friend.get('progress', {}).get('level', 'N/A')
            country = friend.get('countryCode', 'N/A').upper()
            pro = '✅' if friend.get('isProUser') else '❌'
            online = '🟢' if friend.get('isOnline') else '⚪'

            print(f"{username:<20} {level:<8} {country:<10} {pro:<5} {online}")

        # Statistics
        online_count = sum(1 for f in friends if f.get('isOnline'))
        pro_count = sum(1 for f in friends if f.get('isProUser'))

        levels = [f.get('progress', {}).get('level', 0) for f in friends if f.get('progress', {}).get('level')]
        avg_level = sum(levels) / len(levels) if levels else 0

        print(f"\n📊 Statistics:")
        print(f"Total Friends: {len(friends)}")
        print(f"Online Now: {online_count}")
        print(f"Pro Users: {pro_count} ({(pro_count / len(friends) * 100):.1f}%)")
        print(f"Average Level: {avg_level:.1f}")

        # Group by country
        countries = [f.get('countryCode') for f in friends if f.get('countryCode')]
        country_counts = Counter(countries).most_common(5)

        print(f"\n🌍 Top Countries:")
        for country, count in country_counts:
            print(f"{country.upper()}: {count}")

        return friends

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

    # Fetch friends
    friends = get_friends_list(cookie)

    if friends:
        print(f"\n✅ Retrieved {len(friends)} friends!")


if __name__ == '__main__':
    main()
