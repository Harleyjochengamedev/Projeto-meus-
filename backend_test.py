#!/usr/bin/env python3
import requests
import sys
import json
from datetime import datetime

class PlayMatchAPITester:
    def __init__(self, base_url="https://gamematch-30.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.session_token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.session_token:
            test_headers['Authorization'] = f'Bearer {self.session_token}'
        
        if headers:
            test_headers.update(headers)

        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=10)

            success = response.status_code == expected_status
            details = f"Status: {response.status_code}"
            
            if not success:
                details += f" (Expected {expected_status})"
                try:
                    error_data = response.json()
                    details += f" - {error_data.get('detail', 'Unknown error')}"
                except:
                    details += f" - {response.text[:100]}"

            self.log_test(name, success, details)
            
            if success:
                try:
                    return response.json()
                except:
                    return {}
            return None

        except Exception as e:
            self.log_test(name, False, f"Exception: {str(e)}")
            return None

    def test_auth_with_session(self, session_token):
        """Test authentication with session token"""
        print(f"\n🔐 Testing Authentication with session: {session_token[:20]}...")
        self.session_token = session_token
        
        # Test /auth/me endpoint
        user_data = self.run_test(
            "Get current user (/auth/me)",
            "GET",
            "auth/me",
            200
        )
        
        if user_data and 'user_id' in user_data:
            self.user_id = user_data['user_id']
            print(f"   User ID: {self.user_id}")
            print(f"   Name: {user_data.get('name', 'N/A')}")
            return True
        return False

    def test_profile_endpoints(self):
        """Test profile GET and PUT endpoints"""
        print(f"\n👤 Testing Profile Endpoints...")
        
        # Test GET profile
        profile_data = self.run_test(
            "Get user profile (/profile)",
            "GET",
            "profile",
            200
        )
        
        if profile_data:
            # Test PUT profile update
            update_data = {
                "gaming_profile": {
                    "games": ["League of Legends", "Valorant"],
                    "platform": "PC",
                    "style": "Competitivo",
                    "communication": "Voz ativa",
                    "tolerance": 4,
                    "goal": "Rank"
                },
                "availability_schedule": {
                    "monday": ["19:00", "20:00", "21:00"],
                    "tuesday": ["19:00", "20:00"]
                }
            }
            
            updated_profile = self.run_test(
                "Update user profile (/profile)",
                "PUT",
                "profile",
                200,
                data=update_data
            )
            
            return updated_profile is not None
        return False

    def test_matches_endpoints(self):
        """Test matchmaking endpoints"""
        print(f"\n🎮 Testing Matchmaking Endpoints...")
        
        # Test GET matches
        matches_data = self.run_test(
            "Get matches (/matches)",
            "GET",
            "matches?limit=10",
            200
        )
        
        if matches_data is not None:
            print(f"   Found {len(matches_data)} potential matches")
            
            # If we have matches, test match actions
            if len(matches_data) > 0:
                match = matches_data[0]
                other_user_id = match['user']['user_id']
                
                # Test create match
                create_result = self.run_test(
                    "Create match (/matches/create)",
                    "POST",
                    f"matches/create?other_user_id={other_user_id}",
                    200
                )
                
                if create_result and 'match_id' in create_result:
                    match_id = create_result['match_id']
                    print(f"   Created match: {match_id}")
                    
                    # Test match action (like)
                    action_result = self.run_test(
                        "Accept match (/matches/action)",
                        "POST",
                        "matches/action",
                        200,
                        data={"match_id": match_id, "action": "like"}
                    )
                    
                    return action_result is not None
            return True
        return False

    def test_chat_endpoints(self):
        """Test chat endpoints"""
        print(f"\n💬 Testing Chat Endpoints...")
        
        # First we need a match with accepted status
        # For testing, we'll try to get chats and send a message if possible
        
        # This is a simplified test - in real scenario we'd need an accepted match
        # Let's test with a dummy match_id to see error handling
        test_match_id = "test_match_123"
        
        chat_result = self.run_test(
            "Get chat (expected 404)",
            "GET",
            f"chats/{test_match_id}",
            404  # Expected to fail with 404
        )
        
        # Test message sending (also expected to fail)
        message_result = self.run_test(
            "Send message (expected 404)",
            "POST",
            f"chats/{test_match_id}/message",
            404,  # Expected to fail with 404
            data={"text": "Test message"}
        )
        
        return True  # These are expected to fail, so we return True

    def test_ratings_endpoints(self):
        """Test rating endpoints"""
        print(f"\n⭐ Testing Rating Endpoints...")
        
        # Test get ratings for a user (should work even if no ratings exist)
        ratings_result = self.run_test(
            "Get user ratings (/ratings/{user_id})",
            "GET",
            f"ratings/{self.user_id}",
            200
        )
        
        if ratings_result is not None:
            print(f"   Total ratings: {ratings_result.get('total_ratings', 0)}")
            return True
        return False

    def print_summary(self):
        """Print test summary"""
        print(f"\n📊 Test Summary:")
        print(f"   Tests run: {self.tests_run}")
        print(f"   Tests passed: {self.tests_passed}")
        print(f"   Success rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed < self.tests_run:
            print(f"\n❌ Failed tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   - {result['test']}: {result['details']}")

def main():
    # Test session tokens from MongoDB setup
    session_tokens = [
        "test_session_1769091160826",  # User 1
        "test_session_1769091160827"   # User 2
    ]
    
    print("🚀 Starting PlayMatch API Testing...")
    print(f"Backend URL: https://gamematch-30.preview.emergentagent.com")
    
    tester = PlayMatchAPITester()
    
    # Test with first user
    if tester.test_auth_with_session(session_tokens[0]):
        tester.test_profile_endpoints()
        tester.test_matches_endpoints()
        tester.test_chat_endpoints()
        tester.test_ratings_endpoints()
    else:
        print("❌ Authentication failed, skipping other tests")
        return 1
    
    tester.print_summary()
    
    # Return 0 if all critical tests passed, 1 otherwise
    critical_tests = ['Get current user (/auth/me)', 'Get user profile (/profile)', 'Get matches (/matches)']
    critical_passed = sum(1 for result in tester.test_results 
                         if result['test'] in critical_tests and result['success'])
    
    if critical_passed >= len(critical_tests):
        print("\n✅ All critical backend tests passed!")
        return 0
    else:
        print(f"\n❌ Only {critical_passed}/{len(critical_tests)} critical tests passed")
        return 1

if __name__ == "__main__":
    sys.exit(main())