from locust import HttpUser, task, between
import json
import random
import string
import time


class RateLimiterUser(HttpUser):
    wait_time = between(0.1, 0.5)  # Time between requests in seconds

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = self.generate_user_id()

    def generate_user_id(self):
        """Generate a random user ID."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    @task(1)
    def test_rate_limit_single_user(self):
        """Test the rate limiter with the same user ID repeatedly."""
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"userId": self.user_id})

        with self.client.post("/api/check", data=payload, headers=headers, catch_response=True) as response:
            if response.text == "Allowed":
                response.success()
            elif response.text == "Rate limit exceeded":
                # This is expected after hitting the rate limit
                response.success()
            else:
                response.failure(f"Unexpected response: {response.text}")

    @task(2)
    def test_rate_limit_random_users(self):
        """Test the rate limiter with random user IDs."""
        headers = {'Content-Type': 'application/json'}
        random_user_id = self.generate_user_id()
        payload = json.dumps({"userId": random_user_id})

        with self.client.post("/api/check", data=payload, headers=headers, catch_response=True) as response:
            if response.text == "Allowed":
                response.success()
            else:
                response.failure(f"Unexpected response for new user: {response.text}")


class BurstUser(HttpUser):
    """User that sends requests in bursts."""
    wait_time = between(1, 3)  # Longer wait between bursts

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = self.generate_user_id()

    def generate_user_id(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    @task
    def burst_requests(self):
        """Send a burst of requests in quick succession."""
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"userId": self.user_id})

        # Send a burst of 10 requests with minimal delay
        for _ in range(10):
            with self.client.post("/api/check", data=payload, headers=headers, catch_response=True) as response:
                if response.text == "Allowed":
                    response.success()
                elif response.text == "Rate limit exceeded":
                    # This is expected after hitting the rate limit
                    response.success()
                else:
                    response.failure(f"Unexpected response: {response.text}")
            time.sleep(0.05)  # 50ms between requests in the burst


class DistributedUser(HttpUser):
    """User that distributes requests over time to avoid rate limiting."""
    wait_time = between(0.06, 0.07)  # Just slightly above the rate limit window

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = self.generate_user_id()

    def generate_user_id(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    @task
    def distributed_requests(self):
        """Send requests at a rate just below the limit."""
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"userId": self.user_id})

        with self.client.post("/api/check", data=payload, headers=headers, catch_response=True) as response:
            if response.text == "Allowed":
                response.success()
            else:
                response.failure(f"Rate limit exceeded when it shouldn't: {response.text}")

