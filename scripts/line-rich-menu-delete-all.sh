#!/usr/bin/env bash
set -euo pipefail

TOKEN="${LINE_CHANNEL_ACCESS_TOKEN:?Set LINE_CHANNEL_ACCESS_TOKEN first.}"

curl -fsS -X DELETE 'https://api.line.me/v2/bot/user/all/richmenu' \
  -H "Authorization: Bearer ${TOKEN}" >/dev/null || true

echo 'Default rich menu cleared.'

IDS=$(curl -fsS -X GET 'https://api.line.me/v2/bot/richmenu/list' \
  -H "Authorization: Bearer ${TOKEN}" | python3 -c 'import json,sys; print("\n".join([x["richMenuId"] for x in json.load(sys.stdin).get("richmenus", [])]))')

if [[ -z "$IDS" ]]; then
  echo 'No API-created rich menus found.'
  exit 0
fi

while IFS= read -r ID; do
  [[ -z "$ID" ]] && continue
  curl -fsS -X DELETE "https://api.line.me/v2/bot/richmenu/${ID}" \
    -H "Authorization: Bearer ${TOKEN}" >/dev/null
  echo "Deleted ${ID}"
done <<< "$IDS"