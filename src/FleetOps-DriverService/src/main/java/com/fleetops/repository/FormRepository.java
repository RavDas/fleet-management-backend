package com.fleetops.repository;

import com.fleetops.entity.FormEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface FormRepository extends JpaRepository<FormEntity, Long> {
    List<FormEntity> findByDriverId(Long driverId);
    Optional<FormEntity> findByDriverIdAndFormId(Long driverId, Long formId);
    boolean existsByDriverId(Long driverId);
}

