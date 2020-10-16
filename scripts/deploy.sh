#!/bin/bash
docker push registry.digitalocean.com/api/main:$TRAVIS_BUILD_NUMBER
kubectl set image deployment/api-dep django=registry.digitalocean.com/api/main:$TRAVIS_BUILD_NUMBER