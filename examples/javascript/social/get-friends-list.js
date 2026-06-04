/**
 * Get Friends List
 *
 * Retrieves and displays your complete friends list.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com (must be logged in)
 * 2. Paste this code into the console
 * 3. Call: getFriendsList()
 */

async function getFriendsList() {
    try {
        const response = await fetch('https://www.geoguessr.com/api/v3/social/friends', {
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const friends = await response.json();

        if (friends.length === 0) {
            console.log('You have no friends yet. Add some friends to see them here!');
            return [];
        }

        // Display friends list
        console.log(`\n👥 Your Friends (${friends.length} total)\n`);

        const tableData = friends.map(friend => ({
            Username: friend.nick,
            Level: friend.progress?.level || 'N/A',
            Country: friend.countryCode?.toUpperCase() || 'N/A',
            Pro: friend.isProUser ? '✅' : '❌',
            Online: friend.isOnline ? '🟢' : '⚪',
            ID: friend.userId
        }));

        console.table(tableData);

        // Statistics
        const onlineFriends = friends.filter(f => f.isOnline).length;
        const proFriends = friends.filter(f => f.isProUser).length;
        const avgLevel = friends
            .filter(f => f.progress?.level)
            .reduce((sum, f) => sum + f.progress.level, 0) / friends.length;

        console.log(`\n📊 Statistics:`);
        console.log(`Total Friends: ${friends.length}`);
        console.log(`Online Now: ${onlineFriends}`);
        console.log(`Pro Users: ${proFriends} (${((proFriends / friends.length) * 100).toFixed(1)}%)`);
        console.log(`Average Level: ${avgLevel.toFixed(1)}`);

        // Group by country
        const countries = {};
        friends.forEach(f => {
            if (f.countryCode) {
                countries[f.countryCode] = (countries[f.countryCode] || 0) + 1;
            }
        });

        console.log(`\n🌍 Countries Represented:`);
        Object.entries(countries)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .forEach(([code, count]) => {
                console.log(`${code.toUpperCase()}: ${count}`);
            });

        return friends;

    } catch (error) {
        console.error('❌ Error fetching friends:', error.message);
        return null;
    }
}

// Example usage:
// getFriendsList();

// Find a specific friend:
// const friends = await getFriendsList();
// const friend = friends.find(f => f.nick === 'username');
