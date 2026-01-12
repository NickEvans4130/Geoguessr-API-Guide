"""
Search Maps

Search for GeoGuessr maps by name or keywords.

Usage:
    python search_maps.py

Requirements:
    pip install requests

Note: This endpoint does NOT require authentication
"""

import requests


def search_maps(query):
    """
    Search for maps by name or keywords.

    Args:
        query (str): Search query

    Returns:
        list: List of matching maps
    """
    try:
        url = f'https://www.geoguessr.com/api/v3/search/map?q={query}'

        # Note: No authentication required for searching maps
        response = requests.get(url)
        response.raise_for_status()

        maps = response.json()

        if len(maps) == 0:
            print(f"❌ No maps found matching '{query}'")
            return []

        print(f"\n🔍 Search Results for '{query}' ({len(maps)} maps found)\n")
        print(f"{'#':<4} {'Map Name':<40} {'Creator':<20} {'Locations'}")
        print('-' * 90)

        for index, map_data in enumerate(maps, 1):
            name = map_data['name'][:39]
            creator = map_data['creator']['nick'][:19]
            locations = map_data.get('coordinateCount', 'Unknown')

            print(f"{index:<4} {name:<40} {creator:<20} {locations}")

        # Show map links
        print(f"\n🔗 Map Links:")
        for map_data in maps[:10]:  # Show first 10
            print(f"{map_data['name']}: https://www.geoguessr.com/maps/{map_data['id']}")

        # Show difficulty distribution
        difficulties = {}
        for map_data in maps:
            diff = map_data.get('difficulty', 'Unknown')
            difficulties[diff] = difficulties.get(diff, 0) + 1

        if difficulties:
            print(f"\n📊 Difficulty Distribution:")
            for diff, count in sorted(difficulties.items(), key=lambda x: x[1], reverse=True):
                print(f"  {diff}: {count}")

        return maps

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if e.response.status_code == 400:
            print("Note: Empty search queries are not allowed")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return None


def main():
    print("=== GeoGuessr Map Search ===\n")

    query = input("Enter map name or keyword to search: ").strip()

    if not query:
        print("❌ Search query cannot be empty")
        return

    maps = search_maps(query)

    if maps:
        print(f"\n✅ Found {len(maps)} maps!")


if __name__ == '__main__':
    main()
