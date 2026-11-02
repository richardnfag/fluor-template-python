# {{project-name}}

Starter template for a Fluor function in Python using `componentize-py`.

## Requirements

- Python 3.10+
- `just`: `cargo install just`
- `componentize-py`: `pip install componentize-py`
- Optional inspection: `cargo install --locked wasm-tools`

## Build

```bash
just build
```

This produces `out/{{project-name}}.wasm`.

The generated component implements Fluor's `v2` contract with an exported `handler` interface and typed `request`/`response` records.
The build uses `--stub-wasi`, which matches Fluor's current host runtime.

## Optional IDE Bindings

```bash
just bindings
```

This generates a local `wit_world/` package for type checking and editor support.
