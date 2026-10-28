import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(process.argv[2] ?? "npm-smoke");
const destinations = [".codex/skills", ".claude/skills", ".agents/skills"];
const skills = [
  "count-lines",
  "debug-terse-code",
  "evaluate-code-patterns",
  "measure-codebase",
  "tersify-codebase",
];

for (const destination of destinations) {
  for (const skill of skills) {
    assert.ok(existsSync(resolve(root, destination, skill, "SKILL.md")));
  }
}
console.log("installed npm distribution passed");
