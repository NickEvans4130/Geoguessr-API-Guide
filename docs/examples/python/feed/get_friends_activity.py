"""
Get Friends Activity Feed

Retrieves and displays recent activity from your friends.

Usage:
    python get_friends_activity.py

Requirements:
    pip install requests
"""

import requests
import os
import json
from datetime import datetime
from collections import Counter


def get_friends_activity(cookie, pages=1):
    """
    Fetch and display friends' activity feed.

    Args:
        cookie (str): Your _ncfa cookie value
        pages (int): Number of pages to fetch (default: 1)

    Returns:
        list: List of activity entries
    """
    try:
        all_entries = []
        pagination_token = None

        for page in range(pages):
            if pagination_token:
                url = f'https://www.geoguessr.com/api/v4/feed/friends?paginationToken={pagination_token}'
            else:
                url = 'https://www.geoguessr.com/api/v4/feed/friends'

            response = requests.get(url, cookies={'_ncfa': cookie})
            response.raise_for_status()

            data = response.json()
            all_entries.extend(data['entries'])

            if 'paginationToken' not in data or page == pages - 1:
                break

            pagination_token = data['paginationToken']

        print(f"\n🌟 Friends Activity Feed ({len(all_entries)} activities)\n")

        # Parse and display activities
        for entry in all_entries[:20]:  # Show first 20
            time_str = datetime.fromisoformat(entry['time'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
            payload = json.loads(entry['payload'])

            activity_text = ''

            if entry['type'] == 2:  # Standard game
                activity_text = f"scored {payload.get('points', 'N/A')} points on {payload.get('mapName', 'a map')}"
            elif entry['type'] == 6:  # Competitive game started
                activity_text = f"started a {payload.get('competitiveGameMode', 'competitive')} game"
            elif entry['type'] == 9:  # Party game
                activity_text = f"is playing {payload.get('gameMode', 'a game')}"
            elif entry['type'] == 11:  # Competitive game result
                activity_text = f"finished a {payload.get('competitiveGameMode', 'competitive')} game"
            elif entry['type'] == 7:  # Batch activities
                activity_text = "completed multiple activities"
            else:
                activity_text = f"activity type {entry['type']}"

            print(f"[{time_str}] {entry['user']['nick']}: {activity_text}")

        # Statistics
        print(f"\n📊 Activity Breakdown:")
        activity_types = Counter(entry['type'] for entry in all_entries)

        type_names = {
            2: 'Standard Games',
            6: 'Duels Started',
            9: 'Party Games',
            11: 'Duels Completed',
            7: 'Batch Activities'
        }

        for activity_type, count in sorted(activity_types.items()):
            type_name = type_names.get(activity_type, f'Type {activity_type}')
            print(f"{type_name}: {count}")

        # Most active friends
        user_activity = Counter(entry['user']['nick'] for entry in all_entries)
        top_users = user_activity.most_common(5)

        print(f"\n🏆 Most Active Friends:")
        for rank, (nick, count) in enumerate(top_users, 1):
            print(f"{rank}. {nick}: {count} activities")

        # Time analysis
        hours = [datetime.fromisoformat(e['time'].replace('Z', '+00:00')).hour for e in all_entries]
        hour_counts = Counter(hours).most_common(3)
        print(f"\n⏰ Most Active Hours:")
        for hour, count in hour_counts:
            print(f"  {hour:02d}:00 - {count} activities")

        return all_entries

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if e.response.status_code == 401:
            print("Note: Your cookie may be invalid or expired")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing activity payload: {e}")
        return None


def export_to_json(entries, filename='activity_feed.json'):
    """Export activity feed to JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Exported {len(entries)} activities to {filename}")
    except IOError as e:
        print(f"❌ Error writing file: {e}")


def main():
    # Get credentials from environment variables
    cookie = os.getenv('GEOGUESSR_COOKIE')
    if not cookie:
        print("❌ Error: GEOGUESSR_COOKIE environment variable not set")
        print("Set it with: export GEOGUESSR_COOKIE='your_cookie_value'")
        return

    # Ask for number of pages
    pages_input = input("How many pages to fetch? (1 page ≈ 31 activities) [default: 1]: ").strip()
    pages = int(pages_input) if pages_input.isdigit() else 1

    # Fetch activity
    entries = get_friends_activity(cookie, pages)

    if entries:
        print(f"\n✅ Retrieved {len(entries)} activities!")

        # Ask if user wants to export
        export = input("\nExport to JSON? (y/n) [default: n]: ").strip().lower()
        if export == 'y':
            export_to_json(entries)


if __name__ == '__main__':
    main()
