# Social & Friends API

Endpoints for managing friends, badges, and social interactions.

## Table of Contents

- [Overview](#overview)
- [Endpoints](#endpoints)
- [Implementation Examples](#implementation-examples)

## Overview

Social features include friends management, badge collection, and community events.

## Endpoints

### Friends Management

#### Get Friends List

Returns array of all friends for the authenticated user.

**Endpoint:**
```
GET /v3/social/friends
```

**Authentication:** Required

**Response:** Array of friend objects (full user objects)

**Example Response:**
```json
[
  {
    "userId": "553c3b7df27d47b63064cf80",
    "url": "/user/553c3b7df27d47b63064cf80",
    "nick": "username",
    "pin": {
      "url": "pin/...",
      "anchor": "center-center",
      "isDefault": false
    },
    "isProUser": true,
    "isVerified": false,
    "progress": {
      "xp": 123456,
      "level": 42,
      "levelXp": 120000,
      "nextLevel": 43,
      "nextLevelXp": 130000
    },
    "isOnline": false,
    "activity": null,
    "avatar": {
      "fullBodyPath": "pin/..."
    },
    "countryCode": "us",
    "flair": 0
  }
]
```

**Important Notes:**
- Returns complete array (no pagination)
- Each friend object contains full user information
- Use `userId` field for user ID (not `id`)
- `isOnline` indicates current online status
- `activity` contains current game activity if online

---

#### Get Friend Requests Received

Returns array of pending friend requests received from other users.

**Endpoint:**
```
GET /v3/social/friends/received
```

**Authentication:** Required

**Response:** Array of friend request objects (same structure as friends list)

**Example Response:**
```json
[
  {
    "userId": "5ecb6f24282ad28b94fd3705",
    "url": "/user/5ecb6f24282ad28b94fd3705",
    "nick": "requesting_user",
    "pin": {
      "url": "pin/...",
      "anchor": "center-center",
      "isDefault": false
    },
    "isProUser": true,
    "isVerified": false,
    "progress": {
      "xp": 98765,
      "level": 35
    },
    "isOnline": false,
    "activity": null,
    "avatar": {
      "fullBodyPath": "pin/..."
    },
    "countryCode": "gb",
    "flair": 0
  }
]
```

**Important Notes:**
- Returns complete array of all pending requests
- Same object structure as friends list
- No timestamp field for when request was sent

---

#### Get Friend Requests Sent

Returns array of friend requests you have sent to other users.

**Endpoint:**
```
GET /v3/social/friends/sent
```

**Authentication:** Required

**Response:** Array of friend request objects (same structure as friends list)

**Important Notes:**
- Returns empty array if no pending outgoing requests
- Same object structure as received friend requests

---

#### Get Friend Suggestions

Returns array of suggested friends based on mutual friends, location, or other factors.

**Endpoint:**
```
GET /v3/social/friends/suggestions
```

**Authentication:** Required

**Response:** Array of user objects (same structure as friends list)

**Important Notes:**
- May return empty array if no suggestions available
- Same object structure as friends list

---

### Badges & Achievements

#### Get Unclaimed Badges

Returns array of badges earned but not yet claimed by the user.

**Endpoint:**
```
GET /v3/social/badges/unclaimed
```

**Authentication:** Required

**Response:** Array of badge objects

**Example Response:**
```json
[]
```

**Important Notes:**
- Returns empty array if all badges are claimed
- Badge structure includes: id, name, hint, description, imagePath (see claimed badges endpoint for structure)

---

#### Get Claimed Badges

Returns array of all badges that have been claimed by the user.

**Endpoint:**
```
GET /v3/social/badges/claimed
```

**Authentication:** Required

**Response:** Array of badge objects

**Example Response:**
```json
[
  {
    "id": "J6O8UdR14vIqZMkiTWrnFXCgCDxh0X4a",
    "name": "Around the world",
    "hint": "Complete a trip around the world in singleplayer",
    "description": null,
    "imagePath": "badge/005d244aaf428e671f70eaf3fd38ab7d.png"
  }
]
```

**Badge Object Fields:**
- `id` - Unique badge identifier
- `name` - Display name of the badge
- `hint` - Description of how to earn the badge
- `description` - Additional description (may be null)
- `imagePath` - Relative path to badge image

---

#### Claim Badge

Claims an unclaimed badge. (Endpoint structure needs verification)

**Endpoint:**
```
POST /v3/social/badges/claim
```

**Authentication:** Required

**Request Body:** (Structure needs verification)
```json
{
  "badgeId": "badge_id_here"
}
```

**Expected Response:** (Structure needs verification)

---

### Social Events

#### Get Unfinished Games

Returns paginated list of games started but not completed.

**Endpoint:**
```
GET /v3/social/events/unfinishedgames
```

**Authentication:** Required

**Parameters:**
- `offset` (optional) - Pagination offset (default: 0)

**Response:** Object with games array and pagination token

**Example Response:**
```json
{
  "games": [
    {
      "token": "22RJcUdUUwTswQVS",
      "map": "United Kingdom",
      "mapSlug": "uk",
      "score": {
        "amount": "695",
        "unit": "points",
        "percentage": 2.78
      },
      "dateTime": "2026-01-11T00:16:45.4500000Z",
      "lastActivity": "2026-01-11T00:16:51.2820000Z",
      "guesses": [
        {
          "score": {
            "amount": "695",
            "unit": "points",
            "percentage": 13.9
          },
          "distance": {
            "meters": {
              "amount": "219.2",
              "unit": "km"
            },
            "miles": {
              "amount": "136.2",
              "unit": "miles"
            }
          }
        }
      ],
      "rounds": 5,
      "round": 2,
      "type": 0,
      "mode": 0,
      "locationThumbnail": "https://maps.googleapis.com/...",
      "mapImage": "map/33519c07b513f9348cdcae06637ccdd2.jpg",
      "mapAvatar": {
        "background": "morning",
        "decoration": "palmtrees",
        "ground": "green",
        "landscape": "snowmountains"
      }
    }
  ],
  "nextOffset": "10"
}
```

**Unfinished Game Object Fields:**
- `token` - Game token to resume game
- `map` - Map name
- `mapSlug` - Map identifier
- `score` - Current score with amount, unit, and percentage
- `dateTime` - When game was started (ISO 8601)
- `lastActivity` - Last interaction time (ISO 8601)
- `guesses` - Array of completed round guesses
- `rounds` - Total number of rounds
- `round` - Current round number
- `type` - Game type (0 = standard)
- `mode` - Game mode (0 = normal, 1 = country streak, etc.)
- `locationThumbnail` - Street View thumbnail URL
- `mapImage` - Map image path (may be null)
- `mapAvatar` - Map visual theme object (may be null)

**Important Notes:**
- Returns 10 games per page
- Use `nextOffset` for pagination
- Games are sorted by most recent activity

---

## Data Structures

### Friend Object

Complete friend/user object structure:

```typescript
interface FriendObject {
  userId: string;                // User ID (24-character hex)
  url: string;                   // Profile URL path
  nick: string;                  // Username
  pin: {
    url: string;
    anchor: string;
    isDefault: boolean;
  };
  isProUser: boolean;            // Has Pro subscription
  isVerified: boolean;           // Verified account
  progress: {
    xp: number;
    level: number;
    levelXp: number;
    nextLevel: number;
    nextLevelXp: number;
    title?: {
      id: number;
      tierId: number;
    };
  };
  isOnline: boolean;             // Current online status
  activity: any | null;          // Current game activity
  avatar: {
    fullBodyPath: string;
  };
  countryCode: string;           // 2-letter ISO country code
  flair: number;                 // Flair level
  customImage?: string;
  fullBodyPin?: string;
  borderUrl?: string;
  color?: number;
}
```

**Important:** Friends use `userId` field, not `id`.

---

### Badge Object

```typescript
interface BadgeObject {
  id: string;                    // Unique badge identifier
  name: string;                  // Display name
  hint: string;                  // How to earn description
  description: string | null;    // Additional details
  imagePath: string;             // Relative path to badge image
}
```

---

### Unfinished Game Object

```typescript
interface UnfinishedGame {
  token: string;                 // Game token to resume
  map: string;                   // Map display name
  mapSlug: string;               // Map identifier
  score: {
    amount: string;              // Current score as string
    unit: "points";
    percentage: number;          // Score percentage
  };
  dateTime: string;              // Game start time (ISO 8601)
  lastActivity: string;          // Last interaction (ISO 8601)
  guesses: Array<{               // Completed round guesses
    score: {
      amount: string;
      unit: "points";
      percentage: number;
    };
    distance: {
      meters: {
        amount: string;
        unit: "km";
      };
      miles: {
        amount: string;
        unit: "miles";
      };
    };
  }>;
  rounds: number;                // Total rounds
  round: number;                 // Current round
  type: number;                  // Game type (0 = standard)
  mode: number;                  // Game mode (0 = normal, 1 = streak, etc.)
  locationThumbnail: string;     // Street View thumbnail URL
  mapImage: string | null;       // Map image path
  mapAvatar: {                   // Map visual theme
    background: string;
    decoration: string;
    ground: string;
    landscape: string;
  } | null;
}
```

---

## Non-Existent Endpoints

The following endpoints **do not exist** and return HTTP 404:

- `GET /v3/social/events` - Social events list
- `GET /v3/social/events/recent` - Recent social events
- `GET /v4/social/events` - Social events (v4)
- `GET /v3/social/activity` - User activity feed
- `GET /v3/social/notifications` - Notifications
- `GET /v3/social/badges` - All badges endpoint
- `GET /v3/social/leaderboard` - Social leaderboard

If you need social events data, use the `/v3/social/events/unfinishedgames` endpoint which is available.

---

## Implementation Examples

### Example 1: Get Friends List

**JavaScript:**
```javascript
async function getFriends() {
    const response = await fetch('https://www.geoguessr.com/api/v3/social/friends', {
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const friends = await response.json();
    console.log(`You have ${friends.length} friends`);

    friends.forEach(friend => {
        console.log(`- ${friend.nick} (${friend.countryCode})`);
    });

    return friends;
}

// Usage
const friends = await getFriends();
```

**Python:**
```python
import requests

def get_friends(cookie):
    url = 'https://www.geoguessr.com/api/v3/social/friends'
    response = requests.get(url, cookies={'_ncfa': cookie})
    response.raise_for_status()

    friends = response.json()
    print(f'You have {len(friends)} friends')

    for friend in friends:
        print(f"- {friend['nick']} ({friend['countryCode']})")

    return friends

# Usage
# friends = get_friends('YOUR_NCFA_COOKIE')
```

---

### Example 2: Check for Unclaimed Badges

**JavaScript:**
```javascript
async function checkUnclaimedBadges() {
    const response = await fetch('https://www.geoguessr.com/api/v3/social/badges/unclaimed', {
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const badges = await response.json();

    if (badges.length > 0) {
        console.log(`You have ${badges.length} unclaimed badges!`);
        return badges;
    } else {
        console.log('No unclaimed badges');
        return [];
    }
}

// Usage
const unclaimed = await checkUnclaimedBadges();
```

---

### Example 3: Get Friend Requests

**JavaScript:**
```javascript
async function getFriendRequests() {
    const response = await fetch('https://www.geoguessr.com/api/v3/social/friends/received', {
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const requests = await response.json();
    console.log(`You have ${requests.length} pending friend requests`);
    return requests;
}

// Usage
const requests = await getFriendRequests();
```

---

### Example 4: Get Unfinished Games with Pagination

**JavaScript:**
```javascript
async function getUnfinishedGames(offset = 0) {
    const url = `https://www.geoguessr.com/api/v3/social/events/unfinishedgames?offset=${offset}`;
    const response = await fetch(url, { credentials: 'include' });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    console.log(`Found ${data.games.length} unfinished games`);

    data.games.forEach(game => {
        console.log(`- ${game.map} (Round ${game.round}/${game.rounds})`);
    });

    return data;
}

// Get all unfinished games with pagination
async function getAllUnfinishedGames() {
    let allGames = [];
    let offset = 0;

    while (true) {
        const data = await getUnfinishedGames(offset);
        allGames.push(...data.games);

        if (!data.nextOffset) break;
        offset = parseInt(data.nextOffset);
    }

    console.log(`Total unfinished games: ${allGames.length}`);
    return allGames;
}

// Usage
const unfinished = await getAllUnfinishedGames();
```

**Python:**
```python
import requests

def get_unfinished_games(cookie, offset=0):
    url = f'https://www.geoguessr.com/api/v3/social/events/unfinishedgames?offset={offset}'
    response = requests.get(url, cookies={'_ncfa': cookie})
    response.raise_for_status()

    data = response.json()
    print(f"Found {len(data['games'])} unfinished games")

    for game in data['games']:
        print(f"- {game['map']} (Round {game['round']}/{game['rounds']})")

    return data

# Get all unfinished games with pagination
def get_all_unfinished_games(cookie):
    all_games = []
    offset = 0

    while True:
        data = get_unfinished_games(cookie, offset)
        all_games.extend(data['games'])

        if 'nextOffset' not in data:
            break
        offset = int(data['nextOffset'])

    print(f"Total unfinished games: {len(all_games)}")
    return all_games

# Usage
# unfinished = get_all_unfinished_games('YOUR_NCFA_COOKIE')
```

---

## Common Use Cases

### 1. Display Friends List

```javascript
async function displayFriendsList() {
    const friends = await getFriends();

    const html = `
        <ul class="friends-list">
            ${friends.map(friend => `
                <li>
                    <span class="flag">${friend.countryCode}</span>
                    <span class="name">${friend.nick}</span>
                    ${friend.isVerified ? '<span class="verified">✓</span>' : ''}
                </li>
            `).join('')}
        </ul>
    `;

    return html;
}
```

### 2. Badge Notification System

```javascript
async function checkForNewBadges() {
    const badges = await checkUnclaimedBadges();

    if (badges.length > 0) {
        // Show notification
        console.log(`🏆 You earned ${badges.length} new badge(s)!`);

        // Auto-claim badges
        for (const badge of badges) {
            await claimBadge(badge.id);
        }
    }
}
```

---

## Testing

See [social-testing.md](./tests/social-testing.md) for console commands to test these endpoints.

---

## Notes for Documentation Contributors

**Verified:**
- [x] Complete friends list structure (userId field confirmed)
- [x] Friend requests received structure
- [x] Badge structure (id, name, hint, description, imagePath)
- [x] Unfinished games structure with pagination
- [x] Friend requests sent endpoint exists
- [x] Friend suggestions endpoint exists
- [x] Claimed badges endpoint structure
- [x] Non-existent endpoints documented

**Still needs verification:**
- [ ] Friend request acceptance endpoint (POST /v3/social/friends/accept)
- [ ] Friend request rejection endpoint (POST /v3/social/friends/reject)
- [ ] Send friend request endpoint (POST /v3/social/friends/send)
- [ ] Remove friend endpoint (DELETE /v3/social/friends/{userId})
- [ ] Badge claiming process (POST /v3/social/badges/claim)
- [ ] Request body structures for POST/DELETE endpoints
