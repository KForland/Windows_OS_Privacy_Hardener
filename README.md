Windows Privacy Hardener is a lightweight Windows utility for auditing and applying privacy hardening controls using only native Windows mechanisms. It supports audit-only execution, produces a clear summary of changes, and does not install services, tasks, or persistence.

The tool can disable Windows Recall if present, stop and disable telemetry-related services including DiagTrack and dmwappushservice, and apply policy-safe registry settings to reduce telemetry and activity history. All changes are made using built-in Windows tools such as sc, reg, and dism.

Administrator privileges are required. The tool will exit if not run as admin.

On launch, the user selects a mode via dialog:
YES applies changes.
CANCEL runs in audit mode with no changes.
NO is reserved for restore mode, which is not implemented.

After execution, a summary is shown listing applied changes, items already compliant, actions that would be applied in audit mode, and any failures. A reboot is recommended.

The tool makes no network connections, installs nothing, and leaves no background components. It is suitable for personal systems, security labs, and demonstrations of policy-based hardening.

Restore mode is not implemented. Group Policy or enterprise management may override local settings. Recall detection is heuristic-based.

Use at your own risk. Review the source before running.
