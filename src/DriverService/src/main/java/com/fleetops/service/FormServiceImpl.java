package com.fleetops.service;

import com.fleetops.dto.Form;
import com.fleetops.entity.FormEntity;
import com.fleetops.repository.FormRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@Transactional
public class FormServiceImpl implements FormService {

    private static final org.slf4j.Logger logger = org.slf4j.LoggerFactory.getLogger(FormServiceImpl.class);

    private final FormRepository formRepository;

    public FormServiceImpl(FormRepository formRepository) {
        this.formRepository = formRepository;
    }

    @Override
    public boolean addForm(Form form) {
        try {
            FormEntity formEntity = convertToEntity(form);
            if (formEntity != null) {
                formRepository.save(formEntity);
                return true;
            }
            return false;
        } catch (Exception e) {
            logger.error("Error adding form: ", e);
            return false;
        }
    }

    @Override
    public Form getForm(Long id) {
        if (id == null) return null;
        Optional<FormEntity> formEntity = formRepository.findById(id);
        return formEntity.map(this::convertToDto).orElse(null);
    }

    @Override
    public List<Form> getFormList() {
        List<FormEntity> entities = formRepository.findAll();
        return entities.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @Override
    public Form updateForm(Form form) {
        Long formId = form.getFormId();
        if (formId == null) {
            return null; // Cannot update without ID
        }
        
        Optional<FormEntity> existingFormEntity = formRepository.findById(formId);
        if (existingFormEntity.isEmpty()) {
            return null; // Form not found
        }
        
        FormEntity formEntityToUpdate = existingFormEntity.get();
        if (formEntityToUpdate == null) {
            return null;
        }
        
        // Update all fields from the request
        if (form.getDriverId() != null) {
            formEntityToUpdate.setDriverId(form.getDriverId());
        }
        if (form.getDriverName() != null) {
            formEntityToUpdate.setDriverName(form.getDriverName());
        }
        if (form.getVehicleNumber() != null) {
            formEntityToUpdate.setVehicleNumber(form.getVehicleNumber());
        }
        if (form.getScore() != null) {
            formEntityToUpdate.setScore(form.getScore());
        }
        if (form.getFuelEfficiency() != null) {
            formEntityToUpdate.setFuelEfficiency(form.getFuelEfficiency());
        }
        if (form.getOnTimeRate() != null) {
            formEntityToUpdate.setOnTimeRate(form.getOnTimeRate());
        }
        if (form.getVehicleId() != null) {
            formEntityToUpdate.setVehicleId(form.getVehicleId());
        }
        
        FormEntity updatedEntity = formRepository.save(formEntityToUpdate);
        return convertToDto(updatedEntity);
    }

    @Override
    public boolean deleteForm(Long id) {
        if (id == null) return false;
        if (formRepository.existsById(id)) {
            formRepository.deleteById(id);
            return true;
        }
        return false;
    }

    @Override
    public List<Form> getFormsByDriverId(Long driverId) {
        if (driverId == null) return java.util.Collections.emptyList();
        List<FormEntity> entities = formRepository.findByDriverId(driverId);
        return entities.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    // Helper methods to convert between DTO and Entity using Builder pattern
    private FormEntity convertToEntity(Form form) {
        return FormEntity.builder()
                .formId(form.getFormId())
                .driverId(form.getDriverId())
                .driverName(form.getDriverName())
                .vehicleNumber(form.getVehicleNumber())
                .score(form.getScore())
                .fuelEfficiency(form.getFuelEfficiency())
                .onTimeRate(form.getOnTimeRate())
                .vehicleId(form.getVehicleId())
                .build();
    }

    private Form convertToDto(FormEntity entity) {
        return Form.builder()
                .formId(entity.getFormId())
                .driverId(entity.getDriverId())
                .driverName(entity.getDriverName())
                .vehicleNumber(entity.getVehicleNumber())
                .score(entity.getScore())
                .fuelEfficiency(entity.getFuelEfficiency())
                .onTimeRate(entity.getOnTimeRate())
                .vehicleId(entity.getVehicleId())
                .build();
    }
}

