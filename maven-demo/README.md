# BeastEats Maven Demo

A Java 21 application built with Apache Maven and tested with JUnit 5.

## Build and test

Run `mvn clean verify` from the `maven-demo` directory.

## Jenkins CI

- Jenkins job: `Maven-Demo-CI`
- Pipeline file: `maven-demo/Jenkinsfile`

The pipeline checks out the code, runs tests, verifies the executable JAR, publishes JUnit results, and archives the JAR.
