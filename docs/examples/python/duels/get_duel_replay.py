"""
Get Duel Replay Events

Fetches complete replay data for a player's actions during a specific round.
Includes camera movements, map interactions, and guess placement with timestamps.

Usage: python get_duel_replay.py
Requires: pip install requests
"""

import os
import requests
from typing import Dict, List, Any
from collections import Counter
import json


def get_duel_replay(player_id: str, duel_id: str, round_number: int) -> List[Dict]:
    """
    Fetch replay events for a specific player and round.

    Args:
        player_id: The player's user ID
        duel_id: The duel game ID
        round_number: The round number (1-indexed)

    Returns:
        list: Array of replay events with timestamps
    """
    url = f"https://game-server.geoguessr.com/api/replays/{player_id}/{duel_id}/{round_number}"

    cookies = {
        '_ncfa': os.getenv('GEOGUESSR_COOKIE')
    }

    if not cookies['_ncfa']:
        raise ValueError("GEOGUESSR_COOKIE environment variable not set")

    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()

        replay_events = response.json()

        print('=== Duel Replay Events ===')
        print(f"Player ID: {player_id}")
        print(f"Duel ID: {duel_id}")
        print(f"Round: {round_number}")
        print(f"Total Events: {len(replay_events)}")
        print()

        # Analyze event types
        event_types = Counter(event['type'] for event in replay_events)

        print('Event Type Breakdown:')
        for event_type, count in event_types.most_common():
            print(f"  {event_type}: {count}")

        return replay_events

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        raise


def analyze_player_behavior(events: List[Dict]) -> None:
    """
    Analyze player behavior from replay events.

    Args:
        events: Replay events from get_duel_replay
    """
    print('\n=== Player Behavior Analysis ===')

    if not events:
        print("No events to analyze")
        return

    # Calculate total time
    start_time = events[0]['time']
    end_time = events[-1]['time']
    total_seconds = (end_time - start_time) / 1000

    print(f"\nTiming:")
    print(f"  Total Time: {total_seconds:.1f}s")

    # Find key events
    guess_event = next((e for e in events if e['type'] == 'GuessWithLatLng'), None)
    map_display_events = [e for e in events if e['type'] == 'MapDisplay']
    pin_position_events = [e for e in events if e['type'] == 'PinPosition']
    zoom_events = [e for e in events if e['type'] == 'PanoZoom']

    print(f"\nActions:")
    map_opens = sum(1 for e in map_display_events if e['payload'].get('isActive'))
    print(f"  Map Opens: {map_opens}")
    print(f"  Pin Adjustments: {len(pin_position_events)}")
    print(f"  Zoom Changes: {len(zoom_events)}")

    if guess_event:
        guess_time = (guess_event['time'] - start_time) / 1000
        print(f"  Time to Guess: {guess_time:.1f}s")
        print(f"  Final Guess: {guess_event['payload']['lat']:.5f}, {guess_event['payload']['lng']:.5f}")

    # Analyze map usage
    first_map_open = next((e for e in map_display_events if e['payload'].get('isActive')), None)
    if first_map_open:
        map_open_time = (first_map_open['time'] - start_time) / 1000
        print(f"\nMap Usage:")
        print(f"  First Map Open: {map_open_time:.1f}s")

        map_closes = sum(1 for e in map_display_events if not e['payload'].get('isActive'))
        print(f"  Map Opens/Closes: {map_closes} times")

    # Analyze camera movements
    pov_events = [e for e in events if e['type'] == 'PanoPov']
    if pov_events:
        print(f"\nCamera Movement:")
        print(f"  POV Changes: {len(pov_events)}")

        headings = [e['payload']['heading'] for e in pov_events]
        heading_range = max(headings) - min(headings)
        print(f"  Heading Range: {heading_range:.0f}°")


def display_timeline(events: List[Dict], max_events: int = 20) -> None:
    """
    Display replay timeline with key moments.

    Args:
        events: Replay events from get_duel_replay
        max_events: Maximum number of events to display
    """
    print('\n=== Replay Timeline ===')

    if not events:
        print("No events to display")
        return

    start_time = events[0]['time']

    # Filter to important events
    important_types = ['MapDisplay', 'PinPosition', 'GuessWithLatLng', 'PanoPosition']
    important_events = [e for e in events if e['type'] in important_types]

    events_to_show = important_events[:max_events]

    for event in events_to_show:
        relative_time = (event['time'] - start_time) / 1000
        description = ''

        event_type = event['type']
        payload = event['payload']

        if event_type == 'MapDisplay':
            description = '📍 Opened map' if payload.get('isActive') else '📍 Closed map'
        elif event_type == 'PinPosition':
            description = f"📌 Placed pin at {payload['lat']:.2f}, {payload['lng']:.2f}"
        elif event_type == 'GuessWithLatLng':
            description = f"✅ FINAL GUESS at {payload['lat']:.2f}, {payload['lng']:.2f}"
        elif event_type == 'PanoPosition':
            country = payload.get('countryCode', 'unknown').upper()
            description = f"🌍 Moved to {country}"

        print(f"[{relative_time:.1f}s] {description}")

    if len(important_events) > max_events:
        print(f"\n... and {len(important_events) - max_events} more events")


