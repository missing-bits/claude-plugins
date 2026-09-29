# working-process settings — the key registry

The one definition of every settings key. The `process-setup` skill
takes its questions from here, the loader `scripts/load-settings.sh`
its validation and defaults, and the repository's
`test_settings_registry.py` its consistency check; the rules name keys
and nothing more. The shape
is fixed so that `sed` and the test parse it without a Markdown parser:
one `## <key>` heading per key, then exactly these five fields, one per
line, in this order — `scope:` (`team` or `personal`), `values:` (the
allowed values, separated by ` | `), `default:` (a value, or `unset`
where the rule asks), `read-by:` (the files that read the key,
comma-separated, relative to `plugins/`) and `question:` (what the
skill asks, and the comment `--set` writes above the key). A `dir.`
key other than `dir.default` is an exception: absent, it inherits
`dir.default`'s effective value. A key is never renamed; the marker for
a retired key, and how the loader reports one, wait for the first key
that is retired.

## dir.default

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md
question: Which mode does a Process directory get unless an exception names it — tracked or ignored?

## dir.docs/specs

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md
question: Which mode does docs/specs/ get, as an exception to dir.default — tracked or ignored?

## dir.docs/technical-designs

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md
question: Which mode does docs/technical-designs/ get, as an exception to dir.default — tracked or ignored?

## dir.docs/plans

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md
question: Which mode does docs/plans/ get, as an exception to dir.default — tracked or ignored?

## dir.docs/domain

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md
question: Which mode does docs/domain/ get, as an exception to dir.default — tracked or ignored?

## dir.docs/code-review

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md, python-standards/commands/python-review.md, salesforce-standards/commands/salesforce-review.md
question: Which mode does docs/code-review/ get, as an exception to dir.default — tracked or ignored?

## dir..superpowers

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md
question: Which mode does the .superpowers/ family get, as an exception to dir.default — tracked or ignored?

## dir.docs/memory

scope: team
values: tracked | ignored
default: unset
read-by: project-memory/rules/project-memory.md
question: Which mode does docs/memory/ get, as an exception to dir.default — tracked or ignored?

## design.technical-design-offer

scope: team
values: on | off
default: unset
read-by: working-process/rules/workflow.md
question: Is the technical design offered at every consumption gate (on) or never (off)?

## dispatch.propagation-auditor-tier

scope: team
values: cheapest | mid | most-capable
default: cheapest
read-by: working-process/rules/workflow.md, working-process/agents/propagation-auditor.md
question: Which tier runs the propagation gate — cheapest, mid or most-capable?

## docs-branch.merge

scope: team
values: squash | fast-forward
default: unset
read-by: working-process/rules/spec-plan-lifecycle.md
question: How does the topic branch take the .docs branch at the implementation-ready gate — squash or fast-forward?

## consult.personas

scope: personal
values: yes | no
default: unset
read-by: working-process/rules/workflow.md
question: May the architect and system-designer personas be consulted as a design forms?

## review.autonomy

scope: personal
values: yes | no
default: unset
read-by: working-process/rules/workflow.md
question: May the review loop run autonomously, within the round cap?

## review.per-round-commit

scope: personal
values: yes | no
default: unset
read-by: working-process/rules/workflow.md, working-process/rules/spec-plan-lifecycle.md
question: May the review loop commit the reviewed document once per round?
