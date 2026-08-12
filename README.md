# Missing Bits — Claude Code Plugins

Marketplace of [Claude Code](https://code.claude.com) plugins by Missing Bits.

## Installation

```bash
# Add the marketplace (one-time)
/plugin marketplace add missing-bits/claude-plugins

# Install a plugin
/plugin install <plugin>@missing-bits
```

## Plugins

| Plugin | Docs | Description |
|--------|------|-------------|
| `working-process` | [README](plugins/working-process/README.md) | Spec-driven working process: grilling-session, architect-session, system-designer-session and sync-rules skills, architect and plan-adversary review agents, two verdict-free consultation agents, distributed process rules |
| `python-standards` | [README](plugins/python-standards/README.md) | Python coding standards for uv + ruff + pytest + pyright: area skills, code-review stack, plan-review checklist, distributed toolchain rule |
| `salesforce-standards` | [README](plugins/salesforce-standards/README.md) | Salesforce coding standards for the sf CLI toolchain: area skills (Apex, LWC, Flow, data/security model, legacy UI), code-review stack, plan-review checklist, distributed toolchain rule |
| `project-memory` | [README](plugins/project-memory/README.md) | In-repo project memory: committed Team memory (`docs/memory/`) and per-user Private memory (`.claude/memory/`), with `memory-review-session`, `migrate-memory`, and `redirect-memory` skills, distributed as a Rules payload |

## License

[MIT](LICENSE)
