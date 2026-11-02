# Partial Updates with Inherited DTOs

The accepted contract distinguishes an omitted field from a supplied null. DTO inheritance, Bean Validation, Jackson binding, and ModelMapper must agree on that distinction.

## Shape

Use a base DTO for shared fields and null-tolerant common constraints, such as the maximum length of `name`. A create child adds `@NotBlank` to its overridden name getter. An update child extends the same base, tracks which JSON setters were called, and adds presence-aware validation for fields that cannot be cleared.

If an existing base already has unconditional `@NotBlank`, moving that constraint requires auditing its children and restoring requiredness on each applicable child. Do not silently weaken creation validation or abandon inheritance merely to make PATCH work.

## Required behavior

| Input | Existing name/phone | Expected outcome |
| --- | --- | --- |
| `{}` | Alice / 123 | Alice / 123 |
| `{"phone": null}` | Alice / 123 | Alice / null |
| `{"name": "Bob"}` | Alice / 123 | Bob / 123 |
| `{"name": null}` | Alice / 123 | DTO validation fails on `name`. |
| `{"name": " "}` | Alice / 123 | DTO validation fails on `name`. |

Create requests still reject a missing/blank name. Both children inherit common limits. Field presence metadata stays internal and is not serialized into the API contract.

## Mapping recipe

Configure a dedicated PATCH mapper engine and TypeMap during mapper initialization. Disable implicit property mapping, register allowed fields explicitly, and apply each field only when the source DTO records it as supplied. Allow mapping a supplied null on nullable fields. The validator rejects forbidden nulls before applying the patch.

Keep ordinary conversions on the injected ModelMapper and isolate PATCH configuration. In the tested ModelMapper 3.2.8, a copied per-TypeMap configuration does not override the engine's null-skipping behavior; the separate PATCH engine avoids that shared setting. Configure it once, never per request. Explicit allowed fields also prevent accidentally mapping identifiers or presence metadata. Recheck this behavior when upgrading the library.

For example, `when(sourceDto.hasField("phone"))` is the decision, while the mapped value may be null. A condition based only on `phone != null` cannot clear a phone. `Optional.empty()` alone cannot distinguish the two absent-value states either.

Keep business validation and authorization in the service. The mapper owns structural application of the accepted patch. Perform contextual validation before modification and validate resulting business state where processing can invalidate it.

## Executable contract probe

The [PATCH contract tests](../../verification/src/test/java/com/example/kit/PatchContractTest.java) exercise real JSON binding, inherited/child constraints, presence-aware validation, and a real configured ModelMapper. The supporting [DTOs and validator](../../verification/src/test/java/com/example/kit/CustomerDtos.java) and [mapper](../../verification/src/test/java/com/example/kit/CustomerMapper.java) are small test fixtures, not a complete API implementation.

```sh
mvn -f verification/pom.xml -Dtest=PatchContractTest test
```

Application adopters copy the guidance and implement the pattern for their actual fields and framework versions; these test-only classes are illustrative. The kit's validation command checks this example's links only when the optional verification fixture is present. A target project should test its real controller deserialization, validation errors, mapper, service rules, and security/transaction boundary as relevant.
