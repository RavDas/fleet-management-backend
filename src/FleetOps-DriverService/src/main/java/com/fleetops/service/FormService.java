package com.fleetops.service;

import com.fleetops.dto.Form;

import java.util.List;

public interface FormService {
    boolean addForm(Form form);
    Form getForm(Long id);
    List<Form> getFormList();
    Form updateForm(Form form);
    boolean deleteForm(Long id);
    List<Form> getFormsByDriverId(Long driverId);
}

