/**
 * Compare Subscription Plans
 *
 * Retrieves and compares all available GeoGuessr subscription plans.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com
 * 2. Paste this code into the console
 * 3. Call: comparePlans()
 *
 * Note: This endpoint does NOT require authentication
 */

async function comparePlans() {
    try {
        // No authentication required for this endpoint
        const response = await fetch('https://www.geoguessr.com/api/v3/subscriptions/plans');

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const plans = await response.json();

        console.log(`\n💳 Available Subscription Plans (${plans.length} plans)\n`);

        // Group by currency
        const byCurrency = {};
        plans.forEach(plan => {
            if (!byCurrency[plan.currency]) {
                byCurrency[plan.currency] = [];
            }
            byCurrency[plan.currency].push(plan);
        });

        // Display by currency
        Object.entries(byCurrency).forEach(([currency, currencyPlans]) => {
            console.log(`\n💰 ${currency} Plans:\n`);

            const tableData = currencyPlans.map(plan => ({
                'Billing': plan.interval === 1 ? 'Monthly' : 'Yearly',
                'Product': getProductName(plan.product),
                'Total Price': `${currency} ${plan.price}`,
                'Per Month': `${currency} ${plan.pricePerMonth}`,
                'Savings': plan.interval === 2 ? calculateSavings(plan, currencyPlans) : '-'
            }));

            console.table(tableData);
        });

        // Find best value
        console.log(`\n🏆 Best Value Analysis:\n`);

        const yearlyPlans = plans.filter(p => p.interval === 2);
        if (yearlyPlans.length > 0) {
            const bestValue = yearlyPlans.reduce((best, plan) => {
                return plan.pricePerMonth < best.pricePerMonth ? plan : best;
            });

            console.log(`Best value: ${getProductName(bestValue.product)} Yearly`);
            console.log(`Price: ${bestValue.currency} ${bestValue.price}/year (${bestValue.currency} ${bestValue.pricePerMonth}/month)`);
        }

        // Monthly vs Yearly comparison
        console.log(`\n📊 Monthly vs Yearly Savings:\n`);
        const monthlyPlans = plans.filter(p => p.interval === 1);

        monthlyPlans.forEach(monthly => {
            const yearly = plans.find(p =>
                p.interval === 2 &&
                p.currency === monthly.currency &&
                p.product === monthly.product
            );

            if (yearly) {
                const monthlyCostOfYearly = yearly.price / 12;
                const savings = ((monthly.price * 12) - yearly.price).toFixed(2);
                const savingsPercent = ((savings / (monthly.price * 12)) * 100).toFixed(0);

                console.log(`${monthly.currency} ${getProductName(monthly.product)}:`);
                console.log(`  Monthly: ${monthly.currency} ${monthly.price}/month × 12 = ${monthly.currency} ${(monthly.price * 12).toFixed(2)}`);
                console.log(`  Yearly:  ${yearly.currency} ${yearly.price}/year (${yearly.currency} ${monthlyCostOfYearly.toFixed(2)}/month)`);
                console.log(`  💰 Save: ${yearly.currency} ${savings}/year (${savingsPercent}% savings)\n`);
            }
        });

        return plans;

    } catch (error) {
        console.error('❌ Error fetching plans:', error.message);
        return null;
    }
}

// Helper function to get product name
function getProductName(productId) {
    const products = {
        2: 'Pro',
        3: 'Unlimited',
        4: 'Premium',
        5: 'Team'
    };
    return products[productId] || `Product ${productId}`;
}

// Helper function to calculate savings
function calculateSavings(yearlyPlan, allPlans) {
    const monthly = allPlans.find(p =>
        p.interval === 1 &&
        p.currency === yearlyPlan.currency &&
        p.product === yearlyPlan.product
    );

    if (monthly) {
        const savings = ((monthly.price * 12) - yearlyPlan.price).toFixed(2);
        return `${yearlyPlan.currency} ${savings}`;
    }
    return '-';
}

// Example usage:
// comparePlans();

// Get cheapest plan:
// async function getCheapestPlan() {
//     const plans = await fetch('https://www.geoguessr.com/api/v3/subscriptions/plans').then(r => r.json());
//     return plans.reduce((cheapest, plan) => {
//         return plan.pricePerMonth < cheapest.pricePerMonth ? plan : cheapest;
//     });
// }

// Filter plans by currency:
// async function getPlansByCurrency(currency) {
//     const plans = await fetch('https://www.geoguessr.com/api/v3/subscriptions/plans').then(r => r.json());
//     return plans.filter(p => p.currency === currency);
// }

// Get only yearly plans:
// async function getYearlyPlans() {
//     const plans = await fetch('https://www.geoguessr.com/api/v3/subscriptions/plans').then(r => r.json());
//     return plans.filter(p => p.interval === 2);
// }
