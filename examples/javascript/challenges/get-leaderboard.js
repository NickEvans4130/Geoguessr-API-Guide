/**
 * Get Challenge Leaderboard
 *
 * Retrieves and displays the leaderboard for a specific challenge.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com (must be logged in)
 * 2. Paste this code into the console
 * 3. Call: getChallengeLeaderboard('YOUR_CHALLENGE_TOKEN')
 */

async function getChallengeLeaderboard(challengeToken) {
    try {
        const url = `https://www.geoguessr.com/api/v3/results/highscores/${challengeToken}`;

        const response = await fetch(url, {
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        // Extract and format leaderboard
        const leaderboard = data.items.map((item, index) => {
            const player = item.game.player;
            return {
                rank: index + 1,
                username: player.nick,
                score: parseInt(player.totalScore.amount),
                isProUser: player.isProUser,
                countryCode: player.countryCode,
                playedAt: new Date(item.game.created).toLocaleString()
            };
        });

        // Display results
        console.log(`\n🏆 Challenge Leaderboard (${data.items.length} players)\n`);
        console.table(leaderboard);

        // Additional stats
        const totalPlayers = data.items.length;
        const avgScore = leaderboard.reduce((sum, p) => sum + p.score, 0) / totalPlayers;
        const topScore = leaderboard[0]?.score || 0;

        console.log(`\n📊 Statistics:`);
        console.log(`Total Players: ${totalPlayers}`);
        console.log(`Average Score: ${Math.round(avgScore)}`);
        console.log(`Top Score: ${topScore}`);
        console.log(`Winner: ${leaderboard[0]?.username}`);

        return leaderboard;

    } catch (error) {
        console.error('❌ Error fetching leaderboard:', error.message);
        return null;
    }
}

// Example usage:
// getChallengeLeaderboard('6G9h2UPctmUmUtaa');

// Extract token from URL:
// const url = "https://www.geoguessr.com/challenge/6G9h2UPctmUmUtaa";
// const token = url.split('/').pop();
// getChallengeLeaderboard(token);
