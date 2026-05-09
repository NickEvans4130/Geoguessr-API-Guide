"""
Check Authentication Status

Verifies if you're currently authenticated and displays your basic info.

Usage:
    python check_auth_status.py

Requirements:
    pip install requests
"""

import requests
import os
from datetime import datetime


def check_auth_status(cookie):
    """
    Check if authenticated and display user info.

    Args:
        cookie (str): Your _ncfa cookie value

    Returns:
        dict: Authentication status and user info
    """
    try:
        response = requests.get(
            'https://www.geoguessr.com/api/v3/profiles',
            cookies={'_ncfa': cookie}
        )

        if response.status_code == 401:
            print('❌ Not authenticated')
            print('Cookie is invalid or expired.')
            return {'authenticated': False}

        response.raise_for_status()
        profile = response.json()
        user = profile['user']

        # Display authentication status
        print(f"\n✅ Authenticated\n")
        print(f"Username: {user['nick']}")
        print(f"User ID: {user['id']}")
        print(f"Email: {profile['email']}")
        print(f"Country: {user['countryCode'].upper()}")
        print(f"Pro User: {'✅ Yes' if user['isProUser'] else '❌ No'}")
        print(f"Level: {user['progress']['level']}")
        print(f"XP: {user['progress']['xp']:,}")

        if 'competitive' in user and user['competitive']:
            print(f"\n🏆 Competitive:")
            print(f"Rating: {user['competitive']['rating']}")
            if 'division' in user['competitive'] and user['competitive']['division']:
                print(f"Division: {user['competitive']['division'].get('type', 'N/A')}")

        # Account age
        created = datetime.fromisoformat(user['created'].replace('Z', '+00:00'))
        age_in_days = (datetime.now(created.tzinfo) - created).days
        age_in_years = age_in_days / 365

        print(f"\n📅 Account Info:")
        print(f"Created: {created.strftime('%Y-%m-%d')}")
        print(f"Age: {age_in_years:.1f} years ({age_in_days} days)")

        return {
            'authenticated': True,
            'username': user['nick'],
            'userId': user['id'],
            'email': profile['email'],
            'isProUser': user['isProUser'],
            'level': user['progress']['level']
        }

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        return {'authenticated': False, 'error': str(e)}
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return {'authenticated': False, 'error': str(e)}


def main():
    # Get credentials from environment variables
    cookie = os.getenv('GEOGUESSR_COOKIE')
    if not cookie:
        print("❌ Error: GEOGUESSR_COOKIE environment variable not set")
        print("Set it with: export GEOGUESSR_COOKIE='your_cookie_value'")
        return

    # Check authentication
    auth = check_auth_status(cookie)

    if auth['authenticated']:
        print("\n✅ Authentication verified!")
    else:
        print("\n❌ Not authenticated")


if __name__ == '__main__':
    main()
