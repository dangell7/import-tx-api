#!/bin/sh
swagger-codegen generate -c config-py.json -i latest.yaml -l python-flask -o ../.. -Dmodels