# MicroManagerr Feature Research

## Research Summary

This document compiles feature ideas discovered through extensive research of community forums, GitHub issues, and documentation for Sonarr, Radarr, Plex, and the broader self-hosted media server ecosystem. Features are organized by category with context on user pain points.

---

## Category 1: Media Format Detection & Tagging (Core MicroManagerr Features)

These align with the project's current goals and represent significant user pain points.

### 1.1 HDR/Dolby Vision Detection & Tagging
**Pain Point:** Users struggle to identify and tag HDR/DV content correctly. Plex-utills and Kometa can do this but require separate setup and don't integrate with Sonarr/Radarr tagging.

**Features:**
- Scan media files for HDR10, HDR10+, Dolby Vision metadata
- Detect DV profile type (5, 7, 8) and whether HDR fallback exists
- Create/apply tags in Sonarr and Radarr automatically
- Support "hybrid" DV+HDR10 detection
- Generate HDR/DV overlay badges for Plex/Jellyfin (via integration with Kometa)

**Source Context:** Kometa provides overlay automation but requires complex YAML configuration. Users want simpler, Arr-integrated solutions.

### 1.2 IMAX Enhanced Detection
**Pain Point:** No automated way to detect IMAX Enhanced content. Users must manually identify and tag.

**Features:**
- Detect IMAX Enhanced metadata in video files
- Detect IMAX aspect ratio (1.90:1 vs 2.39:1 scenes)
- Identify "IMAX Enhanced" audio tracks (DTS:X IMAX)
- Auto-tag in Sonarr/Radarr

**Source Context:** IMAX metadata is embedded but rarely parsed by home media tools.

### 1.3 Special Edition Detection (Extended/Director's Cut)
**Pain Point:** Difficult to identify theatrical vs extended/director's cut versions. Runtime comparison is the main method.

