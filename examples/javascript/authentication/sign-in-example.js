/**
 * Sign In Example
 *
 * Demonstrates how to sign in to GeoGuessr programmatically.
 *
 * ⚠️  IMPORTANT WARNINGS:
 * 1. This is for EDUCATIONAL purposes only
 * 2. Programmatic login may violate GeoGuessr's Terms of Service
 * 3. May not work in browser due to CORS restrictions
 * 4. Use environment-specific authentication methods instead
 * 5. Never hardcode credentials in your code
 *
 * Usage in browser console (if allowed):
 * 1. Navigate to geoguessr.com
 * 2. Paste this code into the console
 * 3. Call: signIn('email@example.com', 'password')
 *
 * Note: This may only work in same-origin contexts or with proper CORS headers
 */

async function signIn(email, password) {
    try {
        const url = 'https://www.geoguessr.com/api/v3/accounts/signin';

        const response = await fetch(url, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        if (!response.ok) {
            if (response.status === 401) {
                console.log('❌ Invalid email or password');
                return null;
            }
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const user = await response.json();

        // Display success
        console.log(`\n✅ Sign In Successful!\n`);
        console.log(`Welcome, ${user.nick}!`);
        console.log(`Level: ${user.progress.level}`);
        console.log(`XP: ${user.progress.xp.toLocaleString()}`);
        console.log(`Pro User: ${user.isProUser ? '✅ Yes' : '❌ No'}`);

        console.log(`\n🔐 Authentication Cookies Set:`);
        console.log(`- _ncfa (HttpOnly) - Main session cookie`);
        console.log(`- session - Session identifier`);
        console.log(`- devicetoken - Device tracking`);

        console.log(`\n💡 You can now make authenticated requests using credentials: 'include'`);

        return user;

    } catch (error) {
        console.error('❌ Sign in failed:', error.message);
        return null;
    }
}

// ⚠️  DO NOT USE THESE PATTERNS IN PRODUCTION:

// Bad example - hardcoded credentials:
// signIn('user@example.com', 'password123');

// Better example - use environment variables (Node.js):
// const email = process.env.GEOGUESSR_EMAIL;
// const password = process.env.GEOGUESSR_PASSWORD;
// signIn(email, password);

// Best practice - use proper OAuth flows or session management instead

/**
 * Check if sign in was successful
 */
async function verifySignIn() {
    try {
        const response = await fetch('https://www.geoguessr.com/api/v3/profiles', {
            credentials: 'include'
        });

        if (response.ok) {
            const profile = await response.json();
            console.log(`✅ Verified: Signed in as ${profile.user.nick}`);
            return true;
        } else {
            console.log('❌ Not signed in');
            return false;
        }
    } catch (error) {
        console.error('Error verifying sign in:', error);
        return false;
    }
}

// Example usage flow:
// async function authenticateAndVerify() {
//     const user = await signIn(email, password);
//     if (user) {
//         await verifySignIn();
//     }
// }

/**
 * Security Best Practices:
 *
 * 1. Never commit credentials to version control
 * 2. Use environment variables for sensitive data
 * 3. Implement rate limiting to prevent brute force
 * 4. Use HTTPS only
 * 5. Store passwords securely (hashed, salted)
 * 6. Implement proper session management
 * 7. Add 2FA when possible
 * 8. Rotate credentials regularly
 * 9. Monitor for suspicious login attempts
 * 10. Follow GeoGuessr's Terms of Service
 */
