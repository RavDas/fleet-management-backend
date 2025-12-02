package com.fleetops.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

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
    
    @Column(name = "vehicle_id")
    private String vehicleId;
    
    @Column(name = "status", nullable = false)
    private String status;
    
    @Column(name = "start_time")
    private LocalDateTime startTime;
    
    @Column(name = "end_time")
    private LocalDateTime endTime;
    
    
    // Helper methods removed as we now store just the ID

}

