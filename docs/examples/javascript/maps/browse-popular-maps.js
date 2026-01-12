/**
 * Browse Popular Maps
 *
 * Retrieves and displays popular GeoGuessr maps.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com
 * 2. Paste this code into the console
 * 3. Call: browsePopularMaps()
 */

async function browsePopularMaps() {
    try {
        const response = await fetch('https://www.geoguessr.com/api/v3/maps/browse/popular');

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const maps = await response.json();

        console.log(`\n🗺️  Popular Maps (${maps.length} maps)\n`);

        // Display maps
        maps.forEach((map, index) => {
            console.log(`${index + 1}. ${map.name}`);
            console.log(`   Created by: ${map.creator.nick} (${map.creator.countryCode?.toUpperCase() || 'N/A'})`);
            console.log(`   Locations: ${map.coordinateCount}`);
            console.log(`   Difficulty: ${map.difficulty || 'N/A'} (Level ${map.difficultyLevel || 'N/A'})`);
            if (map.description) {
                console.log(`   Description: ${map.description.substring(0, 80)}${map.description.length > 80 ? '...' : ''}`);
            }
            console.log(`   Likes: ${map.likes || 0}`);
            console.log(`   Link: https://www.geoguessr.com/maps/${map.id}`);
            console.log('');
        });

        // Statistics
        const avgLikes = maps.reduce((sum, map) => sum + (map.likes || 0), 0) / maps.length;
        const difficulties = maps.reduce((acc, map) => {
            const diff = map.difficulty || 'Unknown';
            acc[diff] = (acc[diff] || 0) + 1;
            return acc;
        }, {});

        console.log(`\n📊 Statistics:`);
        console.log(`Total Maps: ${maps.length}`);
        console.log(`Average Likes: ${avgLikes.toFixed(1)}`);
        console.log(`\nDifficulties:`);
        Object.entries(difficulties).forEach(([diff, count]) => {
            console.log(`  ${diff}: ${count}`);
        });

        // Top creators
        const creators = {};
        maps.forEach(map => {
            const creator = map.creator.nick;
            creators[creator] = (creators[creator] || 0) + 1;
        });

        console.log(`\n👤 Top Creators:`);
        Object.entries(creators)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .forEach(([creator, count]) => {
                console.log(`  ${creator}: ${count} maps`);
            });

        return maps;

    } catch (error) {
        console.error('❌ Error fetching maps:', error.message);
        return null;
    }
}

// Example usage:
// browsePopularMaps();

// Also available:
// - /api/v3/maps/browse/featured - Featured maps
// - /api/v3/maps/browse/new - New maps
// - /api/v3/maps/browse/hot - Hot/trending maps
