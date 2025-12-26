# MicroManagerr Project Context

## Project Overview
**MicroManagerr** is a planned utility application designed to integrate with **Sonarr** and **Radarr**. Its primary focus is to enhance media library management by automating metadata tagging, fixing display issues (cropping), intelligently upgrading media files to higher quality formats (HDR, Dolby Vision), and ensuring file hygiene.

## Key Features & Goals
Based on `goal.txt`, the project aims to implement the following core functionalities:

### 1. Advanced Media Tagging
*   **HDR & Dolby Vision:** Scan files for HDR and Dolby Vision metadata.
    *   Identify specific Dolby Vision profiles and fallback capabilities.
    *   Automatically apply corresponding tags in Sonarr/Radarr (create new or use existing).
*   **IMAX Enhanced:** Detect and tag IMAX profile content.
*   **Special Editions:** Identify "Extended Edition" or "Director's Cut" versions by comparing file runtimes against known database runtimes. Apply appropriate tags.

### 2. Media File Correction & Hygiene
*   **Letterbox Fix (Quick-Crop):**
    *   Detect letterboxed content.
    *   Apply MKV crop metadata tags using Linux tools (avoiding re-encoding).
    *   Useful for Ultra-Wide monitor support.
*   **Track Declutter:**
    *   Automatically analyze files to strip out unwanted audio (e.g., non-preferred languages) and subtitle tracks.
    *   Reduces file bloat and cleans up player menus.
*   **Library Organization Check:**
    *   Detect if files are in the wrong library (e.g., 1080p movie in a 4K library).
    *   Notify user and offer to move files/update paths in Sonarr/Radarr.

### 3. Media Upgrading
*   **HDR/DoVi Upgrade Search:**
    *   Search indexers for HDR/Dolby Vision versions of existing non-HDR content.
    *   **Auto-Download:** If the found release has a higher score, initiate download via Sonarr/Radarr.
    *   **User Review:** If the found release has a lower score, present it to the user with a comparison of what's missing.
    *   **Post-Processing:** Option to unmonitor items after a successful upgrade and import.

## Future Roadmap (Post-MVP)
*   **Hybrid Remux Assembler:**
    *   "Frankenstein" file creation: Merge the best video source from Release A with the best audio source from Release B.

## Current Status
*   **Phase:** Concept & Planning.
*   **Artifacts:** `goal.txt` (Requirements definition).
*   **Codebase:** Not yet initialized.

## Development Constraints & Conventions
*   **Integrations:** Must interface with Sonarr and Radarr APIs.
*   **Dependencies:** Likely requires access to underlying Linux media tools (e.g., `mkvpropedit`, `ffmpeg`, `mkvmerge`) for file manipulation.
*   **Deployment:** Docker is the intended deployment method.