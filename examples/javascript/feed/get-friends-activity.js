/**
 * Get Friends Activity Feed
 *
 * Retrieves and displays recent activity from your friends.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com (must be logged in)
 * 2. Paste this code into the console
 * 3. Call: getFriendsActivity()
 */

async function getFriendsActivity(pages = 1) {
    try {
        let allEntries = [];
        let paginationToken = null;

        for (let page = 0; page < pages; page++) {
            const url = paginationToken
                ? `https://www.geoguessr.com/api/v4/feed/friends?paginationToken=${encodeURIComponent(paginationToken)}`
                : 'https://www.geoguessr.com/api/v4/feed/friends';

            const response = await fetch(url, { credentials: 'include' });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            allEntries.push(...data.entries);

            if (!data.paginationToken || page === pages - 1) {
                break;
            }

            paginationToken = data.paginationToken;
        }

        console.log(`\n🌟 Friends Activity Feed (${allEntries.length} activities)\n`);

        // Parse and display activities
        allEntries.slice(0, 20).forEach(entry => {
            const time = new Date(entry.time).toLocaleString();
            const payload = JSON.parse(entry.payload);

            let activityText = '';

            switch (entry.type) {
                case 2: // Standard game
                    activityText = `scored ${payload.points} points on ${payload.mapName}`;
                    break;
                case 6: // Competitive game started
                    activityText = `started a ${payload.competitiveGameMode} game`;
                    break;
                case 9: // Party game
                    activityText = `is playing ${payload.gameMode}`;
                    break;
                case 11: // Competitive game result
                    activityText = `finished a ${payload.competitiveGameMode} game`;
                    break;
                default:
                    activityText = `activity type ${entry.type}`;
            }

            console.log(`[${time}] ${entry.user.nick}: ${activityText}`);
        });

        // Statistics
        const activityTypes = {};
        allEntries.forEach(entry => {
            activityTypes[entry.type] = (activityTypes[entry.type] || 0) + 1;
        });

        console.log(`\n📊 Activity Breakdown:`);
        Object.entries(activityTypes).forEach(([type, count]) => {
            const typeName = {
                '2': 'Standard Games',
                '6': 'Duels Started',
                '9': 'Party Games',
                '11': 'Duels Completed',
                '7': 'Batch Activities'
            }[type] || `Type ${type}`;

            console.log(`${typeName}: ${count}`);
        });

        // Most active friends
        const userActivity = {};
        allEntries.forEach(entry => {
            const nick = entry.user.nick;
            userActivity[nick] = (userActivity[nick] || 0) + 1;
        });

        const topUsers = Object.entries(userActivity)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);

        console.log(`\n🏆 Most Active Friends:`);
        topUsers.forEach(([nick, count], index) => {
            console.log(`${index + 1}. ${nick}: ${count} activities`);
        });

        return allEntries;

    } catch (error) {
        console.error('❌ Error fetching activity:', error.message);
        return null;
    }
}

// Example usage:
// getFriendsActivity();

// Get multiple pages:
// getFriendsActivity(3); // Fetch 3 pages (~90 activities)
