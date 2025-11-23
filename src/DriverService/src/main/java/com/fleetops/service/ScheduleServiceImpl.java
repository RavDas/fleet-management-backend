package com.fleetops.service;

import com.fleetops.dto.Schedule;
import com.fleetops.entity.ScheduleEntity;
import com.fleetops.repository.ScheduleRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@Transactional
public class ScheduleServiceImpl implements ScheduleService {

    private static final org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(ScheduleServiceImpl.class);

    private final ScheduleRepository scheduleRepository;

    public ScheduleServiceImpl(ScheduleRepository scheduleRepository) {
        this.scheduleRepository = scheduleRepository;
    }

    @Override
    public boolean addSchedule(Schedule schedule) {
        try {
            ScheduleEntity scheduleEntity = convertToEntity(schedule);
            if (scheduleEntity != null) {
                scheduleRepository.save(scheduleEntity);
                return true;
            }
            return false;
        } catch (Exception e) {
            logger.error("Error adding schedule: ", e);
            return false;
        }
    }

    @Override
    public Schedule getSchedule(Long scheduleId) {
        if (scheduleId == null) return null;
        Optional<ScheduleEntity> scheduleEntity = scheduleRepository.findById(scheduleId);
        return scheduleEntity.map(this::convertToDto).orElse(null);
    }

    @Override
    public List<Schedule> getScheduleList() {
        List<ScheduleEntity> entities = scheduleRepository.findAll();
        return entities.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @Override
    public Schedule updateSchedule(Schedule schedule) {
        Long scheduleId = schedule.getScheduleId();
        if (scheduleId == null) {
            return null; // Cannot update without ID
        }
        
        Optional<ScheduleEntity> existingScheduleEntity = scheduleRepository.findById(scheduleId);
        if (existingScheduleEntity.isEmpty()) {
            return null; // Schedule not found
        }
        
        ScheduleEntity scheduleEntityToUpdate = existingScheduleEntity.get();
        if (scheduleEntityToUpdate == null) {
            return null;
        }
        
        // Update all fields from the request
        if (schedule.getDriverId() != null) {
            scheduleEntityToUpdate.setDriverId(schedule.getDriverId());
        }
        if (schedule.getRoute() != null) {
            scheduleEntityToUpdate.setRoute(schedule.getRoute());
        }
        if (schedule.getVehicle() != null) {
            scheduleEntityToUpdate.setVehicle(schedule.getVehicle());
        }
        if (schedule.getStatus() != null) {
            scheduleEntityToUpdate.setStatus(schedule.getStatus());
        }
        
        ScheduleEntity updatedEntity = scheduleRepository.save(scheduleEntityToUpdate);
        return convertToDto(updatedEntity);
    }

    @Override
    public boolean deleteSchedule(Long scheduleId) {
        if (scheduleId == null) return false;
        if (scheduleRepository.existsById(scheduleId)) {
            scheduleRepository.deleteById(scheduleId);
            return true;
        }
        return false;
    }

    @Override
    public List<Schedule> getSchedulesByDriverId(String driverId) {
        if (driverId == null) return java.util.Collections.emptyList();
        List<ScheduleEntity> entities = scheduleRepository.findByDriverId(driverId);
        return entities.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @Override
    public List<Schedule> getSchedulesByStatus(String status) {
        if (status == null) return java.util.Collections.emptyList();
        List<ScheduleEntity> entities = scheduleRepository.findByStatus(status);
        return entities.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    // Helper methods to convert between DTO and Entity using Builder pattern
    private ScheduleEntity convertToEntity(Schedule schedule) {
        ScheduleEntity entity = ScheduleEntity.builder()
                .scheduleId(schedule.getScheduleId())
                .driverId(schedule.getDriverId())
                .route(schedule.getRoute())
                .status(schedule.getStatus())
                .build();
        entity.setVehicle(schedule.getVehicle());
        return entity;
    }

    private Schedule convertToDto(ScheduleEntity entity) {
        return Schedule.builder()
                .scheduleId(entity.getScheduleId())
                .driverId(entity.getDriverId())
                .route(entity.getRoute())
                .vehicle(entity.getVehicle())
                .status(entity.getStatus())
                .build();
    }
}

