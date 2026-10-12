# Vorssaint (`vorssaint-utils`) — End-to-End Architectural & Codebase Analysis

> **Target Repository:** [vorssaint/vorssaint-utils](https://github.com/vorssaint/vorssaint-utils)  
> **Repository Scale:** ~54 MB, 1,040+ Git objects, 350+ Swift source and test files  
> **Target Platform:** macOS 14+ (Sonoma, Sequoia) — Native Apple Silicon (`arm64`)  
> **License:** GPL-3.0-or-later  
> **Analysis Date:** October 2026  
> **Orchestrated By:** `master-skiller` Architectural Framework (`architecture` + `nodejs-best-practices` + `libreoffice-base` pipeline)

---

## 1. Executive Summary & Value Proposition

**Vorssaint** is a unified, local-first macOS system utility engineered to consolidate the functionality of over a dozen standalone commercial Mac applications into a single, high-performance menu bar application.

### Unified Product Map (Commercial Replacements)

| Category | Commercial / Paid Mac Apps Replaced | Vorssaint Subsystem |
|---|---|---|
| **Audio Routing & Control** | SoundSource, BackgroundMusic, Audio Hijack | `AppVolumeMixer`, `BoostLimiter`, `SoundOutputSwitcher` |
| **System Telemetry & Fans** | iStat Menus, Stats, Macs Fan Control, TG Pro | `SystemMonitor`, `SMCClient`, `FanControlHelper` |
| **Window Management** | Magnet, Rectangle Pro, Moom, BetterSnapTool | `WindowLayoutService`, `WindowGestureSupport` |
| **App Switching & Dock** | AltTab, Contexts, DockDoor, HyperDock | `AppSwitcher`, `DockPreview`, `WindowPreviewProvider` |
| **Screen Capture & OCR** | CleanShot X, Shottr, TextSniper, ScreenFlow | `RecorderCaptureEngine`, `ScreenRecorderService`, `OCR` |
| **Clipboard & Snippets** | Maccy, Paste, TextExpander, Raycast Snippets | `ClipboardHistoryService`, `TextSnippetService` |
| **File Staging** | Dropover, Yoink | `ShelfService`, `ShelfFilePromiseTransfer` |
| **Notch & AI Tracking** | DynamicLake, NotchNook, Claude/Codex CLIs | `NotchService`, `AgentUsageService`, `NotchAgentsView` |
| **App Maintenance** | AppCleaner, CleanMyMac, DaisyDisk | `AppUninstaller`, `JunkCleaner`, `Homebrew` |
| **Display & Energy** | Lunar, MonitorControl, Vivid, Amphetamine | `BrightnessService`, `ExtraBrightnessService`, `KeepAwakeManager` |

---

## 2. Core Architectural Principles

```
┌────────────────────────────────────────────────────────────────────────┐
│                        VORSSAINT ARCHITECTURE                          │
├────────────────────────────────────────────────────────────────────────┤
│ 1. ZERO EXTERNAL SWIFT DEPENDENCIES                                    │
│    Package.swift dependencies: []                                      │
│    Relies strictly on macOS system frameworks (SwiftUI, AppKit,        │
│    CoreAudio, ScreenCaptureKit, Vision, AVFoundation).                 │
│                                                                        │
│ 2. LOW-LEVEL SYSTEM BRIDGING (C / Mach Kernel)                         │
│    • HIDEventSystem: C module intercepting raw mouse/keyboard events.  │
│    • VMStatisticsCompat: Direct Mach kernel memory pressure stats.    │
│    • SMCClient: Apple Silicon System Management Controller bridge.     │
│    • FanControlHelper: XPC root helper for thermal/fan management.     │
│                                                                        │
│ 3. MODULAR FEATURE ISOLATION ("Install Only What You Use")             │
│    Uninstalled modules are unloaded from memory entirely.              │
│    Permissions are requested JIT (Just-In-Time) per enabled feature.  │
│                                                                        │
│ 4. LOCAL-FIRST & ZERO TELEMETRY                                        │
│    No analytics SDKs, no external database, no user accounts.         │
│    Zero network calls except user-initiated actions (Homebrew, etc.).  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Subsystem Breakdown & Implementation Details

### 3.1 Audio Subsystem (`Sources/Vorssaint/Services/Audio`)
- **Per-App Volume Mixing (`AppVolumeMixer.swift`):** Intercepts application audio streams via `CoreAudio` process-level taps without requiring third-party audio drivers or kexts.
- **Volume Booster (`BoostLimiter.swift`):** Applies DSP digital gain amplification beyond 100% (up to 200–400%) with lookahead limiting to prevent clipping distortion.
- **Audio Routing (`SoundOutputSwitcher.swift`, `AirPlayRouteManager.swift`):** Enables splitting audio outputs per application (e.g., routing Spotify to external speakers while Zoom remains on headphones).
- **Music App Launch Blocker (`MusicLaunchBlocker.swift`):** Filters Bluetooth/earphone play button presses via Accessibility taps to stop macOS from automatically launching Apple Music.

### 3.2 Hardware Telemetry & Fan Control (`Services/SystemMonitor`, `Services/FanControl`, `FanControlHelper`)
- **Direct SMC Interfacing (`SMCClient.swift`):** Communicates directly with Apple Silicon SMC keys to extract live thermal readings for CPU clusters (Efficiency & Performance), GPU cores, SoC temperatures, and battery watt-hours.
- **Fan Control Daemon (`FanControlHelper/main.swift`):** A lightweight XPC helper tool installed with root privileges that allows safe manual RPM overrides and custom fan speed curves without requiring the main app to run as root.
- **Mach Memory Diagnostics (`VMStatisticsCompat`):** Calculates exact memory pressure, wired memory, compressed memory, and page-in/page-out rates using Mach `host_statistics64`.

### 3.3 Window Management & Desktop Enhancement (`Services/WindowLayout`, `Services/Switcher`, `Services/DockPreview`)
- **Snapping & Edge Gestures (`WindowLayoutService.swift`):** Implements grid, half, third, and quadrant window snapping using `Accessibility` APIs (`AXUIElementSetAttributeValue`).
- **Live Window Switcher (`AppSwitcher.swift`, `WindowPreviewProvider.swift`):** Replaces default `⌘Tab` with an overlay presenting real-time window thumbnails captured via `ScreenCaptureKit` and `CGWindowListCreateImage`, with instant keyboard filtering.
- **Dock Previews (`DockPreview/`):** Listens to cursor hover events over the macOS Dock; resolves the hovered application bundle ID and displays miniature interactive window previews above the Dock icon.
- **Space Management (`SpacesOrder/`):** Intercepts macOS Mission Control space reordering to keep virtual desktops locked in consistent user-defined slots.

### 3.4 Keyboard & Pointer Engine (`Sources/HIDEventSystem`, `Services/SuperKey`, `Services/Mouse*`)
- **HID Event Tap (`HIDEventSystem`):** Installs low-level `CGEventTap` hooks on the Mach port loop:
  - **Smooth Scrolling (`SmoothScrollService.swift`):** Applies physics-based momentum interpolation to notched mouse wheel inputs.
  - **Super Key (`SuperKey/`):** Re-maps `Caps Lock` to execute hyper-key combinations (e.g., `⌃⌥⇧⌘`) on hold, or trigger custom actions on tap.
  - **Debounce Filters:** Ignores hardware chatter from failing mechanical mouse switches and keyboards (`MouseClickDebounce`, `KeyboardDebounce`).
  - **Linear Scrolling & Direction Inversion:** Independently inverts horizontal/vertical wheel directions without modifying trackpad natural scrolling settings.

### 3.5 AI Agent Dashboard in Dynamic Island (`Services/AgentUsage`, `UI/Notch/NotchAgentsView.swift`)
Vorssaint features an embedded **AI Coding Agent Telemetry Engine** inside the macOS Notch:
- **Supported Providers:**
  - Anthropic **Claude Code**
  - OpenAI **Codex**
  - **OpenCode**
  - **GitHub Copilot**
- **Log Parsing Engine (`AgentLogParser.swift`, `AgentClaudeAppUsage.swift`):**
  - Reads local agent session JSON files and CLI debug streams in real time.
  - Extracts token breakdowns: Prompt input, Cache Write, Cache Read, Output tokens, and Reasoning tokens.
  - Calculates real-time cache hit percentages: `Double(cacheRead) / Double(prompt)`.
  - Estimates session API costs using upstream pricing matrices (`AgentPriceSource.swift`).
  - Tracks 5-hour and weekly allowance resets and notifies the user upon long-running agent turn completion.

### 3.6 Screen Capture, Recording & Studio Tools (`Services/Recorder`, `Services/Media`)
- **Dual-Track Screen Recorder (`RecorderCaptureEngine.swift`, `RecorderSystemAudioTap.swift`):** Captures high-framerate desktop video with separate audio tracks for system audio (via `AudioTap`) and microphone input.
- **Post-Production Engine:**
  - Automatic cursor focus and camera zoom tracking (`RecorderZoomAimingTests.swift`).
  - Blur regions (`RecorderBlurRegion.swift`) to redact API keys and passwords.
  - Hardware-accelerated GIF and MP4 export via `AVAssetWriter`.
- **Offline OCR & Color Picker:** Uses Apple `Vision` framework (`VNRecognizeTextRequest`) to extract on-screen text completely offline.

### 3.7 App Hygiene & Package Management (`Services/Cleaner`, `Services/Uninstall`, `Services/Homebrew`)
- **App Uninstaller (`AppUninstaller.swift`):** Scans the file system for orphaned application containers, caches (`~/Library/Caches`), preferences (`~/Library/Preferences`), Application Support directories, and background daemons (`LaunchAgents`).
- **Homebrew GUI (`Homebrew/`):** Non-blocking subprocess wrapper around the `brew` CLI to search, update, install, and uninstall Formulae and Casks directly from the menu bar.
- **Port Manager (`PortManager/`):** Inspects open TCP/UDP sockets (`lsof` / BSD socket APIs), maps listening ports to running PIDs, and provides instant termination (`KillProcess`).

---

## 4. Codebase Directory Structure

```
vorssaint-utils/
├── Package.swift                  # SwiftPM manifest (Zero third-party dependencies)
├── build.sh                       # Developer build & installation script
│
├── Sources/
│   ├── Vorssaint/                 # Main Application Executable Target
│   │   ├── main.swift             # Application entry point & lifecycle init
│   │   ├── App/                   # App delegate, menu bar controller, state coordinators
│   │   ├── Core/                  # Base utilities, logging, reactive stores, geometry
│   │   ├── Services/              # 35+ Modular business logic subsystems
│   │   │   ├── AgentUsage/        # AI Agent telemetry (Claude, Codex, Copilot logs)
│   │   │   ├── Audio/             # App volume mixer, DSP boost, AirPlay routing
│   │   │   ├── SystemMonitor/     # CPU/GPU graphs, SMC thermal readings
│   │   │   ├── FanControl/        # Fan curves and XPC helper client
│   │   │   ├── WindowLayout/      # Snap geometry, multi-display repositioning
│   │   │   ├── Switcher/          # AltTab window switcher with live thumbnails
│   │   │   ├── DockPreview/       # Dock hover previews
│   │   │   ├── Notch/             # Dynamic Island notch interface & lyrics
│   │   │   ├── Recorder/          # Screen recording, system audio tap, GIF export
│   │   │   ├── Clipboard/         # Clipboard history & auto-clear policies
│   │   │   ├── Snippets/          # Dynamic text macro expansions
│   │   │   ├── Shelf/             # Drag-and-drop cursor staging shelf
│   │   │   ├── Cleaner/           # Cache and junk file scanning
│   │   │   └── Uninstall/         # Application removal & residue cleaner
│   │   ├── UI/                    # SwiftUI interface components & custom overlays
│   │   │   ├── Notch/             # Notch views (Agents, Music, System, Calendar)
│   │   │   ├── MenuPanel/         # Main menu bar popover and tab views
│   │   │   └── Settings/          # Settings window and Features hub
│   │   └── Support/               # Helpers, localization, and shell execution
│   │
│   ├── FanControlHelper/          # Privileged root XPC helper for fan speed control
│   ├── HIDEventSystem/            # C system module for CGEventTap / Mach taps
│   ├── VMStatisticsCompat/        # C system module for Mach VM memory telemetry
│   └── NowPlayingAdapter/         # MediaRemote framework bridge for music controls
│
├── Tests/                         # Comprehensive XCTest & shell verification suite
│   ├── TestSuite.swift            # Master test runner
│   ├── AgentUsage*.swift          # AI agent log parsing & token tests
│   ├── Notch*.swift               # Dynamic Island geometry & event tests
│   ├── Mixer*.swift               # Audio mixing and volume boost tests
│   └── Recorder*.swift            # Audio taps, timeline, and export timing tests
│
└── docs/                          # Architectural documentation
    ├── PERMISSIONS.md             # Detailed breakdown of required macOS permissions
    ├── PRIVACY.md                 # Local-first data handling statement
    └── TROUBLESHOOTING.md         # Diagnostic guidelines for permissions and SMC
```

---

## 5. Security & Permission Model

Vorssaint follows the **Principle of Least Privilege**:
- **On-Demand Permissions:** No permission is requested until the user enables a feature that explicitly requires it.
- **Revocation Alerts:** If a user uninstalls a feature, Vorssaint detects that a previously granted permission is now unused and suggests revoking it.

| Permission | Subsystems Requiring It | Fallback Behavior When Denied |
|---|---|---|
| **Accessibility (`AXUIElement`)** | Window Layout, App Switcher, Super Key, Dock Clicks | Feature disables gracefully; non-intrusive warnings displayed. |
| **Screen Recording (`CGDisplayStream`)** | Live Window Thumbnails, Dock Previews, Screen Recorder, OCR | Switcher falls back to app icons instead of live previews; OCR disabled. |
| **Microphone (`AVAudioSession`)** | Dual-track screen recording voice capture | Screen recording proceeds with system audio only. |
| **Automation (`AppleEvents`)** | Finder shortcuts, Music launch blocker | Fallback to manual clipboard operations. |
| **Root Privileges (XPC)** | Manual Fan Control override | System default thermal throttling handles fan speeds. |

---

## 6. SWOT & Technical Evaluation

### Strengths
1. **Exceptional Dependency Discipline:** Built entirely with native Swift and standard macOS system frameworks (`Package.swift` has zero external packages). This yields sub-second cold starts, zero dependency rot, and minimal binary size.
2. **True Low-Level Engineering:** Uses direct SMC reads, Mach kernel statistics, and C-level event taps rather than shelling out to slow CLI utilities like `top` or `ps`.
3. **Innovative AI Agent Integration:** Native tracking of Claude Code, Codex, and Copilot session logs right in the MacBook notch elevates it above generic utility apps.
4. **Local-First & Privacy Conscious:** Zero tracking, zero telemetry, local caching, and auditable open-source code under GPL-3.0.

### Constraints & Considerations
1. **Apple Silicon & macOS 14+ Exclusivity:** Does not support Intel Macs or older macOS releases (Ventura, Monterey).
2. **Privilege Complexity:** Fan control requires a separate privileged XPC helper (`FanControlHelper`), requiring an installer flow.
3. **Private Framework Reliance:** Media control relies on `MediaRemote` bridges, which are internal macOS APIs subject to change across major macOS updates.

---

## 7. Conclusion

Vorssaint represents one of the most comprehensive, architecturally elegant macOS utility applications available in the open-source ecosystem. By combining low-level Mach/SMC kernel access with modern SwiftUI declarative interfaces, it successfully replaces over 12 standalone commercial Mac applications with zero external dependencies and zero user telemetry.
