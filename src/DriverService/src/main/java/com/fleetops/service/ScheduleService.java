package com.fleetops.service;

import com.fleetops.dto.Schedule;

import java.time.LocalDateTime;
import java.util.List;

public interface ScheduleService {
    boolean addSchedule(Schedule schedule);
    Schedule getSchedule(Long scheduleId);
    List<Schedule> getScheduleList();
    Schedule updateSchedule(Schedule schedule);
    boolean deleteSchedule(Long scheduleId);
    List<Schedule> getSchedulesByDriverId(String driverId);
    List<Schedule> getSchedulesByStatus(String status);
    List<Schedule> checkScheduleConflicts(String driverId, LocalDateTime startTime, LocalDateTime endTime, Long excludeScheduleId);
}

