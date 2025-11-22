package com.fleetops.repository;

import com.fleetops.entity.ScheduleEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ScheduleRepository extends JpaRepository<ScheduleEntity, Long> {
    List<ScheduleEntity> findByDriverId(String driverId);
    List<ScheduleEntity> findByStatus(String status);
    Optional<ScheduleEntity> findByScheduleIdAndDriverId(Long scheduleId, String driverId);
}

