"""
Get Duel Game State

Fetches complete game state for a duel including teams, players,
rounds, health, damage, and final results.

Usage: python get_duel_state.py
Requires: pip install requests
"""

import os
import requests
from typing import Dict, List, Optional


def get_duel_game_state(game_id: str) -> Dict:
    """
    Fetch complete duel game state.

    Args:
        game_id: The duel game ID

    Returns:
        dict: Complete game data with teams, rounds, and results
    """
    url = f"https://game-server.geoguessr.com/api/duels/{game_id}"

    cookies = {
        '_ncfa': os.getenv('GEOGUESSR_COOKIE')
    }

    if not cookies['_ncfa']:
        raise ValueError("GEOGUESSR_COOKIE environment variable not set")

    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()

        game_data = response.json()

        # Display basic game info
        print('=== Duel Game State ===')
        print(f"Game ID: {game_data['gameId']}")
        print(f"Status: {game_data['status']}")
        print(f"Current Round: {game_data['currentRoundNumber']}")
        print(f"Game Mode: {game_data['options']['competitiveGameMode']}")
        print(f"Map: {game_data['options']['map']['name']}")
        print()

        # Display team information
        print('=== Teams ===')
        for team in game_data['teams']:
            team_name = team['name'].upper()
            print(f"\nTeam {team_name}:")
            print(f"  Health: {team['health']}/{game_data['initialHealth']}")
            print(f"  Current Multiplier: {team['currentMultiplier']}x")
            print(f"  Players: {len(team['players'])}")

            for player in team['players']:
                print(f"    - Player ID: {player['playerId']}")
                print(f"      Rating: {player['rating']}")
                print(f"      Country: {player['countryCode'].upper()}")
                print(f"      Guesses: {len(player['guesses'])}")

        # Display result if game is finished
        if game_data['status'] == 'Finished':
            print('\n=== Game Result ===')
            winning_team = next(t for t in game_data['teams'] if t['id'] == game_data['result']['winningTeamId'])
            print(f"Winner: Team {winning_team['name'].upper()}")
            print(f"Victory Type: {game_data['result']['winnerStyle']}")
            print(f"Final Score: {winning_team['health']} HP remaining")

        # Display round summary
        print('\n=== Round Summary ===')
        completed_rounds = [r for r in game_data['rounds'] if r['hasProcessedRoundTimeout']]
        print(f"Completed Rounds: {len(completed_rounds)}")

        for round_data in completed_rounds[:5]:
            print(f"\nRound {round_data['roundNumber']}:")
            print(f"  Location: {round_data['panorama']['countryCode'].upper()}")
            print(f"  Multiplier: {round_data['multiplier']}x")

            # Get round results for each team
            for team in game_data['teams']:
                round_result = next(
                    (r for r in team['roundResults'] if r['roundNumber'] == round_data['roundNumber']),
                    None
                )
                if round_result:
                    print(f"  Team {team['name']}: Score {round_result['score']}, Damage {round_result['damageDealt']}")

        return game_data

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        raise


def analyze_damage(game_data: Dict) -> None:
    """
    Analyze damage dealt across all rounds.

    Args:
        game_data: Game data from get_duel_game_state
    """
    print('\n=== Damage Analysis ===')

    for team in game_data['teams']:
        total_damage = sum(r['damageDealt'] for r in team['roundResults'])
        team_name = team['name'].upper()

        print(f"\nTeam {team_name}:")
        print(f"  Total Damage Dealt: {total_damage}")
        print(f"  Average per Round: {total_damage // len(team['roundResults'])}")

        # Find biggest damage round
        max_damage_round = max(team['roundResults'], key=lambda r: r['damageDealt'])
        print(f"  Biggest Hit: {max_damage_round['damageDealt']} "
              f"(Round {max_damage_round['roundNumber']}, {max_damage_round['multiplier']}x)")


