"""
Sign In Example

Demonstrates how to sign in to GeoGuessr programmatically.

⚠️  IMPORTANT WARNINGS:
1. This is for EDUCATIONAL purposes only
2. Programmatic login may violate GeoGuessr's Terms of Service
3. Never hardcode credentials in your code
4. Use proper authentication methods in production
5. Always store credentials securely

Usage:
    python sign_in_example.py

Requirements:
    pip install requests
"""

import requests
import os
import sys


def sign_in(email, password):
    """
    Sign in to GeoGuessr.

    ⚠️  WARNING: For educational purposes only

    Args:
        email (str): User email
        password (str): User password

    Returns:
        tuple: (session, user_data) or (None, None) if failed
    """
    try:
        url = 'https://www.geoguessr.com/api/v3/accounts/signin'

        session = requests.Session()
        response = session.post(
            url,
            json={
                'email': email,
                'password': password
            }
        )

        if response.status_code == 401:
            print('❌ Invalid email or password')
            return None, None

        response.raise_for_status()
        user = response.json()

        # Display success
        print(f"\n✅ Sign In Successful!\n")
        print(f"Welcome, {user['nick']}!")
        print(f"Level: {user['progress']['level']}")
        print(f"XP: {user['progress']['xp']:,}")
        print(f"Pro User: {'✅ Yes' if user['isProUser'] else '❌ No'}")

        print(f"\n🔐 Authentication Cookies Set:")
        print(f"- _ncfa - Main session cookie")
        print(f"- session - Session identifier")

        # Extract _ncfa cookie for future use
        ncfa_cookie = session.cookies.get('_ncfa')
        if ncfa_cookie:
            print(f"\n💡 Your _ncfa cookie (save this for API requests):")
            print(f"{ncfa_cookie}")

        return session, user

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return None, None


def verify_sign_in(session):
    """Verify that sign in was successful."""
    try:
        response = session.get('https://www.geoguessr.com/api/v3/profiles')

        if response.ok:
            profile = response.json()
            print(f"\n✅ Verified: Signed in as {profile['user']['nick']}")
            return True
        else:
            print('❌ Not signed in')
            return False
    except Exception as e:
        print(f'Error verifying sign in: {e}')
        return False


def main():
    print("=" * 60)
    print("⚠️  WARNING: EDUCATIONAL USE ONLY")
    print("=" * 60)
    print("\nProgrammatic login may violate GeoGuessr's Terms of Service.")
    print("This example is for educational purposes to understand the API.")
    print("In production, use proper OAuth flows or manual cookie extraction.")
    print()

    proceed = input("Do you understand and wish to proceed? (yes/no): ").strip().lower()
    if proceed != 'yes':
        print("Exiting...")
        return

    # Get credentials from environment variables (NEVER hardcode!)
    email = os.getenv('GEOGUESSR_EMAIL')
    password = os.getenv('GEOGUESSR_PASSWORD')

    if not email or not password:
        print("\n❌ Error: Credentials not found in environment variables")
        print("\nSet them with:")
        print("  export GEOGUESSR_EMAIL='your_email@example.com'")
        print("  export GEOGUESSR_PASSWORD='your_password'")
        print("\n⚠️  Security Reminder:")
        print("- Never commit credentials to version control")
        print("- Use .env files with .gitignore")
        print("- Rotate passwords regularly")
        print("- Use strong, unique passwords")
        return

    # Attempt sign in
    session, user = sign_in(email, password)

    if session and user:
        # Verify sign in
        verify_sign_in(session)

        print("\n📝 Next Steps:")
        print("- Save your _ncfa cookie to GEOGUESSR_COOKIE environment variable")
        print("- Use that cookie for future API requests")
        print("- Don't share your cookie publicly")


if __name__ == '__main__':
    main()


"""
SECURITY BEST PRACTICES:

1. Environment Variables:
   - Store credentials in environment variables
   - Never hardcode in source code
   - Use .env files with python-dotenv

2. Password Security:
   - Use strong, unique passwords
   - Enable 2FA when available
   - Rotate credentials regularly

3. Session Management:
   - Store cookies securely
   - Implement timeout mechanisms
   - Clear sessions on logout

4. Rate Limiting:
   - Implement exponential backoff
   - Respect API rate limits
   - Monitor for unusual activity

5. Compliance:
   - Review Terms of Service
   - Obtain proper authorization
   - Document API usage
   - Respect user privacy

6. Error Handling:
   - Never log passwords
   - Handle authentication failures gracefully
   - Implement proper retry logic

7. Network Security:
   - Use HTTPS only
   - Verify SSL certificates
   - Implement timeout mechanisms
"""
