package com.fleetops;

import io.github.cdimascio.dotenv.Dotenv;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Main {
    public static void main(String[] args) {
        // Load .env file before Spring Boot starts
        // This makes environment variables available to Spring Boot's property resolution
        Dotenv dotenv = Dotenv.configure()
                .ignoreIfMissing()  // Don't fail if .env file doesn't exist
                .load();
        
        // Set environment variables as system properties
        // Spring Boot can read from both environment variables and system properties
        dotenv.entries().forEach(entry -> {
            String key = entry.getKey();
            String value = entry.getValue();
            // Only set if not already set (allows system/env vars to override .env)
            if (System.getProperty(key) == null) {
                System.setProperty(key, value);
            }
        });
        
        SpringApplication.run(Main.class, args);
    }
}