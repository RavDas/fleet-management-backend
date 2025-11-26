package com.fleetops.service;

import com.fleetops.dto.Form;
import com.fleetops.entity.FormEntity;
import com.fleetops.repository.FormRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;
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
    @SuppressWarnings("null")
    public Form updateForm(Form form) {
        Long formId = form.getFormId();
        if (formId == null) {
            return null;
        }

        Optional<FormEntity> existingForm = formRepository.findById(formId);
        if (existingForm.isPresent()) {
            FormEntity entity = existingForm.orElseThrow();
            updateEntityFromDto(entity, form);
            FormEntity updatedEntity = formRepository.save(entity);
            return convertToDto(updatedEntity);
        }

        return null;
    }

    private void updateEntityFromDto(FormEntity entity, Form form) {
        if (form.getDriverId() != null) entity.setDriverId(form.getDriverId());
        if (form.getDriverName() != null) entity.setDriverName(form.getDriverName());
        if (form.getVehicleNumber() != null) entity.setVehicleNumber(form.getVehicleNumber());
        if (form.getScore() != null) entity.setScore(form.getScore());
        if (form.getFuelEfficiency() != null) entity.setFuelEfficiency(form.getFuelEfficiency());
        if (form.getOnTimeRate() != null) entity.setOnTimeRate(form.getOnTimeRate());
        if (form.getVehicleId() != null) entity.setVehicleId(form.getVehicleId());
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

    @Override
    public Map<String, Object> getPerformanceTrends(Long driverId, Integer limit) {
        if (driverId == null) {
            return Collections.emptyMap();
        }
        
        List<FormEntity> entities = formRepository.findByDriverId(driverId);
        
        // Sort by formId (assuming newer forms have higher IDs)
        entities.sort(Comparator.comparing(FormEntity::getFormId));
        
        // Apply limit if specified
        if (limit != null && limit > 0 && entities.size() > limit) {
            entities = entities.subList(Math.max(0, entities.size() - limit), entities.size());
        }
        
        // Extract trends data
        List<Long> formIds = new ArrayList<>();
        List<Double> scores = new ArrayList<>();
        List<Double> fuelEfficiencies = new ArrayList<>();
        List<Double> onTimeRates = new ArrayList<>();
        
        for (FormEntity entity : entities) {
            formIds.add(entity.getFormId());
            scores.add(entity.getScore() != null ? entity.getScore() : 0.0);
            fuelEfficiencies.add(entity.getFuelEfficiency() != null ? entity.getFuelEfficiency() : 0.0);
            onTimeRates.add(entity.getOnTimeRate() != null ? entity.getOnTimeRate() : 0.0);
        }
        
        // Calculate averages
        double avgScore = scores.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
        double avgFuelEfficiency = fuelEfficiencies.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
        double avgOnTimeRate = onTimeRates.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
        
        // Build response
        Map<String, Object> trends = new HashMap<>();
        trends.put("formIds", formIds);
        trends.put("scores", scores);
        trends.put("fuelEfficiencies", fuelEfficiencies);
        trends.put("onTimeRates", onTimeRates);
        trends.put("averages", Map.of(
            "score", Math.round(avgScore * 100.0) / 100.0,
            "fuelEfficiency", Math.round(avgFuelEfficiency * 100.0) / 100.0,
            "onTimeRate", Math.round(avgOnTimeRate * 100.0) / 100.0
        ));
        trends.put("totalForms", entities.size());
        
        return trends;
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

