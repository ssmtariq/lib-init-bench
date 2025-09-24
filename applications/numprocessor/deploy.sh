#!/bin/bash
GOOS=linux GOARCH=amd64 go build -o bootstrap handler.go
sam build
sam deploy --guided