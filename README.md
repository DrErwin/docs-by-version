# docs-by-version

一个 **Agent Skill**：把散落、重复、混合了“计划与事实”的项目文档，整理成可以按里程碑（版本）追踪的文档体系。

适用于 Claude Code、Codex、Cursor 等使用 `SKILL.md` 规范的 agent 工具。

## 安装

```bash
# 装到当前项目
npx skills add DrErwin/docs-by-version

# 装到全局（这台电脑所有项目都能用）
npx skills add DrErwin/docs-by-version -g

# 只装给 Codex（全局）
npx skills add DrErwin/docs-by-version -g -a codex
```

安装完成后重启一下 agent 会话即可生效。

## 它解决什么问题

很多项目的文档同时写着“计划要做什么”和“实际做了什么”，还散落在 `docs/`、根目录 README、进度文件里，时间一长就分不清当前完成到哪一步。

这个 skill 会把文档整理成统一结构：

- `docs/README.md` —— 项目简介 + 当前进度 + 版本列表；
- `docs/versions/vX.Y.Z/requirements.md` —— 该阶段原本要做什么；
- `docs/versions/vX.Y.Z/completion.md` —— 该阶段实际完成、如何验证、还剩下什么；
- 跨版本长期有效的资料（架构、术语、规范）留在 `docs/`。

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
└── evals/                          # 用于测试 skill 的样例与断言
```

## License

[MIT](LICENSE)
