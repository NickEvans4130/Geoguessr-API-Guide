/**
 * Check Authentication Status
 *
 * Verifies if you're currently authenticated and displays your basic info.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com
 * 2. Paste this code into the console
 * 3. Call: checkAuthStatus()
 */

async function checkAuthStatus() {
    try {
        const response = await fetch('https://www.geoguessr.com/api/v3/profiles', {
            credentials: 'include'
        });

        if (response.status === 401) {
            console.log('❌ Not authenticated');
            console.log('Please log in to GeoGuessr first.');
            return { authenticated: false };
        }

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const profile = await response.json();
        const user = profile.user;

        // Display authentication status
        console.log(`\n✅ Authenticated\n`);
        console.log(`Username: ${user.nick}`);
        console.log(`User ID: ${user.id}`);
        console.log(`Email: ${profile.email}`);
        console.log(`Country: ${user.countryCode.toUpperCase()}`);
        console.log(`Pro User: ${user.isProUser ? '✅ Yes' : '❌ No'}`);
        console.log(`Level: ${user.progress.level}`);
        console.log(`XP: ${user.progress.xp.toLocaleString()}`);

        if (user.competitive) {
            console.log(`\n🏆 Competitive:`);
            console.log(`Rating: ${user.competitive.rating}`);
            console.log(`Division: ${user.competitive.division?.type || 'N/A'}`);
        }

        // Account age
        const created = new Date(user.created);
        const ageInDays = Math.floor((Date.now() - created) / (1000 * 60 * 60 * 24));
        const ageInYears = (ageInDays / 365).toFixed(1);

        console.log(`\n📅 Account Info:`);
        console.log(`Created: ${created.toLocaleDateString()}`);
        console.log(`Age: ${ageInYears} years (${ageInDays} days)`);

        return {
            authenticated: true,
            username: user.nick,
            userId: user.id,
            email: profile.email,
            isProUser: user.isProUser,
            level: user.progress.level
        };

    } catch (error) {
        console.error('❌ Error checking authentication:', error.message);
        return { authenticated: false, error: error.message };
    }
}

// Example usage:
// checkAuthStatus();

// Use in conditional logic:
// async function doSomethingIfAuthenticated() {
//     const auth = await checkAuthStatus();
//     if (auth.authenticated) {
//         console.log('User is logged in, proceed...');
//     } else {
//         console.log('User is not logged in');
//     }
// }

// Check if Pro user:
// async function isProUser() {
//     const auth = await checkAuthStatus();
//     return auth.authenticated && auth.isProUser;
// }

// Get current user ID:
// async function getCurrentUserId() {
//     const auth = await checkAuthStatus();
//     return auth.authenticated ? auth.userId : null;
// }
