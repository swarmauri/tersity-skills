import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

test("installs all project skills for Codex", async () => {
  const project = await mkdtemp(join(tmpdir(), "tersity-"));
  try {
    const result = spawnSync(
      process.execPath,
      ["npm/cli.mjs", "install", "codex", "--scope", "project", "--project", project],
      { encoding: "utf8" },
    );
    assert.equal(result.status, 0, result.stderr);
    assert.ok(existsSync(join(project, ".codex/skills/measure-codebase/SKILL.md")));
    assert.ok(existsSync(join(project, ".codex/skills/tersify-codebase/SKILL.md")));
  } finally {
    await rm(project, { recursive: true, force: true });
  }
});
