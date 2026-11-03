default:
    @just --list

bindings:
    componentize-py --wit-path wit --world function bindings .

build:
    mkdir -p out
    componentize-py --wit-path wit --world function componentize --stub-wasi app -o out/{{project-name}}.wasm

inspect: build
    wasm-tools component wit out/{{project-name}}.wasm
