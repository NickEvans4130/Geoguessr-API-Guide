"""
Compare Subscription Plans

Retrieves and compares all available GeoGuessr subscription plans.

Usage:
    python compare_plans.py

Requirements:
    pip install requests

Note: This endpoint does NOT require authentication
"""

import requests
from collections import defaultdict


def get_product_name(product_id):
    """Get human-readable product name."""
    products = {
        2: 'Pro',
        3: 'Unlimited',
        4: 'Premium',
        5: 'Team'
    }
    return products.get(product_id, f'Product {product_id}')


def compare_plans():
    """
    Fetch and compare subscription plans.

    Returns:
        list: List of plan objects
    """
    try:
        # No authentication required for this endpoint
        response = requests.get('https://www.geoguessr.com/api/v3/subscriptions/plans')
        response.raise_for_status()

        plans = response.json()

        print(f"\n💳 Available Subscription Plans ({len(plans)} plans)\n")

        # Group by currency
        by_currency = defaultdict(list)
        for plan in plans:
            by_currency[plan['currency']].append(plan)

        # Display by currency
        for currency, currency_plans in by_currency.items():
            print(f"\n💰 {currency} Plans:\n")
            print(f"{'Billing':<10} {'Product':<12} {'Total Price':<15} {'Per Month':<15} {'Savings'}")
            print('-' * 70)

            for plan in sorted(currency_plans, key=lambda p: (p['product'], p['interval'])):
                billing = 'Monthly' if plan['interval'] == 1 else 'Yearly'
                product = get_product_name(plan['product'])
                total = f"{currency} {plan['price']}"
                per_month = f"{currency} {plan['pricePerMonth']}"

                # Calculate savings for yearly plans
                savings = '-'
                if plan['interval'] == 2:
                    monthly_plan = next((p for p in currency_plans
                                       if p['interval'] == 1 and p['product'] == plan['product']), None)
                    if monthly_plan:
                        saved = (monthly_plan['price'] * 12) - plan['price']
                        savings = f"{currency} {saved:.2f}"

                print(f"{billing:<10} {product:<12} {total:<15} {per_month:<15} {savings}")

        # Find best value
        print(f"\n🏆 Best Value Analysis:\n")

        yearly_plans = [p for p in plans if p['interval'] == 2]
        if yearly_plans:
            best_value = min(yearly_plans, key=lambda p: p['pricePerMonth'])

            print(f"Best value: {get_product_name(best_value['product'])} Yearly")
            print(f"Price: {best_value['currency']} {best_value['price']}/year "
                  f"({best_value['currency']} {best_value['pricePerMonth']}/month)")

        # Monthly vs Yearly comparison
        print(f"\n📊 Monthly vs Yearly Savings:\n")
        monthly_plans = [p for p in plans if p['interval'] == 1]

        for monthly in monthly_plans:
            yearly = next((p for p in plans
                          if p['interval'] == 2 and
                          p['currency'] == monthly['currency'] and
                          p['product'] == monthly['product']), None)

            if yearly:
                monthly_total = monthly['price'] * 12
                savings = monthly_total - yearly['price']
                savings_percent = (savings / monthly_total) * 100

                print(f"{monthly['currency']} {get_product_name(monthly['product'])}:")
                print(f"  Monthly: {monthly['currency']} {monthly['price']}/month × 12 = "
                      f"{monthly['currency']} {monthly_total:.2f}")
                print(f"  Yearly:  {yearly['currency']} {yearly['price']}/year "
                      f"({yearly['currency']} {yearly['price'] / 12:.2f}/month)")
                print(f"  💰 Save: {yearly['currency']} {savings:.2f}/year "
                      f"({savings_percent:.0f}% savings)\n")

        return plans

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return None


def filter_plans_by_currency(plans, currency):
    """Filter plans by currency."""
    return [p for p in plans if p['currency'] == currency]


def get_cheapest_plan(plans):
    """Get the cheapest plan based on monthly cost."""
    return min(plans, key=lambda p: p['pricePerMonth'])


def main():
    print("=== GeoGuessr Subscription Plans Comparison ===\n")

    plans = compare_plans()

    if plans:
        print(f"\n✅ Retrieved {len(plans)} plans!")

        # Show available currencies
        currencies = sorted(set(p['currency'] for p in plans))
        print(f"\nAvailable currencies: {', '.join(currencies)}")

        # Show plan breakdown
        products = {}
        for plan in plans:
            product = get_product_name(plan['product'])
            if product not in products:
                products[product] = 0
            products[product] += 1

        print(f"\nPlans per product:")
        for product, count in sorted(products.items()):
            print(f"  {product}: {count} options")


if __name__ == '__main__':
    main()
