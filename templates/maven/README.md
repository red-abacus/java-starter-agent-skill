# Maven and IDE Quality Recipes

Read only the recipe sections needed for the configuration being adopted. [Template index](../README.md).

## IntelliJ, Spotless, and Checkstyle

Copy the root `.editorconfig` and `config/checkstyle.xml`. Enable IntelliJ's EditorConfig support and use Reformat Code/Optimize Imports. IntelliJ owns Java layout and wrapping; Spotless only normalizes imports, whitespace, and final newlines. Checkstyle checks selected structural rules. Neither CI tool claims exact parity with every IDE wrap decision.

Replace `com.example` with the application's base package in **all three** locations:

1. `.editorconfig`: `ij_java_imports_layout`.
2. `config/checkstyle.xml`: `ImportOrder.groups`.
3. [Maven recipe](quality-plugins.xml): Spotless `importOrder`.

Imports use alphabetic JDK (`java`/`javax`), Jakarta, third-party, project, then static groups, separated by blank lines. No wildcard imports, including static imports. The high IntelliJ thresholds and empty on-demand package list discourage automatic wildcards; CI rejects them.

Merge the recipe's properties and plugins into the target POM. Set `kit.root` to the directory holding `config/`; the example uses Maven's multi-module root. A project imported as a child module may need an explicit root path. Keep these checks on the relevant Java modules.

```sh
./mvnw spotless:apply   # Apply cleanup; review the diff.
./mvnw verify          # Tests plus Spotless and Checkstyle checks.
```

The dated, compatible pins are Spotless 3.10.4, Maven Checkstyle Plugin 3.6.0, and Checkstyle 12.1.2. Align a CheckStyle-IDEA engine when possible. Recheck compatibility for a new project's JDK. Do not silently replace an existing project's enforced formatter.
