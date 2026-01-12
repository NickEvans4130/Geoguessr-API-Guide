# Feed & Activity API

Endpoints for viewing activity feeds and recent games.

## Table of Contents

- [Overview](#overview)
- [Endpoints](#endpoints)
- [Implementation Examples](#implementation-examples)

## Overview

Feed endpoints provide activity streams showing recent games, achievements, and social interactions.

**🚀 Ready to use?** Check out the [feed examples](../examples/javascript/feed/) for ready-to-use scripts:
- [Get Friends Activity](../examples/javascript/feed/get-friends-activity.js) - View recent games and activities from friends

## Endpoints

### Friends Feed

Returns paginated activity feed showing recent games and activities from friends.

**Endpoint:**
```
GET /v4/feed/friends
```

**Parameters:**
- `paginationToken` (optional) - Token for next page of results

**Authentication:** Required

**Response:** Object with entries array and pagination token

**Example Response:**
```json
{
  "entries": [
    {
      "type": 6,
      "time": "2026-01-10T23:54:38.8070000Z",
      "user": {
        "id": "62eed3439a1387b217f5832d",
        "nick": "Baumi_geo",
        "isVerified": false,
        "flair": 1,
        "avatar": {
          "url": "pin/48fe421b7cd6be62178d5473e8ce9303.png",
          "anchor": "center-center",
          "isDefault": false
        }
      },
      "payload": "{\"gameId\":\"6962e5f93137693efd1a1934\",\"gameMode\":\"Duels\",\"competitiveGameMode\":\"NmpzDuels\"}"
    },
    {
      "type": 2,
      "time": "2026-01-10T23:52:29.8430000Z",
      "user": {
        "id": "68cb3fdf6f672817f40cf951",
        "nick": "xxfeetluver69 🤤👅🦶",
        "isVerified": false,
        "flair": 0,
        "avatar": {
          "url": "pin/0129cf1d31e8148ad599d34a1547a586.png",
          "anchor": "center-center",
          "isDefault": false
        }
      },
      "payload": "{\"mapSlug\":\"world\",\"mapName\":\"World\",\"points\":462,\"challengeToken\":\"EtWujm3fioJMP5d0\",\"gameMode\":\"Standard\",\"isDailyChallenge\":false}"
    }
  ],
  "paginationToken": "eyJDcmVhdGVkIjp7IlMiOiIyMDI2LTAxLTEwVDIyOjQ4OjUyLjkwNloifSwiSGFzaEtleSI6eyJTIjoiNWRiOWYwNTdkZmE1MTAyMTMwZWFmNzQ3X2ZyaWVuZHMifX0="
}
```

**Important Notes:**
- Returns ~31 entries per page
- Use `paginationToken` for next page: `/v4/feed/friends?paginationToken=...`
- `type` is numeric (see Activity Types section)
- `payload` is a JSON string that needs parsing
- Results ordered by most recent first

---

### Private Feed

Get the authenticated user's private activity feed.

**Endpoint:**
```
GET /v4/feed/private
```

**Authentication:** Required

**Expected Response:** (Structure needs verification)
Similar to friends feed but includes personal activities and notifications.

**Example Request:**
```javascript
fetch('https://www.geoguessr.com/api/v4/feed/private', {
    credentials: 'include'
})
```

---

### Likes

Get or manage likes on maps and content.

**Endpoint:**
```
GET /v3/likes
```

**Authentication:** Required

**Expected Response:** (Structure needs verification)
List of maps or content the user has liked.

**Example Request:**
```javascript
fetch('https://www.geoguessr.com/api/v3/likes', {
    credentials: 'include'
})
```

---

## Data Structures

### Feed Response Object

```typescript
interface FeedResponse {
  entries: FeedEntry[];         // Array of feed entries
  paginationToken: string;      // Token for next page (base64 encoded)
}
```

### Feed Entry Object

Complete feed entry structure:

```typescript
interface FeedEntry {
  type: number;                 // Activity type (numeric: 2, 6, 7, 9, 11, etc.)
  time: string;                 // ISO 8601 timestamp
  user: {
    id: string;                 // User ID (24-character hex)
    nick: string;               // Username
    isVerified: boolean;        // Verified status
    flair: number;              // Flair level
    avatar: {
      url: string;              // Avatar image URL
      anchor: string;           // "center-center"
      isDefault: boolean;       // Whether using default avatar
    };
  };
  payload: string;              // JSON string containing activity data (needs parsing)
}
```

### Payload Structures

The `payload` field is a JSON string that varies by activity type. Parse it with `JSON.parse()`.

**Type 2 - Standard Game Completed:**
```typescript
interface Type2Payload {
  mapSlug: string;              // Map identifier
  mapName: string;              // Map display name
  points: number;               // Score achieved
  challengeToken: string;       // Challenge token
  gameMode: string;             // "Standard"
  isDailyChallenge: boolean;    // Whether daily challenge
}
```

**Type 6 - Competitive Game (Duels):**
```typescript
interface Type6Payload {
  gameId: string;               // Game identifier
  gameMode: string;             // "Duels"
  competitiveGameMode: string;  // "NmpzDuels", "NoMoveDuels", "StandardDuels"
}
```

**Type 9 - Party Game:**
```typescript
interface Type9Payload {
  gameId: string;               // Game UUID
  partyId: string;              // Party UUID
  gameMode: string;             // "Bullseye", "Duels", etc.
}
```

**Type 11 - Competitive Game Result:**
```typescript
interface Type11Payload {
  gameId: string;               // Game identifier
  gameMode: string;             // "Duels"
  competitiveGameMode: string;  // Duel mode type
}
```

**Type 7 - Batch Activity:**
```typescript
// Payload is an array of activities (JSON string of array)
type Type7Payload = Array<{
  type: number;
  time: string;
  payload: object;
}>;
```

---

## Implementation Examples

### Example 1: Get Friends Feed

**JavaScript:**
```javascript
async function getFriendsFeed(paginationToken = null) {
    const url = paginationToken
        ? `https://www.geoguessr.com/api/v4/feed/friends?paginationToken=${encodeURIComponent(paginationToken)}`
        : 'https://www.geoguessr.com/api/v4/feed/friends';

    const response = await fetch(url, {
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    console.log(`Found ${data.entries.length} activities from friends`);

    data.entries.forEach(entry => {
        console.log(`[${entry.time}] ${entry.user.nick}: Type ${entry.type}`);

        // Parse payload for more details
        const payload = JSON.parse(entry.payload);
        if (entry.type === 2) {
            console.log(`  → Scored ${payload.points} on ${payload.mapName}`);
        } else if (entry.type === 6 || entry.type === 11) {
            console.log(`  → Played ${payload.competitiveGameMode}`);
        }
    });

    return data;
}

// Usage
const feed = await getFriendsFeed();

// Get next page
if (feed.paginationToken) {
    const nextPage = await getFriendsFeed(feed.paginationToken);
}
```

**Python:**
```python
import requests
import json

def get_friends_feed(cookie, pagination_token=None):
    url = 'https://www.geoguessr.com/api/v4/feed/friends'
    params = {}
    if pagination_token:
        params['paginationToken'] = pagination_token

    response = requests.get(url, cookies={'_ncfa': cookie}, params=params)
    response.raise_for_status()

    data = response.json()
    print(f"Found {len(data['entries'])} activities from friends")

    for entry in data['entries']:
        user = entry['user']['nick']
        activity_type = entry['type']
        timestamp = entry['time']
        print(f"[{timestamp}] {user}: Type {activity_type}")

        # Parse payload for more details
        payload = json.loads(entry['payload'])
        if activity_type == 2:
            print(f"  → Scored {payload['points']} on {payload['mapName']}")
        elif activity_type in [6, 11]:
            print(f"  → Played {payload['competitiveGameMode']}")

    return data

# Usage
# feed = get_friends_feed('YOUR_NCFA_COOKIE')

# Get next page
# if 'paginationToken' in feed:
#     next_page = get_friends_feed('YOUR_NCFA_COOKIE', feed['paginationToken'])
```

---

### Example 2: Get Private Feed

**JavaScript:**
```javascript
async function getPrivateFeed() {
    const response = await fetch('https://www.geoguessr.com/api/v4/feed/private', {
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const feed = await response.json();
    console.log(`You have ${feed.length} activities`);
    return feed;
}

// Usage
const myActivity = await getPrivateFeed();
```

---

### Example 3: Display Activity Feed

**JavaScript:**
```javascript
async function displayActivityFeed() {
    const feedData = await getFriendsFeed();

    const html = feedData.entries.map(entry => {
        const date = new Date(entry.time).toLocaleString();
        const payload = JSON.parse(entry.payload);

        switch (entry.type) {
            case 2: // Standard game completed
                return `
                    <div class="feed-item">
                        <strong>${entry.user.nick}</strong> scored ${payload.points} points on ${payload.mapName}
                        <span class="time">${date}</span>
                    </div>
                `;
            case 6: // Competitive game
                return `
                    <div class="feed-item">
                        <strong>${entry.user.nick}</strong> started a ${payload.competitiveGameMode} game
                        <span class="time">${date}</span>
                    </div>
                `;
            case 9: // Party game
                return `
                    <div class="feed-item">
                        <strong>${entry.user.nick}</strong> is playing ${payload.gameMode}
                        <span class="time">${date}</span>
                    </div>
                `;
            case 11: // Competitive game result
                return `
                    <div class="feed-item">
                        <strong>${entry.user.nick}</strong> finished a ${payload.competitiveGameMode} game
                        <span class="time">${date}</span>
                    </div>
                `;
            default:
                return `
                    <div class="feed-item">
                        <strong>${entry.user.nick}</strong> - Activity type ${entry.type}
                        <span class="time">${date}</span>
                    </div>
                `;
        }
    }).join('');

    return html;
}
```

---

## Common Use Cases

### 1. Activity Dashboard

```javascript
async function getActivityDashboard() {
    const friendsFeed = await getFriendsFeed();

    return {
        friends: friendsFeed.entries.slice(0, 10), // Latest 10 from friends
        total: friendsFeed.entries.length,
        hasMore: !!friendsFeed.paginationToken
    };
}

// Usage
// const dashboard = await getActivityDashboard();
```

### 2. Get All Feed Pages

```javascript
async function getAllFeedEntries(maxPages = 5) {
    let allEntries = [];
    let paginationToken = null;
    let page = 0;

    while (page < maxPages) {
        const feedData = await getFriendsFeed(paginationToken);
        allEntries.push(...feedData.entries);

        if (!feedData.paginationToken) {
            break; // No more pages
        }

        paginationToken = feedData.paginationToken;
        page++;
    }

    console.log(`Fetched ${allEntries.length} entries across ${page + 1} pages`);
    return allEntries;
}

// Usage
// const allActivities = await getAllFeedEntries(5);
```

### 3. Filter Feed by Activity Type

```javascript
function filterFeedByType(entries, activityType) {
    return entries.filter(entry => entry.type === activityType);
}

// Usage
// const feedData = await getFriendsFeed();
// const standardGames = filterFeedByType(feedData.entries, 2); // Type 2 = standard games
// const duels = filterFeedByType(feedData.entries, 6); // Type 6 = competitive games
// const partyGames = filterFeedByType(feedData.entries, 9); // Type 9 = party games
```

---

## Testing

See [feed-testing.md](./tests/feed-testing.md) for console commands to test these endpoints.

---

## Notes for Documentation Contributors

**Verified:**
- [x] Complete feed response structure (entries array + paginationToken)
- [x] Feed entry structure (type, time, user, payload)
- [x] Pagination support (~31 entries per page)
- [x] Activity types 2, 6, 7, 9, 11 documented
- [x] Payload structure varies by type (JSON string needs parsing)
- [x] User object structure in feed entries
- [x] Payload structures for types 2, 6, 9, 11

**Still needs verification:**
- [ ] Private feed endpoint structure (/v4/feed/private)
- [ ] All activity types (only 2, 6, 7, 9, 11 verified)
- [ ] Time range filtering capabilities
- [ ] Feed refresh rate limits
- [ ] Notification preferences endpoints
- [ ] Like/unlike endpoints structure
- [ ] Comment functionality (if exists)
- [ ] Share functionality endpoints

---

## Activity Types

Activity types are represented as **numeric values**:

**Verified Types:**
- `2` - Standard game completed (contains: mapSlug, mapName, points, challengeToken, gameMode, isDailyChallenge)
- `6` - Competitive game started/in progress (contains: gameId, gameMode "Duels", competitiveGameMode)
- `7` - Batch activity (payload is array of multiple activities)
- `9` - Party game activity (contains: gameId, partyId, gameMode like "Bullseye")
- `11` - Competitive game result/completed (contains: gameId, gameMode, competitiveGameMode)

**Competitive Game Modes** (seen in Type 6/11):
- `NmpzDuels` - No move, pan, zoom duels
- `NoMoveDuels` - No movement duels
- `StandardDuels` - Standard duels

**Note:** Additional activity types may exist. The `payload` structure varies by type and should be parsed as JSON.
