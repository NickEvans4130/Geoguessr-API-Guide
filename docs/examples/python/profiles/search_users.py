"""
Search Users

Searches for GeoGuessr users by username.

Usage:
    python search_users.py

Requirements:
    pip install requests
"""

import requests
import os


def search_users(query, cookie):
    """
    Search for GeoGuessr users.

    Args:
        query (str): Search query (username)
        cookie (str): Your _ncfa cookie value

    Returns:
        list: List of matching users
    """
    try:
        if not query or len(query.strip()) == 0:
            print('❌ Search query cannot be empty')
            return None

        url = f'https://www.geoguessr.com/api/v3/search/user?q={query}'

        response = requests.get(url, cookies={'_ncfa': cookie})
        response.raise_for_status()

        results = response.json()

        if len(results) == 0:
            print(f'❌ No users found matching "{query}"')
            return []

        # Display results
        print(f'\n🔍 Search Results for "{query}" ({len(results)} users found)\n')
        print(f"{'Username':<20} {'Level':<8} {'Country':<10} {'Pro':<5} {'Verified'}")
        print('-' * 60)

        for user in results:
            username = user['nick'][:19]
            level = user.get('progress', {}).get('level', 'N/A')
            country = user.get('countryCode', 'N/A').upper()
            pro = '✅' if user.get('isProUser') else '❌'
            verified = '✅' if user.get('isVerified') else '❌'

            print(f"{username:<20} {level:<8} {country:<10} {pro:<5} {verified}")

        # Show profile links
        print(f'\n🔗 Profile Links:')
        for user in results[:5]:  # Show first 5
            print(f"{user['nick']}: https://www.geoguessr.com/user/{user['id']}")

        return results

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if e.response.status_code == 400:
            print("Note: Empty search queries are not allowed")
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

    # Get search query
    query = input("Enter username to search: ").strip()

    # Search for users
    results = search_users(query, cookie)

    if results:
        print(f"\n✅ Found {len(results)} users!")


if __name__ == '__main__':
    main()
