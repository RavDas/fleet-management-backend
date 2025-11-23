package com.fleetops.component;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fleetops.entity.DriverEntity;
import com.fleetops.entity.FormEntity;
import com.fleetops.repository.DriverRepository;
import com.fleetops.repository.FormRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

@Component
public class DataSeeder implements CommandLineRunner {

    private static final Logger logger = LoggerFactory.getLogger(DataSeeder.class);

    private final DriverRepository driverRepository;
    private final FormRepository formRepository;
    private final ObjectMapper objectMapper;

    public DataSeeder(DriverRepository driverRepository, FormRepository formRepository, ObjectMapper objectMapper) {
        this.driverRepository = driverRepository;
        this.formRepository = formRepository;
        this.objectMapper = objectMapper;
    }

    @Override
    public void run(String... args) {
        seedDrivers();
        seedForms();
    }

    private void seedDrivers() {
        if (driverRepository.count() == 0) {
            logger.info("🚗 No drivers found. Seeding data...");
            try {
                InputStream inputStream = new ClassPathResource("sample_driver_records.json").getInputStream();
                List<DriverEntity> drivers = objectMapper.readValue(inputStream, new TypeReference<List<DriverEntity>>() {});
                
                if (drivers != null && !drivers.isEmpty()) {
                    driverRepository.saveAll(drivers);
                    logger.info("✅ Seeded {} drivers.", drivers.size());
                }
            } catch (IOException e) {
                logger.error("❌ Failed to seed drivers: {}", e.getMessage());
            }
        } else {
            logger.info("ℹ️  Drivers table already populated. Skipping seed.");
        }
    }

    private void seedForms() {
        if (formRepository.count() == 0) {
            logger.info("📝 No forms found. Seeding data...");
            try {
                InputStream inputStream = new ClassPathResource("sample_form_records.json").getInputStream();
                List<FormEntity> forms = objectMapper.readValue(inputStream, new TypeReference<List<FormEntity>>() {});
                
                if (forms != null && !forms.isEmpty()) {
                    formRepository.saveAll(forms);
                    logger.info("✅ Seeded {} forms.", forms.size());
                }
            } catch (IOException e) {
                logger.error("❌ Failed to seed forms: {}", e.getMessage());
            }
        } else {
            logger.info("ℹ️  Forms table already populated. Skipping seed.");
        }
    }
}