def compare_player_replays(players: List[Dict[str, Any]]) -> None:
    """
    Compare replay events from multiple players in the same round.

    Args:
        players: List of dicts with 'playerId', 'duelId', 'roundNumber' keys
    """
    print('\n=== Comparing Player Replays ===')

    replays = []
    for player in players:
        try:
            events = get_duel_replay(
                player['playerId'],
                player['duelId'],
                player['roundNumber']
            )
            replays.append((player, events))
        except Exception as e:
            print(f"Error fetching replay for {player['playerId']}: {e}")

    print('\nComparison Results:')

    for i, (player, events) in enumerate(replays):
        if not events:
            continue

        start_time = events[0]['time']
        end_time = events[-1]['time']
        total_time = (end_time - start_time) / 1000

        guess_event = next((e for e in events if e['type'] == 'GuessWithLatLng'), None)
        guess_time = (guess_event['time'] - start_time) / 1000 if guess_event else None

        map_opens = sum(1 for e in events if e['type'] == 'MapDisplay' and e['payload'].get('isActive'))
        pin_adjustments = sum(1 for e in events if e['type'] == 'PinPosition')

        print(f"\nPlayer {i + 1} ({player['playerId'][:8]}...):")
        print(f"  Total Time: {total_time:.1f}s")
        print(f"  Time to Guess: {guess_time:.1f if guess_time else 'N/A'}s")
        print(f"  Map Opens: {map_opens}")
        print(f"  Pin Adjustments: {pin_adjustments}")
        print(f"  Total Actions: {len(events)}")


def export_replay_as_csv(events: List[Dict], filename: str = 'replay_events.csv') -> None:
    """
    Export replay data as CSV file.

    Args:
        events: Replay events from get_duel_replay
        filename: Output filename
    """
    import csv

    if not events:
        print("No events to export")
        return

    start_time = events[0]['time']

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'RelativeTime(s)', 'EventType', 'Data'])

        for event in events:
            relative_time = (event['time'] - start_time) / 1000
            data = json.dumps(event['payload'])
            writer.writerow([event['time'], f"{relative_time:.3f}", event['type'], data])

    print(f"\n✓ Replay data exported to {filename}")


def export_replay_as_json(events: List[Dict], filename: str = 'replay_events.json') -> None:
    """
    Export replay data as JSON file.

    Args:
        events: Replay events from get_duel_replay
        filename: Output filename
    """
    with open(filename, 'w') as f:
        json.dump(events, f, indent=2)

    print(f"\n✓ Replay data exported to {filename}")


def analyze_all_rounds(player_id: str, duel_id: str, total_rounds: int) -> None:
    """
    Analyze all rounds for a specific player.

    Args:
        player_id: The player's user ID
        duel_id: The duel game ID
        total_rounds: Number of rounds to analyze
    """
    print(f"\n=== Analyzing all rounds for player {player_id[:8]}... ===")

    for round_num in range(1, total_rounds + 1):
        print(f"\n--- Round {round_num} ---")
        try:
            events = get_duel_replay(player_id, duel_id, round_num)
            analyze_player_behavior(events)
        except Exception as e:
            print(f"Error in round {round_num}: {e}")


# ===== USAGE EXAMPLES =====

if __name__ == "__main__":
    # Example 1: Basic usage - get replay for a player
    print('Fetching duel replay...\n')

    try:
        events = get_duel_replay(
            '5b68bcc7f438a60f64005817',
            '6963ff12ec85cd5824375992',
            1
        )

        print('\nReplay data retrieved successfully!')
        print('\nAvailable analysis functions:')
        print('  analyze_player_behavior(events) - Analyze player actions')
        print('  display_timeline(events) - Show event timeline')
        print('  export_replay_as_csv(events) - Export as CSV')
        print('  export_replay_as_json(events) - Export as JSON')

        # Uncomment to run analysis
        # analyze_player_behavior(events)
        # display_timeline(events, 15)

    except Exception as e:
        print(f"Failed to fetch replay: {e}")


# Example 2: Complete analysis of a player's round
"""
if __name__ == "__main__":
    events = get_duel_replay(
        '5b68bcc7f438a60f64005817',
        '6963ff12ec85cd5824375992',
        1
    )
    analyze_player_behavior(events)
    display_timeline(events, 15)
    export_replay_as_csv(events)
"""


# Example 3: Compare two players in the same round
"""
if __name__ == "__main__":
    players = [
        {
            'playerId': '5b68bcc7f438a60f64005817',
            'duelId': '6963ff12ec85cd5824375992',
            'roundNumber': 1
        },
        {
            'playerId': '62248fc297f88100010c1763',
            'duelId': '6963ff12ec85cd5824375992',
            'roundNumber': 1
        }
    ]
    compare_player_replays(players)
"""


# Example 4: Analyze first 5 rounds for a player
"""
if __name__ == "__main__":
    analyze_all_rounds(
        '5b68bcc7f438a60f64005817',
        '6963ff12ec85cd5824375992',
        5
    )
"""


# Example 5: Export replay to both CSV and JSON
"""
if __name__ == "__main__":
    events = get_duel_replay(
        '5b68bcc7f438a60f64005817',
        '6963ff12ec85cd5824375992',
        1
    )
    export_replay_as_csv(events, 'round1_replay.csv')
    export_replay_as_json(events, 'round1_replay.json')
"""
