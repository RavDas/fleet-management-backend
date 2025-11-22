package com.fleetops.controller;

import com.fleetops.dto.Driver;
import com.fleetops.service.DriverService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/drivers")
@CrossOrigin
public class DriverController {

    @Autowired
    private DriverService driverService;

    @GetMapping
    public String test(){
        return "test complete";
    }

    @PostMapping
    public ResponseEntity<?> addDriver(@RequestBody Driver driver) {
        boolean result = driverService.addDriver(driver);
        if (result) {
            return ResponseEntity.status(HttpStatus.CREATED).body("Driver added successfully");
        } else {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Failed to add driver. License number may already exist.");
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<Driver> getDriver(@PathVariable Long id) {
        Driver driver = driverService.getDriver(id);
        if (driver != null) {
            return ResponseEntity.ok(driver);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/list")
    public ResponseEntity<List<Driver>> getDriverList() {
        List<Driver> drivers = driverService.getDriverList();
        return ResponseEntity.ok(drivers);
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateDriver(@PathVariable Long id, @RequestBody Driver driver) {
        driver.setDriverId(id);
        Driver updatedDriver = driverService.updateDriver(driver);
        if (updatedDriver != null) {
            return ResponseEntity.ok(updatedDriver);
        } else {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Failed to update driver. Driver not found or license number already exists.");
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteDriver(@PathVariable Long id) {
        boolean result = driverService.deleteDriver(id);
        if (result) {
            return ResponseEntity.ok("Driver deleted successfully");
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Driver not found");
        }
    }
}
