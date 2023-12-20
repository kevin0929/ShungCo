#!/bin/bash

set -eu

echo "Start lint testing ..."

find backend -type f -name "*.py" | while read -r file; do
  ruff check "$file"
done

echo "Finish lint testing ..."