# Release Rule

## Purpose

This rule automates release.

## Instructions

* When updating version, modify these files below.
  * pyproject.toml: `project.version`
  * uv.lock: Run `uv sync` command
  * template.sar.yaml: `Metadata.AWS::ServerlessRepo::Application.SementicVersion`
* Commit files with message: `release: Update to [SEMANTIC_VERSION]`
* Tag for the git commit with `[SEMANTIC_VERSION]`.
* Push commit and tag to remote repository.
* Create GitHub release using gh CLI:
  * Get commit messages between previous and current tag: `git log --oneline [PREVIOUS_TAG]..[CURRENT_TAG]`
  * Create release: `gh release create [SEMANTIC_VERSION] --title "[SEMANTIC_VERSION]" --notes "[COMMIT_MESSAGES]"`
  * Verify GitHub Actions status: `gh run list --limit 1`

## Priority

Low

## Error Handling

N/A