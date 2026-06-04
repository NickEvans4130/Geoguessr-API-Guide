"""
Browse Popular Maps

Retrieves and displays popular GeoGuessr maps with statistics.

Usage:
    python browse_popular_maps.py

Requirements:
    pip install requests

Note: This endpoint does NOT require authentication
"""

import requests
from collections import Counter


def browse_popular_maps():
    """
    Fetch and display popular maps.

    Returns:
        list: List of popular maps
    """
    try:
        url = 'https://www.geoguessr.com/api/v3/maps/browse/popular'

        # Note: No authentication required for browsing maps
        response = requests.get(url)
        response.raise_for_status()

        maps = response.json()

        print(f"\n🗺️  Popular Maps ({len(maps)} maps)\n")
        print(f"{'#':<4} {'Map Name':<40} {'Creator':<20} {'Locations':<12} {'Difficulty'}")
        print('-' * 100)

        for index, map_data in enumerate(maps, 1):
            name = map_data['name'][:39]
            creator = map_data['creator']['nick'][:19]
            locations = map_data.get('coordinateCount', 'Unknown')
            difficulty = map_data.get('difficulty', 'N/A')

            print(f"{index:<4} {name:<40} {creator:<20} {locations:<12} {difficulty}")

        # Statistics
        print(f"\n📊 Statistics:")
        print(f"Total Maps: {len(maps)}")

        # Average likes
        likes = [m.get('likes', 0) for m in maps]
        avg_likes = sum(likes) / len(likes) if likes else 0
        print(f"Average Likes: {avg_likes:.1f}")

        # Difficulty breakdown
        difficulties = [m.get('difficulty', 'Unknown') for m in maps]
        diff_counts = Counter(difficulties)
        print(f"\nDifficulties:")
        for diff, count in diff_counts.most_common():
            print(f"  {diff}: {count}")

        # Top creators
        creators = [m['creator']['nick'] for m in maps]
        creator_counts = Counter(creators).most_common(5)
        print(f"\n👤 Top Creators:")
        for creator, count in creator_counts:
            print(f"  {creator}: {count} maps")

        # Show some map links
        print(f"\n🔗 Sample Map Links:")
        for map_data in maps[:5]:
            print(f"{map_data['name']}: https://www.geoguessr.com/maps/{map_data['id']}")

        return maps

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return None


def browse_featured_maps():
    """Fetch featured maps."""
    try:
        response = requests.get('https://www.geoguessr.com/api/v3/maps/browse/featured')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching featured maps: {e}")
        return None


def browse_new_maps():
    """Fetch new maps."""
    try:
        response = requests.get('https://www.geoguessr.com/api/v3/maps/browse/new')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching new maps: {e}")
        return None


def browse_hot_maps():
    """Fetch hot/trending maps."""
    try:
        response = requests.get('https://www.geoguessr.com/api/v3/maps/browse/hot')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching hot maps: {e}")
        return None


def main():
    print("=== GeoGuessr Map Browser ===\n")
    print("Select a category:")
    print("1. Popular Maps")
    print("2. Featured Maps")
    print("3. New Maps")
    print("4. Hot/Trending Maps")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        maps = browse_popular_maps()
    elif choice == "2":
        print("\n🌟 Featured Maps:")
        maps = browse_featured_maps()
        if maps:
            for i, m in enumerate(maps, 1):
                print(f"{i}. {m['name']} by {m['creator']['nick']}")
    elif choice == "3":
        print("\n🆕 New Maps:")
        maps = browse_new_maps()
        if maps:
            for i, m in enumerate(maps, 1):
                print(f"{i}. {m['name']} by {m['creator']['nick']}")
    elif choice == "4":
        print("\n🔥 Hot Maps:")
        maps = browse_hot_maps()
        if maps:
            for i, m in enumerate(maps, 1):
                print(f"{i}. {m['name']} by {m['creator']['nick']}")
    else:
        print("Invalid choice")
        return

    if maps:
        print(f"\n✅ Retrieved {len(maps)} maps!")


if __name__ == '__main__':
    main()
