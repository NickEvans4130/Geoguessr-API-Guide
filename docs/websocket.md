# GeoGuessr WebSocket API

The WebSocket API provides live updates for social features, friend presence, chat messages, and personal notifications.

**WebSocket URL:** `wss://api.geoguessr.com/ws`

## Overview

The GeoGuessr WebSocket is used for receiving live notifications and social updates. It is **NOT** used for game state data (duels, challenges, etc.) - that data is retrieved via REST API endpoints.

### What the WebSocket Is Used For

- Friend presence (online/offline status)
- Friend activity updates (what games they're playing)
- Chat messages
- Personal notifications
- Account updates (coins earned, level ups)
- Daily mission updates
- Friends list changes

### What the WebSocket Is NOT Used For

- Duel game state (use [Duels API](duels.md) REST endpoints)
- Challenge data (use REST API)
- Game progress/scores (use REST API)
- Profile data (use [Profiles API](profiles.md))

---

## Connection & Authentication

### Connecting

The WebSocket requires cookie-based authentication via the `_ncfa` cookie.

**Connection URL:**
```
wss://api.geoguessr.com/ws
```

**Required Headers:**
```
Cookie: _ncfa=YOUR_NCFA_COOKIE_VALUE
Origin: https://www.geoguessr.com
```

**Example (JavaScript):**
```javascript
const ws = new WebSocket('wss://api.geoguessr.com/ws');

ws.onopen = () => {
    console.log('Connected to GeoGuessr WebSocket');
};
```

**Example (Python):**
```python
import asyncio
import websockets

async def connect():
    uri = "wss://api.geoguessr.com/ws"
    headers = {
        "Cookie": f"_ncfa={COOKIE_VALUE}",
        "Origin": "https://www.geoguessr.com"
    }

    async with websockets.connect(uri, additional_headers=headers) as ws:
        print("Connected!")
```

### Heartbeat Requirement

**CRITICAL:** You must send a heartbeat message every 15 seconds to keep the connection alive.

**Heartbeat Message:**
```json
{
  "code": "HeartBeat"
}
```

**Example:**
```javascript
// Send heartbeat every 15 seconds
setInterval(() => {
    ws.send(JSON.stringify({ code: 'HeartBeat' }));
}, 15000);
```

**Note:** The server does not send acknowledgments for heartbeat messages.

### Connection Stability

The WebSocket connection may disconnect at random intervals. Implement reconnection logic to handle this:

```javascript
function connectWithReconnect() {
    const ws = new WebSocket('wss://api.geoguessr.com/ws');

    ws.onclose = () => {
        console.log('Disconnected, reconnecting in 5 seconds...');
        setTimeout(connectWithReconnect, 5000);
    };

    // ... rest of setup
}
```

---

## Subscribing to Topics

After connecting, you must subscribe to topics to receive events.

### Subscribe Message Format

```json
{
  "code": "Subscribe",
  "topic": "TOPIC_PATTERN",
  "client": "web"
}
```

### Available Topics

#### 1. Personal Notifications
**Topic:** `self:{userId}`

**Events Received:**
- Friend presence updates
- Account updates
- Notification pings
- Mission updates
- Friend activity changes

**Example:**
```javascript
ws.send(JSON.stringify({
    code: 'Subscribe',
    topic: 'self:5db9f057dfa5102130eaf747',
    client: 'web'
}));
```

#### 2. Friend Chat Messages
**Topic:** `chat:Friend:TextMessages:{userId}`

**Events Received:**
- Chat messages sent and received

**Example:**
```javascript
ws.send(JSON.stringify({
    code: 'Subscribe',
    topic: 'chat:Friend:TextMessages:5db9f057dfa5102130eaf747',
    client: 'web'
}));
```

**Note:** The server does not send acknowledgments for subscribe messages.

---

## Event Types

All incoming messages follow this structure:

```typescript
{
  code: string;           // Event type
  topic: string;          // Topic it was sent to
  payload: string | null; // JSON-encoded payload (or null)
  accessToken: null;      // Always null
  client: "Unknown";      // Client identifier
  timestamp: string;      // ISO 8601 server timestamp
}
```

### 1. FriendCameOnline

Sent when a friend comes online.

**Topic:** `self:{userId}`

**Payload Structure:**
```typescript
{
  friendId: string;
}
```

**Example:**
```json
{
  "code": "FriendCameOnline",
  "topic": "self:5db9f057dfa5102130eaf747",
  "payload": "{\"friendId\":\"5e3f434a1e34a041f065b2f4\"}",
  "accessToken": null,
  "client": "Unknown",
  "timestamp": "2026-01-12T01:02:54.2926573Z"
}
```

---

### 2. FriendWentOffline

Sent when a friend goes offline.

**Topic:** `self:{userId}`

**Payload Structure:**
```typescript
{
  friendId: string;
}
```

**Example:**
```json
{
  "code": "FriendWentOffline",
  "topic": "self:5db9f057dfa5102130eaf747",
  "payload": "{\"friendId\":\"5e3f434a1e34a041f065b2f4\"}",
  "accessToken": null,
  "client": "Unknown",
  "timestamp": "2026-01-12T01:02:52.5097228Z"
}
```

---

### 3. StatusActivityChanged

Sent when a friend's activity status changes (starts playing a game, etc.).

**Topic:** `self:{userId}`

**Payload Structure:**
```typescript
{
  friendId: string;
  activity: {
    activityType: string;  // e.g., "PlayingClassicDistance"
    timestamp: string;     // ISO 8601
    data: {
      map: string;         // Map name
      platform: string;    // "Web", "Mobile", etc.
    };
  };
}
```

**Example:**
```json
{
  "code": "StatusActivityChanged",
  "topic": "self:5db9f057dfa5102130eaf747",
  "payload": "{\"friendId\":\"5bbdcfab2c01735208565bce\",\"activity\":{\"activityType\":\"PlayingClassicDistance\",\"timestamp\":\"2026-01-12T01:08:04.8781141Z\",\"data\":{\"map\":\"A Learnable Meta Brazil - Vegetation\",\"platform\":\"Web\"}}}",
  "accessToken": null,
  "client": "Unknown",
  "timestamp": "2026-01-12T01:08:04.8852497Z"
}
```

**Known Activity Types:**
- `PlayingClassicDistance` - Playing classic distance mode

---

### 4. ChatMessage

Sent when you send or receive a friend chat message.

**Topic:** `chat:Friend:TextMessages:{userId}`

**Payload Structure:**
```typescript
{
  id: string;                    // Message ID
  payloadType: "Text";           // Message type
  textPayload: string;           // Actual message content
  invitePayload: null | object;  // Game invite data (if applicable)
  recipientType: "User";
  recipientId: string;           // Recipient user ID
  sourceType: "User";
  sourceId: string;              // Sender user ID
  sentAt: string;                // ISO 8601 timestamp
  roomId: string;                // Format: "userId1:userId2"
  context: "Friend";
  channel: null | string;
  clubPayload: null | object;
}
```

**Example:**
```json
{
  "code": "ChatMessage",
  "topic": "chat:Friend:TextMessages:5db9f057dfa5102130eaf747",
  "payload": "{\"id\":\"FKXjLFR1U0\",\"payloadType\":\"Text\",\"textPayload\":\"test (ignore this)\",\"invitePayload\":null,\"recipientType\":\"User\",\"recipientId\":\"67928098295f7b13ef8f810f\",\"sourceType\":\"User\",\"sourceId\":\"5db9f057dfa5102130eaf747\",\"sentAt\":\"2026-01-12T01:00:10.4201917Z\",\"roomId\":\"5db9f057dfa5102130eaf747:67928098295f7b13ef8f810f\",\"context\":\"Friend\",\"channel\":null,\"clubPayload\":null}",
  "accessToken": null,
  "client": "Unknown",
  "timestamp": "2026-01-12T01:00:10.4201975Z"
}
```

---

### 5. FriendsUpdated

Sent when your friends list changes.

**Topic:** `self:{userId}`

**Payload:** `null`

**Example:**
```json
{
  "code": "FriendsUpdated",
  "topic": "self:5db9f057dfa5102130eaf747",
  "payload": null,
  "accessToken": null,
  "client": "Unknown",
  "timestamp": "2026-01-12T00:59:14.9872957Z"
}
```

**Important:** Payload is null. This is a signal to refetch friends list via REST API.

---

### 6. NotificationUpdate

Sent when you have new notifications.

**Topic:** `self:{userId}`

**Payload:** `null`

**Example:**
```json
{
  "code": "NotificationUpdate",
  "topic": "self:5db9f057dfa5102130eaf747",
  "payload": null,
  "accessToken": null,
  "client": "Unknown",
  "timestamp": "2026-01-12T00:59:15.0110082Z"
}
```

**Important:** Payload is null. This is a signal to refetch notifications via REST API.

---

### 7. AccountUpdate

Sent when account data changes (coins earned, XP gained, level up, etc.).

**Topic:** `self:{userId}`

**Payload:** `null`

**Example:**
```json
{
  "code": "AccountUpdate",
  "topic": "self:5db9f057dfa5102130eaf747",
  "payload": null,
  "accessToken": null,
  "client": "Unknown",
  "timestamp": "2026-01-12T01:01:43.0524278Z"
}
```

**Important:** Payload is null. This is a signal to refetch account/profile data via REST API.

---

### 8. MissionsUpdated

Sent when daily missions update or progress changes.

**Topic:** `self:{userId}`

**Payload Structure:**
```typescript
{
  missions: Array<{
    id: string;              // Mission ID (UUID)
    type: string;            // e.g., "Score"
    gameMode: string;        // e.g., "Classic"
    currentProgress: number; // Current progress
    targetProgress: number;  // Target to complete
    completed: boolean;
    endDate: string;         // ISO 8601
    rewardAmount: number;
    rewardType: string;      // e.g., "Coins"
    mapName: string;
    mapSlug: string;
  }>;
  nextMissionDate: string;   // ISO 8601
}
```

**Example:**
```json
{
  "code": "MissionsUpdated",
  "topic": "self:5db9f057dfa5102130eaf747",
  "payload": "{\"missions\":[{\"id\":\"223df977-45a2-4f65-9f31-4c6f2423d4df\",\"type\":\"Score\",\"gameMode\":\"Classic\",\"currentProgress\":0,\"targetProgress\":30000,\"completed\":false,\"endDate\":\"2026-01-13T00:00:00Z\",\"rewardAmount\":90,\"rewardType\":\"Coins\",\"mapName\":\"Dominican Republic\",\"mapSlug\":\"dominican-republic\"}],\"nextMissionDate\":\"2026-01-13T00:00:00Z\"}",
  "accessToken": null,
  "client": "Unknown",
  "timestamp": "2026-01-12T01:01:43.11182Z"
}
```

---

## Complete Example (JavaScript)

```javascript
// Connect to WebSocket
const ws = new WebSocket('wss://api.geoguessr.com/ws');
const userId = 'YOUR_USER_ID';

ws.onopen = () => {
    console.log('Connected!');

    // Subscribe to topics
    ws.send(JSON.stringify({
        code: 'Subscribe',
        topic: `self:${userId}`,
        client: 'web'
    }));

    ws.send(JSON.stringify({
        code: 'Subscribe',
        topic: `chat:Friend:TextMessages:${userId}`,
        client: 'web'
    }));

    // Start heartbeat
    setInterval(() => {
        ws.send(JSON.stringify({ code: 'HeartBeat' }));
    }, 15000);
};

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);

    switch (message.code) {
        case 'FriendCameOnline':
            const friendOnline = JSON.parse(message.payload);
            console.log(`Friend ${friendOnline.friendId} came online`);
            break;

        case 'FriendWentOffline':
            const friendOffline = JSON.parse(message.payload);
            console.log(`Friend ${friendOffline.friendId} went offline`);
            break;

        case 'ChatMessage':
            const chat = JSON.parse(message.payload);
            console.log(`Message from ${chat.sourceId}: ${chat.textPayload}`);
            break;

        case 'StatusActivityChanged':
            const activity = JSON.parse(message.payload);
            console.log(`Friend ${activity.friendId} is now: ${activity.activity.activityType}`);
            break;

        case 'MissionsUpdated':
            const missions = JSON.parse(message.payload);
            console.log(`${missions.missions.length} missions available`);
            break;

        case 'AccountUpdate':
            console.log('Account updated - refresh profile data');
            break;

        case 'FriendsUpdated':
            console.log('Friends list updated - refresh friends');
            break;

        case 'NotificationUpdate':
            console.log('New notifications - refresh notification data');
            break;

        default:
            console.log('Unknown event:', message.code);
    }
};

ws.onclose = () => {
    console.log('Disconnected');
};

ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};
```

---

## Complete Example (Python)

```python
import asyncio
import websockets
import json
import os

USER_ID = "YOUR_USER_ID"
COOKIE = os.getenv('GEOGUESSR_COOKIE')

async def handle_message(message_data):
    """Handle incoming WebSocket message"""
    message = json.loads(message_data)
    code = message.get('code')

    if code == 'FriendCameOnline':
        payload = json.loads(message['payload'])
        print(f"Friend {payload['friendId']} came online")

    elif code == 'FriendWentOffline':
        payload = json.loads(message['payload'])
        print(f"Friend {payload['friendId']} went offline")

    elif code == 'ChatMessage':
        payload = json.loads(message['payload'])
        print(f"Message from {payload['sourceId']}: {payload['textPayload']}")

    elif code == 'StatusActivityChanged':
        payload = json.loads(message['payload'])
        activity_type = payload['activity']['activityType']
        print(f"Friend {payload['friendId']} is now: {activity_type}")

    elif code == 'MissionsUpdated':
        payload = json.loads(message['payload'])
        print(f"{len(payload['missions'])} missions available")

    elif code == 'AccountUpdate':
        print("Account updated - refresh profile data")

    elif code == 'FriendsUpdated':
        print("Friends list updated - refresh friends")

    elif code == 'NotificationUpdate':
        print("New notifications - refresh notification data")

    else:
        print(f"Unknown event: {code}")


async def heartbeat(websocket):
    """Send heartbeat every 15 seconds"""
    while True:
        await asyncio.sleep(15)
        await websocket.send(json.dumps({'code': 'HeartBeat'}))


async def listen_to_websocket():
    uri = "wss://api.geoguessr.com/ws"
    headers = {
        "Cookie": f"_ncfa={COOKIE}",
        "Origin": "https://www.geoguessr.com"
    }

    async with websockets.connect(uri, additional_headers=headers) as ws:
        print("Connected!")

        # Subscribe to topics
        await ws.send(json.dumps({
            "code": "Subscribe",
            "topic": f"self:{USER_ID}",
            "client": "web"
        }))

        await ws.send(json.dumps({
            "code": "Subscribe",
            "topic": f"chat:Friend:TextMessages:{USER_ID}",
            "client": "web"
        }))

        # Start heartbeat task
        heartbeat_task = asyncio.create_task(heartbeat(ws))

        try:
            # Listen for messages
            async for message in ws:
                await handle_message(message)
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            heartbeat_task.cancel()


if __name__ == "__main__":
    asyncio.run(listen_to_websocket())
```

---

## Data Structures (TypeScript)

### Base Message

```typescript
interface WebSocketMessage {
  code: WebSocketEventCode;
  topic: string;
  payload: string | null;
  accessToken: null;
  client: "Unknown" | string;
  timestamp: string;  // ISO 8601
}

type WebSocketEventCode =
  | "FriendCameOnline"
  | "FriendWentOffline"
  | "StatusActivityChanged"
  | "ChatMessage"
  | "FriendsUpdated"
  | "NotificationUpdate"
  | "AccountUpdate"
  | "MissionsUpdated"
  | string;
```

### Outgoing Messages

```typescript
interface SubscribeMessage {
  code: "Subscribe";
  topic: string;
  client: "web";
}

interface HeartBeatMessage {
  code: "HeartBeat";
}
```

### Event Payloads

```typescript
interface FriendPresencePayload {
  friendId: string;
}

interface StatusActivityPayload {
  friendId: string;
  activity: {
    activityType: string;
    timestamp: string;
    data: {
      map: string;
      platform: string;
    };
  };
}

interface ChatMessagePayload {
  id: string;
  payloadType: "Text";
  textPayload: string;
  invitePayload: null | object;
  recipientType: "User";
  recipientId: string;
  sourceType: "User";
  sourceId: string;
  sentAt: string;
  roomId: string;
  context: "Friend";
  channel: null | string;
  clubPayload: null | object;
}

interface MissionsUpdatedPayload {
  missions: Mission[];
  nextMissionDate: string;
}

interface Mission {
  id: string;
  type: string;
  gameMode: string;
  currentProgress: number;
  targetProgress: number;
  completed: boolean;
  endDate: string;
  rewardAmount: number;
  rewardType: string;
  mapName: string;
  mapSlug: string;
}
```

---

## Notes

### Payload Encoding

When `payload` is not null, it contains a **JSON-encoded string** that must be parsed:

```javascript
const message = JSON.parse(event.data);  // Parse outer message
if (message.payload) {
    const payload = JSON.parse(message.payload);  // Parse inner payload
}
```

### Null Payloads

Events with null payloads (`FriendsUpdated`, `NotificationUpdate`, `AccountUpdate`) are signals to refresh data via REST API endpoints. They don't contain the actual data.

### Connection Reliability

The WebSocket connection may drop unexpectedly. Always implement:
- Reconnection logic
- Heartbeat monitoring
- Event buffering (if needed)

### No Server Acknowledgments

The server does not send responses for:
- `Subscribe` messages
- `HeartBeat` messages

Assume they succeeded if the connection remains open.

### Topics Requiring IDs

Both topics require your user ID:
- Get your user ID from `/api/v3/profiles` endpoint
- User ID is found in the `id` field of your profile

---

## Related Endpoints

For data retrieval when receiving null-payload events:

- [Profiles API](profiles.md) - Get account/profile data
- [Social API](social.md) - Get friends list and notifications
- [Feed API](feed.md) - Get friend activity details

For game state data:

- [Duels API](duels.md) - Duel game state (uses REST API, not WebSocket)
- [Games API](games.md) - Game sessions and progress
- [Challenges API](challenges.md) - Challenge data
