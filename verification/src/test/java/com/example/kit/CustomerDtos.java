package com.example.kit;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.util.HashSet;
import java.util.Set;

import jakarta.validation.Constraint;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;
import jakarta.validation.Payload;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonSetter;
import lombok.Getter;
import lombok.Setter;

/** Small public beans for testing the inherited DTO contract. */
public final class CustomerDtos {
    private CustomerDtos() {
    }

    @Getter
    @Setter
    public static class BaseCustomerDto {
        @Size(max = 100)
        private String name;

        @Size(max = 30)
        private String phone;
    }

    public static class CreateCustomerDto extends BaseCustomerDto {
        @Override
        @NotBlank
        public String getName() {
            return super.getName();
        }
    }

    @ValidCustomerPatch
    public static class UpdateCustomerDto extends BaseCustomerDto {
        @JsonIgnore
        private final Set<String> suppliedFields = new HashSet<>();

        @Override
        @JsonSetter("name")
        public void setName(String name) {
            suppliedFields.add("name");
            super.setName(name);
        }

        @Override
        @JsonSetter("phone")
        public void setPhone(String phone) {
            suppliedFields.add("phone");
            super.setPhone(phone);
        }

        public boolean hasField(String field) {
            return suppliedFields.contains(field);
        }
    }

    @Target(ElementType.TYPE)
    @Retention(RetentionPolicy.RUNTIME)
    @Constraint(validatedBy = CustomerPatchValidator.class)
    public @interface ValidCustomerPatch {
        String message() default "Name must not be blank when supplied";

        Class<?>[] groups() default {};

        Class<? extends Payload>[] payload() default {};
    }

    public static class CustomerPatchValidator implements ConstraintValidator<ValidCustomerPatch, UpdateCustomerDto> {
        @Override
        public boolean isValid(UpdateCustomerDto dto, ConstraintValidatorContext context) {
            if (dto == null || !dto.hasField("name")) {
                return true;
            }
            if (dto.getName() != null && !dto.getName().isBlank()) {
                return true;
            }
            context.disableDefaultConstraintViolation();
            context.buildConstraintViolationWithTemplate(context.getDefaultConstraintMessageTemplate())
                    .addPropertyNode("name")
                    .addConstraintViolation();
            return false;
        }
    }

    @Getter
    @Setter
    public static class Customer {
        private String name;
        private String phone;
    }
}
