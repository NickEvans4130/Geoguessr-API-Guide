/**
 * Analyze Challenge Performance
 *
 * Compares your score to the leaderboard and shows your ranking.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com (must be logged in)
 * 2. Paste this code into the console
 * 3. Call: analyzePerformance('YOUR_CHALLENGE_TOKEN')
 */

async function analyzePerformance(challengeToken) {
    try {
        // Get your profile
        const profileResponse = await fetch('https://www.geoguessr.com/api/v3/profiles', {
            credentials: 'include'
        });
        const profile = await profileResponse.json();
        const myUserId = profile.user.id;

        // Get leaderboard
        const leaderboardResponse = await fetch(
            `https://www.geoguessr.com/api/v3/results/highscores/${challengeToken}`,
            { credentials: 'include' }
        );
        const data = await leaderboardResponse.json();

        // Find your score
        const myEntry = data.items.find(item => item.game.player.id === myUserId);

        if (!myEntry) {
            console.log('❌ You have not played this challenge yet.');
            return null;
        }

        const myRank = data.items.findIndex(item => item.game.player.id === myUserId) + 1;
        const myScore = parseInt(myEntry.game.player.totalScore.amount);
        const totalPlayers = data.items.length;

        // Calculate statistics
        const scores = data.items.map(item => parseInt(item.game.player.totalScore.amount));
        const topScore = scores[0];
        const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
        const medianScore = scores[Math.floor(scores.length / 2)];

        // Calculate percentile
        const percentile = ((totalPlayers - myRank + 1) / totalPlayers) * 100;

        // Display results
        console.log(`\n📊 Your Performance Analysis\n`);
        console.log(`Your Rank: #${myRank} of ${totalPlayers}`);
        console.log(`Your Score: ${myScore.toLocaleString()}`);
        console.log(`Percentile: Top ${percentile.toFixed(1)}%`);

        console.log(`\n📈 Comparison:`);
        console.log(`Top Score: ${topScore.toLocaleString()} (${topScore - myScore >= 0 ? '+' : ''}${topScore - myScore})`);
        console.log(`Average Score: ${Math.round(avgScore).toLocaleString()} (${Math.round(avgScore) - myScore >= 0 ? '+' : ''}${Math.round(avgScore) - myScore})`);
        console.log(`Median Score: ${medianScore.toLocaleString()} (${medianScore - myScore >= 0 ? '+' : ''}${medianScore - myScore})`);

        // Show nearby players
        console.log(`\n👥 Nearby Players:`);
        const start = Math.max(0, myRank - 3);
        const end = Math.min(totalPlayers, myRank + 2);

        data.items.slice(start, end).forEach((item, index) => {
            const rank = start + index + 1;
            const player = item.game.player;
            const score = parseInt(player.totalScore.amount);
            const indicator = player.id === myUserId ? '👉' : '  ';

            console.log(`${indicator} #${rank} ${player.nick}: ${score.toLocaleString()}`);
        });

        return {
            rank: myRank,
            score: myScore,
            totalPlayers,
            percentile,
            topScore,
            avgScore,
            medianScore
        };

    } catch (error) {
        console.error('❌ Error analyzing performance:', error.message);
        return null;
    }
}

// Example usage:
// analyzePerformance('6G9h2UPctmUmUtaa');
