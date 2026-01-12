# GeoGuessr Duels API

The duels endpoints are hosted on a separate API domain: `https://game-server.geoguessr.com/api`

This API provides game state and replay data for both standard duels (1v1) and team duels (2v2).

**🚀 Ready to use?** Check out the duels examples:
- [JavaScript examples](examples/javascript/duels/) - Browser console
- [Python examples](examples/python/duels/) - Scripts with analysis tools

## Overview

Duels is a competitive game mode where players (or teams) compete head-to-head with a health-based system. Players deal damage to opponents based on score differences, with multipliers increasing as the game progresses. The game ends when one team's health reaches zero.

### Key Concepts

- **Health System**: Each team starts with a configurable amount of health (typically 6000). Damage is dealt based on score differences.
- **Multipliers**: Damage multipliers increase as rounds progress (1x, 1x, 1.5x, 2x, 2.5x, 3x, 3.5x, 4x, etc.), making later rounds more impactful.
- **Teams**: Standard duels have 1 player per team, team duels can have multiple players per team.
- **Rounds**: Games consist of multiple rounds. The best guess from each team is used to calculate damage.
- **Replay System**: Complete player action tracking including camera movements, map interactions, and guess placements.

### Authentication

All duels endpoints require authentication via the `_ncfa` cookie.

---

## Endpoints

### Get Duel Game State

**Endpoint:** `GET /api/duels/{gameId}`
**Base URL:** `https://game-server.geoguessr.com`
**Authentication:** Required
**Response:** Complete game state including teams, players, rounds, and results

This endpoint returns the complete state of a duel game, including all player guesses, health changes, round results, and final outcome. Works for both standard duels and team duels.

