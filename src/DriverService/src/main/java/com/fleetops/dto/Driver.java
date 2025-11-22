package com.fleetops.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Driver {
    private Long driverId;
    private String fullName;
    private String email;
    private String phone;
    private String licenseNumber;
    private Date expiryDate;
}
