# Games & Gameplay API

Endpoints for creating and managing game sessions across different game modes.

## Table of Contents

- [Overview](#overview)
- [Endpoints](#endpoints)
- [Game Modes](#game-modes)
- [Implementation Examples](#implementation-examples)

## Overview

GeoGuessr offers multiple game modes:
- **Standard Games** - Classic 5-round games
- **Streak Mode** - Country/region streak challenges
- **Infinity Mode** - Asynchronous competitive gameplay with friends

## Endpoints

### Standard Games

#### Get Game State

Retrieves the current state of a game including rounds, player progress, and game settings.

**Endpoint:**
```
GET /v3/games/{token}?client=web
```

**Parameters:**
- `token` - Game token (16-character string)
- `client` - Client type (usually "web")

**Authentication:** Required

**Response:** Complete game state object

**Example Response:**
```json
{
  "token": "XB9wycuZvDrhl7cB",
  "type": "standard",
  "mode": "standard",
  "state": "started",
  "roundCount": 5,
  "timeLimit": 0,
  "forbidMoving": true,
  "forbidZooming": true,
  "forbidRotating": true,
  "guessMapType": "roadmap",
  "streakType": "countrystreak",
  "map": "famous-places",
  "mapName": "Famous Places",
  "panoramaProvider": 1,
  "bounds": {
    "min": {
      "lat": -54.846696,
      "lng": -123.115017286215
    },
    "max": {
      "lat": 71.1709290207909,
      "lng": 175.6810699
    }
  },
  "round": 1,
  "rounds": [
    {
      "lat": 48.693670964233526,
      "lng": 6.1832995180016415,
      "panoId": "483030557379774F46576E634D514451657355714A51",
      "heading": 173.3570098876953,
      "pitch": 1.9483630657196045,
      "zoom": 0,
      "streakLocationCode": null,
      "startTime": "2026-01-11T00:10:51.0315710+00:00"
    }
  ],
  "player": {
    "totalScore": {
      "amount": "0",
      "unit": "points",
      "percentage": 0
    },
    "totalDistance": {
      "meters": {
        "amount": "0",
        "unit": "m"
      },
      "miles": {
        "amount": "0",
        "unit": "yd"
      }
    },
    "totalDistanceInMeters": 0,
    "totalStepsCount": 0,
    "totalTime": 0,
    "totalStreak": 0,
    "guesses": [],
    "isLeader": false,
    "currentPosition": 0,
    "pin": {
      "url": "pin/7dd941395a4ce096339065fc766a9482.png",
      "anchor": "center-center",
      "isDefault": false
    },
    "newBadges": [],
    "explorer": null,
    "id": "5db9f057dfa5102130eaf747",
    "nick": "Sirey",
    "isVerified": false,
    "flair": 0,
    "countryCode": "gb"
  },
  "progressChange": null
}
```

**Important Notes:**
- Use this endpoint to resume games or check current game state
- Player guesses are in `player.guesses` array
- Round information in `rounds` array

---

### Streak Mode

#### Create Streak Game

Creates a new country/region streak game.

**Endpoint:**
```
POST /v3/games/streak
```

**Authentication:** Required

**Request Body:**
```json
{
  "forbidMoving": false,
  "forbidRotating": false,
  "forbidZooming": false,
  "streakType": "CountryStreak",
  "timeLimit": 120
}
```

**Request Body Fields:**
- `forbidMoving` - Disable movement (true/false)
- `forbidRotating` - Disable camera rotation (true/false)
- `forbidZooming` - Disable zoom (true/false)
- `streakType` - Streak type ("CountryStreak", etc.)
- `timeLimit` - Time limit in seconds (0 = no limit)

**Response:** Complete game state object (same structure as GET /v3/games/{token})

**Example Response:**
```json
{
  "token": "WQmUfbY87ikn2TNx",
  "type": "standard",
  "mode": "streak",
  "state": "started",
  "roundCount": 1,
  "timeLimit": 120,
  "forbidMoving": false,
  "forbidZooming": false,
  "forbidRotating": false,
  "guessMapType": "roadmap",
  "streakType": "countrystreak",
  "map": "country-streak",
  "mapName": "Country Streak",
  "panoramaProvider": 1,
  "bounds": {
    "min": {
      "lat": 90,
      "lng": 180
    },
    "max": {
      "lat": -90,
      "lng": -180
    }
  },
  "round": 1,
  "rounds": [
    {
      "lat": 53.79796600341797,
      "lng": -1.8176765441894531,
      "panoId": "757A756C527A676150782D34465944487A6D46377251",
      "heading": 0,
      "pitch": 0,
      "zoom": 0,
      "streakLocationCode": "gb",
      "startTime": "2026-01-11T00:13:59.8249055+00:00"
    }
  ],
  "player": {
    "totalScore": {
      "amount": "0",
      "unit": "points",
      "percentage": 0
    },
    "totalDistance": {
      "meters": {
        "amount": "0",
        "unit": "m"
      },
      "miles": {
        "amount": "0",
        "unit": "yd"
      }
    },
    "totalDistanceInMeters": 0,
    "totalStepsCount": 0,
    "totalTime": 0,
    "totalStreak": 0,
    "guesses": [],
    "isLeader": false,
    "currentPosition": 0,
    "pin": {
      "url": "pin/7dd941395a4ce096339065fc766a9482.png",
      "anchor": "center-center",
      "isDefault": false
    },
    "newBadges": [],
    "explorer": null,
    "id": "5db9f057dfa5102130eaf747",
    "nick": "Sirey",
    "isVerified": false,
    "flair": 0,
    "countryCode": "gb"
  },
  "progressChange": null
}
```

**Important Notes:**
- Returns full game state immediately
- `mode` is "streak"
- `streakLocationCode` contains the country code for streak games
- GET requests return 400 - endpoint is POST-only

---

### Infinity Mode

**IMPORTANT: Most Infinity Mode endpoints have been deprecated and return HTTP 404.**

#### Get Infinity Challenges List

The only working Infinity Mode endpoint. Returns list of active infinity challenges.

**Endpoint:**
```
GET /v4/games/infinity/challenges
```

**Authentication:** Required

**Response:** Object with challenges array

**Example Response:**
```json
{
  "challenges": []
}
```

**Important Notes:**
- Returns empty array if no active challenges
- This is the ONLY infinity endpoint that works
- All other infinity endpoints return 404

---

## Deprecated Infinity Endpoints

The following Infinity Mode endpoints **no longer exist** and return HTTP 404:

- `GET /v4/games/infinity` - Main infinity game state (404)
- `GET /v4/games/infinity/inbox` - Inbox of challenges (404)
- `GET /v4/games/infinity/outbox` - Outbox of sent challenges (404)
- `GET /v4/games/infinity/history` - Game history (404)
- `GET /v4/games/infinity/next` - Next location (404)
- `GET /v4/games/infinity/location-overview` - Location overview (404)
- `POST /v4/games/infinity/guess` - Submit guess (likely 404)
- `POST /v4/games/infinity/challenge/new` - Create challenge (likely 404)
- `GET /v4/games/infinity/challenge/random` - Random challenge (likely 404)

**Note:** Infinity Mode appears to have been removed or significantly redesigned. Only the challenges list endpoint remains functional.

---

## Data Structures

### Game State Object

Complete game state object structure:

```typescript
interface GameState {
  token: string;                 // Game token (16 characters)
  type: string;                  // "standard"
  mode: string;                  // "standard", "streak", etc.
  state: string;                 // "started", "finished"
  roundCount: number;            // Total number of rounds
  timeLimit: number;             // Time limit in seconds (0 = no limit)
  forbidMoving: boolean;         // Movement disabled (NMPZ)
  forbidZooming: boolean;        // Zoom disabled (NZ)
  forbidRotating: boolean;       // Rotation disabled (NR)
  guessMapType: string;          // "roadmap"
  streakType: string;            // "countrystreak", etc.
  map: string;                   // Map slug
  mapName: string;               // Map display name
  panoramaProvider: number;      // 1 = Google Street View
  bounds: {
    min: {
      lat: number;
      lng: number;
    };
    max: {
      lat: number;
      lng: number;
    };
  };
  round: number;                 // Current round number
  rounds: Round[];               // Array of round objects
  player: PlayerState;           // Player state
  progressChange: any | null;    // Progress changes
}

interface Round {
  lat: number;                   // Location latitude
  lng: number;                   // Location longitude
  panoId: string;                // Street View panorama ID (hex encoded)
  heading: number;               // Camera heading
  pitch: number;                 // Camera pitch
  zoom: number;                  // Camera zoom level
  streakLocationCode: string | null; // Country code for streak mode
  startTime: string;             // Round start time (ISO 8601)
}

interface PlayerState {
  totalScore: {
    amount: string;              // Score as string
    unit: "points";
    percentage: number;          // Score percentage
  };
  totalDistance: {
    meters: {
      amount: string;
      unit: "m" | "km";
    };
    miles: {
      amount: string;
      unit: "yd" | "miles";
    };
  };
  totalDistanceInMeters: number; // Total distance in meters
  totalStepsCount: number;       // Total movement steps
  totalTime: number;             // Total time in milliseconds
  totalStreak: number;           // Current streak count
  guesses: Guess[];              // Array of guesses
  isLeader: boolean;             // Whether player is leading
  currentPosition: number;       // Current position/rank
  pin: {
    url: string;
    anchor: string;
    isDefault: boolean;
  };
  newBadges: any[];              // Newly earned badges
  explorer: any | null;          // Explorer mode data
  id: string;                    // Player user ID
  nick: string;                  // Player username
  isVerified: boolean;           // Verified status
  flair: number;                 // Flair level
  countryCode: string;           // Player country code
}

interface Guess {
  lat: number;                   // Guessed latitude
  lng: number;                   // Guessed longitude
  // Additional guess fields documented in challenges.md
}
```

---

## Game Modes

### Standard Mode
- Classic GeoGuessr gameplay
- 5 rounds per game
- Configurable time limits and movement restrictions
- Access via: `GET /v3/games/{token}`

### Streak Mode
- Guess until you get one wrong
- Country or region-based
- Tracks longest streaks
- Create via: `POST /v3/games/streak`

### Infinity Mode (Deprecated)
- **DEPRECATED:** Most endpoints return 404
- Only `/v4/games/infinity/challenges` remains functional
- Feature appears to have been removed or significantly redesigned

---

## Implementation Examples

### Example 1: Get Game State

**JavaScript:**
```javascript
async function getGameState(gameToken) {
    const response = await fetch(`https://www.geoguessr.com/api/v3/games/${gameToken}?client=web`, {
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const game = await response.json();
    console.log(`Game: ${game.mapName}`);
    console.log(`Round ${game.round}/${game.roundCount}`);
    console.log(`Score: ${game.player.totalScore.amount} points`);

    return game;
}

// Usage
const game = await getGameState('XB9wycuZvDrhl7cB');
```

**Python:**
```python
import requests

def get_game_state(game_token, cookie):
    url = f'https://www.geoguessr.com/api/v3/games/{game_token}?client=web'
    response = requests.get(url, cookies={'_ncfa': cookie})
    response.raise_for_status()

    game = response.json()
    print(f"Game: {game['mapName']}")
    print(f"Round {game['round']}/{game['roundCount']}")
    print(f"Score: {game['player']['totalScore']['amount']} points")

    return game

# Usage
# game = get_game_state('XB9wycuZvDrhl7cB', 'YOUR_NCFA_COOKIE')
```

---

### Example 2: Create Streak Game

**JavaScript:**
```javascript
async function createStreakGame(settings = {}) {
    const response = await fetch('https://www.geoguessr.com/api/v3/games/streak', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            forbidMoving: settings.nmpz || false,
            forbidRotating: settings.nr || false,
            forbidZooming: settings.nz || false,
            streakType: settings.type || 'CountryStreak',
            timeLimit: settings.timeLimit || 120
        })
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const game = await response.json();
    console.log('Streak game created:', game.token);
    console.log('First location:', game.rounds[0].streakLocationCode);
    return game;
}

// Usage
const streakGame = await createStreakGame({
    type: 'CountryStreak',
    timeLimit: 120
});
```

**Python:**
```python
import requests
import json

def create_streak_game(cookie, settings=None):
    url = 'https://www.geoguessr.com/api/v3/games/streak'

    if settings is None:
        settings = {}

    body = {
        'forbidMoving': settings.get('nmpz', False),
        'forbidRotating': settings.get('nr', False),
        'forbidZooming': settings.get('nz', False),
        'streakType': settings.get('type', 'CountryStreak'),
        'timeLimit': settings.get('timeLimit', 120)
    }

    response = requests.post(
        url,
        cookies={'_ncfa': cookie},
        headers={'Content-Type': 'application/json'},
        data=json.dumps(body)
    )
    response.raise_for_status()

    game = response.json()
    print(f"Streak game created: {game['token']}")
    print(f"First location: {game['rounds'][0]['streakLocationCode']}")
    return game

# Usage
# streak_game = create_streak_game('YOUR_NCFA_COOKIE', {'type': 'CountryStreak', 'timeLimit': 120})
```

---

## Common Use Cases

### 1. Track Game Progress

```javascript
async function trackGameProgress(gameToken) {
    const game = await getGameState(gameToken);

    const progress = {
        currentRound: game.round,
        totalRounds: game.roundCount,
        score: game.player.totalScore.amount,
        scorePercentage: game.player.totalScore.percentage,
        streak: game.player.totalStreak,
        guessesCount: game.player.guesses.length
    };

    console.log(`Round ${progress.currentRound}/${progress.totalRounds}`);
    console.log(`Score: ${progress.score} (${progress.scorePercentage}%)`);

    return progress;
}

// Usage
// const progress = await trackGameProgress('XB9wycuZvDrhl7cB');
```

### 2. Start Custom Streak Challenge

```javascript
async function startCustomStreak(difficulty = 'normal') {
    const settings = {
        type: 'CountryStreak',
        timeLimit: difficulty === 'hard' ? 60 : 120,
        nmpz: difficulty === 'hard',
        nr: difficulty === 'hard',
        nz: difficulty === 'hard'
    };

    const game = await createStreakGame(settings);

    console.log(`Streak started: ${game.token}`);
    console.log(`Difficulty: ${difficulty}`);
    console.log(`Time limit: ${settings.timeLimit}s`);

    return game;
}

// Usage
// const hardStreak = await startCustomStreak('hard');
```

### 3. Resume Unfinished Game

```javascript
async function resumeGame(gameToken) {
    const game = await getGameState(gameToken);

    if (game.state === 'finished') {
        console.log('Game already finished');
        return null;
    }

    console.log(`Resuming: ${game.mapName}`);
    console.log(`Round ${game.round}/${game.roundCount}`);
    console.log(`Current score: ${game.player.totalScore.amount}`);

    return game;
}

// Usage
// const game = await resumeGame('XB9wycuZvDrhl7cB');
```

---

## Testing

See [games-testing.md](./tests/games-testing.md) for console commands to test these endpoints.

---

## Notes for Documentation Contributors

**Verified:**
- [x] Game state structure (GET /v3/games/{token})
- [x] Streak game creation (POST /v3/games/streak)
- [x] Infinity mode deprecated (most endpoints return 404)
- [x] Only /v4/games/infinity/challenges works
- [x] Complete game state object with 30+ fields
- [x] Round structure with location data
- [x] Player state with score, distance, streak tracking

**Still needs verification:**
- [ ] Standard game creation endpoint (POST /v3/games)
- [ ] Guess submission format and endpoint
- [ ] Game completion/finish endpoint
- [ ] Multiplayer/party game endpoints
- [ ] Daily challenge game structure
- [ ] Battle Royale game endpoints
