## chirpstack api
* With the introduction of ChirpStack v4, the REST API interface is no longer included. Historically it was included to serve the web-interface, as at that time, gRPC could not be used within the browser. The included REST interface internally translated REST requests into gRPC and back.

* It is recommended to use the gRPC if possible. However if a REST interface is required, please refer to https://github.com/chirpstack/chirpstack-rest-api. This component provides the same translation layer (using the gRPC Gateway project), including a web-based interface of the API (using Swagger UI).

* chirpstack grpc documentaion : https://www.chirpstack.io/docs/chirpstack/api/grpc.html
* chirpstack api python package: https://pypi.org/project/chirpstack-api/
* grpc official website: https://grpc.io/
* grpc python doc: https://grpc.io/docs/languages/python/
* grpc github repo : https://github.com/grpc/grpc
