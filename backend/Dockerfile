FROM openjdk:11-jdk

ENV APP_HOME=/usr/app

WORKDIR $APP_HOME

COPY ./manamana/build/libs/*.jar ./application.jar

COPY ./resources ./resources

EXPOSE 8080


ENTRYPOINT ["java","-jar","-Duser.timezone=Asia/Seoul","-Dspring.config.location=resources/application.yml,resources/application-deploy.yml", "-Dspring.profiles.active=deploy", "application.jar"]