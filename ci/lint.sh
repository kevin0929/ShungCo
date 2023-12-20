#!/bin/bash

set -eu

echo "Start lint testing ..."

find backend -type f -name "*.py" | while read -r file; do
  echo "Running ruff for file: $file"
  ci/lint.sh "$file"
done

echo "Finish lint testing ..."