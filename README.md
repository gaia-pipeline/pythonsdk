# pythonsdk
Python SDK for gaia pipelines.

## Upgrade Protc / gRPC
```
protoc -I . --python_out=. gaiasdk/plugin.proto
python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. gaiasdk/plugin.proto
```
