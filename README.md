# docs-by-version

一个 **Agent Skill**：把散落、重复、混合了“计划与事实”的项目文档，整理成可以按里程碑（版本）追踪的文档体系。

适用于 Claude Code、Codex 等使用 `SKILL.md` 规范的 agent 工具。

## 它解决什么问题

很多项目的文档同时写着“计划要做什么”和“实际做了什么”，还散落在 `docs/`、根目录 README、进度文件里，时间一长就分不清当前完成到哪一步。

这个 skill 会把文档整理成统一结构：

- `docs/README.md` —— 项目简介 + 当前进度 + 版本列表；
- `docs/versions/vX.Y.Z/requirements.md` —— 该阶段原本要做什么；
- `docs/versions/vX.Y.Z/completion.md` —— 该阶段实际完成、如何验证、还剩下什么；
- 跨版本长期有效的资料（架构、术语、规范）留在 `docs/`。

## 安装

### 用 npx 一键安装

```bash
# 从 npm 官方源（发布后可用）
npx docs-by-version

# 直接从 GitHub 仓库运行（无需 npm 发布，立即可用）
npx github:DrErwin/docs-by-version
```

默认安装到 Claude Code 的技能目录 `~/.claude/skills/docs-by-version`。

```bash
npx docs-by-version --codex      # 安装到 Codex：~/.codex/skills
npx docs-by-version --agents     # 安装到 ~/.agents/skills
npx docs-by-version --dir <路径> # 安装到自定义目录
npx docs-by-version --force      # 目标已存在时覆盖
```

### 手动安装

把这个仓库里的 `SKILL.md`、`references/`、`scripts/`、`evals/` 复制到你的技能目录即可。

## 使用

在 agent 里直接说：

> 把这个项目的文档按里程碑整理，分到 docs/versions/ 下，并更新 docs/README.md 索引。

skill 会自动触发，并按内置规则执行。整理完成后可以用自带脚本校验结构：

```bash
python <技能目录>/docs-by-version/scripts/validate_versioned_docs.py <项目根目录>
```

## 目录结构

```text
.
├── SKILL.md                        # skill 主指令
├── references/
│   └── templates.md                # requirements / completion / README 模板
├── scripts/
│   └── validate_versioned_docs.py  # 文档结构校验脚本
├── evals/                          # 用于测试 skill 的样例与断言
└── bin/
    └── docs-by-version.js          # npx 安装器
```

## License

[MIT](LICENSE)
