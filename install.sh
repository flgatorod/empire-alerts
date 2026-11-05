#!/bin/bash
# Install the empire-alerts relay on the Mac Mini (user moltypham).
#
#   cd ~/empire-alerts && ./install.sh            # install / reinstall both jobs
#   ./install.sh --test                           # send ONE real test iMessage, then exit
#   ./install.sh --uninstall                      # unload and remove both jobs
#
# Needs: Messages signed in on this Mac (the Apple ID Hyperion used), and a
# config.json with your number. The installer creates config.json from the
# example the first time and stops so you can fill it in.
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
AGENTS="$HOME/Library/LaunchAgents"
JOBS=(relay snapshot)
PY="$(command -v python3.12 || command -v python3)"

uninstall() {
  for j in "${JOBS[@]}"; do
    launchctl bootout "gui/$(id -u)/com.empire-alerts.$j" 2>/dev/null || true
    rm -f "$AGENTS/com.empire-alerts.$j.plist"
  done
  echo "Uninstalled. config.json, state/ and logs/ were left in place."
}

case "${1:-}" in
  --uninstall) uninstall; exit 0 ;;
  --test)
    cd "$REPO"
    ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"; id="install-test-$(date +%s)"
    mkdir -p state
    printf '{"id":"%s","created_at":"%s","priority":"urgent","source":"install","text":"Relay test from the Mini. If you can read this, Claude alerts will reach you here."}\n' "$id" "$ts" > "state/$id.json"
    set +e
    "$PY" - "$REPO" "state/$id.json" <<'PY'
import sys, json, os
sys.path.insert(0, os.path.join(sys.argv[1], "relay"))
import send_outbox as s
cfg = s.load_config()
if not cfg["recipient"]:
    sys.exit("TEST NOT SENT — config.json has no real recipient yet. Set it, run ./install.sh, then retry.")
a = s.validate(open(sys.argv[2]).read(), cfg)
ok = s.send_imessage(cfg["prefix"] + a["text"], cfg["recipient"])
print("TEST SENT" if ok else "TEST FAILED — see logs/relay.log")
sys.exit(0 if ok else 1)
PY
    rc=$?; rm -f "state/$id.json"; exit $rc ;;
esac

[ -n "$PY" ] || { echo "python3 not found"; exit 1; }
"$PY" -c 'import zoneinfo' || { echo "Python 3.9+ required ($PY)"; exit 1; }
git -C "$REPO" remote get-url origin >/dev/null || { echo "Run this inside a git clone of flgatorod/empire-alerts"; exit 1; }

if [ ! -f "$REPO/config.json" ]; then
  cp "$REPO/config.example.json" "$REPO/config.json"
  chmod 600 "$REPO/config.json"
  echo "Created config.json. Put your iMessage number (or Apple ID email) in \"recipient\", then rerun ./install.sh"
  exit 1
fi
"$PY" - "$REPO/config.json" <<'PY' || exit 1
import json, sys
r = json.load(open(sys.argv[1])).get("recipient", "")
if not r or r.startswith("+1XXX"):
    sys.exit("config.json has no recipient yet — fill it in and rerun ./install.sh")
PY

mkdir -p "$REPO/logs" "$REPO/state" "$AGENTS"
for j in "${JOBS[@]}"; do
  sed -e "s#__REPO__#$REPO#g" -e "s#__PYTHON__#$PY#g" \
    "$REPO/launchd/com.empire-alerts.$j.plist.template" > "$AGENTS/com.empire-alerts.$j.plist"
  launchctl bootout "gui/$(id -u)/com.empire-alerts.$j" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$AGENTS/com.empire-alerts.$j.plist"
done
sleep 3
launchctl list | grep com.empire-alerts || { echo "jobs did not load"; exit 1; }
echo
echo "Installed: relay (every 2 min) and snapshot (every 15 min)."
echo "Next: ./install.sh --test   (sends one real test text)"
