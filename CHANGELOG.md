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

## [1.1.0] - 2021-10-03

### Deprecated

-   The use of `multipart/form-data` on the POST `/api/hackers/` endpoint.

### Added

-   POST `/api/hackers/resume/` endpoint for uploading a hacker's resume before the hacker is actually created in the DB. Unattached resumes are deleted after 24 hours.
-   Added the ability to upload the hacker document as a `application/json` while providing the optional `resume_id` value to attach a resume to a hacker document which is returned from the `/api/hackers/resume/` endpoint.

### Fixed

-   Fixed get hacker resume field returning a 500 error.

### Security

-   Removed ability for user to provide redirect uri for email verification endpoint.

## [1.0.1] - 2021-09-19

### Changed

-   Metadata in openapi documentation.

## [1.0.0] - 2021-09-19

### Changed

-   Email Verification route redirects client with a 302 to the uri provided in the `redirect_uri` query parameter or if `redirect_uri` is blank, to the frontend.

### Fixed

-   Fixed the url given in verification emails to link directly to backend api.
-   Failing test cases due to unauthorized routes requiring authorization.
-   JSONDecodeError is now handled and raises a 400 with an appropriate message.
-   Updated the `graduation_date` model to be a data type string and updated its schema.

### Added

-   Added `dietary_restrictions` field to Hacker model.

## [0.0.4] - 2021-09-09

### Fixed

-   Fixed ordering by start date of Club Events

## [0.0.3] - 2021-09-09

### Added

-   Authentication

### Changed

-   Verifying email is done through a get request.
-   Require authentication for routes that create/update resources and for endpoints that return sensitive data.

### Fixed

-   Verifying email

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

-   `README.md` now contains org links and contributing section.
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

[Unreleased]: https://github.com/KnightHacks/hackathon-2021-backend/compare/1.1.0...HEAD

[1.1.0]: https://github.com/KnightHacks/hackathon-2021-backend/compare/1.0.1...1.1.0

[1.0.1]: https://github.com/KnightHacks/hackathon-2021-backend/compare/1.0.0...1.0.1

[1.0.0]: https://github.com/KnightHacks/hackathon-2021-backend/compare/0.0.4...1.0.0

[0.0.4]: https://github.com/KnightHacks/hackathon-2021-backend/compare/0.0.3...0.0.4

[0.0.3]: https://github.com/KnightHacks/hackathon-2021-backend/compare/0.0.2...0.0.3

[0.0.2]: https://github.com/KnightHacks/hackathon-2021-backend/compare/0.0.1...0.0.2
