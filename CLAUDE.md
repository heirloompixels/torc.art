# CLAUDE.md

Read `README.md` first — it is this repo's own manual. This file holds
only the cross-repo session rule.

## Sessions end with a PR

A branch is not a deliverable. Before ending any session — web or local:

- Push the work. A `claude/*` branch push opens a draft PR by itself
  (`.github/workflows/claude-branch-pr.yml`); for any other branch, open
  the PR yourself. If the work was committed straight to main, push main.
- Say in the handoff where the work now lives: the PR number, or the main
  push.
- Merged branches delete themselves on GitHub; do not resurrect one.

The PR list is the inbox. Work that ends a session without a PR or a
pushed main strands invisibly.
