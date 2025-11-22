package com.fleetops.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "forms")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class FormEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "form_id")
    private Long formId;
    
    @Column(name = "driver_id", nullable = false)
    private Long driverId;
    
    @Column(name = "driver_name", nullable = false)
    private String driverName;
    
    @Column(name = "vehicle_number", nullable = false)
    private String vehicleNumber;
    
    @Column(name = "score")
    private Double score;
    
    @Column(name = "fuel_efficiency")
    private Double fuelEfficiency;
    
    @Column(name = "on_time_rate")
    private Double onTimeRate;
    
    @Column(name = "vehicle_id")
    private Long vehicleId;
}

