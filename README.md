# GeoGuessr API Documentation

**Unofficial, community-maintained documentation for the GeoGuessr API**

This is a comprehensive guide to the undocumented GeoGuessr API based on reverse engineering and community research. GeoGuessr does not officially support or guarantee these endpoints.

## Disclaimer

This API is not officially documented or supported by GeoGuessr. Use at your own risk and always respect:
- Rate limits
- Terms of Service
- Fair use policies
- User privacy

The API can change at any time without notice.

## Table of Contents

- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [API Basics](#api-basics)
- [Quick Start Examples](#quick-start-examples)
- [API Reference by Category](#api-reference-by-category)
- [Best Practices](#best-practices)
- [Contributing](#contributing)

## Repository Structure

```
.
├── README.md                  # This file - Getting started guide
├── authentication.md          # Authentication & account endpoints
├── challenges.md              # Challenge creation and results
├── feed.md                    # Activity feeds and social streams
├── games.md                   # Game sessions and gameplay modes
├── maps.md                    # Map browsing and searching
├── profiles.md                # User profiles and search
├── social.md                  # Friends, badges, and social features
├── subscriptions.md           # Subscription plans and management
├── examples/                  # 🔥 Ready-to-use code examples
│   ├── README.md              # Examples guide and usage
│   ├── javascript/            # Browser console examples
│   │   ├── challenges/        # Challenge leaderboards, performance analysis
│   │   ├── profiles/          # Profile viewing, user search, comparison
│   │   ├── social/            # Friends list and statistics
│   │   ├── maps/              # Browse and discover maps
│   │   └── feed/              # Activity feeds and tracking
│   └── python/                # Python script examples
│       ├── challenges/        # Challenge leaderboards, performance analysis
│       ├── profiles/          # Profile viewing, user search
│       ├── social/            # Friends list and statistics
│       ├── maps/              # Browse and search maps
│       └── feed/              # Activity feeds and tracking
└── tests/                     # Testing files (not for public use)
    ├── *-testing.md           # Test scripts for each endpoint
    └── *-testing-results.md   # Raw test results
```

**Note**: The `tests/` directory contains internal testing files used to verify API endpoints and is excluded from the main documentation.

### 🚀 Quick Start with Examples

New to the API? Start with the [examples directory](./examples/):

- **JavaScript Examples** - Run directly in your browser console (no setup required!)
- **Python Examples** - Complete scripts ready to use (`pip install requests`)

**Popular examples:**
- [Get Challenge Leaderboard](./examples/javascript/challenges/get-leaderboard.js) - View top players and scores
- [Analyze Your Performance](./examples/javascript/challenges/analyze-performance.js) - See how you rank
- [Get Your Profile](./examples/javascript/profiles/get-my-profile.js) - View your stats
- [Friends Activity Feed](./examples/javascript/feed/get-friends-activity.js) - Track what friends are playing

See [examples/README.md](./examples/README.md) for the complete list and usage instructions.

## Getting Started

### Base URL

All API endpoints use the base URL:
```
https://www.geoguessr.com/api
```

### API Versions

GeoGuessr has multiple API versions:
- **v3**: Legacy endpoints, still widely used
- **v4**: Newer endpoints with enhanced features

Most endpoints are in v3, with newer features migrating to v4.

### Response Format

All endpoints return JSON responses with standard HTTP status codes.

## Authentication

### Cookie-Based Authentication

GeoGuessr uses cookie-based session authentication with a cookie named `_ncfa`.

#### How to Obtain Your Cookie

1. Log in to GeoGuessr in your browser
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies
4. Find the `_ncfa` cookie
5. Copy its value

The cookie typically lasts several months but will expire if you log out or after extended inactivity.

### JavaScript Usage (Browser)

When making requests from the browser, cookies are automatically included:

```javascript
// Fetch API
const response = await fetch('https://www.geoguessr.com/api/v3/profiles', {
    credentials: 'include'  // Include cookies automatically
});
const data = await response.json();
console.log(data);

// XMLHttpRequest
const xhr = new XMLHttpRequest();
xhr.withCredentials = true;
xhr.open('GET', 'https://www.geoguessr.com/api/v3/profiles');
xhr.send();
```

**Important**: The `credentials: 'include'` option is required for authenticated endpoints.

### JavaScript Usage (Node.js)

When making requests from Node.js, you need to manually provide the cookie:

```javascript
// Using fetch (node-fetch or native fetch in Node 18+)
const response = await fetch('https://www.geoguessr.com/api/v3/profiles', {
    headers: {
        'Cookie': '_ncfa=YOUR_NCFA_COOKIE_VALUE'
    }
});
const data = await response.json();

// Using axios
const axios = require('axios');
const response = await axios.get('https://www.geoguessr.com/api/v3/profiles', {
    headers: {
        'Cookie': '_ncfa=YOUR_NCFA_COOKIE_VALUE'
    }
});
console.log(response.data);
```

### Python Usage

```python
import requests

# Set up cookies
cookies = {
    '_ncfa': 'YOUR_NCFA_COOKIE_VALUE'
}

# Make request
response = requests.get(
    'https://www.geoguessr.com/api/v3/profiles',
    cookies=cookies
)

# Parse JSON response
data = response.json()
print(data)
```

**With requests Session (recommended for multiple requests):**

```python
import requests

# Create a session
session = requests.Session()
session.cookies.set('_ncfa', 'YOUR_NCFA_COOKIE_VALUE')

# Make requests
response = session.get('https://www.geoguessr.com/api/v3/profiles')
data = response.json()

# All subsequent requests will use the same cookie
response2 = session.get('https://www.geoguessr.com/api/v3/social/friends')
friends = response2.json()
```

### cURL Usage

```bash
curl 'https://www.geoguessr.com/api/v3/profiles' \
  -H 'Cookie: _ncfa=YOUR_NCFA_COOKIE_VALUE'
```

### Security Best Practices

- Never share your `_ncfa` cookie publicly
- Don't commit cookies to version control
- Use environment variables for sensitive data:

```javascript
// JavaScript
const NCFA_COOKIE = process.env.GEOGUESSR_COOKIE;

// Python
import os
NCFA_COOKIE = os.getenv('GEOGUESSR_COOKIE')
```

## API Basics

### HTTP Methods

The API uses standard HTTP methods:
- **GET**: Retrieve data
- **POST**: Create new resources
- **PUT**: Update existing resources
- **DELETE**: Delete resources

### Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request format |
| 401 | Unauthorized | Invalid or missing authentication |
| 403 | Forbidden | Access denied (e.g., haven't played challenge) |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Temporary server issue |

### Error Handling

Always check for errors in your code:

**JavaScript:**
```javascript
async function fetchAPI(url) {
    try {
        const response = await fetch(url, { credentials: 'include' });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}
```

**Python:**
```python
def fetch_api(url, cookies):
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()  # Raises HTTPError for bad status
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
```

### Rate Limiting

While official rate limits aren't documented, follow these guidelines:
- Don't exceed 10 requests per second
- Add delays between requests (100-500ms recommended)
- Implement exponential backoff on errors
- Cache responses when possible

**JavaScript Rate Limiting:**
```javascript
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchWithRateLimit(urls) {
    const results = [];
    for (const url of urls) {
        const data = await fetchAPI(url);
        results.push(data);
        await sleep(100);  // 100ms delay between requests
    }
    return results;
}
```

**Python Rate Limiting:**
```python
import time

def fetch_with_rate_limit(urls, cookies):
    results = []
    for url in urls:
        data = fetch_api(url, cookies)
        results.append(data)
        time.sleep(0.1)  # 100ms delay
    return results
```

## Quick Start Examples

**💡 Want more examples?** Check out the [examples directory](./examples/) for ready-to-use scripts including leaderboard analysis, user comparison, activity feeds, and more!

### Example 1: Get Your Profile

**JavaScript:**
```javascript
async function getMyProfile() {
    const response = await fetch('https://www.geoguessr.com/api/v3/profiles', {
        credentials: 'include'
    });
    const profile = await response.json();
    console.log(`Welcome, ${profile.user.nick}!`);
    console.log(`Level: ${profile.user.progress.level}`);
    return profile;
}

getMyProfile();
```

**Python:**
```python
import requests

def get_my_profile(cookie):
    response = requests.get(
        'https://www.geoguessr.com/api/v3/profiles',
        cookies={'_ncfa': cookie}
    )
    profile = response.json()
    print(f"Welcome, {profile['user']['nick']}!")
    print(f"Level: {profile['user']['progress']['level']}")
    return profile

# Usage
cookie = 'YOUR_NCFA_COOKIE'
profile = get_my_profile(cookie)
```

### Example 2: Get Challenge Results

**JavaScript:**
```javascript
async function getChallengeResults(challengeToken) {
    const url = `https://www.geoguessr.com/api/v3/results/highscores/${challengeToken}`;
    const response = await fetch(url, { credentials: 'include' });
    const data = await response.json();

    // Process results
    const leaderboard = data.items.map((item, index) => ({
        rank: index + 1,
        player: item.game.player.nick,
        score: parseInt(item.game.player.totalScore.amount)
    }));

    console.table(leaderboard);
    return leaderboard;
}

// Usage
getChallengeResults('6G9h2UPctmUmUtaa');
```

**Python:**
```python
import requests

def get_challenge_results(challenge_token, cookie):
    url = f'https://www.geoguessr.com/api/v3/results/highscores/{challenge_token}'
    response = requests.get(url, cookies={'_ncfa': cookie})
    data = response.json()

    # Process results
    leaderboard = []
    for index, item in enumerate(data['items']):
        player_data = item['game']['player']
        leaderboard.append({
            'rank': index + 1,
            'player': player_data['nick'],
            'score': int(player_data['totalScore']['amount'])
        })

    for entry in leaderboard:
        print(f"{entry['rank']}. {entry['player']}: {entry['score']} points")

    return leaderboard

# Usage
cookie = 'YOUR_NCFA_COOKIE'
results = get_challenge_results('6G9h2UPctmUmUtaa', cookie)
```

### Example 3: Search for a User

**JavaScript:**
```javascript
async function searchUser(username) {
    const url = `https://www.geoguessr.com/api/v3/search/user?q=${encodeURIComponent(username)}`;
    const response = await fetch(url, { credentials: 'include' });
    const results = await response.json();

    results.forEach(user => {
        console.log(`${user.nick} (${user.id})`);
    });

    return results;
}

// Usage
searchUser('brbw');
```

**Python:**
```python
import requests
from urllib.parse import quote

def search_user(username, cookie):
    url = f'https://www.geoguessr.com/api/v3/search/user?q={quote(username)}'
    response = requests.get(url, cookies={'_ncfa': cookie})
    results = response.json()

    for user in results:
        print(f"{user['nick']} ({user['id']})")

    return results

# Usage
cookie = 'YOUR_NCFA_COOKIE'
users = search_user('brbw', cookie)
```

## API Reference by Category

The API endpoints are organized into the following categories:

### [Challenges](./challenges.md)
Challenge creation, results, and information
- Get challenge results and leaderboards
- Get challenge information
- Create new challenges

### [Authentication & Accounts](./authentication.md)
Login, signup, and account management
- Sign in with various providers
- Account deletion
- Password management

### [User Profiles](./profiles.md)
User profile data and management
- Get user profiles
- Search for users
- Profile customization

### [Games & Gameplay](./games.md)
Game sessions and gameplay modes
- Standard games
- Streak mode
- Infinity mode

### [Social & Friends](./social.md)
Friends, badges, and social features
- Friends list management
- Badges and achievements
- Social events

### [Maps](./maps.md)
Map browsing, searching, and scores
- Browse featured and popular maps
- Search for maps
- Map scores and statistics

### [Subscriptions](./subscriptions.md)
Subscription plans and management
- Get subscription status
- Available plans
- Payment methods

### [Feed & Activity](./feed.md)
User feeds and activity streams
- Friends activity
- Private feed
- Recent games

## Best Practices

### 1. Respect Rate Limits
- Add delays between requests
- Use exponential backoff on errors
- Cache responses when appropriate

### 2. Handle Errors Gracefully
- Always check HTTP status codes
- Implement retry logic
- Log errors for debugging

### 3. Validate Data
- Check for null/undefined values
- Verify array lengths
- Handle missing fields

### 4. Security
- Store cookies securely
- Use environment variables
- Never expose cookies in logs or version control

### 5. Be a Good Citizen
- Don't abuse the API
- Respect the platform
- Consider the impact on GeoGuessr's servers

## Common Patterns

### Pagination

Some endpoints support pagination:
```javascript
let allItems = [];
let paginationToken = null;

do {
    const url = paginationToken
        ? `${baseUrl}?token=${paginationToken}`
        : baseUrl;

    const response = await fetch(url, { credentials: 'include' });
    const data = await response.json();

    allItems = allItems.concat(data.items);
    paginationToken = data.paginationToken;

} while (paginationToken);
```

### Extracting IDs from URLs

Challenge Token:
```javascript
const url = "https://www.geoguessr.com/challenge/6G9h2UPctmUmUtaa";
const token = url.split('/').pop();  // "6G9h2UPctmUmUtaa"
```

User ID from Profile URL:
```javascript
const url = "https://www.geoguessr.com/user/59c55f9656b1c23bc81cb742";
const userId = url.split('/').pop();  // "59c55f9656b1c23bc81cb742"
```

## Troubleshooting

### 401 Unauthorized
- Your `_ncfa` cookie is invalid or expired
- Log in again and get a fresh cookie

### 403 Forbidden
- You don't have permission to access this resource
- For challenges: you must have played the challenge first

### 404 Not Found
- The resource doesn't exist
- Check that IDs/tokens are correct

### 429 Too Many Requests
- You're making requests too quickly
- Implement rate limiting and backoff

### 500/503 Server Errors
- GeoGuessr server is experiencing issues
- Retry with exponential backoff
- Check GeoGuessr's status

## Contributing

This documentation is community-maintained and based on real API testing. To contribute:

1. **Test endpoints thoroughly** - Verify behavior with actual API calls
2. **Document complete structures** - Include all fields with TypeScript interfaces
3. **Provide working examples** - Include both JavaScript and Python examples
4. **Note edge cases** - Document errors, deprecated endpoints, and special behaviors
5. **Keep it organized** - Use the existing file structure and formatting conventions

### Documentation Standards

- All endpoint documentation should include:
  - Complete request/response examples
  - TypeScript interfaces for data structures
  - Working code examples in JavaScript and Python
  - Notes about authentication requirements
  - Common errors and edge cases

- Use verified data from actual API testing
- Update the relevant category file (authentication.md, profiles.md, etc.)
- Keep examples simple and practical

## Resources

- [GeoGuessr Website](https://www.geoguessr.com)
- [Community Discord Servers](https://www.geoguessr.com/discord)
- [GitHub Projects](https://github.com/search?q=geoguessr+api)

## License

This documentation is provided as-is for educational purposes. Always respect GeoGuessr's Terms of Service.

---

**Last Updated:** January 2026

**Maintained by:** Community Contributors
