# Change Log

## [2021.8.17] -- 2021-08-17
### Changed
- Fix search_music data parser
- Fix urlencode in search function
- Fix weird search results.


## [2021.1.31] -- 2021-01-31
### Added
- Added support for searching from `music.youtube.com`.
- Extract search results & music tracks from raw json (PR #5 by SK9712).
- Added `search_music` method to `YoutubeClient` object.

### Changed
- Removed `AioYoutubeService`, please use `YoutubeApiV3Client` instead.
