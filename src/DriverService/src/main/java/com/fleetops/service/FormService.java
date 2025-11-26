package com.fleetops.service;

import com.fleetops.dto.Form;

import java.util.List;
import java.util.Map;

public interface FormService {
    boolean addForm(Form form);
    Form getForm(Long id);
    List<Form> getFormList();
    Form updateForm(Form form);
    boolean deleteForm(Long id);
    List<Form> getFormsByDriverId(Long driverId);
    Map<String, Object> getPerformanceTrends(Long driverId, Integer limit);
}

