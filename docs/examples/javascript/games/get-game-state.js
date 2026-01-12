/**
 * Get Game State
 *
 * Retrieves the current state of a game including rounds, progress, and settings.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com (must be logged in)
 * 2. Paste this code into the console
 * 3. Call: getGameState('GAME_TOKEN')
 */

async function getGameState(gameToken) {
    try {
        const url = `https://www.geoguessr.com/api/v3/games/${gameToken}?client=web`;

        const response = await fetch(url, {
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const game = await response.json();

        // Display game information
        console.log(`\n🎮 Game State\n`);
        console.log(`Token: ${game.token}`);
        console.log(`Mode: ${game.mode} (${game.type})`);
        console.log(`State: ${game.state}`);
        console.log(`Map: ${game.mapName}`);

        console.log(`\n⚙️  Settings:`);
        console.log(`Rounds: ${game.roundCount}`);
        console.log(`Time Limit: ${game.timeLimit === 0 ? 'None' : game.timeLimit + 's'}`);
        console.log(`Movement: ${game.forbidMoving ? '❌ Disabled' : '✅ Enabled'}`);
        console.log(`Panning: ${game.forbidRotating ? '❌ Disabled' : '✅ Enabled'}`);
        console.log(`Zooming: ${game.forbidZooming ? '❌ Disabled' : '✅ Enabled'}`);

        console.log(`\n📊 Progress:`);
        console.log(`Current Round: ${game.round} of ${game.roundCount}`);

        if (game.player) {
            const player = game.player;
            console.log(`\n👤 Player Stats:`);
            console.log(`Score: ${parseInt(player.totalScore.amount).toLocaleString()} points`);
            console.log(`Distance: ${player.totalDistanceInMeters.toLocaleString()}m`);
            console.log(`Time: ${player.totalTime}s`);
            console.log(`Guesses: ${player.guesses.length}`);

            if (game.mode === 'streak') {
                console.log(`Streak: ${player.totalStreak}`);
            }
        }

        // Show rounds
        if (game.rounds && game.rounds.length > 0) {
            console.log(`\n📍 Rounds:`);
            game.rounds.forEach((round, index) => {
                const status = game.player?.guesses[index] ? '✅' : '⏳';
                console.log(`${status} Round ${index + 1}: ${round.lat.toFixed(4)}, ${round.lng.toFixed(4)}`);
            });
        }

        // Show guesses if any
        if (game.player?.guesses && game.player.guesses.length > 0) {
            console.log(`\n🎯 Your Guesses:`);
            game.player.guesses.forEach((guess, index) => {
                console.log(`Round ${index + 1}: ${guess.roundScore.amount} points (${guess.distance.meters.amount}m away)`);
            });
        }

        return game;

    } catch (error) {
        console.error('❌ Error fetching game state:', error.message);
        return null;
    }
}

// Example usage:
// getGameState('XB9wycuZvDrhl7cB');

// Get game token from current URL:
// const currentToken = window.location.pathname.split('/').pop();
// getGameState(currentToken);

// Monitor game progress (poll every 5 seconds):
// async function monitorGame(token) {
//     while (true) {
//         const game = await getGameState(token);
//         if (!game || game.state === 'finished') break;
//         await new Promise(r => setTimeout(r, 5000));
//     }
// }
