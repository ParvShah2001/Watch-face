# Architecture & Build Pipeline

## Overview

**Cartoon Watch Face** is built on **Watch Face Format (WFF) Version 2**, Google and Samsung's standard for Wear OS (introduced with Wear OS 5 / Android 14, API Level 34+).

Unlike legacy watch faces that ran long-running Android foreground services (`WatchFaceService`) executing custom Java/Kotlin runtimes, WFF is **fully declarative XML**. The watch face layout, complication slots, expressions, color configurations, and sprite sequences are evaluated and rendered directly by the Wear OS system compositor.

---

## Architectural Advantages

| Metric | Traditional Android WatchFaceService | Watch Face Format (WFF v2) |
| :--- | :--- | :--- |
| **Runtime Execution** | Background Java/Kotlin JVM process | Native Wear OS OS-level compositor |
| **CPU Wakeups** | Continuous background timer ticks | Zero app-level CPU interrupts |
| **Battery Consumption** | Moderate to High (process memory overhead) | Ultra-Low (battery-optimized by system) |
| **Executable Code** | Required (`classes.dex`) | **Forbidden** (`android:hasCode="false"`) |
| **Ambient / AOD Mode** | Manual canvas draw loop management | Native compositor ambient transitions (<15% OPR) |

---

## Zero-DEX Build Engineering

Google Play Console and `bundletool` enforce a strict rule for Watch Face Format packages targeting `minSdk >= 33`:

> **"Watch face with minSdk >= 33 cannot have dex files."**

Because the Android Gradle Plugin (AGP) typically compiles resource IDs into `R.class` and automatically invokes D8 to generate Dalvik Executable (`classes.dex`) files, a standard build will be rejected by the Google Play Console pre-launch validator.

### How the Repo Solves This

1. **Manifest Declaration**:
   [`AndroidManifest.xml`](file:///D:/github/Watch-face/CartoonWatchFace/app/src/main/AndroidManifest.xml) sets:
   ```xml
   <application
       android:hasCode="false"
       android:supportsRtl="true">
       <property
           android:name="com.google.wear.watchface.format.version"
           android:value="2" />
   ```

2. **Kotlin Dependency Elimination** in [`gradle.properties`](file:///D:/github/Watch-face/CartoonWatchFace/gradle.properties) and [`build.gradle.kts`](file:///D:/github/Watch-face/CartoonWatchFace/app/build.gradle.kts):
   ```properties
   kotlin.stdlib.default.dependency=false
   ```
   ```kotlin
   configurations.all {
       exclude(group = "org.jetbrains.kotlin")
       exclude(group = "org.jetbrains")
   }
   ```

3. **Automated DEX Stripping Gradle Hook**:
   [`app/build.gradle.kts`](file:///D:/github/Watch-face/CartoonWatchFace/app/build.gradle.kts) includes an automated post-compilation hook that clears the intermediate DEX artifacts before bundletool runs:
   ```kotlin
   tasks.matching {
       it.name.startsWith("merge") && it.name.contains("Dex")
   }.configureEach {
       doLast {
           val dexDir = layout.buildDirectory.dir("intermediates/dex").get().asFile
           if (dexDir.exists()) {
               dexDir.walkTopDown().filter { it.extension == "dex" }.forEach { dexFile ->
                   dexFile.delete()
               }
           }
       }
   }
   ```

This produces a clean, pure resource-only Android App Bundle (`Cartoon.aab`) and APK (`Cartoon.apk`) containing **0 DEX files**, satisfying all Google Play Console submission criteria.

---

## Ambient Mode (Always-On Display) Optimization

To preserve AMOLED display health and prevent battery drain:
- The dial bezel and background elements are stripped in ambient mode (`target="alpha" value="0"`).
- Character animations switch to high-contrast 1-bit white outline silhouettes (`_aod.png`).
- Digital time switches from colored accent fills to pure white (`#FFFFFFFF`).
- Complication arcs flatten to low-contrast ambient borders.
- Overall On-Pixel Ratio (OPR) is held strictly under **15%**, compliant with Wear OS power guidelines.
