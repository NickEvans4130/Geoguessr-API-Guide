/**
 * Create Streak Game
 *
 * Creates a new country/region streak game with custom settings.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com (must be logged in)
 * 2. Paste this code into the console
 * 3. Call: createStreakGame(options)
 */

async function createStreakGame(options = {}) {
    try {
        const url = 'https://www.geoguessr.com/api/v3/games/streak';

        // Default options
        const settings = {
            forbidMoving: options.forbidMoving || false,
            forbidRotating: options.forbidRotating || false,
            forbidZooming: options.forbidZooming || false,
            streakType: options.streakType || 'CountryStreak',
            timeLimit: options.timeLimit || 0  // 0 = no limit
        };

        const response = await fetch(url, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const game = await response.json();

        // Display game information
        console.log(`\n✅ Streak Game Created!\n`);
        console.log(`Token: ${game.token}`);
        console.log(`Game URL: https://www.geoguessr.com/game/${game.token}`);
        console.log(`Mode: ${game.streakType}`);

        console.log(`\n⚙️  Settings:`);
        console.log(`Time Limit: ${game.timeLimit === 0 ? 'None' : game.timeLimit + 's per round'}`);
        console.log(`Movement: ${game.forbidMoving ? '❌ Disabled (NMPZ)' : '✅ Enabled'}`);
        console.log(`Panning: ${game.forbidRotating ? '❌ Disabled (NR)' : '✅ Enabled'}`);
        console.log(`Zooming: ${game.forbidZooming ? '❌ Disabled (NZ)' : '✅ Enabled'}`);

        console.log(`\n📍 Starting Location:`);
        if (game.rounds && game.rounds[0]) {
            const round = game.rounds[0];
            console.log(`Coordinates: ${round.lat.toFixed(4)}, ${round.lng.toFixed(4)}`);
            console.log(`Country Code: ${round.streakLocationCode || 'N/A'}`);
        }

        console.log(`\n🎮 Ready to play! Navigate to the game URL above.`);

        return game;

    } catch (error) {
        console.error('❌ Error creating streak game:', error.message);
        return null;
    }
}

// Example usage:

// Create default streak game (no restrictions):
// createStreakGame();

// Create NMPZ streak game (no moving, panning, or zooming):
// createStreakGame({
//     forbidMoving: true,
//     forbidRotating: true,
//     forbidZooming: true
// });

// Create timed streak game (60 seconds per round):
// createStreakGame({
//     timeLimit: 60
// });

// Create hard mode streak:
// createStreakGame({
//     timeLimit: 30,
//     forbidMoving: true,
//     forbidZooming: true
// });

// Preset configurations:
const STREAK_PRESETS = {
    easy: {
        forbidMoving: false,
        forbidRotating: false,
        forbidZooming: false,
        timeLimit: 0
    },
    medium: {
        forbidMoving: false,
        forbidRotating: false,
        forbidZooming: false,
        timeLimit: 60
    },
    hard: {
        forbidMoving: true,
        forbidRotating: false,
        forbidZooming: true,
        timeLimit: 30
    },
    nmpz: {
        forbidMoving: true,
        forbidRotating: true,
        forbidZooming: true,
        timeLimit: 0
    }
};

// Use preset:
// createStreakGame(STREAK_PRESETS.hard);
