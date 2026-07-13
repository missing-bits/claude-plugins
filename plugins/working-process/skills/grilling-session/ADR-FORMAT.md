# Format of ADRs

Path: `docs/domain/adr/NNNN-slug.md`, numbered sequentially from `0001`.
Create the directory lazily, when the first ADR lands.

## Shape

    # {Short title}

    {One to three sentences: the context, the decision, the reason.}

A single paragraph is enough — the value is that the decision and its
"why" are written down, not the paperwork around it.

## Earned extras (only when they add something)

- `status` frontmatter:
  `proposed | accepted | deprecated | superseded by ADR-NNNN`
- **Considered options** — when the rejected paths will matter later.
- **Consequences** — when the fallout is non-obvious.

## Bar for writing one

All three must hold, or there is no ADR:

1. Reversing it later would cost real effort.
2. A future reader would ask "why on earth this way?".
3. Genuine alternatives were on the table.
