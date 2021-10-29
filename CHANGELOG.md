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

### Breaking Changes

-   All authentication and authorization is handled through the Knight Hacks Azure AD tenant. Previous authentication routes will no longer work and will return a 404.

### Changed

-   Authentication is provided by Azure AD, applications using this API must be granted the `access_as_user` permission.

### Removed

-   Authentication routes

## [2.1.9] - 2021-10-25

### Changed

-   We now return `email_verification` field.

## [2.1.8] - 2021-10-25

## [2.1.7] - 2021-10-24

### Changed

-   Email verification token expiry time increased to 30 days.

## [2.1.6] - 2021-10-21

### Fixed

-   pages.dev urls added to cors origins.

## [2.1.5] - 2021-10-20

### Fixed

-   `why_attend` schema is updated to no longer show length limit.

### Changed

-   `/api/sponsors/get_all_sponsors/` no longer requires authentication.

## [2.1.4] - 2021-10-20

### Changed

-   `why_attend` field in Hacker model no longer has a limit of 200 characters.

## [2.1.3] - 2021-10-17

### Fixed

-   Fixed route to re-send verification emails.

## [2.1.2] - 2021-10-17

### Fixed

-   Providing temporary datetime to email_acceptance template

## [2.1.1] - 2021-10-17

### Changed

-   20mb file size limit for hacker resumes.

### Fixed

-   CORS policy now allows cookies and credentials to be submitted across domains.

## [2.1.0] - 2021-10-11

### Added

-   POST `/api/sponsors/` endpoint for adding a hackathon sponsor to the DB.
-   GET `/api/sponsors/get_all_sponsors/` endpoint for retrieving information on all of the hackathon sponsors.

### Changed

-   Modified styling of the Email Verification template for Hackathon applicants.

## [2.0.1] - 2021-10-11

### Changed

-   Increased the resource limits and requests for the production backend container.

### Added

-   Sentry Spans to `create_hacker`, `common.jwt.*`, `flask.render_template`.

### Fixed

-   Email templates now provide the full URI to static assets.

## [2.0.0] - 2021-10-11

### Breaking Changes

-   The Fields `/mlh/mlh_code_of_conduct` and `/mlh/mlh_privacy_and_contest_terms` in the Hacker schema must be true when submitting an application, otherwise the api will return a 422.

### Changed

-   The Hacker schema to include the fields:
    -   `/birthday` as a iso8601 date string field
    -   `/country` as a string field
    -   `/mlh/mlh_code_of_conduct` as a required == `true` boolean field **\***
    -   `/mlh/mlh_privacy_and_contest_terms` as a required == `true` boolean field **\***
    -   `/mlh/mlh_send_messages` as a boolean field
    -   `/edu_info/level_of_study` as a string field
        **\*** Submitting these fields as anything besides `true` will return a 422.
-   Updated email templates for email footer, top, and hacker acceptance. (Initial non-Jinja templates created by: @APherwani)
-   Email helper functions and templates specify hackers instead of user.

### Fixed

-   API will return a 418 when fields that do not exist on the Hacker model are submitted to the API.

### Added

-   Email template for hacker confirmation success.
-   Helper functions for hacker confirmation success.

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

[Unreleased]: https://github.com/KnightHacks/hackathon-2021-backend/compare/2.1.9...HEAD

[2.1.9]: https://github.com/KnightHacks/hackathon-2021-backend/compare/2.1.8...2.1.9

[2.1.8]: https://github.com/KnightHacks/hackathon-2021-backend/compare/2.1.7...2.1.8

[2.1.7]: https://github.com/KnightHacks/hackathon-2021-backend/compare/2.1.6...2.1.7

[2.1.6]: https://github.com/KnightHacks/hackathon-2021-backend/compare/2.1.5...2.1.6

[2.1.5]: https://github.com/KnightHacks/hackathon-2021-backend/compare/2.1.4...2.1.5

[2.1.4]: https://github.com/KnightHacks/hackathon-2021-backend/compare/2.1.3...2.1.4

[2.1.3]: https://github.com/KnightHacks/hackathon-2021-backend/compare/2.1.2...2.1.3

[2.1.2]: https://github.com/KnightHacks/hackathon-2021-backend/compare/2.1.1...2.1.2

[2.1.1]: https://github.com/KnightHacks/hackathon-2021-backend/compare/2.1.0...2.1.1

[2.1.0]: https://github.com/KnightHacks/hackathon-2021-backend/compare/2.0.1...2.1.0

[2.0.1]: https://github.com/KnightHacks/hackathon-2021-backend/compare/2.0.0...2.0.1

[2.0.0]: https://github.com/KnightHacks/hackathon-2021-backend/compare/1.1.0...2.0.0

[1.1.0]: https://github.com/KnightHacks/hackathon-2021-backend/compare/1.0.1...1.1.0

[1.0.1]: https://github.com/KnightHacks/hackathon-2021-backend/compare/1.0.0...1.0.1

[1.0.0]: https://github.com/KnightHacks/hackathon-2021-backend/compare/0.0.4...1.0.0

[0.0.4]: https://github.com/KnightHacks/hackathon-2021-backend/compare/0.0.3...0.0.4

[0.0.3]: https://github.com/KnightHacks/hackathon-2021-backend/compare/0.0.2...0.0.3

[0.0.2]: https://github.com/KnightHacks/hackathon-2021-backend/compare/0.0.1...0.0.2
