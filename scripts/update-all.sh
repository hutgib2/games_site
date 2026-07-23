#!/bin/bash

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

flags=()
if [ "$1" = "-v" ] || [ "$1" = "--verbose" ]; then
	flags+='-v'
fi

for dir in ../games/*/; do
	./update.sh "${flags[@]}" "$dir"
done

echo -e "${GREEN}All games rebuilt!${NC}"