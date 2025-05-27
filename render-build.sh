#!/usr/bin/env bash

# Instalación correcta sin usar permisos root
# 1. Instalamos dependencias de node
npm init -y
npm install playwright

# 2. Instalamos solo el navegador Chromium para no fallar por permisos
npx playwright install chromium
