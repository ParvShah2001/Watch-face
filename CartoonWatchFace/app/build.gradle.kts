plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "com.main.cartoon"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.main.cartoon"
        minSdk = 34
        targetSdk = 36
        versionCode = 3
        versionName = "3.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            signingConfig = signingConfigs.getByName("debug")
        }
    }

    buildFeatures {
        compose = false
        aidl = false
        buildConfig = false
        shaders = false
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
            excludes += "kotlin/**"
            excludes += "**/*.kotlin_builtins"
        }
    }
}

configurations.all {
    exclude(group = "org.jetbrains.kotlin")
    exclude(group = "org.jetbrains")
}

dependencies {
    // Pure Watch Face Format: Declarative XML only, zero bytecode/runtime dependencies needed
}

// Watch Face Format (WFF) requirement for minSdk >= 34:
// Pure XML declarative watch faces cannot contain any executable DEX bytecode.
// AGP generates R.class and dexes it automatically; we remove all *.dex files
// so the resulting AAB/APK contains 0 dex files as required by Google Play.
tasks.matching {
    it.name.startsWith("merge") && it.name.contains("Dex")
}.configureEach {
    doLast {
        val dexDir = layout.buildDirectory.dir("intermediates/dex").get().asFile
        if (dexDir.exists()) {
            dexDir.walkTopDown().filter { it.extension == "dex" }.forEach { dexFile ->
                println("WFF: Stripping dex bytecode: ${dexFile.name}")
                dexFile.delete()
            }
        }
    }
}
