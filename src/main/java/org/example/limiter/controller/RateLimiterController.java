package org.example.limiter.controller;


import org.example.limiter.model.RateLimitRequest;
import org.example.limiter.service.RateLimiterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class RateLimiterController {

    @Autowired
    private RateLimiterService rateLimiterService;

    @PostMapping("/check")
    public String checkRateLimit(@RequestBody RateLimitRequest request) {
        boolean allowed = rateLimiterService.isAllowed(request.getUserId());
        return allowed ? "Allowed" : "Rate limit exceeded";
    }
}