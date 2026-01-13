/**
 * Search Users
 *
 * Searches for GeoGuessr users by username.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com (must be logged in)
 * 2. Paste this code into the console
 * 3. Call: searchUsers('username')
 */

async function searchUsers(query) {
    try {
        if (!query || query.trim().length === 0) {
            console.log('❌ Search query cannot be empty');
            return null;
        }

        const url = `https://www.geoguessr.com/api/v3/search/user?q=${encodeURIComponent(query)}`;

        const response = await fetch(url, {
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const results = await response.json();

        if (results.length === 0) {
            console.log(`❌ No users found matching "${query}"`);
            return [];
        }

        // Display results
        console.log(`\n🔍 Search Results for "${query}" (${results.length} users found)\n`);

        const tableData = results.map(user => ({
            Username: user.nick,
            Level: user.progress?.level || 'N/A',
            Country: user.countryCode?.toUpperCase() || 'N/A',
            Pro: user.isProUser ? '✅' : '❌',
            Verified: user.isVerified ? '✅' : '❌',
            ID: user.id
        }));

        console.table(tableData);

        // Show clickable profile links
        console.log(`\n🔗 Profile Links:`);
        results.forEach(user => {
            console.log(`${user.nick}: https://www.geoguessr.com/user/${user.id}`);
        });

        return results;

    } catch (error) {
        console.error('❌ Error searching users:', error.message);
        return null;
    }
}

// Example usage:
// searchUsers('brbw');

// Search and get first result's ID:
// const results = await searchUsers('username');
// const firstUserId = results[0]?.id;
