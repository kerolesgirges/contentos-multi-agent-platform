# Workflow model

The demo workflow uses a small directed dependency graph:

1. Planning turns the brief into explicit requirements.
2. Deliverable workers run independently where possible.
3. Validation checks the artifact set.
4. Human review can approve or request revision.

`needs_review` is a first-class state. It is not represented only by a warning color: the API, task label, review action, and event log all carry the same meaning.
