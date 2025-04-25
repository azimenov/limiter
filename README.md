Rate Limiter Service
Overview
This service implements a sliding window rate limiting algorithm to control the request rate from individual users. The rate limiter is designed to prevent API abuse, maintain service stability, and ensure fair resource allocation among users.
Architecture
Algorithm: Sliding Window Counter
The implementation uses a sliding window approach to rate limiting with the following characteristics:

Time Window: Configurable time period (in seconds) during which requests are counted
Request Counter: Tracks the number of requests made by a user within the current window
Per-User Tracking: Independent rate limits for each user identified by their userId

Implementation Details
Data Structure

ConcurrentHashMap<String, UserRequestInfo>: Thread-safe map to store user request information
UserRequestInfo: Inner class containing:

requestCount: Number of requests in the current window
windowStart: Timestamp (epoch seconds) when the current window started



Request Flow

When a request arrives, the service retrieves the user's current request information
If the time window has expired, a new window is started with the request count reset to 1
If within the current window, the request count is incremented if below the limit
If the request count exceeds the configured limit, the request is rejected
User request information is updated in the map