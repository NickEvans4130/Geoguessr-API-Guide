"""
Check Subscription Status

Retrieves and displays your current GeoGuessr subscription information.

Usage:
    python check_subscription.py

Requirements:
    pip install requests
"""

import requests
import os
from datetime import datetime


def check_subscription(cookie):
    """
    Check and display subscription status.

    Args:
        cookie (str): Your _ncfa cookie value

    Returns:
        dict: Subscription object
    """
    try:
        response = requests.get(
            'https://www.geoguessr.com/api/v3/subscriptions',
            cookies={'_ncfa': cookie}
        )

        if response.status_code == 404:
            print('❌ No active subscription found.')
            return None

        response.raise_for_status()
        subscription = response.json()

        # Display subscription information
        print(f"\n💳 Subscription Status\n")

        if subscription['isActive']:
            print(f"✅ Active Subscription")
        else:
            print(f"❌ Inactive Subscription")

        print(f"\n📋 Plan Details:")
        print(f"Plan: {subscription['plan']}")
        print(f"Cost: {subscription['currency']} {subscription['cost']}")
        billing = 'Monthly' if subscription['interval'] == 1 else 'Yearly'
        print(f"Billing: {billing}")

        print(f"\n📅 Dates:")
        started = datetime.fromisoformat(subscription['startedAt'].replace('Z', '+00:00'))
        print(f"Started: {started.strftime('%Y-%m-%d')}")

        renews = datetime.fromisoformat(subscription['periodEndingAt'].replace('Z', '+00:00'))
        print(f"Renews: {renews.strftime('%Y-%m-%d')}")

        if subscription['isInTrialPeriod']:
            trial_end = datetime.fromisoformat(subscription['trialEndingAt'].replace('Z', '+00:00'))
            print(f"Trial: ✅ In trial period (ends {trial_end.strftime('%Y-%m-%d')})")

        if subscription['canceled']:
            print(f"\n⚠️  Subscription is canceled (access until {renews.strftime('%Y-%m-%d')})")

        # Calculate time remaining
        now = datetime.now(renews.tzinfo)
        days_remaining = (renews - now).days

        print(f"\n⏰ Time Remaining:")
        if days_remaining > 0:
            print(f"{days_remaining} days until renewal")
        else:
            print(f"Expired {abs(days_remaining)} days ago")

        # Calculate value
        monthly_value = subscription['cost'] / 12 if subscription['interval'] == 2 else subscription['cost']

        print(f"\n💰 Value:")
        print(f"Effective monthly cost: {subscription['currency']} {monthly_value:.2f}")

        # Additional info
        print(f"\n🔍 Additional Info:")
        print(f"Subscription ID: {subscription['id']}")
        print(f"Plan ID: {subscription['planId']}")
        print(f"Payment Provider: {subscription['payProvider']}")

        return subscription

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if e.response.status_code == 401:
            print("Note: Your cookie may be invalid or expired")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return None


def main():
    # Get credentials from environment variables
    cookie = os.getenv('GEOGUESSR_COOKIE')
    if not cookie:
        print("❌ Error: GEOGUESSR_COOKIE environment variable not set")
        print("Set it with: export GEOGUESSR_COOKIE='your_cookie_value'")
        return

    # Check subscription
    subscription = check_subscription(cookie)

    if subscription:
        print("\n✅ Subscription information retrieved!")


if __name__ == '__main__':
    main()
