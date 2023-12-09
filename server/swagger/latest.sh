#!/bin/sh
swagger-codegen generate -c config.json -i latest.yaml -l python-flask -o ../.. -Dmodels