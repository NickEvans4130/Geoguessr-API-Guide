# User Profiles API

Endpoints for retrieving and managing user profile information.

## Table of Contents

- [Overview](#overview)
- [Endpoints](#endpoints)
- [Data Structures](#data-structures)
- [Implementation Examples](#implementation-examples)

## Overview

Profile endpoints provide access to user information including stats, customization, and public data.

## Endpoints

### Get Current User Profile

Get the authenticated user's profile including detailed user information, settings, and restrictions.

**Endpoint:**
```
GET /v3/profiles
```

**Authentication:** Required

**Example Request:**
```javascript
fetch('https://www.geoguessr.com/api/v3/profiles', {
    credentials: 'include'
})
```

**Response Structure:**
```json
{
  "user": {
    "nick": "username",
    "created": "2019-10-30T20:19:35.6820000Z",
    "isProUser": true,
    "type": "Unlimited",
    "isVerified": false,
    "pin": {
      "url": "pin/7dd941395a4ce096339065fc766a9482.png",
      "anchor": "center-center",
      "isDefault": false
    },
    "customImage": "pin/...",
    "fullBodyPin": "pin/...",
    "borderUrl": "avatarasseticon/...",
    "color": 0,
    "url": "/user/5db9f057dfa5102130eaf747",
    "id": "5db9f057dfa5102130eaf747",
    "countryCode": "gb",
    "br": {
      "level": 158,
      "division": 50
    },
    "streakProgress": {
      "bronze": 2,
      "silver": 1,
      "gold": 1,
      "platinum": 0
    },
    "explorerProgress": {
      "bronze": 1,
      "silver": 55,
      "gold": 46,
      "platinum": 6
    },
    "dailyChallengeProgress": 0,
    "lastClaimedLevel": 158,
    "progress": {
      "xp": 1456894,
      "level": 158,
      "levelXp": 1448070,
      "nextLevel": 159,
      "nextLevelXp": 1473400,
      "title": {
        "id": 360,
        "tierId": 160
      },
      "competitionMedals": {
        "bronze": 0,
        "silver": 0,
        "gold": 0,
        "platinum": 0
      }
    },
    "competitive": {
      "elo": 766,
      "rating": 1267,
      "lastRatingChange": -10,
      "division": {
        "type": 50,
        "startRating": 1100,
        "endRating": 1500
      },
      "onLeaderboard": true
    },
    "flair": 0,
    "isCreator": false,
    "club": {
      "tag": "SLPH",
      "clubId": "d33bfc7d-c57e-4db5-8293-af6f91a45d6f",
      "level": 10
    }
  },
  "playingRestriction": {
    "restriction": 0,
    "canPlayGame": true,
    "canHostParty": true,
    "description": "You can play as many games as you want."
  },
  "email": "user@example.com",
  "isEmailChangeable": false,
  "isEmailVerified": true,
  "emailNotificationSettings": {
    "sendDailyChallengeNotifications": true,
    "sendDailyGameNotifications": true,
    "sendChallengeNotifications": true,
    "sendNewsNotifications": true,
    "sendPromotionalNotifications": true,
    "sendSocialNotifications": true,
    "sendCompetitiveNotifications": true
  },
  "isBanned": false,
  "chatBan": false,
  "distanceUnit": 0,
  "dateFormat": 0,
  "hideCustomAvatars": false,
  "shareActivities": true
}
```

**Important Notes:**
- User information is nested within the `user` object
- User ID is at `user.id`, not at top level
- Username is at `user.nick`
- Pro status is at `user.isProUser`

---

### Get User Profile by ID

**This endpoint does not exist.** Returns 404 Not Found.

To get information about other users:
- Use the Search Users endpoint below
- Information about users appears in challenge results, friend lists, and other endpoints

---

### Search Users

Search for users by username. Returns up to 10 results.

**Endpoint:**
```
GET /v3/search/user?q={query}
```

**Parameters:**
- `q` (query) - Search query (username to search for, minimum 1 character)

**Authentication:** Required

**Example Request:**
```javascript
const username = 'brbw';
fetch(`https://www.geoguessr.com/api/v3/search/user?q=${encodeURIComponent(username)}`, {
    credentials: 'include'
})
```

**Response Structure:**
```json
[
  {
    "nick": "brbw",
    "created": "2017-09-22T17:15:02.2400000Z",
    "isProUser": true,
    "type": "Pro",
    "isVerified": false,
    "pin": {
      "url": "pin/1447b93700d85076e0dcddbbd081e1de.png",
      "anchor": "center-center",
      "isDefault": false
    },
    "customImage": "pin/1447b93700d85076e0dcddbbd081e1de.png",
    "fullBodyPin": "pin/...",
    "borderUrl": "avatarasseticon/...",
    "color": 0,
    "url": "/user/59c55f9656b1c23bc81cb742",
    "id": "59c55f9656b1c23bc81cb742",
    "countryCode": "us",
    "flair": 0
  }
]
```

**Important Notes:**
- Returns array of user objects (up to 10 results)
- Empty query string returns HTTP 400
- Search is case-insensitive
- Partial matching is supported

---

### Get User Maps

Get maps created by the authenticated user.

**Endpoint:**
```
GET /v3/profiles/maps
```

**Authentication:** Required

**Response Structure:**
```json
[
  {
    "id": "6636a36a5054eeed5ecf8e7a",
    "name": "My Custom Map",
    "slug": "6636a36a5054eeed5ecf8e7a",
    "description": "Map description...",
    "published": true,
    "coordinateCount": "1000+",
    "likes": 42
  }
]
```

**Returns:** Array of map objects created by the user

---

### Update Profile Pin

Customize the user's map pin.

**Endpoint:**
```
POST /v3/profiles/pin
```

**Authentication:** Required

**Request Body:** (Structure needs verification)
```json
{
  "pinUrl": "..."
}
```

**Expected Response:** (Structure needs verification)

---

## Data Structures

### Profile Response Object

```typescript
interface ProfileResponse {
  user: UserObject;
  playingRestriction: PlayingRestriction;
  email: string;
  isEmailChangeable: boolean;
  isEmailVerified: boolean;
  emailNotificationSettings: EmailNotifications;
  isBanned: boolean;
  chatBan: boolean;
  distanceUnit: number;          // 0 = km, 1 = miles
  dateFormat: number;            // Date format preference
  hideCustomAvatars: boolean;
  shareActivities: boolean;
  deviceToken?: string;
}

interface UserObject {
  nick: string;                  // Username
  created: string;               // ISO 8601 creation date
  isProUser: boolean;            // Has Pro subscription
  type: string;                  // "Unlimited", "Pro", "Elite", etc.
  isVerified: boolean;           // Verified account
  pin: {
    url: string;
    anchor: string;
    isDefault: boolean;
  };
  customImage: string;
  fullBodyPin: string;
  borderUrl: string;
  color: number;
  url: string;                   // Profile URL path
  id: string;                    // User ID (24-character hex string)
  countryCode: string;           // 2-letter ISO country code
  br: {                          // Battle Royale stats
    level: number;
    division: number;
  };
  streakProgress: {
    bronze: number;
    silver: number;
    gold: number;
    platinum: number;
  } | null;
  explorerProgress: {
    bronze: number;
    silver: number;
    gold: number;
    platinum: number;
  } | null;
  dailyChallengeProgress: number;
  lastClaimedLevel: number;
  progress: {
    xp: number;
    level: number;
    levelXp: number;             // XP at current level
    nextLevel: number;
    nextLevelXp: number;         // XP needed for next level
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
  lastNameChange: string;        // ISO 8601 timestamp
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
}

interface PlayingRestriction {
  restriction: number;
  canPlayGame: boolean;
  canHostParty: boolean;
  description: string;
  ticket: any | null;
  periodicAllowanceMetadata: any | null;
  noRestrictionEndsAt: string | null;
}

interface EmailNotifications {
  sendDailyChallengeNotifications: boolean;
  sendDailyGameNotifications: boolean;
  sendChallengeNotifications: boolean;
  sendNewsNotifications: boolean;
  sendPromotionalNotifications: boolean;
  sendSocialNotifications: boolean;
  sendCompetitiveNotifications: boolean;
  unsubscribeToken?: string;
}
```

---

## Implementation Examples

### Example 1: Get My Profile

**JavaScript:**
```javascript
async function getMyProfile() {
    const response = await fetch('https://www.geoguessr.com/api/v3/profiles', {
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const profile = await response.json();
    const user = profile.user;

    console.log(`User: ${user.nick} (Level ${user.progress.level})`);
    console.log(`User ID: ${user.id}`);
    console.log(`Pro User: ${user.isProUser}`);
    console.log(`Country: ${user.countryCode}`);
    console.log(`Email: ${profile.email}`);

    return profile;
}

// Usage
const profile = await getMyProfile();
```

**Python:**
```python
import requests

def get_my_profile(cookie):
    url = 'https://www.geoguessr.com/api/v3/profiles'
    response = requests.get(url, cookies={'_ncfa': cookie})
    response.raise_for_status()

    profile = response.json()
    user = profile['user']

    print(f"User: {user['nick']} (Level {user['progress']['level']})")
    print(f"User ID: {user['id']}")
    print(f"Pro User: {user['isProUser']}")
    print(f"Country: {user['countryCode']}")
    print(f"Email: {profile['email']}")

    return profile

# Usage
# profile = get_my_profile('YOUR_NCFA_COOKIE')
```

---

### Example 2: Search for Users

**JavaScript:**
```javascript
async function searchUsers(query) {
    const url = `https://www.geoguessr.com/api/v3/search/user?q=${encodeURIComponent(query)}`;
    const response = await fetch(url, { credentials: 'include' });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const users = await response.json();
    console.log(`Found ${users.length} users matching "${query}"`);

    users.forEach(user => {
        console.log(`- ${user.nick} (${user.id})`);
    });

    return users;
}

// Usage
const results = await searchUsers('brbw');
```

**Python:**
```python
import requests
from urllib.parse import quote

def search_users(query, cookie):
    url = f'https://www.geoguessr.com/api/v3/search/user?q={quote(query)}'
    response = requests.get(url, cookies={'_ncfa': cookie})
    response.raise_for_status()

    users = response.json()
    print(f'Found {len(users)} users matching "{query}"')

    for user in users:
        print(f"- {user['nick']} ({user['id']})")

    return users

# Usage
# results = search_users('brbw', 'YOUR_NCFA_COOKIE')
```

---

### Example 3: Get Another User's Profile

**JavaScript:**
```javascript
async function getUserProfile(userId) {
    const url = `https://www.geoguessr.com/api/v3/profiles/${userId}`;
    const response = await fetch(url, { credentials: 'include' });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const profile = await response.json();
    return profile;
}

// Usage
const userProfile = await getUserProfile('59c55f9656b1c23bc81cb742');
console.log(userProfile);
```

---

## Common Use Cases

### 1. Display User Card

```javascript
async function displayUserCard(userId) {
    const profile = await getUserProfile(userId);

    return `
        <div class="user-card">
            <img src="${profile.pin?.url || 'default-pin.png'}" alt="Pin">
            <h3>${profile.nick}</h3>
            <p>Level: ${profile.levelProgress?.level || 'N/A'}</p>
            <p>Country: ${profile.countryCode.toUpperCase()}</p>
            ${profile.isVerified ? '<span class="verified">✓ Verified</span>' : ''}
        </div>
    `;
}
```

### 2. Autocomplete User Search

```javascript
async function autocompleteUsers(query, limit = 5) {
    if (query.length < 2) return [];

    const users = await searchUsers(query);
    return users.slice(0, limit).map(user => ({
        label: user.nick,
        value: user.id
    }));
}

// Usage in input field
// const suggestions = await autocompleteUsers(inputValue);
```

### 3. Check If User Exists

```javascript
async function userExists(username) {
    try {
        const results = await searchUsers(username);
        return results.some(user =>
            user.nick.toLowerCase() === username.toLowerCase()
        );
    } catch (error) {
        console.error('Error checking user:', error);
        return false;
    }
}

// Usage
// const exists = await userExists('brbw');
```

---

## Testing

See [profiles-testing.md](./tests/profiles-testing.md) for console commands to test these endpoints.

---

## Notes for Documentation Contributors

The following aspects need verification:

- [ ] Complete structure of profile response
- [ ] All available fields in user profile
- [ ] Profile visibility settings (public vs private)
- [ ] Search result limit and pagination
- [ ] Profile statistics included
- [ ] Map list structure
- [ ] Pin customization options
