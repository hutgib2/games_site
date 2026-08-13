import { $ } from "bun";
import { resolve, basename } from "node:path";
import { statSync } from "node:fs";

const RED = '\x1b[0;31m';
const BLUE = '\x1b[0;34m';
const GREEN = '\x1b[0;32m';
const NC = '\x1b[0m';
const color = (c, s) => Bun.enableANSIColors ? `${c}${s}${NC}` : s;

const arg = Bun.argv[2];
if (!arg) {
	console.log(color(RED, "npm run update:submdoule <game-directory>"));
	process.exit(1);
}
const gameDir = resolve(arg);
const name = basename(gameDir);
try {
	if (!statSync(gameDir).isDirectory()) throw new Error();
} catch {
	console.log(color(RED, `${name} does not exist or is not a directory`));
	process.exit(1);
}

console.log(color(BLUE, ` ${name}: updating submodule..`));
try {
	await $`git submodule update --init -- ${gameDir}`;
	await $`git submodule update --remote --merge -- ${gameDir}`;
	console.log(color(BLUE, `${name}: submodule updated!`));
} catch (err) {
	console.log(color(RED, `Failed to update ${name}`));
	console.log(err.stderr?.toString() ?? err.message);
}