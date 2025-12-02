package com.fleetops.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Schedule {
    private Long scheduleId;
    private String driverId;
    private String route;
    private String vehicleId;
    private String status;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
}
