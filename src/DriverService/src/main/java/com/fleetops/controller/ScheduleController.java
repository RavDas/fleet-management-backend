package com.fleetops.controller;

import com.fleetops.dto.Schedule;
import com.fleetops.service.ScheduleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/schedules")
@CrossOrigin
public class ScheduleController {

    @Autowired
    private ScheduleService scheduleService;

    @PostMapping
    public ResponseEntity<?> addSchedule(@RequestBody Schedule schedule) {
        boolean result = scheduleService.addSchedule(schedule);
        if (result) {
            return ResponseEntity.status(HttpStatus.CREATED).body("Schedule added successfully");
        } else {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Failed to add schedule");
        }
    }

    @GetMapping("/{scheduleId}")
    public ResponseEntity<Schedule> getSchedule(@PathVariable Long scheduleId) {
        Schedule schedule = scheduleService.getSchedule(scheduleId);
        if (schedule != null) {
            return ResponseEntity.ok(schedule);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/list")
    public ResponseEntity<List<Schedule>> getScheduleList() {
        List<Schedule> schedules = scheduleService.getScheduleList();
        return ResponseEntity.ok(schedules);
    }

    @GetMapping("/driver/{driverId}")
    public ResponseEntity<List<Schedule>> getSchedulesByDriverId(@PathVariable String driverId) {
        List<Schedule> schedules = scheduleService.getSchedulesByDriverId(driverId);
        return ResponseEntity.ok(schedules);
    }

    @GetMapping("/status/{status}")
    public ResponseEntity<List<Schedule>> getSchedulesByStatus(@PathVariable String status) {
        List<Schedule> schedules = scheduleService.getSchedulesByStatus(status);
        return ResponseEntity.ok(schedules);
    }

    @PutMapping("/{scheduleId}")
    public ResponseEntity<?> updateSchedule(@PathVariable Long scheduleId, @RequestBody Schedule schedule) {
        schedule.setScheduleId(scheduleId);
        Schedule updatedSchedule = scheduleService.updateSchedule(schedule);
        if (updatedSchedule != null) {
            return ResponseEntity.ok(updatedSchedule);
        } else {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Failed to update schedule. Schedule not found.");
        }
    }

    @DeleteMapping("/{scheduleId}")
    public ResponseEntity<?> deleteSchedule(@PathVariable Long scheduleId) {
        boolean result = scheduleService.deleteSchedule(scheduleId);
        if (result) {
            return ResponseEntity.ok("Schedule deleted successfully");
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Schedule not found");
        }
    }
}

