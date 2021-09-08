# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Types of Changes:
 - `Added` for new features.
 - `Changed` for changes in existing functionality.
 - `Deprecated` for soon-to-be removed features.
 - `Removed` for now removed features.
 - `Fixed` for any bug fixes.
 - `Security` in case of vulnerabilities.
-->

## [Unreleased]

## [0.0.2] - 2021-09-08

### Added

-   `CHANGELOG.md`
-   `create_release` workflow to facilitate the creation and preparation of new releases.
-   Issue Templates
-   Security Policy
-   Pull Request template
-   Version number stored in `__version__` 
-   Dependabot

### Changed

-   `README.md`  now contains org links and contributing section.
-   Sentry release name uses `__version__`
-   Flasgger gets version number from `__version__`
-   Hacker is no longer a user.
-   Sponsor is no longer a user.
-   Added description and socials fields to Sponsor model

### Removed

-   Admin routes.
-   Authentication routes.
-   Authentication using JWT tokens and session management.
-   Category routes.
-   Group routes.
-   Live Update routes.

## [0.0.1]

### Added

-   Admin routes.
-   Authentication routes.
-   Authentication using JWT tokens and session management.
-   Category routes.
-   Club event routes.
-   Email verification routes.
-   Event routes.
-   Group routes.
-   Hacker routes.
-   Live Update routes.
-   Sponsor routes.
-   Stats routes.

[Unreleased]: https://github.com/KnightHacks/hackathon-2021-backend/compare/0.0.2...HEAD

[0.0.2]: https://github.com/KnightHacks/hackathon-2021-backend/compare/0.0.1...0.0.2
