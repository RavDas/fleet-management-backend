package com.fleetops.service;

import com.fleetops.dto.Driver;
import com.fleetops.entity.DriverEntity;
import com.fleetops.repository.DriverRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@Transactional
public class DriverServiceImpl implements DriverService {

    private static final org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(DriverServiceImpl.class);

    private final DriverRepository driverRepository;

    public DriverServiceImpl(DriverRepository driverRepository) {
        this.driverRepository = driverRepository;
    }

    @Override
    public boolean addDriver(Driver driver) {
        try {
            if (driverRepository.existsByLicenseNumber(driver.getLicenseNumber())) {
                return false; // Driver with this license number already exists
            }
            DriverEntity driverEntity = convertToEntity(driver);
            if (driverEntity != null) {
                driverRepository.save(driverEntity);
                return true;
            }
            return false;
        } catch (Exception e) {
            logger.error("Error adding driver: ", e);
            return false;
        }
    }

    @Override
    public Driver getDriver(Long id) {
        if (id == null) return null;
        Optional<DriverEntity> driverEntity = driverRepository.findById(id);
        return driverEntity.map(this::convertToDto).orElse(null);
    }

    @Override
    public List<Driver> getDriverList() {
        List<DriverEntity> entities = driverRepository.findAll();
        return entities.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @Override
    public Driver updateDriver(Driver driver) {
        Long driverId = driver.getDriverId();
        if (driverId == null) {
            return null; // Cannot update without ID
        }
        
        Optional<DriverEntity> existingDriverEntity = driverRepository.findById(driverId);
        if (existingDriverEntity.isEmpty()) {
            return null; // Driver not found
        }
        
        DriverEntity driverEntityToUpdate = existingDriverEntity.get();
        if (driverEntityToUpdate == null) {
            return null;
        }
        
        // Update fields if provided
        if (driver.getFullName() != null) {
            driverEntityToUpdate.setFullName(driver.getFullName());
        }
        if (driver.getEmail() != null) {
            driverEntityToUpdate.setEmail(driver.getEmail());
        }
        if (driver.getPhone() != null) {
            driverEntityToUpdate.setPhone(driver.getPhone());
        }
        if (driver.getLicenseNumber() != null && !driver.getLicenseNumber().equals(driverEntityToUpdate.getLicenseNumber())) {
            // Check if new license number already exists
            if (driverRepository.existsByLicenseNumber(driver.getLicenseNumber())) {
                return null; // License number already exists
            }
            driverEntityToUpdate.setLicenseNumber(driver.getLicenseNumber());
        }
        if (driver.getExpiryDate() != null) {
            driverEntityToUpdate.setExpiryDate(driver.getExpiryDate());
        }
        
        DriverEntity updatedEntity = driverRepository.save(driverEntityToUpdate);
        return convertToDto(updatedEntity);
    }

    @Override
    public boolean deleteDriver(Long id) {
        if (id == null) return false;
        if (driverRepository.existsById(id)) {
            driverRepository.deleteById(id);
            return true;
        }
        return false;
    }

    // Helper methods to convert between DTO and Entity using Builder pattern
    private DriverEntity convertToEntity(Driver driver) {
        return DriverEntity.builder()
                .driverId(driver.getDriverId())
                .fullName(driver.getFullName())
                .email(driver.getEmail())
                .phone(driver.getPhone())
                .licenseNumber(driver.getLicenseNumber())
                .expiryDate(driver.getExpiryDate())
                .build();
    }

    private Driver convertToDto(DriverEntity entity) {
        return Driver.builder()
                .driverId(entity.getDriverId())
                .fullName(entity.getFullName())
                .email(entity.getEmail())
                .phone(entity.getPhone())
                .licenseNumber(entity.getLicenseNumber())
                .expiryDate(entity.getExpiryDate())
                .build();
    }
}

