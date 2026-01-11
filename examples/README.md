# GeoGuessr API Examples

This directory contains practical, ready-to-use code examples for interacting with the GeoGuessr API in both JavaScript and Python.

## Directory Structure

```
examples/
├── javascript/          # Browser console examples
│   ├── challenges/      # Challenge leaderboards and info
│   ├── profiles/        # User profiles and search
│   ├── social/          # Friends and social features
│   ├── maps/            # Map browsing
│   ├── feed/            # Activity feeds
│   ├── games/           # Game sessions
│   ├── duels/           # Duels state and replays
│   ├── subscriptions/   # Subscription info
│   └── authentication/  # Login and auth
│
└── python/              # Python script examples
    ├── challenges/      # Challenge leaderboards and info
    ├── profiles/        # User profiles and search
    ├── social/          # Friends and social features
    ├── maps/            # Map browsing
    ├── feed/            # Activity feeds
    ├── games/           # Game sessions
    ├── duels/           # Duels state and replays
    ├── subscriptions/   # Subscription info
    └── authentication/  # Login and auth
```

## Quick Start

### JavaScript Examples (Browser Console)

JavaScript examples are designed to run in your browser's developer console:

1. Navigate to https://www.geoguessr.com (must be logged in for most endpoints)
2. Open Developer Tools (F12 or Cmd+Option+I)
3. Go to the Console tab
4. Copy and paste the example code
5. Call the function with appropriate parameters

**Example:**
```javascript
// Copy the entire contents of get-leaderboard.js
// Then call:
getChallengeLeaderboard('6G9h2UPctmUmUtaa');
```

### Python Examples

Python examples require the `requests` library and use environment variables for authentication:

1. Install requirements:
   ```bash
   pip install requests
   ```

2. Set your cookie as an environment variable:
   ```bash
   export GEOGUESSR_COOKIE='your_ncfa_cookie_value'
   ```

3. Run the example:
   ```bash
   python examples/python/challenges/get_leaderboard.py
   ```

## Available Examples

### Challenges

**JavaScript:**
- `get-leaderboard.js` - Get and display challenge leaderboard with statistics
- `get-challenge-info.js` - View challenge settings and map information
- `analyze-performance.js` - Compare your score to the leaderboard

**Python:**
- `get_leaderboard.py` - Get and display challenge leaderboard with statistics
- `get_challenge_info.py` - View challenge settings and map information
- `analyze_performance.py` - Compare your score to the leaderboard

**What you can do:**
- View top players and their scores
- Analyze your ranking and percentile
- Compare your performance to average/median
- See nearby players on the leaderboard

### Profiles

**JavaScript:**
- `get-my-profile.js` - View your complete profile information
- `search-users.js` - Search for users by username
- `compare-users.js` - Compare statistics between two users

**Python:**
- `get_my_profile.py` - View your complete profile information
- `search_users.py` - Search for users by username

**What you can do:**
- Check your level, XP, and progress
- View competitive rating and division
- Find other players
- Compare stats between players

### Social & Friends

**JavaScript:**
- `get-friends-list.js` - View all your friends with statistics

**Python:**
- `get_friends_list.py` - View all your friends with statistics

**What you can do:**
- See who's online
- View friends by country
- Check average friend level
- See Pro user percentage

### Feed & Activity

**JavaScript:**
- `get-friends-activity.js` - View recent activity from friends with analytics

**Python:**
- `get_friends_activity.py` - View recent activity from friends with analytics and export options

**What you can do:**
- See what your friends are playing
- Track most active friends
- View activity type breakdown
- Monitor recent games
- Analyze peak activity hours
- Export activity data to JSON

### Maps

**JavaScript:**
- `browse-popular-maps.js` - Browse popular maps with statistics
- `search-maps.js` - Search for maps by name or keywords

**Python:**
- `browse_popular_maps.py` - Browse popular, featured, new, or hot maps with statistics
- `search_maps.py` - Search for maps by name or keywords

**What you can do:**
- Discover popular maps
- Find maps by difficulty
- See map creators
- View location counts and likes
- Search for specific maps
- Browse different map categories

### Games & Gameplay

**JavaScript:**
- `get-game-state.js` - View current game state and progress
- `create-streak-game.js` - Create custom streak games with presets

**Python:**
- `get_game_state.py` - View current game state and progress
- `create_streak_game.py` - Create custom streak games with interactive setup

**What you can do:**
- Check game progress and statistics
- View round details and guesses
- Create streak games with custom settings
- Use difficulty presets (easy, medium, hard, NMPZ)
- Monitor game state and progress

### Duels

**JavaScript:**
- `get-duel-state.js` - View complete duel game state with teams, health, and damage
- `get-duel-replay.js` - Analyze player actions and behavior from replay data

**Python:**
- `get_duel_state.py` - View complete duel game state with detailed analysis
- `get_duel_replay.py` - Analyze player actions and export replay data

