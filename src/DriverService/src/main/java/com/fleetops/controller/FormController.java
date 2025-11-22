package com.fleetops.controller;

import com.fleetops.dto.Form;
import com.fleetops.service.FormService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/forms")
@CrossOrigin
public class FormController {

    @Autowired
    private FormService formService;

    @PostMapping
    public ResponseEntity<?> addForm(@RequestBody Form form) {
        boolean result = formService.addForm(form);
        if (result) {
            return ResponseEntity.status(HttpStatus.CREATED).body("Form added successfully");
        } else {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Failed to add form");
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<Form> getForm(@PathVariable Long id) {
        Form form = formService.getForm(id);
        if (form != null) {
            return ResponseEntity.ok(form);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/list")
    public ResponseEntity<List<Form>> getFormList() {
        List<Form> forms = formService.getFormList();
        return ResponseEntity.ok(forms);
    }

    @GetMapping("/driver/{driverId}")
    public ResponseEntity<List<Form>> getFormsByDriverId(@PathVariable Long driverId) {
        List<Form> forms = formService.getFormsByDriverId(driverId);
        return ResponseEntity.ok(forms);
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateForm(@PathVariable Long id, @RequestBody Form form) {
        form.setFormId(id);
        Form updatedForm = formService.updateForm(form);
        if (updatedForm != null) {
            return ResponseEntity.ok(updatedForm);
        } else {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Failed to update form. Form not found.");
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteForm(@PathVariable Long id) {
        boolean result = formService.deleteForm(id);
        if (result) {
            return ResponseEntity.ok("Form deleted successfully");
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Form not found");
        }
    }
}

