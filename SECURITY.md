# Security Policy

## Reporting a Vulnerability

If you discover a security issue in this template (for example, a workflow
that leaks secrets, an unsafe default permission, or a vulnerable pinned
dependency), please report it privately:

- Open a [private security advisory](https://github.com/yama662607/quarto-textbook-template/security/advisories/new), or
- Email the maintainer

Please **do not** open a public issue for security reports.

## Scope

This is a project template — derived repositories own their own deployments.
The maintainers will:

1. Acknowledge receipt within 7 days.
2. Patch the template repository for issues that affect the scaffolding
   itself (e.g. CI permissions, default actions, dependency pins).
3. Note the fix in `CHANGELOG.md`.

## Hardening recommendations for derived repositories

- **Pin third-party GitHub Actions to commit SHAs** (Dependabot can automate
  this). The template uses tag pins (`@v3`, `@v4`) for readability.
- Enable **branch protection** on `main` and require the `Quality Checks`
  workflow to pass before merging.
- Review the `.github/workflows/publish.yml` `permissions:` block before
  enabling additional features.
- Keep `uv.lock` committed and pin Python version in CI.
