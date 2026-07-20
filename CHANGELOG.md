# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Fixed a dead API router that prevented some endpoints from being registered.
- Fixed a path traversal vulnerability in photo upload/serving.
- Fixed incorrect report status scoring logic.
- Fixed false-positive matches in AI-generated phrase detection.

### Changed
- Frontend UX improvements across report creation and listing pages.

## [1.0.0] - 2026-05-01

### Added
- Initial release: FastAPI + MongoDB missing person reporting system.
- Role-based access control for Admins, Rescuers, and public Users.
- Missing person report creation, status tracking, and tip submission.
- Automatic image compression for low-bandwidth environments.
- Auto-expiring reports (default 30 days) and urgent-case flagging.
- Public statistics dashboard and Swagger/ReDoc API documentation.

[Unreleased]: https://github.com/NurAbir/disaster-missing-persons/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/NurAbir/disaster-missing-persons/releases/tag/v1.0.0
