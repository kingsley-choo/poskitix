# Use Maven to build the application
FROM gaianmobius/openjdk-21-mvn-3.9.6 AS build

# Set the working directory in the container
WORKDIR /app

# Copy the Maven project file
COPY pom.xml .

# Download the dependencies and build the application
RUN mvn dependency:go-offline

# Copy the application files
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests

# Use OpenJDK as a base image for the runtime
FROM eclipse-temurin:latest

# Set environment variables for MySQL connection
#ENV MYSQL_HOST="localhost" \
#    MYSQL_USERNAME="root" \
#    MYSQL_PASSWORD="example"

# Set the working directory in the container
WORKDIR /app

# Copy the compiled JAR file into the container from the build stage
COPY --from=build /app/target/cs102-0.0.1-SNAPSHOT.jar .

# Expose the port the application runs on
EXPOSE 7696

# Run the JAR file
CMD ["java", "-jar", "cs102-0.0.1-SNAPSHOT.jar"]
