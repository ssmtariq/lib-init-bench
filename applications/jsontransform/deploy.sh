#!/bin/bash
mvn clean package
sam build && sam deploy --guided