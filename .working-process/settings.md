# working-process settings

Which mode does a Process directory get unless an exception names it — tracked or ignored?
dir.default: tracked

Which mode does docs/code-review/ get, as an exception to dir.default — tracked or ignored?
dir.docs/code-review: ignored

Which mode does the .superpowers/ family get, as an exception to dir.default — tracked or ignored?
dir..superpowers: ignored

Is the technical design offered at every consumption gate (on) or never (off)?
design.technical-design-offer: off

How does the topic branch take the .docs branch at the implementation-ready gate — squash or fast-forward?
docs-branch.merge: squash

Which directory under docs/ holds one directory per ticket, if the project keeps them?
ticket.root: docs/tickets
