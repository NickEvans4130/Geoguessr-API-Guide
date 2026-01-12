# Maps API

Endpoints for browsing, searching, and managing maps.

## Table of Contents

- [Overview](#overview)
- [Endpoints](#endpoints)
- [Implementation Examples](#implementation-examples)

## Overview

Maps are collections of locations used to create games. Users can create custom maps or play official/community maps.

**🚀 Ready to use?** Check out the [maps examples](../examples/javascript/maps/) for ready-to-use scripts:
- [Browse Popular Maps](../examples/javascript/maps/browse-popular-maps.js) - Discover popular community maps with statistics

## Endpoints

### Browse Maps

#### Browse Featured Maps

Returns 10 featured maps curated by GeoGuessr.

**Endpoint:**
```
GET /v3/social/maps/browse/featured
```

**Authentication:** Not required

**Response:** Array of 10 map objects (see Data Structures section for complete object)

---

#### Browse Popular Maps (All)

Returns 10 popular community maps sorted by popularity.

**Endpoint:**
```
GET /v3/social/maps/browse/popular/all
```

**Authentication:** Not required

**Response:** Array of 10 map objects sorted by likes/popularity

---

#### Browse Popular Official Maps

Returns 10 popular official GeoGuessr maps.

**Endpoint:**
```
GET /v3/social/maps/browse/popular/official
```

**Authentication:** Not required

**Response:** Array of 10 official map objects

---

### Search Maps

#### Search for Maps

Search for maps by name. Returns up to 10 results.

**Endpoint:**
```
GET /v4/search/map?q={query}
```

**Parameters:**
- `q` (query) - Search query (map name, can be empty for default results)

**Authentication:** Required

**Example Request:**
```javascript
const query = 'world';
fetch(`https://www.geoguessr.com/api/v4/search/map?q=${encodeURIComponent(query)}`, {
    credentials: 'include'
})
```

**Response:** Array of up to 10 map objects matching the search query

**Important Notes:**
- Empty query string returns default popular maps (still returns 200)
- Search is case-insensitive
- Partial matching is supported
- Returns same structure as browse endpoints

---

### Map Scores

#### Get Map Scores

**This endpoint currently returns HTTP 500 error.**

**Endpoint:**
```
GET /v3/scores/maps
```

**Authentication:** Required

**Status:** Returns 500 Internal Server Error (endpoint may be deprecated or experiencing issues)

---

## Data Structures

### Map Object

Complete map object structure with all 36 fields:

```typescript
interface MapObject {
  id: string;                    // Unique map ID (24-character hex)
  name: string;                  // Map name
  slug: string;                  // URL slug (usually same as ID)
  description: string | null;    // Map description
  url: string;                   // Map page URL path
  playUrl: string;               // Play URL path
  published: boolean;            // Whether map is published
  banned: boolean;               // Whether map is banned

  images: {
    backgroundLarge: string | null;
    incomplete: boolean;
  };

  bounds: {                      // Geographic bounds
    min: {
      lat: number;
      lng: number;
    };
    max: {
      lat: number;
      lng: number;
    };
  };

  customCoordinates: any | null;
  coordinateCount: string;       // Formatted string: "10K+", "100K+", "1M+"
  regions: any | null;

  creator: {                     // Map creator (full user object)
    nick: string;
    id: string;
    countryCode: string;
    isProUser: boolean;
    type: string;
    isVerified: boolean;
    pin: {
      url: string;
      anchor: string;
      isDefault: boolean;
    };
    customImage: string | null;
    fullBodyPin: string;
    borderUrl: string;
    color: number;
    url: string;
    br: {
      level: number;
      division: number;
    };
    streakProgress: any | null;
    explorerProgress: any | null;
    dailyChallengeProgress: number;
    lastClaimedLevel: number;
    progress: {
      xp: number;
      level: number;
      levelXp: number;
      nextLevel: number;
      nextLevelXp: number;
      title: {
        id: number;
        tierId: number;
      };
      competitionMedals: {
        bronze: number;
        silver: number;
        gold: number;
        platinum: number;
      };
    };
    competitive: {
      elo: number;
      rating: number;
      lastRatingChange: number;
      division: {
        type: number;
        startRating: number;
        endRating: number;
      };
      onLeaderboard: boolean;
    };
    lastNameChange: string;
    lastNickOrCountryChange: string;
    isBanned: boolean;
    chatBan: boolean;
    nameChangeAvailableAt: string | null;
    avatar: {
      fullBodyPath: string;
    };
    isBotUser: boolean;
    suspendedUntil: string | null;
    wallet: any | null;
    flair: number;
    isCreator: boolean;
    isAppAnonymous: boolean;
    club: {
      tag: string;
      clubId: string;
      level: number;
    } | null;
  };

  createdAt: string;             // ISO 8601 timestamp
  updatedAt: string;             // ISO 8601 timestamp
  numFinishedGames: number;      // Number of completed games
  likedByUser: boolean | null;   // Whether current user liked it
  averageScore: number;          // Average score across all games

  avatar: {                      // Map avatar/thumbnail
    background: string;
    decoration: string;
    ground: string;
    landscape: string;
  };

  difficulty: string;            // "EASY", "MEDIUM", "HARD"
  difficultyLevel: number;       // Numeric difficulty (1-5)
  highscore: any | null;         // User's high score on this map
  isUserMap: boolean;            // Whether it's user-created
  highlighted: boolean;          // Whether map is highlighted
  deleted: boolean;              // Whether map is deleted
  free: boolean;                 // Whether map is free to play
  panoramaProvider: string;      // "StreetView" or other providers
  inExplorerMode: boolean;
  maxErrorDistance: number;      // Maximum distance error in meters
  likes: number;                 // Number of likes
  locationSelectionMode: number; // Location selection mode
  tags: string[];                // Map tags (e.g., "Global", "Hand-picked")
  collaborators: any | null;     // Map collaborators
  flair: number;                 // Map flair level
  mapSize: any | null;           // Map size metadata
}
```

**Key Fields:**
- `coordinateCount`: Formatted as "250+", "1000+", "10K+", "50K+", "100K+", "1M+"
- `creator`: Full user object with all profile information
- `difficulty`: String values "EASY", "MEDIUM", "HARD"
- `difficultyLevel`: Numeric 1-5
- `tags`: Array of strings like "Global", "Hand-picked", "Official Cov."

---

## Implementation Examples

### Example 1: Browse Featured Maps

**JavaScript:**
```javascript
async function getFeaturedMaps() {
    const response = await fetch('https://www.geoguessr.com/api/v3/social/maps/browse/featured', {
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const maps = await response.json();
    console.log(`Found ${maps.length} featured maps`);

    maps.forEach(map => {
        console.log(`- ${map.name} (${map.numLocations || 'unknown'} locations)`);
    });

    return maps;
}

// Usage
const featured = await getFeaturedMaps();
```

**Python:**
```python
import requests

def get_featured_maps(cookie=None):
    url = 'https://www.geoguessr.com/api/v3/social/maps/browse/featured'

    cookies = {'_ncfa': cookie} if cookie else None
    response = requests.get(url, cookies=cookies)
    response.raise_for_status()

    maps = response.json()
    print(f'Found {len(maps)} featured maps')

    for map_data in maps:
        locations = map_data.get('numLocations', 'unknown')
        print(f"- {map_data['name']} ({locations} locations)")

    return maps

# Usage
# featured = get_featured_maps('YOUR_NCFA_COOKIE')
```

---

### Example 2: Search for Maps

**JavaScript:**
```javascript
async function searchMaps(query) {
    const url = `https://www.geoguessr.com/api/v4/search/map?q=${encodeURIComponent(query)}`;

    const response = await fetch(url, { credentials: 'include' });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const results = await response.json();
    console.log(`Found ${results.length} maps matching "${query}"`);

    results.forEach(map => {
        console.log(`- ${map.name} by ${map.creator?.nick || 'Unknown'}`);
    });

    return results;
}

// Usage
const results = await searchMaps('europe');
```

**Python:**
```python
import requests
from urllib.parse import quote

def search_maps(query, cookie):
    url = f'https://www.geoguessr.com/api/v4/search/map?q={quote(query)}'

    response = requests.get(url, cookies={'_ncfa': cookie})
    response.raise_for_status()

    results = response.json()
    print(f'Found {len(results)} maps matching "{query}"')

    for map_data in results:
        creator = map_data.get('creator', {}).get('nick', 'Unknown')
        print(f"- {map_data['name']} by {creator}")

    return results

# Usage
# results = search_maps('europe', 'YOUR_NCFA_COOKIE')
```

---

### Example 3: Get Popular Maps

**JavaScript:**
```javascript
async function getPopularMaps(official = false) {
    const endpoint = official ? 'popular/official' : 'popular/all';
    const url = `https://www.geoguessr.com/api/v3/social/maps/browse/${endpoint}`;

    const response = await fetch(url, { credentials: 'include' });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const maps = await response.json();
    const type = official ? 'official' : 'community';
    console.log(`Found ${maps.length} popular ${type} maps`);

    return maps;
}

// Usage
const officialMaps = await getPopularMaps(true);
const communityMaps = await getPopularMaps(false);
```

---

## Common Use Cases

### 1. Map Browser UI

```javascript
async function buildMapBrowser() {
    const [featured, popular] = await Promise.all([
        getFeaturedMaps(),
        getPopularMaps()
    ]);

    return {
        featured: featured,
        popular: popular,
        categories: ['Featured', 'Popular', 'Official']
    };
}

// Usage
// const mapData = await buildMapBrowser();
```

### 2. Map Search with Autocomplete

```javascript
async function autocompleteMapSearch(query, limit = 5) {
    if (query.length < 2) return [];

    const results = await searchMaps(query);

    return results.slice(0, limit).map(map => ({
        label: map.name,
        value: map.id,
        creator: map.creator?.nick
    }));
}

// Usage
// const suggestions = await autocompleteMapSearch('world');
```

### 3. Fetch Map by ID

```javascript
async function getMapById(mapId) {
    // Note: Exact endpoint TBD, might be /v3/maps/{mapId}
    const response = await fetch(
        `https://www.geoguessr.com/api/v3/maps/${mapId}`,
        { credentials: 'include' }
    );

    if (!response.ok) {
        throw new Error(`Map not found: ${mapId}`);
    }

    return await response.json();
}
```

---

## Testing

See [maps-testing.md](./tests/maps-testing.md) for console commands to test these endpoints.

---

## Notes for Documentation Contributors

The following aspects need verification:

- [ ] Complete map object structure
- [ ] Pagination for browse endpoints
- [ ] Search result format
- [ ] Map creation endpoint
- [ ] Map editing/deletion endpoints
- [ ] Map likes/favorites endpoint
- [ ] Map statistics structure
- [ ] Individual map details endpoint
