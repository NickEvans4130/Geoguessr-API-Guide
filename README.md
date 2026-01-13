# GeoGuessr API Documentation

**Unofficial, community-maintained documentation for the GeoGuessr API**

> Comprehensive guide to the undocumented GeoGuessr API based on reverse engineering and community research.

## 📖 View Documentation

**[Read the full documentation →](https://geoguessr-api-docs.netlify.app/)**

## What's Included

- **🔐 Authentication** - Cookie-based authentication and account management
- **👤 User Profiles** - Profile data, search, and statistics
- **🎮 Games & Gameplay** - Standard games, streaks, and infinity mode
- **⚔️ Duels** - Competitive duels and replay analysis
- **🗺️ Maps** - Browsing, searching, and map statistics
- **🏆 Challenges** - Challenge creation, leaderboards, and results
- **👥 Social** - Friends, badges, and social features
- **📡 Feed** - Activity streams and tracking
- **💳 Subscriptions** - Plan information and management
- **🔌 WebSocket** - Live notifications and social updates
- **💻 Code Examples** - Ready-to-use JavaScript and Python examples

## Quick Start

### JavaScript (Browser Console)

```javascript
// Get your profile
const response = await fetch('https://www.geoguessr.com/api/v3/profiles', {
    credentials: 'include'
});
const profile = await response.json();
console.log(profile);
```

### Python

```python
import requests

cookies = {'_ncfa': 'YOUR_COOKIE_VALUE'}
response = requests.get('https://www.geoguessr.com/api/v3/profiles', cookies=cookies)
profile = response.json()
print(profile)
```

## Examples

This repository includes 40+ ready-to-use code examples:

- Challenge leaderboards and analysis
- User profile comparison
- Friends activity tracking
- Map browsing and search
- Game state monitoring
- Duel replay analysis
- Subscription management
- And much more!

[View all examples](https://nickevans4130.github.io/Geoguessr-API-Guide/examples/)

## Documentation Structure

```
docs/
├── README.md              # Main documentation
├── authentication.md      # Auth & account endpoints
├── profiles.md            # User profiles
├── games.md               # Game sessions
├── duels.md               # Duels (game-server API)
├── challenges.md          # Challenge endpoints
├── maps.md                # Map browsing
├── social.md              # Friends & social
├── feed.md                # Activity feeds
├── subscriptions.md       # Subscription info
├── websocket.md           # WebSocket API
└── examples/              # Code examples
    ├── javascript/        # Browser examples
    └── python/            # Python scripts
```

## Contributing

This documentation is community-maintained and welcomes contributions!

- 🐛 Report incorrect information
- 📝 Improve documentation
- 💻 Add code examples
- 🧪 Test and verify endpoints
- 🆕 Document new features

See [CONTRIBUTING.md](https://nickevans4130.github.io/Geoguessr-API-Guide/CONTRIBUTING/) for guidelines.

## Disclaimer

This API is not officially documented or supported by GeoGuessr. Use at your own risk and always respect:

- Rate limits
- Terms of Service
- Fair use policies
- User privacy

The API can change at any time without notice.

## Resources

- **[Full Documentation](https://geoguessr-api-docs.netlify.app/)**
- **[Code Examples](https://nickevans4130.github.io/Geoguessr-API-Guide/examples/)**
- **[Contributing Guide](https://nickevans4130.github.io/Geoguessr-API-Guide/CONTRIBUTING/)**
- [GeoGuessr Website](https://www.geoguessr.com)

## License

This documentation is provided as-is for educational purposes. Always respect GeoGuessr's Terms of Service.

---

**Last Updated:** January 2026 | **Maintained by:** Community Contributors
