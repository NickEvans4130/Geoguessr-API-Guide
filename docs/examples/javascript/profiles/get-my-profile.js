/**
 * Get My Profile
 *
 * Retrieves and displays your own GeoGuessr profile information.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com (must be logged in)
 * 2. Paste this code into the console
 * 3. Call: getMyProfile()
 */

async function getMyProfile() {
    try {
        const response = await fetch('https://www.geoguessr.com/api/v3/profiles', {
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const profile = await response.json();
        const user = profile.user;

        // Display profile information
        console.log(`\n👤 Your Profile\n`);
        console.log(`Username: ${user.nick}`);
        console.log(`User ID: ${user.id}`);
        console.log(`Country: ${user.countryCode.toUpperCase()}`);
        console.log(`Created: ${new Date(user.created).toLocaleDateString()}`);
        console.log(`Pro User: ${user.isProUser ? '✅ Yes' : '❌ No'}`);
        console.log(`Verified: ${user.isVerified ? '✅ Yes' : '❌ No'}`);

        console.log(`\n📊 Progress:`);
        console.log(`Level: ${user.progress.level}`);
        console.log(`XP: ${user.progress.xp.toLocaleString()}`);
        console.log(`Next Level: ${user.progress.nextLevel} (${user.progress.nextLevelXp.toLocaleString()} XP)`);
        const xpToNext = user.progress.nextLevelXp - user.progress.xp;
        console.log(`XP to Next Level: ${xpToNext.toLocaleString()}`);

        if (user.competitive) {
            console.log(`\n🏆 Competitive:`);
            console.log(`Rating: ${user.competitive.rating}`);
            console.log(`Division: ${user.competitive.division?.type || 'N/A'}`);
            console.log(`On Leaderboard: ${user.competitive.onLeaderboard ? '✅ Yes' : '❌ No'}`);
        }

        console.log(`\n🌍 Achievements:`);
        if (user.streakProgress) {
            const streak = user.streakProgress;
            console.log(`Streak Badges: Bronze ${streak.bronze}, Silver ${streak.silver}, Gold ${streak.gold}, Platinum ${streak.platinum}`);
        }
        if (user.explorerProgress) {
            const explorer = user.explorerProgress;
            console.log(`Explorer Badges: Bronze ${explorer.bronze}, Silver ${explorer.silver}, Gold ${explorer.gold}, Platinum ${explorer.platinum}`);
        }

        return profile;

    } catch (error) {
        console.error('❌ Error fetching profile:', error.message);
        return null;
    }
}

// Example usage:
// getMyProfile();
