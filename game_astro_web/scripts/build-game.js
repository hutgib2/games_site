import { $ } from "bun";
import { statSync, rmSync, cpSync, existsSync } from "node:fs";

const RED = '\x1b[0;31m';
const BLUE = '\x1b[0;34m';
const GREEN = '\x1b[0;32m';
const NC = '\x1b[0m';
const color = (c, s) => Bun.enableANSIColors ? `${c}${s}${NC}` : s;

const GAMES_DIR = '../games';
const SHARED_UTILS_DIR = '../pygame-utils';
const TARGET_BUILD_DIR = './public/games';

const name = Bun.argv[2];
if (!name) {
	console.log(color(RED, "npm run build:game <game-directory>"));
	process.exit(1);
}
const gameDir = `${GAMES_DIR}/${name}`;

const srcBuild = `${gameDir}/src/build`;
const targetBuildDir = `${TARGET_BUILD_DIR}/${name}`;
const targetUtilsDir = `${gameDir}/src/utils`;
const srcAudio = `${gameDir}/src/assets/audio`;

// console.log("game dir", gameDir);
// console.log("Target dir", targetDir);
// console.log("src dir", srcBuild);

try {
	if (!statSync(gameDir).isDirectory()) throw new Error();
} catch {
	console.log(color(RED, `${gameDir} does not exist or is not a directory`));
	process.exit(1);
}

console.log(color(BLUE, `Building ${name}..`));
try {
	rmSync(srcBuild, { recursive: true, force: true });
	cpSync(SHARED_UTILS_DIR, targetUtilsDir, { recursive: true });

	try {
		rmSync(srcBuild, { recursive: true, force: true });
		await $`pygbag --build --ume_block=0 ${gameDir}/src || python -m pygbag --build --ume_block=0 ${gameDir}/src`.quiet();
	} catch {
		console.log(color(RED, `pygbag build failed for ${name}`));
		process.exit(1);
	}	

	rmSync(`${targetBuildDir}/build`, { recursive: true, force: true });
	cpSync(srcBuild, `${targetBuildDir}/build`, { recursive: true });
	rmSync(srcBuild, { recursive: true, force: true });

	if (existsSync(srcAudio)) {
		cpSync(srcAudio, `${targetBuildDir}/audio`, { recursive: true });
	}

	console.log(color(BLUE, `Built ${name}`));
} catch (err) {
	console.log(color(RED, `Failed to build ${name}`));
	console.log(err.stderr?.toString() ?? err.message);
}