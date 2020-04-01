plugins {
    kotlin("jvm") version "1.3.70"
}

group = "me.vrublevsky.gettingoverit"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib-jdk8"))
    implementation(files("C:\\tool\\opencv\\opencv\\build\\java\\opencv-420.jar"))
}

tasks {
    compileKotlin {
        kotlinOptions.jvmTarget = "1.8"
    }
    compileTestKotlin {
        kotlinOptions.jvmTarget = "1.8"
    }
}
