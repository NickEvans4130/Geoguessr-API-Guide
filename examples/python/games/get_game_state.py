"""
Get Game State

Retrieves the current state of a game including rounds, progress, and settings.

Usage:
    python get_game_state.py

Requirements:
    pip install requests
"""

import requests
import os
from datetime import datetime


def get_game_state(game_token, cookie):
    """
    Fetch and display game state.

    Args:
        game_token (str): Game token (16-character string)
        cookie (str): Your _ncfa cookie value

    Returns:
        dict: Game state object
    """
    try:
        url = f'https://www.geoguessr.com/api/v3/games/{game_token}?client=web'

        response = requests.get(url, cookies={'_ncfa': cookie})
        response.raise_for_status()

        game = response.json()

        # Display game information
        print(f"\n🎮 Game State\n")
        print(f"Token: {game['token']}")
        print(f"Mode: {game['mode']} ({game['type']})")
        print(f"State: {game['state']}")
        print(f"Map: {game['mapName']}")

        print(f"\n⚙️  Settings:")
        print(f"Rounds: {game['roundCount']}")
        time_limit = 'None' if game['timeLimit'] == 0 else f"{game['timeLimit']}s"
        print(f"Time Limit: {time_limit}")
        print(f"Movement: {'❌ Disabled' if game['forbidMoving'] else '✅ Enabled'}")
        print(f"Panning: {'❌ Disabled' if game['forbidRotating'] else '✅ Enabled'}")
        print(f"Zooming: {'❌ Disabled' if game['forbidZooming'] else '✅ Enabled'}")

        print(f"\n📊 Progress:")
        print(f"Current Round: {game['round']} of {game['roundCount']}")

        if 'player' in game and game['player']:
            player = game['player']
            print(f"\n👤 Player Stats:")
            print(f"Score: {int(player['totalScore']['amount']):,} points")
            print(f"Distance: {player['totalDistanceInMeters']:,}m")
            print(f"Time: {player['totalTime']}s")
            print(f"Guesses: {len(player['guesses'])}")

            if game['mode'] == 'streak':
                print(f"Streak: {player['totalStreak']}")

        # Show rounds
        if 'rounds' in game and game['rounds']:
            print(f"\n📍 Rounds:")
            for index, round_data in enumerate(game['rounds']):
                status = '✅' if game.get('player', {}).get('guesses', []) and len(game['player']['guesses']) > index else '⏳'
                print(f"{status} Round {index + 1}: {round_data['lat']:.4f}, {round_data['lng']:.4f}")

        # Show guesses if any
        if game.get('player', {}).get('guesses'):
            print(f"\n🎯 Your Guesses:")
            for index, guess in enumerate(game['player']['guesses']):
                score = int(guess['roundScore']['amount'])
                distance = int(guess['distance']['meters']['amount'])
                print(f"Round {index + 1}: {score:,} points ({distance:,}m away)")

        return game

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if e.response.status_code == 401:
            print("Note: Your cookie may be invalid or expired")
        elif e.response.status_code == 404:
            print("Note: Game not found or you don't have access")
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

    # Get game token
    game_token = input("Enter game token: ").strip()

    if not game_token:
        print("❌ Game token cannot be empty")
        return

    # Fetch game state
    game = get_game_state(game_token, cookie)

    if game:
        print("\n✅ Game state retrieved successfully!")


if __name__ == '__main__':
    main()