**What you can do:**
- View duel game state
- Track team health and multipliers
- Analyze damage dealt per round
- View player performance statistics
- Get complete replay of player actions
- Compare multiple players' strategies
- Export replay data to CSV/JSON
- Monitor ongoing duels
- Analyze timing and behavior patterns

### Subscriptions

**JavaScript:**
- `check-subscription.js` - View your subscription status and billing info
- `compare-plans.js` - Compare all available subscription plans

**Python:**
- `check_subscription.py` - View your subscription status and billing info
- `compare_plans.py` - Compare all available subscription plans with analysis

**What you can do:**
- Check if you have Pro features
- View subscription end date and renewal info
- Compare plan pricing across currencies
- Calculate savings between monthly/yearly plans
- Find best value subscriptions
- No authentication needed for viewing plans

### Authentication

**JavaScript:**
- `check-auth-status.js` - Verify you're logged in and view account details
- `sign-in-example.js` - Sign in programmatically (educational purposes only)

**Python:**
- `check_auth_status.py` - Verify you're logged in and view account details
- `sign_in_example.py` - Sign in programmatically (educational purposes only)

**What you can do:**
- Check authentication status
- Verify if cookies are valid
- View account age and creation date
- Educational sign-in examples

**⚠️  Important Notes:**
- Sign-in examples are for educational purposes only
- Programmatic login may violate Terms of Service
- Use proper OAuth flows in production
- Never hardcode or commit credentials
- Always use environment variables for sensitive data

## Getting Your Cookie

To use these examples, you need your `_ncfa` cookie:

1. Log in to https://www.geoguessr.com
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies → https://www.geoguessr.com
4. Find the `_ncfa` cookie
5. Copy its value

**Security Warning:** Never share your cookie publicly. Treat it like a password.

### Setting Cookie in Python

**Option 1: Environment Variable (Recommended)**
```bash
export GEOGUESSR_COOKIE='your_cookie_value'
```

**Option 2: .env File**
Create a `.env` file:
```
GEOGUESSR_COOKIE=your_cookie_value
```

Load it in your script:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Common Usage Patterns

### Extract IDs from URLs

**Challenge Token:**
```javascript
const url = "https://www.geoguessr.com/challenge/6G9h2UPctmUmUtaa";
const token = url.split('/').pop();
// Result: "6G9h2UPctmUmUtaa"
```

**User ID:**
```javascript
const url = "https://www.geoguessr.com/user/5db9f057dfa5102130eaf747";
const userId = url.split('/').pop();
// Result: "5db9f057dfa5102130eaf747"
```

### Error Handling

All examples include error handling for common issues:

- **401 Unauthorized** - Invalid or expired cookie
- **403 Forbidden** - Haven't played the challenge yet
- **404 Not Found** - Resource doesn't exist
- **429 Too Many Requests** - Rate limited

### Rate Limiting

Be respectful of the API:
- Don't make excessive requests
- Add delays between bulk operations
- Cache results when possible
- Implement exponential backoff on errors

**Example Rate Limiting (JavaScript):**
```javascript
async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

for (const token of challengeTokens) {
    await getChallengeLeaderboard(token);
    await sleep(100); // 100ms delay between requests
}
```

**Example Rate Limiting (Python):**
```python
import time

for token in challenge_tokens:
    get_challenge_leaderboard(token, cookie)
    time.sleep(0.1)  # 100ms delay
```

## Modifying Examples

All examples are designed to be easy to modify and extend:

1. **Change output format** - Modify the display sections
2. **Add filtering** - Filter results by criteria
3. **Export data** - Save results to JSON/CSV
4. **Combine examples** - Mix functionality from multiple examples

**Example: Export to JSON (JavaScript)**
```javascript
const data = await getChallengeLeaderboard('token');
const json = JSON.stringify(data, null, 2);
console.log(json);
// Or save to file in Node.js:
// require('fs').writeFileSync('leaderboard.json', json);
```

**Example: Export to CSV (Python)**
```python
import csv

leaderboard = get_challenge_leaderboard(token, cookie)
with open('leaderboard.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['rank', 'username', 'score'])
    writer.writeheader()
    writer.writerows(leaderboard)
```

## Contributing Examples

Want to add more examples? Follow these guidelines:

1. **Use clear, descriptive names** - Function and file names should explain what they do
2. **Include comprehensive comments** - Explain parameters and return values
3. **Add error handling** - Handle common error cases gracefully
4. **Follow the existing format** - Match the style of current examples
5. **Test thoroughly** - Verify examples work with real data
6. **Document requirements** - List any dependencies or prerequisites

## Need Help?

- Check the [main documentation](../README.md) for API endpoint details
- Review specific endpoint docs in the root directory (challenges.md, profiles.md, etc.)
- Look at similar examples for patterns and best practices

## License

These examples are provided as-is for educational purposes. Always respect GeoGuessr's Terms of Service when using the API.
