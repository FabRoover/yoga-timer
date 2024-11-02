[app]
title = Yoga Timer
package.name = yogatimer
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav
version = 0.1

requirements = python3,kivy==2.2.1,pillow,android,plyer,Cython==0.29.33

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# Android API
android.api = 33

# Minimum API required
android.minapi = 21

# Android NDK
android.ndk = 25b

# Android SDK
android.sdk = 33

# Architecture
android.arch = arm64-v8a

# Bootstrap
android.bootstrap = sdl2

# Orientation
android.orientation = portrait

# Android logcat filters to use
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
