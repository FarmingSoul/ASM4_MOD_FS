#!/bin/bash

# Note: -noobsolete to remove obsolete strings from already present ts-files

# Define used binaries
pylupdate=pylupdate5.bat


# Collect available translation files
ts_files=asm4te.ts

# Collect all strings from python files
$pylupdate -verbose $1 -translate-function _atr ../*.py -ts $ts_files
