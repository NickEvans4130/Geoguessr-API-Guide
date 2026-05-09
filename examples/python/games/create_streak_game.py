"""
Create Streak Game

Creates a new country/region streak game with custom settings.

Usage:
    python create_streak_game.py

Requirements:
    pip install requests
"""

import requests
import os


# Preset configurations
STREAK_PRESETS = {
    'easy': {
        'forbidMoving': False,
        'forbidRotating': False,
        'forbidZooming': False,
        'timeLimit': 0
    },
    'medium': {
        'forbidMoving': False,
        'forbidRotating': False,
        'forbidZooming': False,
        'timeLimit': 60
    },
    'hard': {
        'forbidMoving': True,
        'forbidRotating': False,
        'forbidZooming': True,
        'timeLimit': 30
    },
    'nmpz': {
        'forbidMoving': True,
        'forbidRotating': True,
        'forbidZooming': True,
        'timeLimit': 0
    }
}


def create_streak_game(cookie, settings=None):
    """
    Create a new streak game.

    Args:
        cookie (str): Your _ncfa cookie value
        settings (dict): Game settings (optional)

    Returns:
        dict: Game state object
    """
    try:
        url = 'https://www.geoguessr.com/api/v3/games/streak'

        # Default settings
        if settings is None:
            settings = {
                'forbidMoving': False,
                'forbidRotating': False,
                'forbidZooming': False,
                'streakType': 'CountryStreak',
                'timeLimit': 0
            }

        response = requests.post(
            url,
            json=settings,
            cookies={'_ncfa': cookie}
        )
        response.raise_for_status()

        game = response.json()

        # Display game information
        print(f"\n✅ Streak Game Created!\n")
        print(f"Token: {game['token']}")
        print(f"Game URL: https://www.geoguessr.com/game/{game['token']}")
        print(f"Mode: {game['streakType']}")

        print(f"\n⚙️  Settings:")
        time_limit = 'None' if game['timeLimit'] == 0 else f"{game['timeLimit']}s per round"
        print(f"Time Limit: {time_limit}")
        print(f"Movement: {'❌ Disabled (NMPZ)' if game['forbidMoving'] else '✅ Enabled'}")
        print(f"Panning: {'❌ Disabled (NR)' if game['forbidRotating'] else '✅ Enabled'}")
        print(f"Zooming: {'❌ Disabled (NZ)' if game['forbidZooming'] else '✅ Enabled'}")

        print(f"\n📍 Starting Location:")
        if 'rounds' in game and game['rounds']:
            round_data = game['rounds'][0]
            print(f"Coordinates: {round_data['lat']:.4f}, {round_data['lng']:.4f}")
            print(f"Country Code: {round_data.get('streakLocationCode', 'N/A')}")

        print(f"\n🎮 Ready to play! Navigate to the game URL above.")

        return game

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

    # Show preset options
    print("\n🎮 Create Streak Game\n")
    print("Select difficulty preset:")
    print("1. Easy (No restrictions, unlimited time)")
    print("2. Medium (60s per round)")
    print("3. Hard (NMPZ, 30s per round)")
    print("4. NMPZ (No moving, panning, or zooming)")
    print("5. Custom")

    choice = input("\nEnter choice (1-5) [default: 1]: ").strip() or "1"

    settings = None
    if choice == "1":
        settings = STREAK_PRESETS['easy'].copy()
    elif choice == "2":
        settings = STREAK_PRESETS['medium'].copy()
    elif choice == "3":
        settings = STREAK_PRESETS['hard'].copy()
    elif choice == "4":
        settings = STREAK_PRESETS['nmpz'].copy()
    elif choice == "5":
        print("\nCustom Settings:")
        settings = {
            'forbidMoving': input("Forbid moving? (y/n) [n]: ").strip().lower() == 'y',
            'forbidRotating': input("Forbid panning? (y/n) [n]: ").strip().lower() == 'y',
            'forbidZooming': input("Forbid zooming? (y/n) [n]: ").strip().lower() == 'y',
            'streakType': 'CountryStreak',
            'timeLimit': 0
        }
        time_input = input("Time limit in seconds (0 for none) [0]: ").strip()
        if time_input.isdigit():
            settings['timeLimit'] = int(time_input)
    else:
        print("Invalid choice")
        return

    settings['streakType'] = 'CountryStreak'

    # Create game
    game = create_streak_game(cookie, settings)

    if game:
        print("\n✅ Game created successfully!")


if __name__ == '__main__':
    main()
