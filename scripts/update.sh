#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# parse flags first
show_logs=false
if [ "$1" = "-v" ] || [ "$1" = "--verbose" ]; then
	show_logs=true
	shift
fi

log() {
	[ "$show_logs" = "true" ] && echo "+ $*"
	"$@"
}

# reject no argument
if [ -z "$1" ]; then
	echo -e "${YELLOW}Usage: $0 [-v|--verbose] <game-directory>${NC}"
	exit 1
fi

# reject non-existent dir
dir=$1
if [ ! -d "$dir" ]; then
	echo -e "${YELLOW}$dir does not exist or is not a directory${NC}"
	exit 1
fi

name=$(basename "$dir")
echo -e "${BLUE}Building $name${NC}"
(
	cd "$dir" || exit 1
	
	# rebuild pygbag output
	log rm -rf src/build
	redirect="/dev/null"
	[ "$show_logs" = "true" ] && redirect="/dev/stdout"
	pygbag --build --ume_block=0 ./src > "$redirect" 2>&1

	# continue to next dir if pygbag fails
	rc=$?
	if [ $rc -ne 0 ]; then
		echo "${RED}pygbag build failed for $name${NC}"
		exit 1
	fi

	# overwrite pygbag output in game_astro_web with newly built one
	dest="../../game_astro_web/public/games/$name"
	log rm -rf "$dest/build"
	log mkdir -p "$dest"
	log mv src/build "$dest/"
	
) || echo -e "${RED}Failed to build $name${NC}"