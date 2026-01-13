/**
 * Compare Users
 *
 * Compares statistics between two GeoGuessr users.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com (must be logged in)
 * 2. Paste this code into the console
 * 3. Call: compareUsers('username1', 'username2')
 */

async function compareUsers(username1, username2) {
    try {
        // Search for both users
        const search1 = await fetch(
            `https://www.geoguessr.com/api/v3/search/user?q=${encodeURIComponent(username1)}`,
            { credentials: 'include' }
        );
        const search2 = await fetch(
            `https://www.geoguessr.com/api/v3/search/user?q=${encodeURIComponent(username2)}`,
            { credentials: 'include' }
        );

        const results1 = await search1.json();
        const results2 = await search2.json();

        if (results1.length === 0) {
            console.log(`❌ User "${username1}" not found`);
            return null;
        }
        if (results2.length === 0) {
            console.log(`❌ User "${username2}" not found`);
            return null;
        }

        const user1 = results1[0];
        const user2 = results2[0];

        // Display comparison
        console.log(`\n⚔️  User Comparison\n`);

        const comparison = [
            {
                Stat: 'Username',
                [user1.nick]: user1.nick,
                [user2.nick]: user2.nick
            },
            {
                Stat: 'Level',
                [user1.nick]: user1.progress?.level || 'N/A',
                [user2.nick]: user2.progress?.level || 'N/A'
            },
            {
                Stat: 'XP',
                [user1.nick]: user1.progress?.xp?.toLocaleString() || 'N/A',
                [user2.nick]: user2.progress?.xp?.toLocaleString() || 'N/A'
            },
            {
                Stat: 'Rating',
                [user1.nick]: user1.competitive?.rating || 'N/A',
                [user2.nick]: user2.competitive?.rating || 'N/A'
            },
            {
                Stat: 'Country',
                [user1.nick]: user1.countryCode?.toUpperCase() || 'N/A',
                [user2.nick]: user2.countryCode?.toUpperCase() || 'N/A'
            },
            {
                Stat: 'Pro User',
                [user1.nick]: user1.isProUser ? '✅' : '❌',
                [user2.nick]: user2.isProUser ? '✅' : '❌'
            },
            {
                Stat: 'Verified',
                [user1.nick]: user1.isVerified ? '✅' : '❌',
                [user2.nick]: user2.isVerified ? '✅' : '❌'
            }
        ];

        console.table(comparison);

        // Determine who's ahead in different categories
        console.log(`\n📊 Head-to-Head:\n`);

        if (user1.progress && user2.progress) {
            const levelDiff = user1.progress.level - user2.progress.level;
            if (levelDiff > 0) {
                console.log(`🏆 ${user1.nick} is ${levelDiff} levels ahead`);
            } else if (levelDiff < 0) {
                console.log(`🏆 ${user2.nick} is ${Math.abs(levelDiff)} levels ahead`);
            } else {
                console.log(`🤝 Same level!`);
            }

            const xpDiff = user1.progress.xp - user2.progress.xp;
            if (xpDiff !== 0) {
                const leader = xpDiff > 0 ? user1.nick : user2.nick;
                console.log(`📈 ${leader} has ${Math.abs(xpDiff).toLocaleString()} more XP`);
            }
        }

        if (user1.competitive && user2.competitive) {
            const ratingDiff = user1.competitive.rating - user2.competitive.rating;
            if (ratingDiff !== 0) {
                const leader = ratingDiff > 0 ? user1.nick : user2.nick;
                console.log(`⭐ ${leader} has ${Math.abs(ratingDiff)} higher rating`);
            }
        }

        return { user1, user2 };

    } catch (error) {
        console.error('❌ Error comparing users:', error.message);
        return null;
    }
}

// Example usage:
// compareUsers('user1', 'user2');

// Compare yourself to another user:
// const myProfile = await fetch('https://www.geoguessr.com/api/v3/profiles', {credentials: 'include'}).then(r => r.json());
// compareUsers(myProfile.user.nick, 'other_user');
