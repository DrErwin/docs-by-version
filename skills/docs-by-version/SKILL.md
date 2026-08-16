---
name: docs-by-version
description: Use this skill whenever a user asks to organize, split, migrate, audit, or maintain project documents by version or milestone; wants requirements and completion status separated; asks for a concise docs/README.md version index; or mentions 按版本、按里程碑、需求文档、完成情况、开发计划、文档整理. Also use it when deciding whether an extra document belongs in docs/ or a specific docs/versions/vX.Y.Z/ directory.
---

# Versioned Project Docs

把散落、重复、混合“计划与事实”的项目文档，整理成可以按里程碑追踪的文档体系。

## 目标结果

整理后，读者应能快速回答四个问题：

1. 这个项目是什么；
2. 当前完成到哪个里程碑；
3. 某个里程碑原本要做什么；
4. 该里程碑实际完成了什么、如何验证、还剩什么。

## 先判断用户是在讨论还是要求执行

- 用户只是在提问、咨询或评审方案时，只给建议，不改文件。
- 用户明确说“整理、迁移、创建、开始、执行”时，才修改文档。
- 修改前先读项目内的 `AGENTS.md`、贡献说明或其他工作约束。
- 如果项目要求“完成阶段后先更新进度文档”，先更新对应的完成情况，再进入下一阶段。

## 两类文档的归属规则

用“这份内容是否只解释一个阶段”作为首要判断。

### 放进具体版本目录

只属于一个版本或一个开发阶段的资料放入：

`docs/versions/vX.Y.Z/`

包括：

- 该阶段的需求和范围；
- 该阶段的完成情况和验证记录；
- 该阶段的设计方案与取舍；
- 该阶段的实施计划；
- 该阶段的验收记录；
- 该阶段的迁移说明、复盘或遗留问题。

推荐文件名：

- `requirements.md`
- `completion.md`
- `design.md`
- `implementation-plan.md`
- `acceptance.md`
- `migration.md`
- `retrospective.md`

### 放在 docs 目录

跨多个版本长期有效、描述整个项目的资料放在 `docs/`。

包括：

- 项目总体架构；
- 统一术语和领域模型；
- 长期开发规范；
- 数据、安全、部署或运维原则；
- 面向所有版本的贡献指南和故障排查；
- 跨版本仍然成立的重大决策说明。

优先使用清楚的文件名，例如：

- `docs/architecture.md`
- `docs/domain-model.md`
- `docs/development-guide.md`
- `docs/deployment.md`
- `docs/troubleshooting.md`

如果一份文档同时包含项目总体内容和某个版本内容，拆开：长期有效部分留在 `docs/`，阶段限定部分进入对应版本目录。

## 标准目录结构

```text
docs/
├── README.md
├── architecture.md                 # 可选：项目总体资料
├── development-guide.md            # 可选：项目总体资料
└── versions/
    ├── v0.1.0/
    │   ├── requirements.md
    │   ├── completion.md
    │   └── design.md                # 可选：仅属于 v0.1.0
    └── v0.2.0/
        ├── requirements.md
        ├── completion.md
        └── implementation-plan.md   # 可选：仅属于 v0.2.0
```

必须遵守：

- 一个版本只代表一个里程碑。
- 每个版本至少有 `requirements.md` 和 `completion.md`。
- 版本目录里不创建 `README.md`。
- `docs/README.md` 保留简要介绍、当前进度、版本列表和链接。
- `docs/README.md` 不复制每个版本的完整需求。
- 项目总体文档可以与 `README.md`、`versions/` 一起存在于 `docs/`。

## 版本号规则

1. 优先采用用户已经确认的里程碑版本号。
2. 没有明确版本映射时，从现有需求、进度文档、提交历史和发布记录中还原阶段。
3. 不要仅凭 `package.json` 或安装包版本推断文档里程碑。
4. 如果文档版本不等同于软件发布版本，在 `docs/README.md` 中明确说明。
5. 如果有两种同样合理的拆分方式，而且会影响大量文件，先向用户确认，不要擅自发明历史。