**Example Request (JavaScript):**
```javascript
/**
 * Fetch complete duel game state
 * @param {string} gameId - The duel game ID
 * @returns {Promise<DuelGame>} Complete game data
 */
async function getDuelGameState(gameId) {
    const url = `https://game-server.geoguessr.com/api/duels/${gameId}`;

    const response = await fetch(url, {
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const gameData = await response.json();

    console.log('Game Status:', gameData.status);
    console.log('Current Round:', gameData.currentRoundNumber);
    console.log('Winner:', gameData.result.winningTeamId);

    // Display team health
    gameData.teams.forEach(team => {
        console.log(`Team ${team.name}: ${team.health} HP`);
    });

    return gameData;
}

// Usage
getDuelGameState('6963ff12ec85cd5824375992')
    .then(data => console.log('Game data:', data))
    .catch(err => console.error('Error:', err));
```

**Example Request (Python):**
```python
import os
import requests

def get_duel_game_state(game_id: str) -> dict:
    """
    Fetch complete duel game state.

    Args:
        game_id: The duel game ID

    Returns:
        dict: Complete game data
    """
    url = f"https://game-server.geoguessr.com/api/duels/{game_id}"

    cookies = {
        '_ncfa': os.getenv('GEOGUESSR_COOKIE')
    }

    response = requests.get(url, cookies=cookies)
    response.raise_for_status()

    game_data = response.json()

    print(f"Game Status: {game_data['status']}")
    print(f"Current Round: {game_data['currentRoundNumber']}")
    print(f"Winner: {game_data['result']['winningTeamId']}")

    # Display team health
    for team in game_data['teams']:
        print(f"Team {team['name']}: {team['health']} HP")

    return game_data

# Usage
if __name__ == "__main__":
    game_data = get_duel_game_state('6963ff12ec85cd5824375992')
    print('Game data retrieved successfully')
```

**Example Response:**
```json
{
  "gameId": "6963ff12ec85cd5824375992",
  "status": "Finished",
  "currentRoundNumber": 8,
  "teams": [
    {
      "id": "2d25a0c4-5df8-4b7c-93c7-a3a98daa2172",
      "name": "blue",
      "health": 0,
      "players": [...],
      "roundResults": [...],
      "isMultiplierActive": true,
      "currentMultiplier": 3
    },
    {
      "id": "bb08d9e1-d4c7-4287-bf21-4959afd12ca1",
      "name": "red",
      "health": 105,
      "players": [...],
      "roundResults": [...],
      "isMultiplierActive": true,
      "currentMultiplier": 3
    }
  ],
  "rounds": [...],
  "result": {
    "isDraw": false,
    "winningTeamId": "bb08d9e1-d4c7-4287-bf21-4959afd12ca1",
    "winnerStyle": "Victory"
  },
  "options": {...},
  "movementOptions": {
    "forbidMoving": true,
    "forbidZooming": false,
    "forbidRotating": false
  },
  "mapBounds": {...},
  "initialHealth": 6000,
  "maxNumberOfRounds": 0,
  "isPaused": false,
  "version": 102
}
```

**Important Notes:**
- The same endpoint structure is used for both standard duels and team duels
- Team duels have multiple players per team with `isTeamDuels: true` in options
- The `version` field increments with each game state update
- `maxNumberOfRounds: 0` means unlimited rounds until one team's health reaches zero
- Winner style can be "Victory", "ComebackVictory", or check for "isDraw"

---

### Get Duel Replay

**Endpoint:** `GET /api/replays/{playerId}/{duelId}/{roundNumber}`
**Base URL:** `https://game-server.geoguessr.com`
**Authentication:** Required
**Response:** Array of replay events with timestamps

Returns a complete replay of a specific player's actions during a round, including camera movements, map interactions, and guess placement. Useful for analyzing player behavior or creating replay visualizations.

**Example Request (JavaScript):**
```javascript
/**
 * Fetch replay data for a specific player and round
 * @param {string} playerId - The player's user ID
 * @param {string} duelId - The duel game ID
 * @param {number} roundNumber - The round number (1-indexed)
 * @returns {Promise<ReplayEvent[]>} Array of replay events
 */
async function getDuelReplay(playerId, duelId, roundNumber) {
    const url = `https://game-server.geoguessr.com/api/replays/${playerId}/${duelId}/${roundNumber}`;

    const response = await fetch(url, {
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const replayEvents = await response.json();

    console.log(`Total events: ${replayEvents.length}`);

    // Analyze event types
    const eventTypes = {};
    replayEvents.forEach(event => {
        eventTypes[event.type] = (eventTypes[event.type] || 0) + 1;
    });

    console.log('Event types:', eventTypes);

    // Find the final guess
    const guessEvent = replayEvents.find(e => e.type === 'GuessWithLatLng');
    if (guessEvent) {
        console.log('Final guess:', guessEvent.payload);
    }

    return replayEvents;
}

// Usage
getDuelReplay('5b68bcc7f438a60f64005817', '6963ff12ec85cd5824375992', 1)
    .then(events => console.log('Replay events:', events))
    .catch(err => console.error('Error:', err));
```

**Example Request (Python):**
```python
import os
import requests
from typing import List, Dict

def get_duel_replay(player_id: str, duel_id: str, round_number: int) -> List[Dict]:
    """
    Fetch replay data for a specific player and round.

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

    response = requests.get(url, cookies=cookies)
    response.raise_for_status()

    replay_events = response.json()

    print(f"Total events: {len(replay_events)}")

    # Analyze event types
    event_types = {}
    for event in replay_events:
        event_type = event['type']
        event_types[event_type] = event_types.get(event_type, 0) + 1

    print('Event types:', event_types)

    # Find the final guess
    guess_events = [e for e in replay_events if e['type'] == 'GuessWithLatLng']
    if guess_events:
        print('Final guess:', guess_events[0]['payload'])

    return replay_events

# Usage
if __name__ == "__main__":
    events = get_duel_replay('5b68bcc7f438a60f64005817', '6963ff12ec85cd5824375992', 1)
    print(f'Retrieved {len(events)} replay events')
```

**Example Response:**
```json
[
  {
    "time": 1768161047513,
    "type": "PanoPosition",
    "payload": {
      "lat": -37.70238286995826,
      "lng": 142.48918578117917,
      "panoId": "nyfpaD0EKB_tBJbCAy7acA"
    }
  },
  {
    "time": 1768161047513,
    "type": "PanoPov",
    "payload": {
      "heading": 164.00824,
      "pitch": 0.5
    }
  },
  {
    "time": 1768161047513,
    "type": "PanoZoom",
    "payload": {
      "zoom": 0.16992569
    }
  },
  {
    "time": 1768161054395,
    "type": "MapDisplay",
    "payload": {
      "isActive": true,
      "isSticky": false,
      "size": 3
    }
  },
  {
    "time": 1768161056606,
    "type": "PinPosition",
    "payload": {
      "lat": -37.59225,
      "lng": 142.953
    }
  },
  {
    "time": 1768161065112,
    "type": "GuessWithLatLng",
    "payload": {
      "lat": -37.95357,
      "lng": 142.85567
    }
  }
]
```

**Replay Event Types:**
- `PanoPosition` - Panorama location change (with panoId, lat, lng)
- `PanoPov` - Camera heading/pitch change
- `PanoZoom` - Panorama zoom level change
- `MapDisplay` - Map opened/closed (with size and sticky state)
- `MapPosition` - Map panning (lat/lng change)
- `MapZoom` - Map zoom level change
- `PinPosition` - Guess pin placement/movement
- `GuessWithLatLng` - Final guess submission

**Important Notes:**
- All times are Unix timestamps in milliseconds
- Events are ordered chronologically
- The round number is 1-indexed (first round is 1, not 0)
- Works for both standard duels and team duels
- Not all players may have replay data if they timed out or disconnected

---

## Data Structures

### DuelGame

Complete duel game state.

```typescript
interface DuelGame {
  gameId: string;
  teams: DuelTeam[];
  rounds: DuelRound[];
  currentRoundNumber: number;
  status: "InProgress" | "Finished" | "Paused";
  version: number;
  options: DuelOptions;
  movementOptions: MovementOptions;
  mapBounds: MapBounds;
  initialHealth: number;
  maxNumberOfRounds: number;
  result: DuelResult;
  isPaused: boolean;
  gameServerNodeId: string | null;
  tournamentId: string;
}
```

### DuelTeam

Team data including players and round results.

```typescript
interface DuelTeam {
  id: string;
  name: "blue" | "red";
  health: number;
  players: DuelPlayer[];
  roundResults: TeamRoundResult[];
  isMultiplierActive: boolean;
  currentMultiplier: number;
}
```

### DuelPlayer

Player data within a duel.

```typescript
interface DuelPlayer {
  playerId: string;
  guesses: DuelGuess[];
  rating: number;
  countryCode: string;
  progressChange: ProgressChange;
  pin: {
    lat: number;
    lng: number;
  };
  helpRequested: boolean;
  isSteam: boolean;
}
```

### DuelGuess

Individual guess in a duel round.

```typescript
interface DuelGuess {
  roundNumber: number;
  lat: number;
  lng: number;
  distance: number;
  created: string; // ISO 8601 timestamp
  isTeamsBestGuessOnRound: boolean;
  score: number | null; // null if not the team's best guess
}
```

### TeamRoundResult

Team's result for a specific round.

```typescript
interface TeamRoundResult {
  roundNumber: number;
  score: number;
  healthBefore: number;
  healthAfter: number;
  bestGuess: DuelGuess;
  activeMultiplier: boolean;
  damageDealt: number;
  multiplier: number;
}
```

### DuelRound

Round configuration and timing.

```typescript
interface DuelRound {
  roundNumber: number;
  panorama: {
    panoId: string;
    lat: number;
    lng: number;
    countryCode: string;
    heading: number;
    pitch: number;
    zoom: number;
  };
  hasProcessedRoundTimeout: boolean;
  isHealingRound: boolean;
  multiplier: number;
  damageMultiplier: number;
  startTime: string | null; // ISO 8601 timestamp
  endTime: string | null; // ISO 8601 timestamp
  timerStartTime: string | null; // ISO 8601 timestamp
}
```

### DuelOptions

Game configuration options.

```typescript
interface DuelOptions {
  initialHealth: number;
  individualInitialHealth: boolean;
  initialHealthTeamOne: number;
  initialHealthTeamTwo: number;
  roundTime: number; // seconds per round
  maxRoundTime: number;
  gracePeriodTime: number;
  gameTimeOut: number;
  maxNumberOfRounds: number; // 0 = unlimited
  healingRounds: number[]; // array of round numbers
  movementOptions: MovementOptions;
  mapSlug: string;
  isRated: boolean;
  map: {
    name: string;
    slug: string;
    bounds: MapBounds;
    maxErrorDistance: number;
  };
  duelRoundOptions: any[];
  roundsWithoutDamageMultiplier: number;
  disableMultipliers: boolean;
  multiplierIncrement: number;
  disableHealing: boolean;
  isTeamDuels: boolean;
  gameContext: {
    type: string;
    id: string;
  } | null;
  roundStartingBehavior: string;
  flashbackRounds: number[];
  competitiveGameMode: "NoMoveDuels" | "MoveDuels" | "None";
  countAllGuesses: boolean;
  masterControlAutoStartRounds: boolean;
  consumedLocationsIdentifier: string;
  useCuratedLocations: boolean;
  extraWaitTimeBetweenRounds: number;
  roundCountdownDelay: number;
  guessMapType: string;
  botBehaviors: any | null;
  activeMultiplier: boolean;
}
```

### MovementOptions

Movement restrictions for the game.

```typescript
interface MovementOptions {
  forbidMoving: boolean;    // NMPZ (No Move, Pan, Zoom)
  forbidZooming: boolean;    // NZ (No Zoom)
  forbidRotating: boolean;   // NR (No Rotate)
}
```

### DuelResult

Game outcome.

```typescript
interface DuelResult {
  isDraw: boolean;
  winningTeamId: string;
  winnerStyle: "Victory" | "ComebackVictory";
}
```

### ProgressChange

Player progression data (XP, rating, etc.).

```typescript
interface ProgressChange {
  xpProgressions: Array<{
    xp: number;
    currentLevel: {
      level: number;
      xpStart: number;
    };
    nextLevel: {
      level: number;
      xpStart: number;
    };
    currentTitle: {
      id: number;
      tierId: number;
    };
  }>;
  awardedXp: {
    totalAwardedXp: number;
    xpAwards: Array<{
      xp: number;
      reason: "DuelCompleted" | "Marathon" | "HpBonus";
      count: number;
    }>;
  };
  medal: "None" | string;
  competitiveProgress: any | null;
  rankedSystemProgress: RankedProgress | null;
  rankedTeamDuelsProgress: any | null;
  quickplayDuelsProgress: any | null;
}
```

### RankedProgress

Ranked duel progression data.

```typescript
interface RankedProgress {
  points: Record<string, any>;
  totalWeeklyPoints: number;
  weeklyCap: number;
  gamesPlayedWithinWeeklyCap: number;
  positionBefore: number;
  positionAfter: number;
  ratingBefore: number;
  ratingAfter: number;
  winStreak: number;
  bucketSortedBy: "Rating";
  gameMode: "NoMoveDuels" | "MoveDuels";
  gameModeRatingBefore: number;
  gameModeRatingAfter: number;
  gameModeGamesPlayed: number;
  gameModeGamesRequired: number;
  placementGamesPlayed: number;
  placementGamesRequired: number;
}
```

### MapBounds

Map boundary coordinates.

```typescript
interface MapBounds {
  min: {
    lat: number;
    lng: number;
  };
  max: {
    lat: number;
    lng: number;
  };
}
```

### ReplayEvent

Replay event with timestamp and payload.

```typescript
interface ReplayEvent {
  time: number; // Unix timestamp in milliseconds
  type: ReplayEventType;
  payload: any; // Structure varies by event type
}

type ReplayEventType =
  | "PanoPosition"
  | "PanoPov"
  | "PanoZoom"
  | "MapDisplay"
  | "MapPosition"
  | "MapZoom"
  | "PinPosition"
  | "GuessWithLatLng";
```

#### Replay Event Payloads

**PanoPosition:**
```typescript
{
  lat: number;
  lng: number;
  panoId: string;
}
```

**PanoPov:**
```typescript
{
  heading: number;
  pitch: number;
}
```

**PanoZoom:**
```typescript
{
  zoom: number;
}
```

**MapDisplay:**
```typescript
{
  isActive: boolean;
  isSticky: boolean;
  size: number;
}
```

**MapPosition:**
```typescript
{
  lat: number;
  lng: number;
}
```

**MapZoom:**
```typescript
{
  zoom: number;
}
```

**PinPosition:**
```typescript
{
  lat: number;
  lng: number;
}
```

**GuessWithLatLng:**
```typescript
{
  lat: number;
  lng: number;
}
```

---

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Unauthorized"
}
```
Authentication required. Ensure `_ncfa` cookie is valid and included.

### 404 Not Found
```json
{
  "error": "Game not found"
}
```
The game ID doesn't exist or you don't have permission to view it.

---

## Notes

- **Separate API Domain**: Duels API is on `game-server.geoguessr.com`, not `www.geoguessr.com`
- **Game IDs**: Can be found in duel game URLs or from the main GeoGuessr API endpoints
- **Team Colors**: Always "blue" and "red"
- **Health System**: Damage calculation is based on score differences and active multipliers
- **Multipliers**: Increase with specific rounds (typically every few rounds), making late-game rounds critical
- **Healing Rounds**: Some game modes have designated healing rounds (e.g., round 5) where teams can recover health
- **Movement Options**: NMPZ (No Move, Pan, Zoom) is common in competitive duels
- **Replay Data**: Complete action history allows for detailed analysis and replay visualization
- **Team Duels**: Use `isTeamDuels: true` in options, with multiple players per team
- **Rating Changes**: Included in `progressChange.rankedSystemProgress` for ranked games
- **Game Versions**: The `version` field increments with each state update

---

## Related Endpoints

For creating duels and finding games, see:
- [Games Endpoints](games.md) - Creating and managing games
- [Profiles Endpoints](profiles.md) - Getting player IDs for replay data
- [Maps Endpoints](maps.md) - Getting map slugs for game options
