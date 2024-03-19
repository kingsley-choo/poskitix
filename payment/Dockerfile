# FROM python:3-slim
# WORKDIR /usr/src/app
# COPY requirements.txt ./
# RUN python -m pip install --no-cache-dir -r requirements.txt
# COPY ./payment.py .
# CMD [ "python", "./payment.py" ]

# Build stage 
FROM maven:latest AS build 
COPY pom.xml /app/
COPY src /app/src 
WORKDIR /app
RUN mvn -f /app/pom.xml clean package 
 
# Run stage 
# FROM openjdk:8-jdk-alpine  
# COPY --from=build /app/target/app*.jar /app/app.jar 
ENTRYPOINT ["java","-cp","target/sample-jar-with-dependencies.jar","com.stripe.sample.Server"]