def display_player_stats(game_data: Dict) -> None:
    """
    Display player performance statistics.

    Args:
        game_data: Game data from get_duel_game_state
    """
    print('\n=== Player Performance ===')

    for team in game_data['teams']:
        print(f"\nTeam {team['name'].upper()}:")

        for player in team['players']:
            valid_guesses = [g for g in player['guesses'] if g['score'] is not None]

            if valid_guesses:
                total_score = sum(g['score'] for g in valid_guesses)
                avg_score = total_score / len(valid_guesses)
                avg_distance = sum(g['distance'] for g in valid_guesses) / len(valid_guesses)

                print(f"\n  Player {player['playerId'][:8]}...")
                print(f"    Rating: {player['rating']}")
                print(f"    Country: {player['countryCode'].upper()}")
                print(f"    Rounds Played: {len(valid_guesses)}")
                print(f"    Average Score: {avg_score:.0f}")
                print(f"    Average Distance: {avg_distance / 1000:.1f} km")

                # Rating change
                rating_change = player['progressChange'].get('rankedSystemProgress')
                if rating_change:
                    change = rating_change['gameModeRatingAfter'] - rating_change['gameModeRatingBefore']
                    print(f"    Rating Change: {'+' if change > 0 else ''}{change}")


def export_to_json(game_data: Dict, filename: str = 'duel_state.json') -> None:
    """
    Export game data to JSON file.

    Args:
        game_data: Game data from get_duel_game_state
        filename: Output filename
    """
    import json

    with open(filename, 'w') as f:
        json.dump(game_data, f, indent=2)

    print(f"\n✓ Game data exported to {filename}")


def monitor_game(game_id: str, interval_seconds: int = 10, max_checks: int = 100) -> None:
    """
    Monitor an ongoing game with periodic updates.

    Args:
        game_id: The duel game ID
        interval_seconds: Seconds between checks
        max_checks: Maximum number of checks before stopping
    """
    import time

    print(f"Monitoring game {game_id}...")

    for i in range(max_checks):
        try:
            data = get_duel_game_state(game_id)

            print(f"\n[Update {i+1}] Round {data['currentRoundNumber']} - Status: {data['status']}")
            for team in data['teams']:
                print(f"  Team {team['name']}: {team['health']} HP ({team['currentMultiplier']}x)")

            if data['status'] == 'Finished':
                print('\nGame finished! Stopping monitor.')
                break

            if i < max_checks - 1:  # Don't sleep after last check
                time.sleep(interval_seconds)

        except Exception as e:
            print(f"Monitor error: {e}")
            break


# ===== USAGE EXAMPLES =====

if __name__ == "__main__":
    # Example 1: Basic usage - get game state
    print('Fetching duel game state...\n')

    try:
        game_data = get_duel_game_state('6963ff12ec85cd5824375992')

        print('\nGame data retrieved successfully!')
        print('\nAvailable analysis functions:')
        print('  analyze_damage(game_data) - View damage statistics')
        print('  display_player_stats(game_data) - View player performance')
        print('  export_to_json(game_data) - Save to JSON file')

        # Uncomment to run analysis
        # analyze_damage(game_data)
        # display_player_stats(game_data)

    except Exception as e:
        print(f"Failed to fetch game: {e}")


# Example 2: Complete analysis with all functions
"""
if __name__ == "__main__":
    game_data = get_duel_game_state('6963ff12ec85cd5824375992')
    analyze_damage(game_data)
    display_player_stats(game_data)
    export_to_json(game_data)
"""


# Example 3: Monitor an ongoing game
"""
if __name__ == "__main__":
    monitor_game('YOUR_GAME_ID', interval_seconds=10, max_checks=50)
"""


# Example 4: Batch analysis of multiple games
"""
def analyze_multiple_games(game_ids: List[str]) -> None:
    results = []

    for game_id in game_ids:
        try:
            print(f"\nAnalyzing game {game_id}...")
            game_data = get_duel_game_state(game_id)

            # Extract key metrics
            winner = next(t for t in game_data['teams'] if t['id'] == game_data['result']['winningTeamId'])
            results.append({
                'game_id': game_id,
                'winner': winner['name'],
                'rounds': game_data['currentRoundNumber'],
                'game_mode': game_data['options']['competitiveGameMode']
            })

        except Exception as e:
            print(f"Error analyzing game {game_id}: {e}")

    # Display summary
    print('\n=== Batch Analysis Summary ===')
    for result in results:
        print(f"Game {result['game_id']}: Winner {result['winner']}, {result['rounds']} rounds")


if __name__ == "__main__":
    game_ids = [
        '6963ff12ec85cd5824375992',
        'YOUR_GAME_ID_2',
        'YOUR_GAME_ID_3'
    ]
    analyze_multiple_games(game_ids)
"""
