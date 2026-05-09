/**
 * Get Challenge Information
 *
 * Retrieves detailed information about a challenge including map, settings, and creator.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com (must be logged in)
 * 2. Paste this code into the console
 * 3. Call: getChallengeInfo('YOUR_CHALLENGE_TOKEN')
 */

async function getChallengeInfo(challengeToken) {
    try {
        const url = `https://www.geoguessr.com/api/v3/challenges/${challengeToken}`;

        const response = await fetch(url, {
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const challenge = await response.json();

        // Display formatted challenge information
        console.log(`\n🎮 Challenge Information\n`);
        console.log(`Map: ${challenge.map.name}`);
        console.log(`Creator: ${challenge.creator.nick} (${challenge.creator.countryCode})`);
        console.log(`Created: ${new Date(challenge.created).toLocaleString()}`);
        console.log(`\n⚙️  Settings:`);
        console.log(`- Rounds: ${challenge.roundCount}`);
        console.log(`- Time Limit: ${challenge.timeLimit === 0 ? 'None' : challenge.timeLimit + 's'}`);
        console.log(`- Movement: ${challenge.forbidMoving ? '❌ Disabled' : '✅ Enabled'}`);
        console.log(`- Panning: ${challenge.forbidRotating ? '❌ Disabled' : '✅ Enabled'}`);
        console.log(`- Zooming: ${challenge.forbidZooming ? '❌ Disabled' : '✅ Enabled'}`);

        console.log(`\n📍 Map Details:`);
        console.log(`- Type: ${challenge.map.name}`);
        console.log(`- Description: ${challenge.map.description || 'N/A'}`);
        console.log(`- Locations: ${challenge.map.coordinateCount || 'Unknown'}`);

        // Return full challenge object
        return challenge;

    } catch (error) {
        console.error('❌ Error fetching challenge info:', error.message);
        return null;
    }
}

// Example usage:
// getChallengeInfo('6G9h2UPctmUmUtaa');

// Get info for current page challenge:
// const currentToken = window.location.pathname.split('/').pop();
// getChallengeInfo(currentToken);
