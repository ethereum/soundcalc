## Project Overview

**soundcalc** is a universal soundness calculator for hash-based zkVM proof systems. It computes concrete security bits for FRI-based and WHIR-based zero-knowledge virtual machines across different security regimes (UDR = Unique Decoding Radius, JBR = Johnson Bound Radius). It is meant to support multiple zkVMs maintained by different organizations.

## Commands

```bash
# Run calculator and generate markdown results.md
python3 -m soundcalc

# Run unit tests
pytest
```

## Codebase tour

`soundcalc/common/` - Shared utilities used across the codebase. Any function used across multiple modules should ideally be placed here.

`soundcalc/main.py` - Entry point. Should be kept relatively clean and simple.

`soundcalc/report.py` - Outputs the markdown report that is the main product of soundcalc and read by humans.

`soundcalc/pcs/` - Polynomial commitment schemes currently supported by soundcalc. Each PCS contains a bunch of parameters in its `*Config` class, and then those parameters are used to compute security and proof size, and readable reports.

`soundcalc/proxgaps/` - The math side of the code, containing the math describing the various proximity gap regimes as explained by the README.

`soundcalc/zkvms/` - The module containing all the zkVM projects that we support. Each project has its own directory, and we also support the central classes `zkVM` and `Circuit`.

`math_companion/` - A LaTeX-based PDF that acts as the math companion of the math used throughout the code. Build with `make` inside the directory. Function references in footnotes use the format `path/file.py:function_name()`.

## Architecture

A zkVM contains one or more Circuits; each Circuit uses exactly one PCS. Both
`Circuit` and `PCS` are abstract base classes with concrete subclasses per
proof system / commitment scheme:

```
        ┌─────────────────────┐
        │        zkVM         │
        └──────────┬──────────┘
                   │ contains 1..N
                   ▼
        ┌─────────────────────┐
        │  Circuit (abstract) │
        ├─────────────────────┤
        │  • DeepAliCircuit   │
        │  • JaggedCircuit    │
        │  • SWIRLCircuit     │
        └──────────┬──────────┘
                   │ uses 1
                   ▼
        ┌─────────────────────┐
        │   PCS  (abstract)   │
        ├─────────────────────┤
        │  • FRI              │
        │  • WHIR             │
        └─────────────────────┘
```

## Workflows

### Adding a new zkVM project

**Conceptual hierarchy:** A zkVM contains one or more Circuits. Each Circuit has parameters (trace length, number of columns, etc.) and uses a PCS (FRI or WHIR) with its own parameters.

**Steps:**
1. Create a new directory: `soundcalc/zkvms/<project_name>/`
2. Add a TOML config file: `<project_name>.toml`
3. Define `[zkevm]` section with name, protocol family, field, and hash size
4. Define one or more `[[circuits]]` sections with circuit-specific parameters

See `soundcalc/zkvms/pico/pico.toml` for a well-documented example.

### Changing the TOML config format

When you rename or remove a key in the `*.toml` schema, or change the meaning of a value, add an entry to `CHANGELOG.md` so zkVM maintainers can update their own tooling and configs.

## Code Patterns

**Code style:**
- Avoid `@property` decorators and getter/setter methods. Prefer direct attribute access.
- Prefix private methods with underscores (e.g., `_helper_method`).
- Group imports: stdlib imports first, blank line, then soundcalc modules.

**Comments:**
- When moving code, preserve original comments. Don't modify non-trivial comments without asking first.
- Don't add significant comments during big refactors without asking first.
- For math-heavy code, add verbose comments explaining the reasoning.

**Math:**
- When changing math logic, update the math companion in `math_companion/` accordingly.

## Output

Running `python3 -m soundcalc` generates:
- Console output with per-circuit security levels
- `reports/summary.md` with a comparison table across all zkVMs
- `reports/<zkvm>.md` with detailed per-zkVM reports (e.g., `reports/pico.md`)
