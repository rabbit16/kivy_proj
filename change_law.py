import os

p = "/home/hljiang/kivy_proj/.buildozer/android/app/kivy-deps-build/kivy-dependencies/build/SDL2_ttf-2.20.2/external/freetype/src/tools/"
f = os.listdir("/home/hljiang/kivy_proj/.buildozer/android/app/kivy-deps-build/kivy-dependencies/build/SDL2_ttf-2.20.2/external/freetype/src/tools/")
for i in f:
    if ".py" in i:
        os.system(f"2to3 -w {p}/{i}")