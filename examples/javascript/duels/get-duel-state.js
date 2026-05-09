/**
 * Get Duel Game State
 *
 * Fetches complete game state for a duel including teams, players,
 * rounds, health, damage, and final results.
 *
 * Usage: Run in browser console while logged into GeoGuessr
 */

/**
 * Fetch complete duel game state
 * @param {string} gameId - The duel game ID
 * @returns {Promise<object>} Complete game data with teams, rounds, and results
 */
async function getDuelGameState(gameId) {
    const url = `https://game-server.geoguessr.com/api/duels/${gameId}`;

    try {
        const response = await fetch(url, {
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const gameData = await response.json();

        // Display basic game info
        console.log('=== Duel Game State ===');
        console.log(`Game ID: ${gameData.gameId}`);
        console.log(`Status: ${gameData.status}`);
        console.log(`Current Round: ${gameData.currentRoundNumber}`);
        console.log(`Game Mode: ${gameData.options.competitiveGameMode}`);
        console.log(`Map: ${gameData.options.map.name}`);
        console.log('');

        // Display team information
        console.log('=== Teams ===');
        gameData.teams.forEach(team => {
            const teamName = team.name.toUpperCase();
            console.log(`\nTeam ${teamName}:`);
            console.log(`  Health: ${team.health}/${gameData.initialHealth}`);
            console.log(`  Current Multiplier: ${team.currentMultiplier}x`);
            console.log(`  Players: ${team.players.length}`);

            team.players.forEach(player => {
                console.log(`    - Player ID: ${player.playerId}`);
                console.log(`      Rating: ${player.rating}`);
                console.log(`      Country: ${player.countryCode.toUpperCase()}`);
                console.log(`      Guesses: ${player.guesses.length}`);
            });
        });

        // Display result if game is finished
        if (gameData.status === 'Finished') {
            console.log('\n=== Game Result ===');
            const winningTeam = gameData.teams.find(t => t.id === gameData.result.winningTeamId);
            console.log(`Winner: Team ${winningTeam.name.toUpperCase()}`);
            console.log(`Victory Type: ${gameData.result.winnerStyle}`);
            console.log(`Final Score: ${winningTeam.health} HP remaining`);
        }

        // Display round summary
        console.log('\n=== Round Summary ===');
        const completedRounds = gameData.rounds.filter(r => r.hasProcessedRoundTimeout);
        console.log(`Completed Rounds: ${completedRounds.length}`);

        completedRounds.slice(0, 5).forEach(round => {
            console.log(`\nRound ${round.roundNumber}:`);
            console.log(`  Location: ${round.panorama.countryCode.toUpperCase()}`);
            console.log(`  Multiplier: ${round.multiplier}x`);

            // Get round results for each team
            gameData.teams.forEach(team => {
                const roundResult = team.roundResults.find(r => r.roundNumber === round.roundNumber);
                if (roundResult) {
                    console.log(`  Team ${team.name}: Score ${roundResult.score}, Damage ${roundResult.damageDealt}`);
                }
            });
        });

        return gameData;

    } catch (error) {
        console.error('Error fetching duel game state:', error);
        throw error;
    }
}

/**
 * Analyze damage dealt across all rounds
 * @param {object} gameData - Game data from getDuelGameState
 */
function analyzeDamage(gameData) {
    console.log('\n=== Damage Analysis ===');

    gameData.teams.forEach(team => {
        const totalDamage = team.roundResults.reduce((sum, r) => sum + r.damageDealt, 0);
        console.log(`\nTeam ${team.name.toUpperCase()}:`);
        console.log(`  Total Damage Dealt: ${totalDamage}`);
        console.log(`  Average per Round: ${(totalDamage / team.roundResults.length).toFixed(0)}`);

        // Find biggest damage round
        const maxDamageRound = team.roundResults.reduce((max, r) =>
            r.damageDealt > max.damageDealt ? r : max
        );
        console.log(`  Biggest Hit: ${maxDamageRound.damageDealt} (Round ${maxDamageRound.roundNumber}, ${maxDamageRound.multiplier}x)`);
    });
}

/**
 * Display player performance statistics
 * @param {object} gameData - Game data from getDuelGameState
 */
function displayPlayerStats(gameData) {
    console.log('\n=== Player Performance ===');

    gameData.teams.forEach(team => {
        console.log(`\nTeam ${team.name.toUpperCase()}:`);

        team.players.forEach(player => {
            const validGuesses = player.guesses.filter(g => g.score !== null);
            const totalScore = validGuesses.reduce((sum, g) => sum + g.score, 0);
            const avgScore = validGuesses.length > 0 ? totalScore / validGuesses.length : 0;
            const avgDistance = validGuesses.reduce((sum, g) => sum + g.distance, 0) / validGuesses.length;

            console.log(`\n  Player ${player.playerId.substring(0, 8)}...`);
            console.log(`    Rating: ${player.rating}`);
            console.log(`    Country: ${player.countryCode.toUpperCase()}`);
            console.log(`    Rounds Played: ${validGuesses.length}`);
            console.log(`    Average Score: ${avgScore.toFixed(0)}`);
            console.log(`    Average Distance: ${(avgDistance / 1000).toFixed(1)} km`);

            // Rating change
            const ratingChange = player.progressChange?.rankedSystemProgress;
            if (ratingChange) {
                const change = ratingChange.gameModeRatingAfter - ratingChange.gameModeRatingBefore;
                console.log(`    Rating Change: ${change > 0 ? '+' : ''}${change}`);
            }
        });
    });
}

// ===== USAGE EXAMPLES =====

// Example 1: Basic usage - get game state
console.log('Fetching duel game state...');
getDuelGameState('6963ff12ec85cd5824375992')
    .then(data => {
        console.log('\nGame data retrieved successfully!');
        console.log(`\nUse these functions for more analysis:`);
        console.log(`  analyzeDamage(data) - View damage statistics`);
        console.log(`  displayPlayerStats(data) - View player performance`);
    })
    .catch(err => console.error('Failed to fetch game:', err));

// Example 2: Complete analysis with all functions
/*
getDuelGameState('6963ff12ec85cd5824375992')
    .then(data => {
        analyzeDamage(data);
        displayPlayerStats(data);
    });
*/

// Example 3: Monitor an ongoing game
/*
async function monitorGame(gameId, intervalSeconds = 5) {
    console.log(`Monitoring game ${gameId}...`);

    const interval = setInterval(async () => {
        try {
            const data = await getDuelGameState(gameId);

            console.log(`\n[Update] Round ${data.currentRoundNumber} - Status: ${data.status}`);
            data.teams.forEach(team => {
                console.log(`  Team ${team.name}: ${team.health} HP (${team.currentMultiplier}x)`);
            });

            if (data.status === 'Finished') {
                console.log('\nGame finished! Stopping monitor.');
                clearInterval(interval);
            }
        } catch (error) {
            console.error('Monitor error:', error);
            clearInterval(interval);
        }
    }, intervalSeconds * 1000);

    return interval;
}

// Start monitoring
const monitor = monitorGame('YOUR_GAME_ID', 10);

// Stop monitoring manually
// clearInterval(monitor);
*/
