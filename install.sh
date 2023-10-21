#!/bin/bash

echo "  ______                                   _"
echo "|  ____|                                 | |"
echo "| |__   ___ ___  ___ _ __ ___   __ _ _ __| |_"
echo "|  __| / __/ _ \/ __| '_  _  \ / _  | '__| __|"
echo "| |___| (_| (_) \__ \ | | | | | (_| | |  | |_"
echo "|______\___\___/|___/_| |_| |_|\__,_|_|   \__|"

# Cambia al directorio padre
cd ..

# Copia recursivamente los contenidos de la carpeta "Ecosmart" al directorio actual
cp -r ./Ecosmart/* ./

# Elimina la carpeta "Ecosmart" y su contenido de manera recursiva
rm -rf ./Ecosmart

echo "REINICIA HOME ASSISTANT"
