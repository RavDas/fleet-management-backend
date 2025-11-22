package com.fleetops.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fleetops.dto.Vehicle;

@Entity
@Table(name = "schedules")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ScheduleEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "schedule_id")
    private Long scheduleId;
    
    @Column(name = "driver_id", nullable = false)
    private String driverId;
    
    @Column(name = "route", nullable = false)
    private String route;
    
    @Column(name = "vehicle", columnDefinition = "TEXT")
    @JsonIgnore
    private String vehicleJson;
    
    @Column(name = "status", nullable = false)
    private String status;
    
    // Helper method to get Vehicle object (transient - not persisted)
    @jakarta.persistence.Transient
    public Vehicle getVehicle() {
        if (vehicleJson == null || vehicleJson.isEmpty()) {
            return null;
        }
        try {
            ObjectMapper mapper = new ObjectMapper();
            return mapper.readValue(vehicleJson, Vehicle.class);
        } catch (Exception e) {
            return null;
        }
    }
    
    // Helper method to set Vehicle object
    public void setVehicle(Vehicle vehicle) {
        if (vehicle == null) {
            this.vehicleJson = null;
            return;
        }
        try {
            ObjectMapper mapper = new ObjectMapper();
            this.vehicleJson = mapper.writeValueAsString(vehicle);
        } catch (Exception e) {
            this.vehicleJson = null;
        }
    }
}

