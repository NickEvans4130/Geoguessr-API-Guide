/**
 * Get Duel Replay Events
 *
 * Fetches complete replay data for a player's actions during a specific round.
 * Includes camera movements, map interactions, and guess placement with timestamps.
 *
 * Usage: Run in browser console while logged into GeoGuessr
 */

/**
 * Fetch replay events for a specific player and round
 * @param {string} playerId - The player's user ID
 * @param {string} duelId - The duel game ID
 * @param {number} roundNumber - The round number (1-indexed)
 * @returns {Promise<Array>} Array of replay events with timestamps
 */
async function getDuelReplay(playerId, duelId, roundNumber) {
    const url = `https://game-server.geoguessr.com/api/replays/${playerId}/${duelId}/${roundNumber}`;

    try {
        const response = await fetch(url, {
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const replayEvents = await response.json();

        console.log('=== Duel Replay Events ===');
        console.log(`Player ID: ${playerId}`);
        console.log(`Duel ID: ${duelId}`);
        console.log(`Round: ${roundNumber}`);
        console.log(`Total Events: ${replayEvents.length}`);
        console.log('');

        // Analyze event types
        const eventTypes = {};
        replayEvents.forEach(event => {
            eventTypes[event.type] = (eventTypes[event.type] || 0) + 1;
        });

        console.log('Event Type Breakdown:');
        Object.entries(eventTypes).forEach(([type, count]) => {
            console.log(`  ${type}: ${count}`);
        });

        return replayEvents;

    } catch (error) {
        console.error('Error fetching duel replay:', error);
        throw error;
    }
}

/**
 * Analyze player behavior from replay events
 * @param {Array} events - Replay events from getDuelReplay
 */
function analyzePlayerBehavior(events) {
    console.log('\n=== Player Behavior Analysis ===');

    // Calculate total time
    const startTime = events[0]?.time || 0;
    const endTime = events[events.length - 1]?.time || 0;
    const totalSeconds = (endTime - startTime) / 1000;

    console.log(`\nTiming:`);
    console.log(`  Total Time: ${totalSeconds.toFixed(1)}s`);

    // Find key events
    const guessEvent = events.find(e => e.type === 'GuessWithLatLng');
    const mapDisplayEvents = events.filter(e => e.type === 'MapDisplay');
    const pinPositionEvents = events.filter(e => e.type === 'PinPosition');
    const zoomEvents = events.filter(e => e.type === 'PanoZoom');

    console.log(`\nActions:`);
    console.log(`  Map Opens: ${mapDisplayEvents.filter(e => e.payload.isActive).length}`);
    console.log(`  Pin Adjustments: ${pinPositionEvents.length}`);
    console.log(`  Zoom Changes: ${zoomEvents.length}`);

    if (guessEvent) {
        const guessTime = (guessEvent.time - startTime) / 1000;
        console.log(`  Time to Guess: ${guessTime.toFixed(1)}s`);
        console.log(`  Final Guess: ${guessEvent.payload.lat.toFixed(5)}, ${guessEvent.payload.lng.toFixed(5)}`);
    }

    // Analyze map usage
    const firstMapOpen = mapDisplayEvents.find(e => e.payload.isActive);
    if (firstMapOpen) {
        const mapOpenTime = (firstMapOpen.time - startTime) / 1000;
        console.log(`\nMap Usage:`);
        console.log(`  First Map Open: ${mapOpenTime.toFixed(1)}s`);

        const mapCloses = mapDisplayEvents.filter(e => !e.payload.isActive).length;
        console.log(`  Map Opens/Closes: ${mapCloses} times`);
    }

    // Analyze camera movements
    const povEvents = events.filter(e => e.type === 'PanoPov');
    if (povEvents.length > 0) {
        console.log(`\nCamera Movement:`);
        console.log(`  POV Changes: ${povEvents.length}`);

        const headings = povEvents.map(e => e.payload.heading);
        const headingRange = Math.max(...headings) - Math.min(...headings);
        console.log(`  Heading Range: ${headingRange.toFixed(0)}°`);
    }
}

/**
 * Display replay timeline with key moments
 * @param {Array} events - Replay events from getDuelReplay
 * @param {number} maxEvents - Maximum number of events to display (default: 20)
 */
function displayTimeline(events, maxEvents = 20) {
    console.log('\n=== Replay Timeline ===');

    const startTime = events[0]?.time || 0;

    // Filter to important events
    const importantTypes = ['MapDisplay', 'PinPosition', 'GuessWithLatLng', 'PanoPosition'];
    const importantEvents = events.filter(e => importantTypes.includes(e.type));

    const eventsToShow = importantEvents.slice(0, maxEvents);

    eventsToShow.forEach(event => {
        const relativeTime = ((event.time - startTime) / 1000).toFixed(1);
        let description = '';

        switch (event.type) {
            case 'MapDisplay':
                description = event.payload.isActive ? '📍 Opened map' : '📍 Closed map';
                break;
            case 'PinPosition':
                description = `📌 Placed pin at ${event.payload.lat.toFixed(2)}, ${event.payload.lng.toFixed(2)}`;
                break;
            case 'GuessWithLatLng':
                description = `✅ FINAL GUESS at ${event.payload.lat.toFixed(2)}, ${event.payload.lng.toFixed(2)}`;
                break;
            case 'PanoPosition':
                description = `🌍 Moved to ${event.payload.countryCode?.toUpperCase() || 'unknown'}`;
                break;
        }

        console.log(`[${relativeTime}s] ${description}`);
    });

    if (importantEvents.length > maxEvents) {
        console.log(`\n... and ${importantEvents.length - maxEvents} more events`);
    }
}

/**
 * Compare replay events from multiple players in the same round
 * @param {Array<{playerId: string, duelId: string, roundNumber: number}>} players - Array of player info
 */
async function comparePlayerReplays(players) {
    console.log('\n=== Comparing Player Replays ===');

    try {
        const replays = await Promise.all(
            players.map(p => getDuelReplay(p.playerId, p.duelId, p.roundNumber))
        );

        console.log('\nComparison Results:');

        replays.forEach((events, index) => {
            const player = players[index];
            const startTime = events[0]?.time || 0;
            const endTime = events[events.length - 1]?.time || 0;
            const totalTime = (endTime - startTime) / 1000;

            const guessEvent = events.find(e => e.type === 'GuessWithLatLng');
            const guessTime = guessEvent ? (guessEvent.time - startTime) / 1000 : null;

            const mapOpens = events.filter(e => e.type === 'MapDisplay' && e.payload.isActive).length;
            const pinAdjustments = events.filter(e => e.type === 'PinPosition').length;

            console.log(`\nPlayer ${index + 1} (${player.playerId.substring(0, 8)}...):`);
            console.log(`  Total Time: ${totalTime.toFixed(1)}s`);
            console.log(`  Time to Guess: ${guessTime?.toFixed(1) || 'N/A'}s`);
            console.log(`  Map Opens: ${mapOpens}`);
            console.log(`  Pin Adjustments: ${pinAdjustments}`);
            console.log(`  Total Actions: ${events.length}`);
        });

    } catch (error) {
        console.error('Error comparing replays:', error);
    }
}

/**
 * Export replay data as CSV
 * @param {Array} events - Replay events from getDuelReplay
 * @returns {string} CSV formatted string
 */
function exportReplayAsCSV(events) {
    const startTime = events[0]?.time || 0;

    let csv = 'Timestamp,RelativeTime(s),EventType,Data\n';

    events.forEach(event => {
        const relativeTime = ((event.time - startTime) / 1000).toFixed(3);
        const data = JSON.stringify(event.payload).replace(/"/g, '""');
        csv += `${event.time},${relativeTime},${event.type},"${data}"\n`;
    });

    console.log('CSV data generated. Copy the output below:');
    console.log(csv);

    return csv;
}

// ===== USAGE EXAMPLES =====

// Example 1: Basic usage - get replay for a player
console.log('Fetching duel replay...');
getDuelReplay('5b68bcc7f438a60f64005817', '6963ff12ec85cd5824375992', 1)
    .then(events => {
        console.log('\nReplay data retrieved successfully!');
        console.log(`\nUse these functions for more analysis:`);
        console.log(`  analyzePlayerBehavior(events) - Analyze player actions`);
        console.log(`  displayTimeline(events) - Show event timeline`);
        console.log(`  exportReplayAsCSV(events) - Export as CSV`);
    })
    .catch(err => console.error('Failed to fetch replay:', err));

// Example 2: Complete analysis of a player's round
/*
getDuelReplay('5b68bcc7f438a60f64005817', '6963ff12ec85cd5824375992', 1)
    .then(events => {
        analyzePlayerBehavior(events);
        displayTimeline(events, 15);
    });
*/

// Example 3: Compare two players in the same round
/*
comparePlayerReplays([
    {
        playerId: '5b68bcc7f438a60f64005817',
        duelId: '6963ff12ec85cd5824375992',
        roundNumber: 1
    },
    {
        playerId: '62248fc297f88100010c1763',
        duelId: '6963ff12ec85cd5824375992',
        roundNumber: 1
    }
]);
*/

// Example 4: Export replay to CSV for external analysis
/*
getDuelReplay('5b68bcc7f438a60f64005817', '6963ff12ec85cd5824375992', 1)
    .then(events => {
        const csv = exportReplayAsCSV(events);
        // Copy the CSV output and paste into a spreadsheet
    });
*/

// Example 5: Analyze all rounds for a player
/*
async function analyzeAllRounds(playerId, duelId, totalRounds) {
    console.log(`\n=== Analyzing all rounds for player ${playerId.substring(0, 8)}... ===`);

    for (let round = 1; round <= totalRounds; round++) {
        console.log(`\n--- Round ${round} ---`);
        try {
            const events = await getDuelReplay(playerId, duelId, round);
            analyzePlayerBehavior(events);
        } catch (error) {
            console.error(`Error in round ${round}:`, error);
        }
    }
}

// Analyze first 5 rounds
analyzeAllRounds('5b68bcc7f438a60f64005817', '6963ff12ec85cd5824375992', 5);
*/
