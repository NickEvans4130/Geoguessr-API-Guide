# Subscriptions API

Endpoints for managing GeoGuessr Pro subscriptions and plans.

## Table of Contents

- [Overview](#overview)
- [Endpoints](#endpoints)
- [Implementation Examples](#implementation-examples)

## Overview

GeoGuessr offers Pro subscriptions with additional features. These endpoints allow checking subscription status, available plans, and payment methods.

**🚀 Ready to use?** Check out the [subscriptions examples](../examples/javascript/subscriptions/) for ready-to-use scripts:
- [Check Subscription](../examples/javascript/subscriptions/check-subscription.js) - View your subscription status and billing
- [Compare Plans](../examples/javascript/subscriptions/compare-plans.js) - Compare all available plans and find best value

## Endpoints

### Get Subscription Status

Get the current user's subscription information including plan details, billing dates, and status.

**Endpoint:**
```
GET /v3/subscriptions
```

**Authentication:** Required

**Response:** Subscription object with 21 fields

**Example Response:**
```json
{
  "id": "sub_01kats6ms4h08eaqyvw7tabp23",
  "type": 0,
  "payProvider": 6,
  "created": "2021-07-10T13:07:49.0000000Z",
  "plan": "GeoGuessr Unlimited Yearly",
  "planId": "pri_01jwb1q8brvfyr398bzsqxnh7e",
  "cost": 35.88,
  "currency": "USD",
  "started": "2021-07-10",
  "startedAt": "2021-07-10T13:07:49.0000000Z",
  "trialEnd": "2021-07-20",
  "trialEndingAt": "2021-07-20T13:07:51.0000000Z",
  "periodEndsAt": "2026-07-20",
  "periodEndingAt": "2026-07-20T06:12:56.0000000Z",
  "canceled": false,
  "interval": 2,
  "memberLimit": 0,
  "product": 3,
  "isActive": true,
  "isInTrialPeriod": false,
  "isReferralReceiver": false
}
```

**Important Notes:**
- Use `isActive` field to determine if user has Pro features
- `plan` contains human-readable plan name
- `planId` is the plan identifier for API calls
- `periodEndingAt` shows when subscription renews
- `interval`: 1 = monthly, 2 = yearly

---

### Get Subscription Plans

Returns array of all available subscription plans with pricing information. Returns 14 plans covering different subscription types and billing periods.

**Endpoint:**
```
GET /v3/subscriptions/plans
```

**Authentication:** Not required

**Response:** Array of 14 plan objects

**Example Response:**
```json
[
  {
    "id": "832300",
    "type": 0,
    "interval": 1,
    "trialDays": 0,
    "members": 0,
    "product": 2,
    "currency": "GBP",
    "price": 3.19,
    "pricePerMonth": 3.19,
    "discount": null,
    "payProvider": 5,
    "checkoutUrl": null
  },
  {
    "id": "pri_01jwb1q8brvfyr398bzsqxnh7e",
    "type": 0,
    "interval": 2,
    "trialDays": 0,
    "members": 0,
    "product": 3,
    "currency": "USD",
    "price": 35.88,
    "pricePerMonth": 2.99,
    "discount": null,
    "payProvider": 6,
    "checkoutUrl": null
  }
]
```

**Plan Object Fields:**
- `id` - Plan identifier (used in subscriptions)
- `type` - Plan type (0 = standard)
- `interval` - Billing interval (1 = monthly, 2 = yearly)
- `trialDays` - Number of trial days
- `members` - Member limit (0 = no limit)
- `product` - Product tier (2 = Pro, 3 = Unlimited, etc.)
- `currency` - Currency code (USD, GBP, EUR, etc.)
- `price` - Total price for billing period
- `pricePerMonth` - Effective monthly cost
- `discount` - Discount information (may be null)
- `payProvider` - Payment provider ID
- `checkoutUrl` - Checkout URL (may be null)

**Important Notes:**
- No authentication required - can be called anonymously
- Returns 14 plans covering different subscription tiers
- Use `interval` to distinguish monthly vs yearly plans
- `pricePerMonth` is pre-calculated for comparison

---

### Get Subscription Invoices

Returns billing history and invoices for the authenticated user.

**Endpoint:**
```
GET /v3/subscriptions/invoices
```

**Authentication:** Required

**Response:** Array of invoice objects

**Example Response:**
```json
[
  {
    "id": "40996693-116711856",
    "date": "01/01/0001",
    "total": "3.99",
    "paid": true,
    "invoiceUrl": "https://my.paddle.com/receipt/..."
  }
]
```

**Invoice Object Fields:**
- `id` - Invoice identifier
- `date` - Invoice date
- `total` - Total amount charged
- `paid` - Payment status
- `invoiceUrl` - URL to view/download invoice

---

### Google Play Subscriptions

Manage subscriptions through Google Play Store.

**Endpoint:**
```
POST /v3/subscriptions/google
```

**Authentication:** Required

**Status:** Returns 405 Method Not Allowed on GET (requires POST)

**Request Body:** (Structure needs verification)
Likely contains Google Play purchase token or receipt.

**Expected Response:** (Structure needs verification)

**Note:** This endpoint is primarily used by the Android app for subscription verification.

---

## Data Structures

### Subscription Object

Complete subscription object with all 21 fields:

```typescript
interface Subscription {
  id: string;                  // Subscription ID
  type: number;                // Subscription type
  payProvider: number;         // Payment provider ID (5 = Paddle, 6 = Stripe, etc.)
  created: string;             // Creation timestamp (ISO 8601)
  plan: string;                // Human-readable plan name
  planId: string;              // Plan identifier for API calls
  cost: number;                // Total cost for billing period
  currency: string;            // Currency code (USD, GBP, EUR, etc.)
  started: string;             // Start date (YYYY-MM-DD)
  startedAt: string;           // Start timestamp (ISO 8601)
  trialEnd: string;            // Trial end date (YYYY-MM-DD)
  trialEndingAt: string;       // Trial end timestamp (ISO 8601)
  periodEndsAt: string;        // Period end date (YYYY-MM-DD)
  periodEndingAt: string;      // Period end timestamp (ISO 8601)
  canceled: boolean;           // Whether subscription is canceled
  interval: number;            // Billing interval (1 = monthly, 2 = yearly)
  memberLimit: number;         // Member limit (0 = no limit)
  product: number;             // Product tier (2 = Pro, 3 = Unlimited, etc.)
  isActive: boolean;           // Whether subscription is active (USE THIS FOR PRO STATUS)
  isInTrialPeriod: boolean;    // Whether currently in trial period
  isReferralReceiver: boolean; // Whether subscription is from referral
}
```

**Key Fields for Pro Status:**
- `isActive` - Primary field to check if user has Pro access
- `canceled` - If true, subscription won't renew
- `periodEndingAt` - When current period ends

---

### Plan Object

Complete plan object structure:

```typescript
interface Plan {
  id: string;                  // Plan identifier (use in subscription calls)
  type: number;                // Plan type (0 = standard)
  interval: number;            // Billing interval (1 = monthly, 2 = yearly)
  trialDays: number;           // Number of trial days
  members: number;             // Member limit (0 = no limit)
  product: number;             // Product tier (2 = Pro, 3 = Unlimited, etc.)
  currency: string;            // Currency code (USD, GBP, EUR, etc.)
  price: number;               // Total price for billing period
  pricePerMonth: number;       // Effective monthly cost
  discount: any | null;        // Discount information
  payProvider: number;         // Payment provider ID
  checkoutUrl: string | null;  // Checkout URL (may be null)
}
```

---

### Invoice Object

```typescript
interface Invoice {
  id: string;                  // Invoice identifier
  date: string;                // Invoice date
  total: string;               // Total amount (as string)
  paid: boolean;               // Payment status
  invoiceUrl: string;          // URL to view/download invoice
}
```

---

## Implementation Examples

### Example 1: Check Subscription Status

**JavaScript:**
```javascript
async function checkSubscription() {
    const response = await fetch('https://www.geoguessr.com/api/v3/subscriptions', {
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const subscription = await response.json();

    if (subscription.isActive) {
        console.log('✅ Pro User');
        console.log(`Plan: ${subscription.plan}`);
        console.log(`Cost: ${subscription.cost} ${subscription.currency}`);
        console.log(`Renews: ${subscription.periodEndingAt}`);
        console.log(`Canceled: ${subscription.canceled}`);
    } else {
        console.log('❌ Free User or Expired Subscription');
    }

    return subscription;
}

// Usage
const subscription = await checkSubscription();
```

**Python:**
```python
import requests

def check_subscription(cookie):
    url = 'https://www.geoguessr.com/api/v3/subscriptions'
    response = requests.get(url, cookies={'_ncfa': cookie})
    response.raise_for_status()

    subscription = response.json()

    if subscription.get('isActive'):
        print('✅ Pro User')
        print(f"Plan: {subscription.get('plan')}")
        print(f"Cost: {subscription.get('cost')} {subscription.get('currency')}")
        print(f"Renews: {subscription.get('periodEndingAt')}")
        print(f"Canceled: {subscription.get('canceled')}")
    else:
        print('❌ Free User or Expired Subscription')

    return subscription

# Usage
# subscription = check_subscription('YOUR_NCFA_COOKIE')
```

---

### Example 2: Get Available Plans

**JavaScript:**
```javascript
async function getSubscriptionPlans() {
    const response = await fetch('https://www.geoguessr.com/api/v3/subscriptions/plans');
    // No credentials needed - endpoint is public

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const plans = await response.json();

    console.log(`Found ${plans.length} subscription plans:`);
    plans.forEach(plan => {
        const period = plan.interval === 1 ? 'monthly' : 'yearly';
        const price = `${plan.price} ${plan.currency}`;
        const perMonth = `(${plan.pricePerMonth}/month)`;
        console.log(`- Plan ${plan.id}: ${price}/${period} ${perMonth}`);
    });

    return plans;
}

// Usage
const plans = await getSubscriptionPlans();
```

**Python:**
```python
import requests

def get_subscription_plans():
    url = 'https://www.geoguessr.com/api/v3/subscriptions/plans'
    # No authentication needed
    response = requests.get(url)
    response.raise_for_status()

    plans = response.json()

    print(f'Found {len(plans)} subscription plans:')
    for plan in plans:
        period = 'monthly' if plan['interval'] == 1 else 'yearly'
        price = f"{plan['price']} {plan['currency']}"
        per_month = f"({plan['pricePerMonth']}/month)"
        print(f"- Plan {plan['id']}: {price}/{period} {per_month}")

    return plans

# Usage
# plans = get_subscription_plans()
```

---

### Example 3: Check if User is Pro

**JavaScript:**
```javascript
async function isProUser() {
    try {
        const subscription = await checkSubscription();
        return subscription.isActive === true;
    } catch (error) {
        console.error('Error checking Pro status:', error);
        return false;
    }
}

// Usage
if (await isProUser()) {
    console.log('User has Pro features');
} else {
    console.log('User has limited features');
}
```

---

### Example 4: Get Billing History

**JavaScript:**
```javascript
async function getBillingHistory() {
    const response = await fetch('https://www.geoguessr.com/api/v3/subscriptions/invoices', {
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const invoices = await response.json();

    console.log(`Found ${invoices.length} invoices:`);
    invoices.forEach(invoice => {
        const status = invoice.paid ? '✅ Paid' : '❌ Unpaid';
        console.log(`- ${invoice.date}: ${invoice.total} ${status}`);
        console.log(`  URL: ${invoice.invoiceUrl}`);
    });

    return invoices;
}

// Usage
const invoices = await getBillingHistory();
```

**Python:**
```python
import requests

def get_billing_history(cookie):
    url = 'https://www.geoguessr.com/api/v3/subscriptions/invoices'
    response = requests.get(url, cookies={'_ncfa': cookie})
    response.raise_for_status()

    invoices = response.json()

    print(f'Found {len(invoices)} invoices:')
    for invoice in invoices:
        status = '✅ Paid' if invoice['paid'] else '❌ Unpaid'
        print(f"- {invoice['date']}: {invoice['total']} {status}")
        print(f"  URL: {invoice['invoiceUrl']}")

    return invoices

# Usage
# invoices = get_billing_history('YOUR_NCFA_COOKIE')
```

---

## Common Use Cases

### 1. Display Subscription Status

```javascript
async function displaySubscriptionStatus() {
    const subscription = await checkSubscription();

    if (subscription.isActive) {
        const expiryDate = new Date(subscription.periodEndingAt);
        const daysRemaining = Math.ceil((expiryDate - new Date()) / (1000 * 60 * 60 * 24));
        const isCanceled = subscription.canceled ? ' (Canceling)' : '';

        return `
            <div class="subscription-status pro">
                <h3>GeoGuessr Pro ⭐${isCanceled}</h3>
                <p>Plan: ${subscription.plan}</p>
                <p>Cost: ${subscription.cost} ${subscription.currency}</p>
                <p>Renews: ${expiryDate.toLocaleDateString()}</p>
                <p>Days remaining: ${daysRemaining}</p>
                ${subscription.isInTrialPeriod ? '<p class="trial">🎁 In Trial Period</p>' : ''}
            </div>
        `;
    } else {
        return `
            <div class="subscription-status free">
                <h3>Free Account</h3>
                <button onclick="upgradeToPro()">Upgrade to Pro</button>
            </div>
        `;
    }
}
```

### 2. Feature Gating

```javascript
async function checkFeatureAccess(feature) {
    const proFeatures = [
        'unlimited_games',
        'custom_maps',
        'no_ads',
        'party_mode'
    ];

    if (proFeatures.includes(feature)) {
        const isPro = await isProUser();
        if (!isPro) {
            throw new Error('This feature requires GeoGuessr Pro');
        }
    }

    return true;
}

// Usage
// try {
//     await checkFeatureAccess('custom_maps');
//     // Allow access to feature
// } catch (error) {
//     // Show upgrade prompt
// }
```

### 3. Compare Plans

```javascript
async function comparePlans() {
    const plans = await getSubscriptionPlans();

    // Group by product tier
    const comparison = plans.map(plan => {
        const period = plan.interval === 1 ? 'Monthly' : 'Yearly';

        // Find corresponding monthly plan for savings calculation
        const monthlyPlan = plans.find(p =>
            p.product === plan.product &&
            p.interval === 1 &&
            p.currency === plan.currency
        );

        const yearlyCost = plan.interval === 2 ? plan.price : null;
        const monthlyCost = monthlyPlan ? monthlyPlan.price : null;
        const savings = (yearlyCost && monthlyCost)
            ? ((monthlyCost * 12) - yearlyCost).toFixed(2)
            : null;

        return {
            id: plan.id,
            product: plan.product,
            period: period,
            price: `${plan.price} ${plan.currency}`,
            perMonth: `${plan.pricePerMonth} ${plan.currency}`,
            savings: savings ? `${savings} ${plan.currency}` : 'N/A'
        };
    });

    console.table(comparison);
    return comparison;
}
```

---

## Non-Working Endpoints

The following endpoints exist but return **405 Method Not Allowed** on GET requests. They likely require POST with specific request bodies:

- `POST /v3/subscriptions/status` - Subscription status update (405 on GET)
- `POST /v3/subscriptions/history` - Subscription history (405 on GET)
- `POST /v3/subscriptions/cancel` - Cancel subscription (405 on GET)
- `POST /v3/subscriptions/apple` - Apple App Store verification (405 on GET)
- `POST /v3/subscriptions/stripe` - Stripe payment handling (405 on GET)
- `POST /v3/subscriptions/upgrade` - Upgrade subscription (405 on GET)

**Non-existent endpoints (404):**
- `GET /v4/subscriptions` - v4 subscriptions endpoint doesn't exist

**Note:** Most subscription management (upgrades, cancellations) is typically handled through payment providers (Paddle, Stripe) or the web UI rather than direct API calls.

---

## Testing

See [subscriptions-testing.md](./tests/subscriptions-testing.md) for console commands to test these endpoints.

---

## Notes for Documentation Contributors

**Verified:**
- [x] Complete subscription object structure (21 fields)
- [x] All available plans structure (14 plans, 12 fields each)
- [x] Plans endpoint doesn't require authentication
- [x] Invoice/billing history endpoint
- [x] Trial period information fields
- [x] Google Play, Apple, Stripe endpoints exist (require POST)
- [x] Payment provider IDs (5 = Paddle, 6 = Stripe, etc.)

**Still needs verification:**
- [ ] Request body structures for POST endpoints
- [ ] Subscription cancel process
- [ ] Subscription upgrade process
- [ ] Promotional codes/discounts structure
- [ ] Complete invoice object structure
- [ ] Payment method management endpoints
- [ ] Refund/chargeback handling

---

## Important Notes

1. **Subscription Management**: Most subscription changes (upgrades, cancellations) are likely handled through the web UI or payment providers (Stripe, Google Play, Apple App Store) rather than direct API calls.

2. **Pricing**: Prices may vary by region and are subject to change.

3. **Free Tier**: Free users have limited daily games and access to fewer features.

4. **Pro Features** (typical):
   - Unlimited games
   - Custom map creation
   - No advertisements
   - Party mode
   - Advanced statistics
