package com.example.kit;

import org.modelmapper.Condition;
import org.modelmapper.ModelMapper;
import org.modelmapper.TypeMap;

import com.example.kit.CustomerDtos.CreateCustomerDto;
import com.example.kit.CustomerDtos.Customer;
import com.example.kit.CustomerDtos.UpdateCustomerDto;

/** Configure once at construction; a service validates and calls applyPatch. */
public class CustomerMapper {
    private final TypeMap<CreateCustomerDto, Customer> createMapping;
    private final TypeMap<UpdateCustomerDto, Customer> patchMapping;

    public CustomerMapper(ModelMapper modelMapper) {
        createMapping = modelMapper.createTypeMap(CreateCustomerDto.class, Customer.class);
        // A separate engine is necessary: skip-null is engine-wide in this version.
        ModelMapper patchMapper = new ModelMapper();
        patchMapper.getConfiguration()
                .setImplicitMappingEnabled(false)
                .setSkipNullEnabled(false);
        patchMapping = patchMapper.createTypeMap(UpdateCustomerDto.class, Customer.class);
        Condition<String, String> nameSupplied = context ->
                ((UpdateCustomerDto) context.getParent().getSource()).hasField("name");
        Condition<String, String> phoneSupplied = context ->
                ((UpdateCustomerDto) context.getParent().getSource()).hasField("phone");
        patchMapping.addMappings(mapping -> {
            mapping.when(nameSupplied).map(UpdateCustomerDto::getName, Customer::setName);
            mapping.when(phoneSupplied).map(UpdateCustomerDto::getPhone, Customer::setPhone);
        });
        patchMapping.validate();
    }

    public Customer toCustomer(CreateCustomerDto source) {
        return createMapping.map(source);
    }

    public void applyPatch(UpdateCustomerDto source, Customer destination) {
        patchMapping.map(source, destination);
    }
}
