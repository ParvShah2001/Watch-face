# ⌚ Cartoon Watch Face for Wear OS

A modern, power-efficient animated digital watch face for Wear OS smartwatches (Samsung Galaxy Watch, Google Pixel Watch, etc.) built natively on the **Watch Face Format (WFF v2)**.

---

## ✨ Features & Architecture

1. **6 Iconic Cartoon Characters (Full Customization)**:
   - **Mickey Mouse**
   - **Doraemon**
   - **Shin-chan**
   - **Pikachu**
   - **Goku**
   - **Oggy**
   - Select your favorite character directly in the on-watch customization menu.

2. **Ultra-Smooth Animation & Pure Black Background**:
   - Clean, side-view animated walk cycles positioned directly in the center below the digital clock.
   - All animations have transparent backgrounds that blend seamlessly onto the pure `#000000` AMOLED display.

3. **7 Vibrant Color Themes**:
   - Amber (Default), Lime, Coral, Teal, Lavender, Mint, and Classic White.
   - Tint dynamically applies to the digital clock and complication accents.

4. **Dynamic Complications**:
   - **Left**: Battery / Health
   - **Center**: Date / Calendar
   - **Right**: Steps / Activity
   - Complication slots dynamically adapt to the user's chosen provider.

5. **Optimized Always-On Display (AOD)**:
   - High-contrast pure white outline silhouettes for each character.
   - Battery-saving black-and-white ambient palette complying with Wear OS pixel ratio standards (<15% OPR) for all-day battery life.

6. **Snappy & Lightweight (Pure WFF v2)**:
   - **Zero background Kotlin/Java CPU overhead** (`android:hasCode="false"`).
   - Rendered natively by the Wear OS system compositor.
   - Ultra-compact build: **~3.4 MB** total APK size.

---

## 📦 Project Structure

* **Project Directory**: [`CartoonWatchFace`](file:///D:/watchface/CartoonWatchFace)
* **Application ID / Package**: `com.example.cartoon`
* **App Name**: `Cartoon Watch face`
* **Watch Face Name**: `Cartoon`
* **Compiled APK**: [`D:\watchface\Cartoon.apk`](file:///D:/watchface/Cartoon.apk)

---

## 📲 Manual Installation via ADB

Run the following command to install the APK onto your connected Wear OS watch or emulator:

```powershell
adb install -r "D:\watchface\Cartoon.apk"
```

Once installed, long-press your watch face, tap **Add watch face** (`+`), and select **Cartoon**!
