# claude-plugins — domain glossary

Missing Bits marketplace of Claude Code plugins; its domain is the working
process the plugins support and the marketplace machinery that ships them.

## Language

**Process directory**:
A directory the working process creates in a project repo (e.g.
`docs/domain/`, `docs/specs/`, `docs/plans/`).
_Avoid_: artifact folder

**First-create question**:
The question — ignored mode or tracked mode — asked when a process
directory is created for the first time, or exists with no observable
prior decision (neither a `.gitignore` with `*` nor a git-tracked file).
Never asked when either signal is present.
_Avoid_: self-ignore

**Ignored mode**:
A process directory with a `.gitignore` containing `*`; its contents stay
out of the repo's git status.

**Tracked mode**:
A process directory whose files are committed; detected by any git-tracked
file under it.
