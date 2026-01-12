/**
 * Search Maps
 *
 * Search for GeoGuessr maps by name or keywords.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com
 * 2. Paste this code into the console
 * 3. Call: searchMaps('keyword')
 *
 * Note: This endpoint does NOT require authentication
 */

async function searchMaps(query) {
    try {
        if (!query || query.trim().length === 0) {
            console.log('❌ Search query cannot be empty');
            return null;
        }

        const url = `https://www.geoguessr.com/api/v3/search/map?q=${encodeURIComponent(query)}`;

        // Note: No authentication required for searching maps
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const maps = await response.json();

        if (maps.length === 0) {
            console.log(`❌ No maps found matching "${query}"`);
            return [];
        }

        // Display results
        console.log(`\n🔍 Search Results for "${query}" (${maps.length} maps found)\n`);

        const tableData = maps.map(map => ({
            Name: map.name,
            Creator: map.creator.nick,
            Locations: map.coordinateCount || 'Unknown',
            Difficulty: map.difficulty || 'N/A',
            Likes: map.likes || 0
        }));

        console.table(tableData);

        // Show map links
        console.log(`\n🔗 Map Links:`);
        maps.slice(0, 10).forEach(map => {
            console.log(`${map.name}: https://www.geoguessr.com/maps/${map.id}`);
        });

        // Difficulty distribution
        const difficulties = {};
        maps.forEach(map => {
            const diff = map.difficulty || 'Unknown';
            difficulties[diff] = (difficulties[diff] || 0) + 1;
        });

        console.log(`\n📊 Difficulty Distribution:`);
        Object.entries(difficulties)
            .sort((a, b) => b[1] - a[1])
            .forEach(([diff, count]) => {
                console.log(`  ${diff}: ${count}`);
            });

        // Top creators in results
        const creators = {};
        maps.forEach(map => {
            const creator = map.creator.nick;
            creators[creator] = (creators[creator] || 0) + 1;
        });

        const topCreators = Object.entries(creators)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);

        if (topCreators.length > 0) {
            console.log(`\n👤 Top Creators in Results:`);
            topCreators.forEach(([creator, count]) => {
                console.log(`  ${creator}: ${count} maps`);
            });
        }

        return maps;

    } catch (error) {
        console.error('❌ Error searching maps:', error.message);
        return null;
    }
}

// Example usage:
// searchMaps('famous places');
// searchMaps('europe');
// searchMaps('hard');

// Get popular maps and then search for similar:
// const popular = await fetch('https://www.geoguessr.com/api/v3/maps/browse/popular').then(r => r.json());
// const firstMapName = popular[0].name;
// searchMaps(firstMapName);
