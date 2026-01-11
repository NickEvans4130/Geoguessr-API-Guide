# Authentication & Accounts API

Endpoints for authentication, account creation, and account management.

## Table of Contents

- [Overview](#overview)
- [Endpoints](#endpoints)
  - [Sign In](#sign-in)
  - [Social Sign In](#social-sign-in)
  - [Account Management](#account-management)
  - [Password Management](#password-management)
- [Data Structures](#data-structures)
- [Implementation Examples](#implementation-examples)

## Overview

GeoGuessr supports multiple authentication methods:
- **Email/Password** - Traditional account creation
- **Google** - Google account sign-in
- **Facebook** - Facebook account sign-in
- **Apple** - Apple account sign-in

All authentication endpoints use the `_ncfa` cookie for session management after successful login.

**Important:** These endpoints are primarily used by the GeoGuessr client application and may require specific headers or request formats.

## Endpoints

### Sign In

Standard email/password authentication.

**Endpoint:**
```
POST /v3/accounts/signin
```

**Authentication:** Not required (this endpoint creates authentication)

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** Complete user object (same structure as GET /v3/profiles response)

**Example Response:**
```json
{
  "nick": "Sirey",
  "created": "2019-10-30T20:19:35.6820000Z",
  "isProUser": true,
  "type": "Unlimited",
  "isVerified": false,
  "pin": {
    "url": "pin/7dd941395a4ce096339065fc766a9482.png",
    "anchor": "center-center",
    "isDefault": false
  },
  "id": "5db9f057dfa5102130eaf747",
  "countryCode": "gb",
  "progress": {
    "xp": 1456894,
    "level": 158
  },
  "competitive": {
    "elo": 766,
    "rating": 1267
  }
}
```

**Important Notes:**
- Returns user object directly (not wrapped in `user` property)
- Sets `session` cookie and `_ncfa` cookie (HttpOnly, not visible to JavaScript)
- Sets `devicetoken` cookie
- Response body is the full user object sent in request (visible in Network tab)
- After successful login, use `GET /v3/profiles` to check authentication status

---

### Social Sign In

#### Google Sign In

**Endpoint:**
```
POST /v3/googleplus/signin
```

**Authentication:** Not required

**Request Body:** (Structure needs verification)
Likely contains Google OAuth token or authorization code.

**Note:** This endpoint needs testing to verify exact request/response format.

---

#### Facebook Sign In

**Endpoint:**
```
POST /v3/facebook/signin
```

**Authentication:** Not required

**Request Body:** (Structure needs verification)
Likely contains Facebook OAuth token or authorization code.

**Note:** This endpoint needs testing to verify exact request/response format.

---

#### Apple Sign In

**Endpoint:**
```
POST /v3/apple/signin
```

**Authentication:** Not required

**Request Body:** (Structure needs verification)
Likely contains Apple ID token or authorization code.

**Note:** This endpoint needs testing to verify exact request/response format.

---

### Account Management

#### Delete Account

Permanently deletes a user account.

**Endpoint:**
```
DELETE /v3/accounts/delete
```

**Authentication:** Required

**Request Body:** (Structure needs verification)
May require password confirmation or other verification.

**Expected Response:** (Structure needs verification)

**Warning:** This action is likely irreversible. Use with extreme caution.

**Note:** This endpoint needs testing to verify exact request/response format.

---

### Password Management

#### Set Password

Sets a password for an account (possibly for accounts created via social login).

**Endpoint:**
```
POST /v3/profiles/setpassword
```

**Authentication:** Required

**Request Body:** (Structure needs verification)
```json
{
  "password": "newpassword123"
}
```

**Note:** This endpoint needs testing to verify exact request/response format.

---

#### Reset Password

Initiates password reset flow by sending a reset email to the user.

**Endpoint:**
```
POST /v3/profiles/resetpassword
```

**Authentication:** Not required (this is for forgotten passwords)

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:** Returns 200 OK with user object

**Example Response:**
```json
{
  "nick": "Sirey",
  "created": "2019-10-30T20:19:35.6820000Z",
  "isProUser": true,
  "type": "Unlimited",
  "isVerified": false,
  "id": "5db9f057dfa5102130eaf747",
  "countryCode": "gb"
}
```

**Important Notes:**
- Returns 200 OK and user object if email exists
- Sends password reset email to the specified address
- Email contains a reset link to complete the password change
- Does not reveal whether the email exists (returns user object regardless)

---

### Check Authentication Status

To verify if a user is authenticated, use the profiles endpoint.

**Endpoint:**
```
GET /v3/profiles
```

**Authentication:** Required

**Response:** Full profile object if authenticated, 401 if not

**Usage:**
```javascript
async function isAuthenticated() {
    try {
        const response = await fetch('https://www.geoguessr.com/api/v3/profiles', {
            credentials: 'include'
        });
        return response.ok;
    } catch {
        return false;
    }
}
```

**Important Notes:**
- Use this endpoint to check if the user has a valid session
- Returns 401 Unauthorized if not authenticated
- Returns full profile object (with `user` nested inside) if authenticated
- The `_ncfa` cookie is HttpOnly and cannot be accessed from JavaScript

---

## Data Structures

### Sign In Response

The sign-in endpoint returns a complete user object:

```typescript
interface SignInResponse {
  nick: string;                  // Username
  created: string;               // Account creation date (ISO 8601)
  isProUser: boolean;            // Pro subscription status
  type: string;                  // Account type ("Unlimited", "Pro", etc.)
  isVerified: boolean;           // Verified account status
  pin: {
    url: string;
    anchor: string;
    isDefault: boolean;
  };
  id: string;                    // User ID (24-character hex)
  countryCode: string;           // 2-letter country code
  progress: {
    xp: number;
    level: number;
    levelXp: number;
    nextLevel: number;
    nextLevelXp: number;
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
  // ... additional user fields (33+ fields total)
}
```

**Important:** The response is the user object directly, NOT wrapped in a parent object.

---

### Session Cookies

After successful authentication, the following cookies are set:

- `_ncfa` - Main authentication cookie (HttpOnly, not accessible from JavaScript)
- `session` - Session information (Base64 encoded, contains SessionId and Expires)
- `devicetoken` - Device identifier
- `g_state` - Google state information

**Note:** The `_ncfa` cookie is HttpOnly for security and cannot be read by JavaScript.

---

## Implementation Examples

### Example 1: Sign In

**JavaScript:**
```javascript
async function signIn(email, password) {
    const response = await fetch('https://www.geoguessr.com/api/v3/accounts/signin', {
        method: 'POST',
        credentials: 'include',  // Important: to receive cookies
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const user = await response.json();
    console.log(`Signed in as ${user.nick} (Level ${user.progress.level})`);
    console.log(`Pro user: ${user.isProUser}`);

    // The _ncfa cookie is now set (HttpOnly)
    // The session cookie is now set
    return user;
}

// Usage
// await signIn('user@example.com', 'password123');
```

**Python:**
```python
import requests

def sign_in(email, password):
    url = 'https://www.geoguessr.com/api/v3/accounts/signin'

    payload = {
        'email': email,
        'password': password
    }

    session = requests.Session()
    response = session.post(url, json=payload)
    response.raise_for_status()

    user = response.json()
    print(f"Signed in as {user['nick']} (Level {user['progress']['level']})")
    print(f"Pro user: {user['isProUser']}")

    # The session now has the authentication cookies
    # Use this session for subsequent authenticated requests
    return session, user

# Usage
# session, user = sign_in('user@example.com', 'password123')
```

---

### Example 2: Check Current Authentication

You can verify if you're currently authenticated by fetching your profile:

**JavaScript:**
```javascript
async function checkAuthentication() {
    try {
        const response = await fetch('https://www.geoguessr.com/api/v3/profiles', {
            credentials: 'include'
        });

        if (response.status === 401) {
            console.log('Not authenticated');
            return false;
        }

        if (response.ok) {
            const profile = await response.json();
            console.log('Authenticated as:', profile.user.nick);
            return true;
        }

        return false;

    } catch (error) {
        console.error('Error checking authentication:', error);
        return false;
    }
}

// Usage
checkAuthentication();
```

**Python:**
```python
import requests

def check_authentication(cookie):
    url = 'https://www.geoguessr.com/api/v3/profiles'

    try:
        response = requests.get(url, cookies={'_ncfa': cookie})

        if response.status_code == 401:
            print('Not authenticated')
            return False

        if response.status_code == 200:
            profile = response.json()
            print(f'Authenticated as: {profile["user"]["nick"]}')
            return True

        return False

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return False

# Usage
# check_authentication('YOUR_NCFA_COOKIE')
```

---

## Common Use Cases

### 1. Programmatic Login

For automated scripts that need to authenticate:

```javascript
async function loginAndGetCookie(email, password) {
    // Sign in
    const authData = await signIn(email, password);

    // Extract cookie from browser's cookie store
    const cookies = document.cookie.split(';');
    const ncfaCookie = cookies.find(c => c.trim().startsWith('_ncfa='));

    if (ncfaCookie) {
        const cookieValue = ncfaCookie.split('=')[1];
        console.log('Authentication cookie:', cookieValue);
        return cookieValue;
    }

    throw new Error('Cookie not found after login');
}
```

**Warning:** Programmatic login may violate GeoGuessr's Terms of Service. This is for educational purposes only.

---

### 2. Session Management

For long-running applications:

```javascript
class GeoGuessrSession {
    constructor() {
        this.authenticated = false;
    }

    async login(email, password) {
        await signIn(email, password);
        this.authenticated = await this.checkAuth();
        return this.authenticated;
    }

    async checkAuth() {
        const response = await fetch('https://www.geoguessr.com/api/v3/profiles', {
            credentials: 'include'
        });
        return response.ok;
    }

    async makeRequest(url) {
        if (!this.authenticated) {
            throw new Error('Not authenticated');
        }

        return fetch(url, { credentials: 'include' });
    }
}

// Usage
// const session = new GeoGuessrSession();
// await session.login('user@example.com', 'password123');
// const response = await session.makeRequest('https://www.geoguessr.com/api/v3/...');
```

---

## Security Considerations

### 1. Cookie Security

The `_ncfa` cookie is your session credential:
- **Never share it publicly**
- **Don't commit it to version control**
- **Treat it like a password**
- **Rotate it regularly by logging out and back in**

### 2. Password Handling

If implementing authentication:
- **Never log passwords**
- **Use HTTPS only**
- **Don't store passwords in plaintext**
- **Implement rate limiting to prevent brute force**

### 3. Social Login

Social login endpoints require OAuth tokens:
- Follow OAuth best practices
- Validate tokens server-side
- Handle token expiration

---

## Error Handling

### Common Errors

**401 Unauthorized - Invalid Credentials:**
```javascript
if (response.status === 401) {
    console.error('Invalid email or password');
    // Show error to user
}
```

**429 Too Many Requests - Rate Limited:**
```javascript
if (response.status === 429) {
    console.error('Too many login attempts. Please wait and try again.');
    // Implement exponential backoff
}
```

**400 Bad Request - Invalid Format:**
```javascript
if (response.status === 400) {
    console.error('Invalid request format');
    // Check request body structure
}
```

---

## Best Practices

### 1. Use Environment Variables

Never hardcode credentials:

```javascript
// JavaScript
const email = process.env.GEOGUESSR_EMAIL;
const password = process.env.GEOGUESSR_PASSWORD;

// Python
import os
email = os.getenv('GEOGUESSR_EMAIL')
password = os.getenv('GEOGUESSR_PASSWORD')
```

### 2. Implement Retry Logic

Authentication can fail due to network issues:

```javascript
async function signInWithRetry(email, password, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await signIn(email, password);
        } catch (error) {
            if (i === maxRetries - 1) throw error;
            console.log(`Retry ${i + 1}/${maxRetries}...`);
            await sleep(1000 * (i + 1)); // Exponential backoff
        }
    }
}
```

### 3. Validate Before Sending

Validate inputs before making requests:

```javascript
function validateCredentials(email, password) {
    if (!email || !email.includes('@')) {
        throw new Error('Invalid email address');
    }
    if (!password || password.length < 6) {
        throw new Error('Password must be at least 6 characters');
    }
}
```

---

## Testing

See [authentication-testing.md](./tests/authentication-testing.md) for console commands to test these endpoints.

**Important:** Many of these endpoints cannot be easily tested without potentially logging out or creating test accounts. Exercise caution when testing authentication endpoints.

---

## Notes for Documentation Contributors

The following aspects need verification through testing:

- [ ] Exact request body structure for `/v3/accounts/signin`
- [ ] Response structure for successful sign in
- [ ] Social login request/response formats
- [ ] Account deletion confirmation requirements
- [ ] Password reset flow and response
- [ ] Set password requirements (minimum length, special characters, etc.)
- [ ] Error messages and status codes
- [ ] Rate limiting thresholds
- [ ] Cookie attributes (_ncfa cookie flags, expiration, etc.)

If you test these endpoints, please document:
1. Complete request structure (headers, body)
2. Complete response structure
3. Error responses for different scenarios
4. Any special behaviors or requirements
