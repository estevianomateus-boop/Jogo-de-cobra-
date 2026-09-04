[app]
title = Cobra PRO
package.name = cobrapro
package.domain = org.cobrapro

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 1.0

requirements = python3,pygame

orientation = portrait
fullscreen = 1

# Ícone e imagem de splash (opcionais - remove estas 2 linhas se não tiveres os ficheiros)
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions = WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
