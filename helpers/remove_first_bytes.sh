#!/bin/bash

#Fuente: https://stackpointer.io/unix/unix-linux-remove-bytes-beginning-file/556/
if [ $# -ne 3 ]; then
    echo "Uso: $0 <input-file> <output-file> <nBytes-to-remove>"
    exit 1
fi

dd if=$1 of=$2 ibs=$3 skip=1