## 执行流程

### 1. 盘点现状

- 查看 `docs/`、根目录 README、需求、计划、进度和设计文件。
- 查看 Git 状态，保护用户已有的无关修改。
- 搜索所有旧文档链接和对旧路径的引用。
- 识别当前阶段、计划阶段、暂停阶段和已经被后续版本替代的能力。

### 2. 先建立迁移映射

在真正移动文件前，列出：

- 原文档；
- 目标版本或项目总体位置；
- 要保留的事实；
- 重复内容的唯一保留位置；
- 需要更新的引用。

这个映射可以在工作说明中展示，不必为了映射额外创建永久文档。

### 3. 建立版本骨架

为每个里程碑创建：

- `requirements.md`：当时的目标、范围、验收标准和不做什么；
- `completion.md`：当前状态、实际结果、验证、遗留和下一步。

需要模板时读取 [references/templates.md](references/templates.md)。

### 4. 分类额外文档

逐份应用归属规则：

- 只解释一个阶段：移入对应版本目录；
- 对所有阶段长期有效：留在 `docs/`；
- 两者混合：拆成两份并建立互相链接；
- 纯重复内容：确认新位置完整后删除重复副本。

### 5. 编写简明索引

`docs/README.md` 至少包含：

- 一段项目简介；
- 当前最新完成里程碑和下一计划里程碑；
- 文档版本号的含义；
- 版本列表；
- 每个版本的状态、需求链接、完成情况链接和额外资料链接；
- 项目总体文档链接；
- 简短的阅读与维护规则。

版本状态必须明确区分：

- 已完成；
- 进行中；
- 计划中；
- 暂缓；
- 已取消。

### 6. 保留真实历史

- 已完成版本只记录当时实际完成的结果，不把后来功能的删除改写成“当时未完成”。
- 后续版本如果替代或删除旧功能，在后续版本记录变化，并在旧版本完成情况中用一句话指向后续版本。
- 计划中的 `completion.md` 明确写“尚未开始”或当前准备情况，不虚构完成结果和验证。
- 暂缓版本记录暂缓原因、恢复条件和依赖。
- “计划做什么”和“实际做了什么”不要混在同一段落里。

### 7. 更新所有链接

- 更新根 README、代码注释和其他文档中的旧路径。
- 使用相对链接，确保从当前 Markdown 文件位置可以打开。
- 删除旧文件前再次搜索旧文件名，避免留下死链接。

### 8. 验证

先运行技能自带的结构检查：

```bash
python path/to/docs-by-version/scripts/validate_versioned_docs.py .
```

再完成以下检查：

- 每个版本都有 `requirements.md` 和 `completion.md`；
- 版本目录没有 `README.md`；
- `docs/README.md` 列出所有版本并链接到核心文件；
- 所有本地 Markdown 链接都能解析；
- 不再引用已经移走或删除的旧路径；
- 计划中、已完成、暂缓没有混写；
- Git diff 只包含本次文档整理和用户已有的无关修改；
- 如果是 Git 项目，运行 `git diff --check`。

不要只因为目录看起来正确就宣布完成；至少打开一个已完成版本和一个计划版本，核对内容是否真实。

## 安全边界

- 不覆盖用户未提交的无关修改。
- 不删除无法确认归属的历史资料；先移到明确位置或请用户确认。
- 不把软件版本号自动当作文档里程碑号。
- 不为了整齐合并语义不同的阶段。
- 不创建空泛的“完成情况”；没有证据就明确标记待验证。
- 不提交 Git，除非用户明确要求提交或仓库规则已授权。

## 交付说明

完成后简要报告：

- 建立了多少个里程碑；
- 哪些资料留在 `docs/`，哪些进入版本目录；
- 当前最新完成和下一计划版本；
- 运行了哪些验证及结果；
- 是否保留了未处理或需要用户决定的资料。
