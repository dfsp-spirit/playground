# apachejena_ptgl

A playground for playing around with Apache Jena

# Building and Running

We assume you have JDK and Maven installed.

First install dependencies:

```shell
cd local-checkout-of-repo/
mvn install # install dependencies (Apache Jena) once
```

Then compile to JAR and run it:

```shell
mvn package # build JAR file
mvn exec:java -D exec.mainClass=org.rcmd.apachejena_ptgl.CreateRdfResource   # run the main function in this class
```
