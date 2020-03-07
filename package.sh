#!/bin/bash
set -e -x
rm -f "function.zip"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd ".env/lib/python3.8/site-packages"
zip -r9 "${DIR}/function.zip" .
cd "${DIR}"
zip -g "function.zip" "lambda_function.py"
