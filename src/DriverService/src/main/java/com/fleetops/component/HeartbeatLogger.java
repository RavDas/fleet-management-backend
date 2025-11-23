package com.fleetops.component;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class HeartbeatLogger {
    private static final Logger logger = LoggerFactory.getLogger(HeartbeatLogger.class);

    @Scheduled(fixedRate = 10000)
    public void logHeartbeat() {
        logger.info("💓 Driver Service is alive and running...");
    }
}

