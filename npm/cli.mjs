#!/usr/bin/env node
import { cp, mkdir, readdir, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const targets = {
  codex: [".codex/skills", join(homedir(), ".codex/skills")],
  claude: [".claude/skills", join(homedir(), ".claude/skills")],
  antigravity: [".agents/skills", join(homedir(), ".gemini/config/skills")],
};

function value(flag, fallback) {
  const index = process.argv.indexOf(flag);
  return index < 0 ? fallback : process.argv[index + 1];
}

async function install(target) {
  if (!targets[target] && target !== "all") throw new Error(`unknown target: ${target}`);
  const scope = value("--scope", "user");
  const project = resolve(value("--project", process.cwd()));
  const force = process.argv.includes("--force");
  const names = target === "all" ? Object.keys(targets) : [target];
  for (const name of names) {
    const destination = scope === "project" ? join(project, targets[name][0]) : targets[name][1];
    await mkdir(destination, { recursive: true });
    for (const skill of await readdir(join(root, "skills"), { withFileTypes: true })) {
      if (!skill.isDirectory()) continue;
      const source = join(root, "skills", skill.name);
      if (!existsSync(join(source, "SKILL.md"))) continue;
      const output = join(destination, skill.name);
      if (existsSync(output) && !force) throw new Error(`${output} exists; pass --force`);
      if (existsSync(output)) await rm(output, { recursive: true });
      await cp(source, output, { recursive: true });
      console.log(`installed ${name}:${skill.name} -> ${output}`);
    }
  }
}

function scan(args, command = "scan") {
  const helper = command === "count-lines"
    ? "skills/count-lines/scripts/count_lines.py"
    : "skills/measure-codebase/scripts/tersity_scan.py";
  const script = join(root, helper);
  for (const executable of ["python3", "python"]) {
    const result = spawnSync(executable, [script, ...args], { stdio: "inherit" });
    if (!result.error) return result.status ?? 1;
  }
  throw new Error("Python 3.10+ is required for the bundled scanner");
}

async function main() {
  const [, , command, target, ...rest] = process.argv;
  if (command === "path") return console.log(root);
  if (command === "scan") return process.exitCode = scan([target, ...rest].filter(Boolean));
  if (command === "count-lines") {
    return process.exitCode = scan([target, ...rest].filter(Boolean), command);
  }
  if (command === "install" && target) return install(target);
  console.error("usage: tersity-skills <path|scan|count-lines|install TARGET> [options]");
  process.exitCode = 2;
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
