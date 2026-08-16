#!/usr/bin/env node
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");

const SKILL_NAME = "docs-by-version";
const PACKAGE_ROOT = path.resolve(__dirname, "..");
const SKILL_ENTRIES = ["SKILL.md", "references", "scripts", "evals"];

function printHelp() {
  console.log(`
docs-by-version —— 安装"按里程碑整理项目文档"的 Agent Skill

用法:
  npx docs-by-version                 安装到 Claude Code (默认 ~/.claude/skills)
  npx docs-by-version --codex         安装到 Codex (~/.codex/skills)
  npx docs-by-version --agents        安装到 ~/.agents/skills
  npx docs-by-version --dir <路径>    安装到指定目录
  npx docs-by-version --force         目标已存在时覆盖

选项:
  --codex, --claude, --agents, --dir <path>, --force, --help
`);
}

function expandHome(p) {
  if (!p) return p;
  if (p === "~") return os.homedir();
  if (p.startsWith("~/") || p.startsWith("~\\")) {
    return path.join(os.homedir(), p.slice(2));
  }
  return p;
}

function parseArgs(argv) {
  const opts = { target: null, dir: null, force: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--codex") opts.target = "codex";
    else if (a === "--claude") opts.target = "claude";
    else if (a === "--agents") opts.target = "agents";
    else if (a === "--dir") {
      opts.target = "dir";
      opts.dir = argv[i + 1];
      i++;
    } else if (a === "--force" || a === "-f") opts.force = true;
    else if (a === "--help" || a === "-h") opts.help = true;
  }
  return opts;
}

function resolveSkillsRoot(opts) {
  const home = os.homedir();
  if (opts.target === "dir") {
    if (!opts.dir) {
      console.error("错误：--dir 需要一个路径，例如 npx docs-by-version --dir ~/.codex/skills");
      process.exit(1);
    }
    return path.resolve(expandHome(opts.dir));
  }
  if (opts.target === "codex") {
    return path.join(process.env.CODEX_HOME || path.join(home, ".codex"), "skills");
  }
  if (opts.target === "agents") {
    return path.join(home, ".agents", "skills");
  }
  return path.join(home, ".claude", "skills");
}

function copyEntry(src, dest, force) {
  if (!fs.existsSync(src)) {
    console.error("错误：找不到 " + src);
    process.exit(1);
  }
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const name of fs.readdirSync(src)) {
      if (name === "__pycache__") continue;
      copyEntry(path.join(src, name), path.join(dest, name), force);
    }
  } else {
    if (fs.existsSync(dest) && !force) return;
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
  }
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    printHelp();
    process.exit(0);
  }

  const skillsRoot = resolveSkillsRoot(opts);
  const destDir = path.join(skillsRoot, SKILL_NAME);

  if (fs.existsSync(destDir) && !opts.force) {
    console.error("目标已存在：" + destDir);
    console.error("如果确定要覆盖，请加 --force。");
    process.exit(1);
  }

  if (opts.force && fs.existsSync(destDir)) {
    fs.rmSync(destDir, { recursive: true, force: true });
  }

  fs.mkdirSync(destDir, { recursive: true });
  for (const entry of SKILL_ENTRIES) {
    copyEntry(path.join(PACKAGE_ROOT, entry), path.join(destDir, entry), opts.force);
  }

  console.log("已安装 " + SKILL_NAME + " 到：" + destDir);
  console.log("重新启动你的 agent 会话即可生效。");
}

main();
