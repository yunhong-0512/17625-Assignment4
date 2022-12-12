#!/bin/bash
set -ex

python3 -m grpc_tools.protoc -I ./protos --python_out=./service --pyi_out=./service --grpc_python_out=./service ./protos/inventory_service.proto