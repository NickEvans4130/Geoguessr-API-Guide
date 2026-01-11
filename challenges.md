# Challenges API

Endpoints for creating, viewing, and interacting with GeoGuessr challenges.

## Table of Contents

- [Overview](#overview)
- [Endpoints](#endpoints)
  - [Get Challenge Results](#get-challenge-results)
  - [Get Challenge Info](#get-challenge-info)
- [Data Structures](#data-structures)
- [Implementation Examples](#implementation-examples)
- [Common Use Cases](#common-use-cases)

## Overview

Challenges are custom games that can be shared with other players. Each challenge has a unique token and can contain multiple rounds.

**🚀 Ready to use?** Check out the [challenge examples](../examples/javascript/challenges/) for ready-to-use scripts:
- [Get Leaderboard](../examples/javascript/challenges/get-leaderboard.js) - View top players and statistics
- [Analyze Performance](../examples/javascript/challenges/analyze-performance.js) - Compare your score to others
- [Get Challenge Info](../examples/javascript/challenges/get-challenge-info.js) - View challenge settings

**Key Concepts:**
- **Challenge Token**: 16-character alphanumeric identifier (e.g., `6G9h2UPctmUmUtaa`)
- **Rounds**: Typically 5 rounds per challenge
- **Results**: Detailed player-by-player scoring data
- **Access Restriction**: You must have played a challenge to view its detailed results

## Endpoints

### Get Challenge Results

Returns detailed results for all players who completed a challenge, including round-by-round data.

**Endpoint:**
```
GET /v3/results/highscores/{challengeToken}
```

**Parameters:**
- `{challengeToken}` (path) - The unique identifier for the challenge

**Authentication:** Required (must have played the challenge)

**Example Request:**
```javascript
fetch('https://www.geoguessr.com/api/v3/results/highscores/6G9h2UPctmUmUtaa', {
    credentials: 'include'
})
```

**Response Structure:**
```json
{
  "items": [
    {
      "game": {
        "token": "nZ2NT4HDJW01n4Hd",
        "type": "challenge",
        "mode": "standard",
        "state": "finished",
        "roundCount": 5,
        "timeLimit": 0,
        "forbidMoving": true,
        "forbidZooming": true,
        "forbidRotating": true,
        "streakType": "countrystreak",
        "map": "6089bfcff6a0770001f645dd",
        "mapName": "An Arbitrary World",
        "round": 5,
        "rounds": [
          {
            "lat": -6.555895114892618,
            "lng": -78.44216538640902,
            "panoId": "445842434D466D5773373974514E67575A634A337077",
            "heading": 224,
            "pitch": 2,
            "zoom": 0,
            "streakLocationCode": "pe",
            "startTime": "2026-01-10T18:11:42.5090000Z"
          }
        ],
        "player": {
          "id": "59c55f9656b1c23bc81cb742",
          "nick": "brbw",
          "isVerified": false,
          "flair": 0,
          "countryCode": "us",
          "totalScore": {
            "amount": "19570",
            "unit": "points",
            "percentage": 78.28
          },
          "totalDistance": {
            "meters": {
              "amount": "2498.6",
              "unit": "km"
            }
          },
          "totalDistanceInMeters": 2498561.458729427,
          "totalTime": 96,
          "guesses": [
            {
              "lat": -12.692075399442235,
              "lng": -75.26799581445442,
              "timedOut": false,
              "roundScore": {
                "amount": "3305",
                "unit": "points",
                "percentage": 66.1
              },
              "roundScoreInPoints": 3305,
              "distance": {
                "meters": {
                  "amount": "765.8",
                  "unit": "km"
                }
              },
              "distanceInMeters": 765843.4375052782,
              "time": 34
            }
          ]
        }
      }
    }
  ],
  "paginationToken": null
}
```

**Important Notes:**

- Scores are in `player.guesses[]`, NOT in `rounds[]`
- `rounds[]` contains only location data
- `guesses[]` contains player performance (scores, distances, times)
- `player.id` is the unique player identifier (use this, not nick)
- Must have played the challenge to access this endpoint

---

### Get Challenge Info

Returns basic information about a challenge without player results.

**Endpoint:**
```
GET /v3/challenges/{challengeToken}
```

**Parameters:**
- `{challengeToken}` (path) - The unique identifier for the challenge

**Authentication:** Not required for public challenges

**Example Request:**
```javascript
fetch('https://www.geoguessr.com/api/v3/challenges/6G9h2UPctmUmUtaa', {
    credentials: 'include'
})
```

**Response Structure:**
```json
{
  "token": "6G9h2UPctmUmUtaa",
  "name": "Challenge Name",
  "map": "6089bfcff6a0770001f645dd",
  "mapName": "An Arbitrary World",
  "mode": "standard",
  "timeLimit": 0,
  "forbidMoving": true,
  "forbidZooming": true,
  "forbidRotating": true,
  "rounds": 5,
  "creator": {
    "id": "5f98ae9e94816c000199aee4",
    "nick": "Username"
  }
}
```

**Response Fields:**
- `token` - Challenge token
- `name` - Challenge name (if set by creator)
- `map` - Map ID
- `mapName` - Human-readable map name
- `mode` - Game mode (e.g., "standard")
- `timeLimit` - Time limit per round in seconds (0 = no limit)
- `forbidMoving` - NMPZ (No Moving) restriction
- `forbidZooming` - NZ (No Zooming) restriction
- `forbidRotating` - NR (No Rotating) restriction
- `rounds` - Number of rounds
- `creator` - Challenge creator information

---

## Data Structures

### Player Result Object

```typescript
interface PlayerResult {
  game: {
    token: string;              // Unique game session token
    type: "challenge";
    mode: string;               // "standard", "moving", etc.
    state: "finished";
    roundCount: number;         // Number of rounds (usually 5)
    timeLimit: number;          // Seconds per round (0 = no limit)
    forbidMoving: boolean;      // NMPZ restriction
    forbidZooming: boolean;     // NZ restriction
    forbidRotating: boolean;    // NR restriction
    streakType: string;         // e.g., "countrystreak"
    map: string;                // Map ID
    mapName: string;            // Map name
    round: number;              // Last round played

    rounds: Round[];            // Location data for each round

    player: {
      id: string;               // Player UserID (unique identifier)
      nick: string;             // Display name
      isVerified: boolean;
      flair: number;
      countryCode: string;      // 2-letter ISO country code

      totalScore: {
        amount: string;         // Total points as string
        unit: "points";
        percentage: number;     // 0-100
      };

      totalDistance: {
        meters: {
          amount: string;
          unit: "km";
        };
      };

      totalDistanceInMeters: number;
      totalTime: number;        // Total seconds

      guesses: Guess[];         // Array of guesses (scores here!)
    };
  };
}

interface Round {
  lat: number;                  // Location latitude
  lng: number;                  // Location longitude
  panoId: string;               // Street View panorama ID
  heading: number;              // Camera heading (0-360)
  pitch: number;                // Camera pitch
  zoom: number;                 // Camera zoom level
  streakLocationCode: string;   // Country code
  startTime: string;            // ISO 8601 timestamp
}

interface Guess {
  lat: number;                  // Guess latitude
  lng: number;                  // Guess longitude
  timedOut: boolean;

  roundScore: {
    amount: string;
    unit: "points";
    percentage: number;
  };

  roundScoreInPoints: number;   // USE THIS for scoring!

  distance: {
    meters: {
      amount: string;
      unit: "km";
    };
  };

  distanceInMeters: number;     // Distance in meters
  time: number;                 // Seconds taken
  stepsCount: number;           // Number of moves
}
```

### Challenge Token

Challenge tokens are extracted from challenge URLs:

```
https://www.geoguessr.com/challenge/6G9h2UPctmUmUtaa
                                    ^^^^^^^^^^^^^^^^
                                    Challenge Token
```

**Characteristics:**
- 16 characters long
- Alphanumeric (a-z, A-Z, 0-9)
- Case-sensitive
- May contain hyphens or underscores

**Extracting from URL (JavaScript):**
```javascript
const url = "https://www.geoguessr.com/challenge/6G9h2UPctmUmUtaa";
const token = url.split('/').pop();  // "6G9h2UPctmUmUtaa"

// Or with regex:
const token = url.match(/challenge\/([a-zA-Z0-9_-]+)/)[1];
```

**Extracting from URL (Python):**
```python
url = "https://www.geoguessr.com/challenge/6G9h2UPctmUmUtaa"
token = url.split('/')[-1]  # "6G9h2UPctmUmUtaa"

# Or with regex:
import re
match = re.search(r'challenge/([a-zA-Z0-9_-]+)', url)
token = match.group(1) if match else None
```

---

## Implementation Examples

### Example 1: Get Leaderboard

**JavaScript:**
```javascript
async function getChallengeLeaderboard(challengeToken) {
    const url = `https://www.geoguessr.com/api/v3/results/highscores/${challengeToken}`;

    const response = await fetch(url, { credentials: 'include' });
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    // Extract and sort players by total score
    const leaderboard = data.items.map(item => {
        const player = item.game.player;
        return {
            userId: player.id,
            username: player.nick,
            country: player.countryCode,
            totalScore: parseInt(player.totalScore.amount),
            totalTime: player.totalTime,
            totalDistance: player.totalDistanceInMeters
        };
    });

    // Sort by score descending
    leaderboard.sort((a, b) => b.totalScore - a.totalScore);

    // Add rank
    leaderboard.forEach((player, index) => {
        player.rank = index + 1;
    });

    return leaderboard;
}

// Usage
const leaderboard = await getChallengeLeaderboard('6G9h2UPctmUmUtaa');
console.table(leaderboard);
```

**Python:**
```python
import requests

def get_challenge_leaderboard(challenge_token, cookie):
    url = f'https://www.geoguessr.com/api/v3/results/highscores/{challenge_token}'

    response = requests.get(url, cookies={'_ncfa': cookie})
    response.raise_for_status()

    data = response.json()

    # Extract and process players
    leaderboard = []
    for item in data['items']:
        player = item['game']['player']
        leaderboard.append({
            'userId': player['id'],
            'username': player['nick'],
            'country': player['countryCode'],
            'totalScore': int(player['totalScore']['amount']),
            'totalTime': player['totalTime'],
            'totalDistance': player['totalDistanceInMeters']
        })

    # Sort by score descending
    leaderboard.sort(key=lambda x: x['totalScore'], reverse=True)

    # Add rank
    for index, player in enumerate(leaderboard):
        player['rank'] = index + 1

    return leaderboard

# Usage
cookie = 'YOUR_NCFA_COOKIE'
leaderboard = get_challenge_leaderboard('6G9h2UPctmUmUtaa', cookie)
for player in leaderboard:
    print(f"{player['rank']}. {player['username']}: {player['totalScore']} points")
```

---

### Example 2: Calculate Round Winners

**JavaScript:**
```javascript
async function getRoundWinners(challengeToken) {
    const url = `https://www.geoguessr.com/api/v3/results/highscores/${challengeToken}`;
    const response = await fetch(url, { credentials: 'include' });
    const data = await response.json();

    const roundCount = data.items[0]?.game.roundCount || 5;
    const roundWinners = [];

    for (let roundIndex = 0; roundIndex < roundCount; roundIndex++) {
        // Get all scores for this round
        const roundScores = data.items.map(item => ({
            userId: item.game.player.id,
            username: item.game.player.nick,
            score: item.game.player.guesses[roundIndex]?.roundScoreInPoints || 0,
            distance: item.game.player.guesses[roundIndex]?.distanceInMeters || 0,
            time: item.game.player.guesses[roundIndex]?.time || 0
        }));

        // Sort by score descending
        roundScores.sort((a, b) => b.score - a.score);

        roundWinners.push({
            round: roundIndex + 1,
            winner: roundScores[0],
            top3: roundScores.slice(0, 3)
        });
    }

    return roundWinners;
}

// Usage
const roundWinners = await getRoundWinners('6G9h2UPctmUmUtaa');
roundWinners.forEach(round => {
    console.log(`Round ${round.round}: ${round.winner.username} (${round.winner.score} pts)`);
});
```

**Python:**
```python
def get_round_winners(challenge_token, cookie):
    url = f'https://www.geoguessr.com/api/v3/results/highscores/{challenge_token}'
    response = requests.get(url, cookies={'_ncfa': cookie})
    data = response.json()

    round_count = data['items'][0]['game']['roundCount'] if data['items'] else 5
    round_winners = []

    for round_index in range(round_count):
        # Get all scores for this round
        round_scores = []
        for item in data['items']:
            player = item['game']['player']
            guess = player['guesses'][round_index] if round_index < len(player['guesses']) else None

            round_scores.append({
                'userId': player['id'],
                'username': player['nick'],
                'score': guess['roundScoreInPoints'] if guess else 0,
                'distance': guess['distanceInMeters'] if guess else 0,
                'time': guess['time'] if guess else 0
            })

        # Sort by score descending
        round_scores.sort(key=lambda x: x['score'], reverse=True)

        round_winners.append({
            'round': round_index + 1,
            'winner': round_scores[0],
            'top3': round_scores[:3]
        })

    return round_winners

# Usage
winners = get_round_winners('6G9h2UPctmUmUtaa', cookie)
for round_data in winners:
    winner = round_data['winner']
    print(f"Round {round_data['round']}: {winner['username']} ({winner['score']} pts)")
```

---

### Example 3: Get Player Statistics

**JavaScript:**
```javascript
async function getPlayerStats(challengeToken, userId) {
    const url = `https://www.geoguessr.com/api/v3/results/highscores/${challengeToken}`;
    const response = await fetch(url, { credentials: 'include' });
    const data = await response.json();

    const playerData = data.items.find(item => item.game.player.id === userId);

    if (!playerData) {
        throw new Error('Player not found in challenge results');
    }

    const player = playerData.game.player;
    const guesses = player.guesses;

    return {
        username: player.nick,
        country: player.countryCode,
        totalScore: parseInt(player.totalScore.amount),
        totalTime: player.totalTime,
        totalDistance: player.totalDistanceInMeters,

        // Round-by-round data
        rounds: guesses.map((guess, index) => ({
            round: index + 1,
            score: guess.roundScoreInPoints,
            distance: guess.distanceInMeters,
            time: guess.time,
            moves: guess.stepsCount || 0
        })),

        // Statistics
        averageScore: guesses.reduce((sum, g) => sum + g.roundScoreInPoints, 0) / guesses.length,
        bestRound: Math.max(...guesses.map(g => g.roundScoreInPoints)),
        worstRound: Math.min(...guesses.map(g => g.roundScoreInPoints)),
        perfectGuesses: guesses.filter(g => g.roundScoreInPoints === 5000).length
    };
}

// Usage
const stats = await getPlayerStats('6G9h2UPctmUmUtaa', '59c55f9656b1c23bc81cb742');
console.log(`${stats.username}: ${stats.totalScore} points (avg: ${stats.averageScore.toFixed(0)})`);
```

---

## Common Use Cases

### 1. Building a Leaderboard Widget

Display real-time challenge leaderboards:

```javascript
async function displayLeaderboard(challengeToken, elementId) {
    const leaderboard = await getChallengeLeaderboard(challengeToken);

    const html = `
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Player</th>
                    <th>Score</th>
                    <th>Time</th>
                </tr>
            </thead>
            <tbody>
                ${leaderboard.map(player => `
                    <tr>
                        <td>${player.rank}</td>
                        <td>${player.username}</td>
                        <td>${player.totalScore.toLocaleString()}</td>
                        <td>${player.totalTime}s</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    document.getElementById(elementId).innerHTML = html;
}
```

### 2. Challenge Comparison

Compare performance across multiple challenges:

```javascript
async function comparePlayerAcrossChallenges(userId, challengeTokens) {
    const results = [];

    for (const token of challengeTokens) {
        try {
            const stats = await getPlayerStats(token, userId);
            results.push({
                challenge: token,
                score: stats.totalScore,
                average: stats.averageScore
            });
        } catch (error) {
            console.error(`Failed to get stats for ${token}:`, error);
        }
    }

    return results;
}
```

### 3. Round-by-Round Analysis

Analyze performance trends across rounds:

```javascript
async function analyzeRoundPerformance(challengeToken, userId) {
    const url = `https://www.geoguessr.com/api/v3/results/highscores/${challengeToken}`;
    const response = await fetch(url, { credentials: 'include' });
    const data = await response.json();

    const playerData = data.items.find(item => item.game.player.id === userId);
    const guesses = playerData.game.player.guesses;

    // Calculate performance metrics per round
    return guesses.map((guess, index) => ({
        round: index + 1,
        score: guess.roundScoreInPoints,
        scorePercentage: guess.roundScoreInPercentage,
        distance: (guess.distanceInMeters / 1000).toFixed(1) + ' km',
        time: guess.time + 's',
        efficiency: (guess.roundScoreInPoints / guess.time).toFixed(2) // points per second
    }));
}
```

---

## Error Handling

### Common Errors

**403 Forbidden - Haven't Played Challenge:**
```javascript
if (response.status === 403) {
    console.error('You must play this challenge before viewing results');
    // Redirect user to play the challenge
    window.location.href = `https://www.geoguessr.com/challenge/${challengeToken}`;
}
```

**404 Not Found - Invalid Token:**
```javascript
if (response.status === 404) {
    console.error('Challenge not found. The token may be invalid or the challenge may have been deleted.');
}
```

### Robust Error Handling Example

```javascript
async function fetchChallengeResultsSafely(challengeToken) {
    try {
        const url = `https://www.geoguessr.com/api/v3/results/highscores/${challengeToken}`;
        const response = await fetch(url, { credentials: 'include' });

        if (response.status === 401) {
            throw new Error('Authentication failed. Please log in to GeoGuessr.');
        }

        if (response.status === 403) {
            throw new Error('You must play this challenge before viewing results.');
        }

        if (response.status === 404) {
            throw new Error('Challenge not found.');
        }

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();

    } catch (error) {
        console.error('Error fetching challenge results:', error);
        return null;
    }
}
```

---

## Testing

See [challenges-testing.md](./tests/challenges-testing.md) for console commands to test these endpoints.