**Features:**
- Compare file runtime against TMDB/IMDB theatrical runtime
- Detect edition keywords in filename (Extended, Director's Cut, Unrated, Uncut, Remastered)
- Cross-reference with known edition databases
- Apply appropriate tags for filtering
- FileBot pattern matching: `(Extended.|Ultimate.)?(Director.?s|Collector.?s|Theatrical|Ultimate|Final|Extended|Rogue|Special|Despecialized|R.Rated).(Cut|Edition|Version)|Extended|Remastered|Recut|Uncut|Uncensored|Unrated|IMAX`

**Source Context:** tinyMediaManager added "movie editions" field for this purpose. Users want this integrated with Arr stack.

### 1.4 Letterbox Cropping Metadata
**Pain Point:** Letterboxed content displays with black bars even on ultrawide monitors. Transcoding to remove bars is time-consuming.

**Features:**
- Detect letterboxing using ffmpeg cropdetect
- Apply MKV container crop metadata (non-destructive)
- Batch processing capability
- Preview mode before applying
- Integration with Aspect Ratio Detector tool concepts

**Source Context:** MKV supports crop metadata but few players honor it. Plex does respect this metadata.

---

## Category 2: Quality Management & Upgrades

### 2.1 HDR/DV Upgrade Discovery
**Pain Point:** Users have SDR content they'd like to upgrade to HDR/DV but Sonarr/Radarr only look for upgrades within the same quality tier.

**Features:**
- Search indexers for HDR/DV versions of non-HDR content
- Score comparison between current file and potential upgrade
- Auto-download if upgrade score exceeds threshold
- Manual review queue for edge cases
- Option to unmonitor after successful upgrade

**Source Context:** Users frequently ask about upgrading existing content to HDR. Custom formats can prefer HDR but don't actively search for upgrades.

### 2.2 Quality Profile Mismatch Detection
**Pain Point:** Files end up in wrong libraries (1080p in 4K folder, etc.) due to configuration mistakes.

**Features:**
- Scan libraries for quality/path mismatches
- Detect when file quality doesn't match folder structure
- Suggest correct location based on quality profile
- Automate move via Sonarr/Radarr API
- Alert on new mismatches

**Source Context:** This is mentioned in the original goal.txt as a common user mistake.

### 2.3 Multi-Instance Sync Management
**Pain Point:** Running separate 4K and 1080p instances requires manual sync or third-party tools like Syncarr.

**Features:**
- Unified view of content across multiple Radarr/Sonarr instances
- One-click sync between instances
- Quality profile mapping between instances
- Conflict detection and resolution

**Source Context:** TRaSH Guides recommend dual instances but sync is cumbersome.

### 2.4 Custom Format Scoring Audit
**Pain Point:** Users don't understand why certain releases are grabbed over others.

**Features:**
- Visual breakdown of custom format scores for any release
- Comparison tool: "Why did Radarr pick X over Y?"
- Custom format conflict detection
- Suggestions for profile optimization

---

## Category 3: Library Health & Maintenance

### 3.1 Corrupt/Incomplete File Detection
**Pain Point:** Media files can become corrupt and there's no automated way to detect this.

**Features:**
- Scan files for playability/integrity
- Detect truncated or incomplete downloads
- Identify files with missing audio/video streams
- Trigger re-download via Sonarr/Radarr
- Integration with Checkrr concepts

**Source Context:** Checkrr exists but is a separate tool. Integration into unified dashboard would be valuable.

### 3.2 Orphaned/Stalled Download Cleanup
**Pain Point:** Downloads get stuck, leave orphaned files, or become "stalled" requiring manual intervention.

**Features:**
- Detect stalled/stuck downloads
- Identify orphaned files not tracked by Arr apps
- Automatic cleanup with configurable retention
- Malware/suspicious file detection
- Integration with Cleanuparr/Decluttarr concepts

**Source Context:** Cleanuparr and Decluttarr are popular tools addressing this exact problem.

### 3.3 Database Health Monitoring
**Pain Point:** SQLite database corruption can cause major issues. Recovery is complex.

**Features:**
- Automated database integrity checks
- Backup automation with retention
- Corruption detection and alerting
- Recovery guidance/automation
- Index rebuild scheduling

**Source Context:** Plex and Jellyfin database corruption is a recurring issue in forums.

### 3.4 Missing Media Audit
**Pain Point:** Jellyfin deletes library entries when drives are temporarily disconnected.

**Features:**
- Track expected vs actual files
- Detect missing files without auto-removal
- Alert on unexpected file disappearance
- Protect against mount point failures

**Source Context:** Jellyfin feature request: "Don't remove missing media during library scan"

---

## Category 4: Metadata & Matching Issues

### 4.1 Metadata Mismatch Detection
**Pain Point:** Plex/Jellyfin frequently mismatch movies and shows, requiring manual fix.

**Features:**
- Cross-reference local files with TMDB/TVDB
- Detect probable mismatches based on runtime, year discrepancies
- Bulk fix suggestions
- Integration with media servers to trigger re-match

**Source Context:** "Plex Not Matching? Your Guide to Fixing Metadata Issues" - common user issue.

### 4.2 Anime Dual Audio Management
**Pain Point:** Sonarr has issues with dual audio anime releases. Custom formats based on filenames break when downloaded files have different names.

**Features:**
- Detect multi-language audio streams via MediaInfo
- Override custom format scoring based on actual file content (not just filename)
- Prefer dual audio releases intelligently
- Handle XEM mapping issues

**Source Context:** GitHub issue #6710: "Honor custom formats from release name and media details in addition to file name"

### 4.3 Collection/Franchise Management
**Pain Point:** Radarr's collection management is limited. Users want franchise-level organization.

**Features:**
- View and manage entire collections as units
- Add all movies in a collection at once
- Suggest missing collection entries
- Cross-reference with Plex collections

**Source Context:** GitHub issue #9279: "Collections - Management made easy"

---

## Category 5: Automation & Workflow

### 5.1 Task Priority Management
**Pain Point:** Sonarr's task scheduler blocks important operations. Missing episode searches can run for days, blocking import of finished downloads.

**Features:**
- Pause/resume bulk operations
- Prioritize import over search tasks
- Schedule intensive tasks for off-peak hours
- Cancel bulk operations gracefully

**Source Context:** GitHub issue #4907: "Missing Episode Searches should take a break for higher priority tasks"

### 5.2 Subtitle Management
**Pain Point:** Bazarr integration is good but has gaps. Subtitles don't auto-download consistently.

**Features:**
- Unified subtitle status view
- Manual trigger for subtitle search
- Track subtitle quality/sync issues
- Multi-language subtitle management

**Source Context:** Bazarr issues with auto-download are frequently reported.

### 5.3 Request Management Enhancement
**Pain Point:** Overseerr/Jellyseerr have limitations, especially around request limits and performance.

**Features:**
- Unified request view across instances
- Request status tracking
- Smart request fulfillment (check multiple instances)
- Request analytics and reporting

**Source Context:** Users running both Plex and Jellyfin need cross-platform request management.

### 5.4 Configuration Management & Backup
**Pain Point:** Configuration takes hours. No easy way to reproduce or backup settings.

**Features:**
- Export/import Arr configurations
- Version control for settings
- Sync settings across instances
- Configuration audit and diff

**Source Context:** Buildarr exists but integration with other tools is limited.

---

## Category 6: Monitoring & Notifications

### 6.1 Unified Dashboard
**Pain Point:** Users run multiple dashboards (Homarr, Homepage) plus individual Arr UIs.

**Features:**
- Single pane of glass for all Arr apps
- Real-time status of downloads, imports, issues
- Health status aggregation
- Quick actions from dashboard

**Source Context:** Homarr provides some Arr integration but users want deeper features.

### 6.2 Smart Notification Filtering
**Pain Point:** Notification overload from multiple services leads to alert fatigue.

**Features:**
- Consolidate similar notifications
- Priority-based filtering
- Digest mode (hourly/daily summaries)
- Suppress known false positives

**Source Context:** 68% of Americans say notification frequency interferes with productivity.

### 6.3 Health Check Enhancement
**Pain Point:** Health check warnings include false positives, especially around Docker path mappings.

**Features:**
- Suppress known false positives
- Custom health check rules
- Historical health tracking
- Proactive issue prediction

**Source Context:** GitHub issues around false positive health checks are common.

### 6.4 Analytics & Reporting
**Pain Point:** Tautulli provides great analytics for Plex but no equivalent for Arr stack activity.

**Features:**
- Download/import statistics over time
- Quality upgrade tracking
- Storage usage trends
- User request analytics

**Source Context:** Tautulli users wish for historical import capability.

---

## Category 7: Storage Management

### 7.1 Disk Space Monitoring
**Pain Point:** Running out of space causes download failures. No proactive warning.

**Features:**
- Real-time storage monitoring
- Threshold-based alerts
- Predictive space exhaustion warnings
- Storage usage by quality/category

### 7.2 Duplicate Detection
**Pain Point:** Duplicate files waste storage. Detection is manual.

**Features:**
- Identify duplicate media files
- Compare quality of duplicates
- Suggest which version to keep
- Safe deletion with confirmation

**Source Context:** Cleanarr (se1exin) exists for this purpose.

### 7.3 Automatic Cleanup Policies
**Pain Point:** Old, unwatched content consumes space indefinitely.

**Features:**
- Rule-based content cleanup
- Integrate with watch history (Tautulli)
- Protect requested content
- Retention policies by quality/age

**Source Context:** Janitorr and Maintainerr address this need.

---

## Category 8: Integration Gaps

### 8.1 Cross-Platform Sync
**Pain Point:** Plex and Jellyfin users want synced libraries but no native solution exists.

**Features:**
- Sync watch status between platforms
- Sync collections and playlists
- Unified user management

### 8.2 Trakt.tv Deep Integration
**Pain Point:** Trakt sync exists but is limited.

**Features:**
- Auto-add from Trakt lists
- Sync watch history bidirectionally
- Recommendation integration

### 8.3 Download Client Health
**Pain Point:** Download clients have issues that Arr apps don't always surface.

**Features:**
- Unified download client monitoring
- Detect VPN issues
- Rate limiting detection
- Indexer health correlation

---

## Priority Features for MicroManagerr

Based on research frequency and user impact, here are the highest-priority features beyond the current goals:

### Tier 1 (Most Requested / Highest Impact)
1. **HDR/DV/IMAX tagging automation** - Core goal, heavily requested
2. **Quality path mismatch detection** - Core goal, common problem
3. **Letterbox cropping** - Core goal, unique differentiator
4. **Orphaned/stalled download cleanup** - Very common pain point
5. **Health check with false positive suppression** - Frequently complained about

### Tier 2 (Frequently Requested)
6. **Multi-instance unified view** - Growing need as dual 4K/1080p setups become standard
7. **Anime dual audio handling** - Niche but vocal user base
8. **Database health monitoring** - Prevents catastrophic data loss
9. **Collection/franchise management** - Long-standing Radarr limitation
10. **Corrupt file detection** - Important for library integrity

### Tier 3 (Nice to Have)
11. **Unified dashboard** - Many solutions exist but integration depth varies
12. **Smart notifications** - Quality of life improvement
13. **Storage analytics** - Useful for planning
14. **Configuration backup** - Buildarr exists but could be integrated

---

## Sources Referenced

- [TRaSH Guides](https://trash-guides.info/)
- [Servarr Wiki](https://wiki.servarr.com/)
- [Sonarr GitHub Issues](https://github.com/Sonarr/Sonarr/issues)
- [Radarr GitHub Issues](https://github.com/Radarr/Radarr/issues)
- [Kometa Wiki](https://kometa.wiki/)
- [Cleanuparr](https://github.com/Cleanuparr/Cleanuparr)
- [Decluttarr](https://github.com/ManiMatter/decluttarr)
- [Recyclarr](https://github.com/recyclarr/recyclarr)
- [Syncarr](https://github.com/syncarr/syncarr)
- [plex-utills](https://github.com/jkirkcaldy/plex-utills)
- [Aspect Ratio Detector](https://www.avsforum.com/threads/aspect-ratio-detector-get-the-real-ar-and-write-it-into-mkvs-meta-data-nfo-files-or-filename-tags.3176044/)
- [Tautulli](https://tautulli.com/)
- [Homarr](https://homarr.dev/)
- Plex Forums
- Jellyfin Feature Requests
- Sonarr Forums
