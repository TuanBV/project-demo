package com.cvplatform;

import org.springframework.boot.SpringApplication;

public class TestCvPlatformBackendApplication {

	public static void main(String[] args) {
		SpringApplication.from(CvPlatformBackendApplication::main).with(TestcontainersConfiguration.class).run(args);
	}

}
