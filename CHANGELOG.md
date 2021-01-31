# Change Log

## [2021.1.31] -- 2021-01-31
### Added
- Added support for searching from `music.youtube.com`.
- Extract search results & music tracks from raw json (PR #5 by SK9712).
- Added `search_music` method to `YoutubeClient` object.

### Changed
- Removed `AioYoutubeService`, please use `YoutubeApiV3Client` instead.
