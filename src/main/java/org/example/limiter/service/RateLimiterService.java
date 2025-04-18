package org.example.limiter.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class RateLimiterService {

    @Value("${rate.limit.maxRequests}")
    private int MAX_REQUESTS;

    @Value("${rate.limit.windowSeconds}")
    private int WINDOW_SECONDS;

    private final ConcurrentHashMap<String, UserRequestInfo> requestMap = new ConcurrentHashMap<>();

    public boolean isAllowed(String userId) {
        long currentTime = Instant.now().getEpochSecond();
        UserRequestInfo info = requestMap.getOrDefault(userId, new UserRequestInfo(0, currentTime));

        if (currentTime - info.windowStart >= WINDOW_SECONDS) {
            info = new UserRequestInfo(1, currentTime);
        } else {
            if (info.requestCount >= MAX_REQUESTS) return false;
            info.requestCount++;
        }

        requestMap.put(userId, info);
        return true;
    }

    private static class UserRequestInfo {
        int requestCount;
        long windowStart;

        public UserRequestInfo(int requestCount, long windowStart) {
            this.requestCount = requestCount;
            this.windowStart = windowStart;
        }
    }
}