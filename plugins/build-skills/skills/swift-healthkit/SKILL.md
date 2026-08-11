---
name: swift-healthkit
description: Write SwiftUI + HealthKit code for the YogaBiometrics iOS app. Use when Louis asks for changes to yoga-tracker, YogaBiometrics, HealthKitService.swift, SessionAnalysisService, ClassTemplate, PoseSlot, PoseWindow join logic, or any Apple Watch biometric work. Encodes the data model, HealthKit access patterns, and the core pose window join algorithm.
---

# Swift + HealthKit Skill (YogaBiometrics)

This skill is the reusable patterns layer. The project's CLAUDE.md is the source of truth for phase status, data models, and file structure. Read it first.

## Canonical HealthKit access pattern

Always request permissions for the full set up front:

```swift
let typesToRead: Set<HKObjectType> = [
    HKObjectType.quantityType(forIdentifier: .heartRate)!,
    HKObjectType.quantityType(forIdentifier: .heartRateVariabilitySDNN)!,
    HKObjectType.quantityType(forIdentifier: .respiratoryRate)!
]
try await healthStore.requestAuthorization(toShare: [], read: typesToRead)
```

Never call `requestAuthorization` inside a service that also reads data — permissions must be granted before any query runs or the query returns empty results silently.

## Query type selection

- `HKStatisticsCollectionQuery` — interval-averaged HR (1-minute buckets work well)
- `HKSampleQuery` — HRV (SDNN), respiratory rate (too infrequent to bucket)
- `HKAnchoredObjectQuery` — only if you need incremental updates; overkill for post-session analysis

## Pose window join — the core algorithm

```swift
func buildPoseWindows(session: Session, template: ClassTemplate, samples: [BiometricSample]) -> [PoseWindow] {
    template.poses.map { slot in
        let windowStart = session.startedAt.addingTimeInterval(Double(slot.offsetSeconds))
        let windowEnd = windowStart.addingTimeInterval(Double(slot.expectedDurationSeconds))
        let windowSamples = samples.filter { $0.timestamp >= windowStart && $0.timestamp < windowEnd }
        let avgHR = windowSamples.isEmpty
            ? 0
            : windowSamples.map(\.heartRate).reduce(0, +) / Double(windowSamples.count)
        return PoseWindow(
            sessionId: session.id,
            poseName: slot.poseName,
            actualStartSeconds: slot.offsetSeconds,
            actualEndSeconds: slot.offsetSeconds + slot.expectedDurationSeconds,
            samples: windowSamples,
            avgHeartRate: avgHR,
            avgHrv: nil
        )
    }
}
```

## Anchoring rules

- All `PoseSlot.offsetSeconds` are relative to `session.startedAt`, not wall clock.
- If `startedAt` is wrong, the entire join is wrong. Build UI for confirming or adjusting it.
- Consider HR-baseline-elevation inference as a fallback for detecting true session start.

## Nil-handling

- HRV (SDNN): sampled infrequently, may be nil for any given pose window.
- Respiratory rate: device-dependent; not all Apple Watch models report it.
- Never crash on nil biometric values; report "—" in UI and exclude from averages.

## project.pbxproj edits

DO NOT hand-edit `YogaBiometrics.xcodeproj/project.pbxproj` except to register a new file. Structural changes go through Xcode's UI. If Louis asks to "reorganize the project structure," direct him to Xcode rather than editing the pbxproj directly.
