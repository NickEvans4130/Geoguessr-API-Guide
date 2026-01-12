"""
Get Challenge Information

Retrieves detailed information about a challenge including map, settings, and creator.

Usage:
    python get_challenge_info.py

Requirements:
    pip install requests
"""

import requests
import os
from datetime import datetime


def get_challenge_info(challenge_token, cookie):
    """
    Fetch and display challenge information.

    Args:
        challenge_token (str): The challenge token/ID
        cookie (str): Your _ncfa cookie value

    Returns:
        dict: Challenge information
    """
    try:
        url = f'https://www.geoguessr.com/api/v3/challenges/{challenge_token}'

        response = requests.get(url, cookies={'_ncfa': cookie})
        response.raise_for_status()

        challenge = response.json()

        # Display formatted challenge information
        print(f"\n🎮 Challenge Information\n")
        print(f"Map: {challenge['map']['name']}")
        print(f"Creator: {challenge['creator']['nick']} ({challenge['creator']['countryCode']})")
        print(f"Created: {datetime.fromisoformat(challenge['created'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')}")

        print(f"\n⚙️  Settings:")
        print(f"- Rounds: {challenge['roundCount']}")
        time_limit = 'None' if challenge['timeLimit'] == 0 else f"{challenge['timeLimit']}s"
        print(f"- Time Limit: {time_limit}")
        print(f"- Movement: {'❌ Disabled' if challenge['forbidMoving'] else '✅ Enabled'}")
        print(f"- Panning: {'❌ Disabled' if challenge['forbidRotating'] else '✅ Enabled'}")
        print(f"- Zooming: {'❌ Disabled' if challenge['forbidZooming'] else '✅ Enabled'}")

        print(f"\n📍 Map Details:")
        print(f"- Name: {challenge['map']['name']}")
        print(f"- Description: {challenge['map'].get('description', 'N/A')}")
        print(f"- Locations: {challenge['map'].get('coordinateCount', 'Unknown')}")

        if 'bounds' in challenge['map']:
            print(f"- Bounds: {challenge['map']['bounds']}")

        return challenge

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if e.response.status_code == 403:
            print("Note: You may need to play the challenge first to view details")
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

    # Fetch challenge info
    challenge = get_challenge_info(challenge_token, cookie)

    if challenge:
        print("\n✅ Successfully retrieved challenge information!")


if __name__ == '__main__':
    main()
