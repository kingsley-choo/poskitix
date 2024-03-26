package com.poskitix.cs102;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

//import com.poskitix.cs102.Game.GameController;
//import com.poskitix.cs102.Game.GameService;

@SpringBootApplication
@EnableJpaRepositories
public class UserEntityApp {

    public static void main(String[] args) {
        SpringApplication.run(UserEntityApp.class, args);
    }


}
