import { $ } from "bun";
import { readdirSync } from "node:fs";
import { resolve } from "node:path";

const root = (await $`git rev-parse --show-toplevel`.text()).trim();
const gamesDir = resolve(root, "games");

const games = readdirSync(gamesDir, { withFileTypes: true })
	.filter(d => d.isDirectory())
	.map(d => resolve(gamesDir, d.name));

for (const dir of games) {
	await $`bun run scripts/build-game.js ${dir}`;
}