#!/usr/bin/env bash
# railway-doctor: diagnose a Railway service
set -uo pipefail

URL="${1:-}"
PROJECT="${2:-}"

if [ -z "$URL" ]; then
    echo "Usage: doctor.sh <service-url> [project-name]"
    exit 1
fi

DOMAIN=$(echo "$URL" | sed -E 's|https?://||' | cut -d/ -f1)

echo "=== Railway Doctor: $DOMAIN ==="
echo
echo "## DNS"
echo "CNAME:"
dig +short CNAME "$DOMAIN" || echo "  (no CNAME — may be apex domain)"
echo "A:"
dig +short A "$DOMAIN"
echo "_railway-verify TXT:"
VERIFY=$(dig +short TXT "_railway-verify.$DOMAIN")
if [ -z "$VERIFY" ]; then
    echo "  MISSING — domain verification will fail"
else
    echo "  $VERIFY"
fi
echo
echo "## SSL"
echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null \
    | openssl x509 -noout -issuer -dates 2>/dev/null \
    || echo "  SSL handshake failed"
echo
echo "## HTTP health"
HEALTH_URL="$URL/api/health"
curl -sS -m 10 -o /tmp/health.out -w "Status: %{http_code}  |  Time: %{time_total}s\n" "$HEALTH_URL" || echo "  Request failed"
if [ -s /tmp/health.out ]; then
    echo "Body:"
    head -c 500 /tmp/health.out
    echo
fi
echo
echo "## Railway CLI"
if command -v railway >/dev/null 2>&1; then
    if [ -n "$PROJECT" ]; then
        echo "Logs tail for $PROJECT (last 30 lines):"
        railway logs --project "$PROJECT" 2>&1 | tail -30 || echo "  (railway CLI returned error — check auth with 'railway whoami')"
    else
        railway status 2>&1 || echo "  Not in a linked Railway project. Run 'railway link' first."
    fi
else
    echo "  railway CLI not installed. Install: npm i -g @railway/cli"
fi
echo
echo "=== end ==="
