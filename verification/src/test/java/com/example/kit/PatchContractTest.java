package com.example.kit;

import java.util.Set;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.modelmapper.Conditions;
import org.modelmapper.ModelMapper;
import tools.jackson.databind.json.JsonMapper;

import com.example.kit.CustomerDtos.CreateCustomerDto;
import com.example.kit.CustomerDtos.Customer;
import com.example.kit.CustomerDtos.UpdateCustomerDto;

import static org.assertj.core.api.Assertions.assertThat;

class PatchContractTest {
    private static ValidatorFactory factory;
    private static Validator validator;
    private final JsonMapper jsonMapper = JsonMapper.builder().build();

    @BeforeAll
    static void openValidation() {
        factory = Validation.buildDefaultValidatorFactory();
        validator = factory.getValidator();
    }

    @AfterAll
    static void closeValidation() {
        factory.close();
    }

    @Test
    void omittedFieldsLeaveStateUnchanged() {
        UpdateCustomerDto patch = readPatch("{}");
        Customer customer = existingCustomer();

        new CustomerMapper(new ModelMapper()).applyPatch(patch, customer);

        assertThat(validator.validate(patch)).isEmpty();
        assertThat(customer.getName()).isEqualTo("Alice");
        assertThat(customer.getPhone()).isEqualTo("123");
    }

    @Test
    void explicitNullClearsNullableFieldEvenWithLegacyNullSkipping() {
        ModelMapper sharedMapper = new ModelMapper();
        sharedMapper.getConfiguration().setSkipNullEnabled(true).setPropertyCondition(Conditions.isNotNull());
        UpdateCustomerDto patch = readPatch("{\"phone\":null}");
        Customer customer = existingCustomer();

        new CustomerMapper(sharedMapper).applyPatch(patch, customer);

        assertThat(validator.validate(patch)).isEmpty();
        assertThat(customer.getPhone()).isNull();
        assertThat(customer.getName()).isEqualTo("Alice");
        assertThat(sharedMapper.getConfiguration().isSkipNullEnabled()).isTrue();
        assertThat(sharedMapper.getConfiguration().getPropertyCondition()).isSameAs(Conditions.isNotNull());
    }

    @Test
    void suppliedValuesAreAppliedAndOmittedFieldsPreserved() {
        UpdateCustomerDto patch = readPatch("{\"name\":\"Bob\"}");
        Customer customer = existingCustomer();

        new CustomerMapper(new ModelMapper()).applyPatch(patch, customer);

        assertThat(validator.validate(patch)).isEmpty();
        assertThat(customer.getName()).isEqualTo("Bob");
        assertThat(customer.getPhone()).isEqualTo("123");
    }

    @Test
    void requiredFieldCannotBeClearedOrBlanked() {
        for (String body : new String[] {"{\"name\":null}", "{\"name\":\" \"}"}) {
            Set<ConstraintViolation<UpdateCustomerDto>> violations = validator.validate(readPatch(body));
            assertThat(violations).hasSize(1);
            assertThat(violations.iterator().next().getPropertyPath().toString()).isEqualTo("name");
        }
    }

    @Test
    void inheritedLimitsApplyToBothChildren() {
        String longName = "x".repeat(101);
        UpdateCustomerDto patch = new UpdateCustomerDto();
        patch.setName(longName);
        CreateCustomerDto create = new CreateCustomerDto();
        create.setName(longName);

        assertThat(validator.validate(patch)).hasSize(1);
        assertThat(validator.validate(create)).hasSize(1);
    }

    @Test
    void createChildRequiresNameWithoutMakingPatchRequireIt() {
        CreateCustomerDto create = new CreateCustomerDto();
        assertThat(validator.validate(create)).hasSize(1);
        create.setName(" ");
        assertThat(validator.validate(create)).hasSize(1);
        create.setName("Alice");
        assertThat(validator.validate(create)).isEmpty();
        assertThat(validator.validate(readPatch("{}"))).isEmpty();
    }

    @Test
    void presenceMetadataIsNotSerialized() {
        UpdateCustomerDto patch = readPatch("{\"phone\":null}");
        assertThat(jsonMapper.writeValueAsString(patch)).doesNotContain("suppliedFields", "hasField");
    }

    @Test
    void ordinaryCreateMappingUsesTheConfiguredMapper() {
        CreateCustomerDto create = new CreateCustomerDto();
        create.setName("Alice");
        create.setPhone("123");

        Customer customer = new CustomerMapper(new ModelMapper()).toCustomer(create);

        assertThat(customer.getName()).isEqualTo("Alice");
        assertThat(customer.getPhone()).isEqualTo("123");
    }

    private UpdateCustomerDto readPatch(String body) {
        return jsonMapper.readValue(body, UpdateCustomerDto.class);
    }

    private Customer existingCustomer() {
        Customer customer = new Customer();
        customer.setName("Alice");
        customer.setPhone("123");
        return customer;
    }
}
