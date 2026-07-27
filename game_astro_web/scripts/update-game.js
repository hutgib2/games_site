import { $ } from "bun";
import { statSync, rmSync, mkdirSync, cpSync } from "node:fs";

const RED = '\x1b[0;31m';
const BLUE = '\x1b[0;34m';
const GREEN = '\x1b[0;32m';
const NC = '\x1b[0m';
const color = (c, s) => Bun.enableANSIColors ? `${c}${s}${NC}` : s;

const GAMES_DIR = '../games';
const PUBLIC_DIR = '../../game_astro_web/public/games';

const name = Bun.argv[2];
if (!name) {
	console.log(color(RED, "npm run build:game <game-directory>"));
	process.exit(1);
}
const gameDir = `${GAMES_DIR}/${name}`;
const srcBuild = `${gameDir}/src/build`;
const destDir = `${PUBLIC_DIR}/${name}`;

try {
	if (!statSync(gameDir).isDirectory()) throw new Error();
} catch {
	console.log(color(RED, `${gameDir} does not exist or is not a directory`));
	process.exit(1);
}

console.log(color(BLUE, `Building ${name}..`));
try {
	rmSync(srcBuild, { recursive: true, force: true });

	try {
		await $`python -m pygbag --build --ume_block=0 ${gameDir}/src`.quiet();
	} catch {
		console.log(color(RED, `pygbag build failed for ${name}`));
		process.exit(1);
	}

	rmSync(`${destDir}/build`, { recursive: true, force: true });
	mkdirSync(destDir, { recursive: true });
	cpSync(srcBuild, `${destDir}/build`, { recursive: true });
	rmSync(srcBuild, { recursive: true, force: true });

	console.log(color(BLUE, `Built ${name}`));
} catch (err) {
	console.log(color(RED, `Failed to build ${name}`));
	console.log(err.stderr?.toString() ?? err.message);
}