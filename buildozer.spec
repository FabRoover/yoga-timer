[app]
title = Yoga Timer
package.name = yogatimer
package.domain = org.example
source.dir = .
source.include_exts = py,wav
version = 0.1

requirements = python3,kivy,plyer,android,Cython==0.29.33

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# Update bootstrap setting
p4a.bootstrap = sdl2

# Update architectures setting
android.archs = arm64-v8a, armeabi-v7a

# Basic Android settings
android.api = 33
android.minapi = 21
android.ndk = 25b

android.orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
