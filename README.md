Windows Privacy Hardener

Windows Privacy Hardener is a lightweight Windows utility for auditing and applying basic privacy hardening controls using only native Windows mechanisms. It is designed to be transparent, minimal, and dependency-free.

The tool supports audit-only execution, produces a clear post-run summary, and does not install services, scheduled tasks, drivers, or any form of persistence.

Windows Privacy Hardener can detect and disable Windows Recall if present, stop and disable telemetry-related services such as DiagTrack and dmwappushservice, and apply policy-safe registry settings to reduce telemetry collection and activity history. All changes are performed using built-in Windows tools including sc, reg, and dism.

Administrator privileges are required. If the tool is not run as Administrator, it will exit immediately without making changes.

On launch, the user selects an execution mode through a dialog prompt. Selecting YES applies privacy hardening changes. Selecting CANCEL runs the tool in audit mode and makes no changes. Selecting NO is reserved for restore mode, which is not implemented in the current build.

After execution, a summary dialog is displayed showing which changes were applied, which items were already compliant, which actions would have been applied in audit mode, and any operations that failed. A system reboot is recommended after applying changes.

The tool makes no network connections, installs nothing, and leaves no background components. It is suitable for personal systems, security labs, and demonstrations of policy-based Windows hardening.

Restore mode is not implemented. Group Policy or enterprise management solutions may override local settings. Windows Recall detection is heuristic-based and may vary across Windows versions.

Use at your own risk. Review the source code before running.
