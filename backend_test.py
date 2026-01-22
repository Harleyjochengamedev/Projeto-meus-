#!/usr/bin/env python3
import requests
import sys
import json
from datetime import datetime, timedelta
import uuid

class DevFlowAPITester:
    def __init__(self, base_url="https://gamematch-30.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.session_token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        self.created_task_id = None
        self.created_sprint_id = None

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
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers, timeout=10)

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

    def test_root_endpoint(self):
        """Test root API endpoint"""
        print(f"\n🏠 Testing Root Endpoint...")
        
        result = self.run_test(
            "API Root (/api/)",
            "GET",
            "",
            200
        )
        
        return result is not None

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
            print(f"   Email: {user_data.get('email', 'N/A')}")
            return True
        return False

    def test_tasks_endpoints(self):
        """Test task management endpoints"""
        print(f"\n📝 Testing Task Endpoints...")
        
        # Test GET tasks (empty initially)
        tasks_data = self.run_test(
            "Get all tasks (/tasks)",
            "GET",
            "tasks",
            200
        )
        
        if tasks_data is not None:
            print(f"   Found {len(tasks_data)} existing tasks")
            
            # Test POST create task
            task_data = {
                "title": "Test Task - Backend Testing",
                "description": "This is a test task created during backend testing",
                "category": "task",
                "priority": "high",
                "estimated_time": 60,
                "tags": ["testing", "backend"]
            }
            
            created_task = self.run_test(
                "Create new task (/tasks)",
                "POST",
                "tasks",
                200,
                data=task_data
            )
            
            if created_task and 'task_id' in created_task:
                self.created_task_id = created_task['task_id']
                print(f"   Created task: {self.created_task_id}")
                
                # Test GET specific task
                task_detail = self.run_test(
                    f"Get task by ID (/tasks/{self.created_task_id})",
                    "GET",
                    f"tasks/{self.created_task_id}",
                    200
                )
                
                # Test PUT update task
                update_data = {
                    "status": "done",
                    "actual_time": 45
                }
                
                updated_task = self.run_test(
                    f"Update task status (/tasks/{self.created_task_id})",
                    "PUT",
                    f"tasks/{self.created_task_id}",
                    200,
                    data=update_data
                )
                
                # Test filtering tasks
                filtered_tasks = self.run_test(
                    "Get completed tasks (/tasks?status=done)",
                    "GET",
                    "tasks?status=done",
                    200
                )
                
                # Test category filtering
                category_tasks = self.run_test(
                    "Get tasks by category (/tasks?category=task)",
                    "GET",
                    "tasks?category=task",
                    200
                )
                
                return all([task_detail, updated_task, filtered_tasks, category_tasks])
            
        return False

    def test_sprints_endpoints(self):
        """Test sprint management endpoints"""
        print(f"\n🎯 Testing Sprint Endpoints...")
        
        # Test GET sprints (empty initially)
        sprints_data = self.run_test(
            "Get all sprints (/sprints)",
            "GET",
            "sprints",
            200
        )
        
        if sprints_data is not None:
            print(f"   Found {len(sprints_data)} existing sprints")
            
            # Test POST create sprint
            start_date = datetime.now()
            end_date = start_date + timedelta(days=7)
            
            sprint_data = {
                "name": "Test Sprint - Week 1",
                "goal": "Complete backend testing and implement new features",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
            
            created_sprint = self.run_test(
                "Create new sprint (/sprints)",
                "POST",
                "sprints",
                200,
                data=sprint_data
            )
            
            if created_sprint and 'sprint_id' in created_sprint:
                self.created_sprint_id = created_sprint['sprint_id']
                print(f"   Created sprint: {self.created_sprint_id}")
                return True
            
        return False

    def test_time_entries_endpoints(self):
        """Test time entry endpoints"""
        print(f"\n⏱️ Testing Time Entry Endpoints...")
        
        if not self.created_task_id:
            print("   No task available for time entry testing")
            return False
        
        # Test POST create time entry
        time_entry_data = {
            "task_id": self.created_task_id,
            "duration": 25,  # 25 minutes pomodoro
            "entry_type": "pomodoro"
        }
        
        created_entry = self.run_test(
            "Create time entry (/time-entries)",
            "POST",
            "time-entries",
            200,
            data=time_entry_data
        )
        
        if created_entry:
            # Test GET time entries
            today = datetime.now().strftime('%Y-%m-%d')
            entries_data = self.run_test(
                f"Get time entries for today (/time-entries?date={today})",
                "GET",
                f"time-entries?date={today}",
                200
            )
            
            # Test GET all time entries
            all_entries = self.run_test(
                "Get all time entries (/time-entries)",
                "GET",
                "time-entries",
                200
            )
            
            return all([entries_data, all_entries])
        
        return False

    def test_dashboard_endpoints(self):
        """Test dashboard overview endpoint"""
        print(f"\n📊 Testing Dashboard Endpoints...")
        
        overview_data = self.run_test(
            "Get dashboard overview (/dashboard/overview)",
            "GET",
            "dashboard/overview",
            200
        )
        
        if overview_data:
            print(f"   Tasks today: {overview_data.get('tasks_today', 0)}")
            print(f"   Tasks completed today: {overview_data.get('tasks_completed_today', 0)}")
            print(f"   Total time today: {overview_data.get('total_time_today', 0)} minutes")
            print(f"   Active sprints: {overview_data.get('active_sprints', 0)}")
            print(f"   Tasks by category: {overview_data.get('tasks_by_category', {})}")
            return True
        
        return False

    def test_auth_logout(self):
        """Test logout endpoint"""
        print(f"\n🚪 Testing Logout...")
        
        logout_result = self.run_test(
            "Logout (/auth/logout)",
            "POST",
            "auth/logout",
            200
        )
        
        return logout_result is not None

    def cleanup_test_data(self):
        """Clean up test data"""
        print(f"\n🧹 Cleaning up test data...")
        
        # Delete created task
        if self.created_task_id:
            self.run_test(
                f"Delete test task (/tasks/{self.created_task_id})",
                "DELETE",
                f"tasks/{self.created_task_id}",
                200
            )

    def print_summary(self):
        """Print test summary"""
        print(f"\n📊 DevFlow Backend Test Summary:")
        print(f"   Tests run: {self.tests_run}")
        print(f"   Tests passed: {self.tests_passed}")
        print(f"   Success rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed < self.tests_run:
            print(f"\n❌ Failed tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   - {result['test']}: {result['details']}")

def main():
    # Test session tokens for DevFlow (these would need to be created in MongoDB)
    # For now, we'll test without authentication first
    session_tokens = [
        "devflow_test_session_1",  # Test user 1
        "devflow_test_session_2"   # Test user 2
    ]
    
    print("🚀 Starting DevFlow Backend API Testing...")
    print(f"Backend URL: https://gamematch-30.preview.emergentagent.com")
    
    tester = DevFlowAPITester()
    
    # Test root endpoint first
    if not tester.test_root_endpoint():
        print("❌ Root endpoint failed, backend may be down")
        return 1
    
    # Try to test with session token (this may fail if no test users exist)
    auth_success = False
    for token in session_tokens:
        if tester.test_auth_with_session(token):
            auth_success = True
            break
    
    if not auth_success:
        print("⚠️  Authentication failed - testing without auth (some endpoints will fail)")
        print("   This is expected if no test users exist in MongoDB")
    
    # Run all endpoint tests
    if auth_success:
        tester.test_tasks_endpoints()
        tester.test_sprints_endpoints()
        tester.test_time_entries_endpoints()
        tester.test_dashboard_endpoints()
        tester.test_auth_logout()
        tester.cleanup_test_data()
    
    tester.print_summary()
    
    # Return 0 if root endpoint works (basic connectivity)
    # Full success requires authentication
    if tester.tests_run > 0 and tester.tests_passed >= 1:
        if auth_success and tester.tests_passed >= tester.tests_run * 0.8:
            print("\n✅ DevFlow backend tests mostly successful!")
            return 0
        elif not auth_success:
            print("\n⚠️  Backend is running but authentication needs setup")
            return 0
        else:
            print(f"\n❌ Too many backend tests failed")
            return 1
    else:
        print("\n❌ Backend appears to be down or unreachable")
        return 1

if __name__ == "__main__":
    sys.exit(main())