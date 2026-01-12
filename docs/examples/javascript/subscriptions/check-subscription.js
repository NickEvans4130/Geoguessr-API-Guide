/**
 * Check Subscription Status
 *
 * Retrieves and displays your current GeoGuessr subscription information.
 *
 * Usage in browser console:
 * 1. Navigate to geoguessr.com (must be logged in)
 * 2. Paste this code into the console
 * 3. Call: checkSubscription()
 */

async function checkSubscription() {
    try {
        const response = await fetch('https://www.geoguessr.com/api/v3/subscriptions', {
            credentials: 'include'
        });

        if (!response.ok) {
            if (response.status === 404) {
                console.log('❌ No active subscription found.');
                return null;
            }
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const subscription = await response.json();

        // Display subscription information
        console.log(`\n💳 Subscription Status\n`);

        if (subscription.isActive) {
            console.log(`✅ Active Subscription`);
        } else {
            console.log(`❌ Inactive Subscription`);
        }

        console.log(`\n📋 Plan Details:`);
        console.log(`Plan: ${subscription.plan}`);
        console.log(`Cost: ${subscription.currency} ${subscription.cost}`);
        console.log(`Billing: ${subscription.interval === 1 ? 'Monthly' : 'Yearly'}`);

        console.log(`\n📅 Dates:`);
        console.log(`Started: ${new Date(subscription.startedAt).toLocaleDateString()}`);
        console.log(`Renews: ${new Date(subscription.periodEndingAt).toLocaleDateString()}`);

        if (subscription.isInTrialPeriod) {
            console.log(`Trial: ✅ In trial period (ends ${new Date(subscription.trialEndingAt).toLocaleDateString()})`);
        }

        if (subscription.canceled) {
            console.log(`\n⚠️  Subscription is canceled (access until ${new Date(subscription.periodEndingAt).toLocaleDateString()})`);
        }

        // Calculate time remaining
        const now = new Date();
        const endDate = new Date(subscription.periodEndingAt);
        const daysRemaining = Math.ceil((endDate - now) / (1000 * 60 * 60 * 24));

        console.log(`\n⏰ Time Remaining:`);
        if (daysRemaining > 0) {
            console.log(`${daysRemaining} days until renewal`);
        } else {
            console.log(`Expired ${Math.abs(daysRemaining)} days ago`);
        }

        // Calculate value
        const monthlyValue = subscription.interval === 2
            ? (subscription.cost / 12).toFixed(2)
            : subscription.cost;

        console.log(`\n💰 Value:`);
        console.log(`Effective monthly cost: ${subscription.currency} ${monthlyValue}`);

        // Additional info
        console.log(`\n🔍 Additional Info:`);
        console.log(`Subscription ID: ${subscription.id}`);
        console.log(`Plan ID: ${subscription.planId}`);
        console.log(`Payment Provider: ${subscription.payProvider}`);

        return subscription;

    } catch (error) {
        console.error('❌ Error checking subscription:', error.message);
        return null;
    }
}

// Example usage:
// checkSubscription();

// Check if user has Pro features:
// async function hasProFeatures() {
//     const sub = await checkSubscription();
//     return sub && sub.isActive;
// }

// Get subscription end date:
// async function getSubscriptionEndDate() {
//     const sub = await checkSubscription();
//     return sub ? new Date(sub.periodEndingAt) : null;
// }

// Check if in trial:
// async function isInTrial() {
//     const sub = await checkSubscription();
//     return sub && sub.isInTrialPeriod;
// }
