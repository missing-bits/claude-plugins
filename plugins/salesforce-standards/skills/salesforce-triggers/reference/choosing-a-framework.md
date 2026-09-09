# Choosing a trigger framework

Read at step (c) of the resolution protocol, when neither a declaration
nor a fingerprint settled the framework. Present the case for and
against each shipped approach; the developer chooses; the session
writes the declaration — a `trigger-framework:` line in the root
`CLAUDE.md` or the trigger directory's — so the question is not asked
again. The developer's existing code decides more than any argument
here: a project already extending a base class has chosen.

## Base-class (`base-class`)

**For.** One virtual class copied into the org, no metadata to
maintain, and a handler shape every Salesforce developer recognises.
Bypass and loop-count APIs come with it. Two products share the shape,
so hiring and code review carry over.

**Against.** Execution order within a context is the order of calls in
the handler, so reordering is a code deployment. The handler cannot be
called without DML, so handler tests are integration tests. The two
products differ in what an exceeded loop count does — one throws, one
silences — and the difference is a private method in a class the
project copied and may have edited.

## Metadata-driven (`metadata-driven`)

**For.** Order and bypasses live in Custom Metadata, so an admin can
reorder or disable an action without a deployment of code. An action
is a plain class implementing an interface, callable in a test without
DML. Permission-based bypasses come with it.

**Against.** A stale metadata record fails every DML on its object.
The dispatch is invisible in code — a reader must open the records to
learn what runs — and a trigger that runs nothing looks identical to
one that runs ten actions. The framework is a dependency the project
installs and upgrades.

## Frameworkless (`frameworkless`)

**For.** Nothing to install or upgrade; one static entry point per
object; the handler is callable in a test without DML. The whole
dispatch fits in twenty lines a newcomer reads in one sitting.

**Against.** Bypass and recursion control are the project's to write,
and each project writes them differently. Nothing recognises the shape
from outside, so the framework must be declared to be resolved.

## Something else

A recognition label — fflib, TDTM, a dispatcher — or a framework this
plugin has never seen: the framework is sound and only the document is
missing. Offer to write a project document describing the project's own
code, answering the four questions the `salesforce-triggers` skill
asks, and declare it with a `doc-path:` locator. Never compare it to
the three above — this plugin cannot write that comparison, and a
document written from a pattern found on the internet describes
somebody else's framework.
