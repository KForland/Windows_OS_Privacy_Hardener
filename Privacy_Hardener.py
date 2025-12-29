import ctypes
import subprocess
import sys
import glob

# ---------------- State buckets ----------------

applied = []
already = []
restored = []
failed = []
audit = []

# ---------------- Helpers ----------------

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def msgbox(text, title="Privacy Hardener", flags=0):
    return ctypes.windll.user32.MessageBoxW(0, text, title, flags)

def run(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.returncode == 0, p.stdout

# ---------------- Service helpers ----------------

def get_service_start_type(name):
    ok, out = run(f'sc qc {name}')
    if not ok:
        return None
    for line in out.splitlines():
        if "START_TYPE" in line:
            return line.split()[-1]
    return None

def ensure_service_disabled(name, label, mode):
    start_type = get_service_start_type(name)

    if start_type is None:
        already.append(label + " (service not present)")
        return

    if start_type == "DISABLED":
        already.append(label)
        return

    if mode == "audit":
        audit.append(label)
        return

    run(f'sc stop {name}')
    ok, _ = run(f'sc config {name} start= disabled')

    if ok:
        applied.append(label)
    else:
        failed.append(label)

# ---------------- Registry helpers ----------------

def reg_get(path, name):
    ok, out = run(f'reg query "{path}" /v {name}')
    return ok, out

def ensure_reg_value(path, name, rtype, value, label, mode):
    exists, out = reg_get(path, name)

    if exists and str(value) in out:
        already.append(label)
        return

    if mode == "audit":
        audit.append(label)
        return

    ok, _ = run(f'reg add "{path}" /v {name} /t {rtype} /d {value} /f')

    if ok:
        applied.append(label)
    else:
        failed.append(label)

# ---------------- Recall helpers (FIXED) ----------------

def recall_payload_present():
    matches = glob.glob(r"C:\Windows\WinSxS\*Recall*")
    return len(matches) > 0

def ensure_recall_disabled(mode):
    label = "Windows Recall"

    if not recall_payload_present():
        already.append(label)
        return

    if mode == "audit":
        audit.append(label)
        return

    ok, _ = run('dism /Online /Disable-Feature /FeatureName:Recall /Remove')

    if ok:
        applied.append(label)
    else:
        failed.append(label)

# ---------------- Admin check ----------------

if not is_admin():
    msgbox(
        "This tool must be run as Administrator.\n\n"
        "Right-click the EXE and choose:\n"
        "'Run as administrator'",
        "Administrator Required",
        0x10
    )
    sys.exit(1)

# ---------------- Mode selection ----------------

choice = msgbox(
    "WINDOWS PRIVACY HARDENER\n\n"
    "YES  → Apply privacy hardening\n"
    "NO   → Restore defaults (not implemented in this build)\n"
    "CANCEL → Audit mode (no changes)\n\n"
    "Audit mode makes NO system changes.",
    "Privacy Hardener",
    0x23
)

if choice == 6:
    mode = "apply"
elif choice == 7:
    mode = "restore"
else:
    mode = "audit"

# ---------------- APPLY / AUDIT ----------------

if mode in ("apply", "audit"):

    ensure_recall_disabled(mode)

    ensure_service_disabled("DiagTrack", "Telemetry service (DiagTrack)", mode)
    ensure_service_disabled("dmwappushservice", "Telemetry service (dmwappush)", mode)

    ensure_reg_value(
        r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection",
        "AllowTelemetry",
        "REG_DWORD", 0,
        "Telemetry level",
        mode
    )

    ensure_reg_value(
        r"HKLM\SOFTWARE\Policies\Microsoft\Windows\System",
        "EnableActivityFeed",
        "REG_DWORD", 0,
        "Activity history",
        mode
    )

# ---------------- SUMMARY (FULL VISIBILITY) ----------------

summary = ""

if applied:
    summary += "✔ Applied (changed this run):\n" + "\n".join(f"• {i}" for i in applied) + "\n\n"

if already:
    summary += "➖ Already compliant:\n" + "\n".join(f"• {i}" for i in already) + "\n\n"

if audit:
    summary += "🔍 Would be applied (audit mode):\n" + "\n".join(f"• {i}" for i in audit) + "\n\n"

if failed:
    summary += "✖ Failed:\n" + "\n".join(f"• {i}" for i in failed) + "\n\n"

if not summary:
    summary = "No managed items detected."

summary += "Reboot recommended."

msgbox(summary.strip(), "Privacy Hardener Result", 0x40)
