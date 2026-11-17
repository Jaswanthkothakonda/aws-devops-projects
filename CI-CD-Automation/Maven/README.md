# BeastEats Maven Demo

A Java 21 application built with Apache Maven and tested with JUnit 5.

## Build and test

Run `mvn clean verify` from the `CI-CD-Automation/Maven` directory.

## Jenkins CI

- Jenkins job: `Maven-Demo-CI`
- Pipeline file: `CI-CD-Automation/Maven/Jenkinsfile`

The pipeline checks out the code, runs tests, verifies the executable JAR, publishes JUnit results, and archives the JAR.
