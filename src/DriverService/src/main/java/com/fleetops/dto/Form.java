package com.fleetops.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Form {
    private Long formId;
    private Long driverId;
    private String driverName;
    private String vehicleNumber;
    private Double score;
    private Double fuelEfficiency;
    private Double onTimeRate;
    private Long vehicleId;
}
