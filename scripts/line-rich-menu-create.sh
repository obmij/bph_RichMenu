#!/usr/bin/env bash
set -euo pipefail

TOKEN="${LINE_CHANNEL_ACCESS_TOKEN:?Set LINE_CHANNEL_ACCESS_TOKEN first.}"
JSON_PATH="${1:-richmenu/bph-rich-menu-area-map.json}"
IMAGE_PATH="${2:-richmenu/bph-rich-menu-main-2500x1686.png}"

if [[ ! -f "$JSON_PATH" ]]; then
  echo "Missing rich menu JSON: $JSON_PATH" >&2
  exit 1
fi
if [[ ! -f "$IMAGE_PATH" ]]; then
  echo "Missing rich menu image: $IMAGE_PATH" >&2
  echo "Run: python3 tools/generate_richmenu_art.py" >&2
  exit 1
fi

curl -fsS -X POST 'https://api.line.me/v2/bot/richmenu/validate' \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  --data-binary "@${JSON_PATH}" >/dev/null

echo 'Rich menu JSON validated.'

RICH_MENU_ID=$(curl -fsS -X POST 'https://api.line.me/v2/bot/richmenu' \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  --data-binary "@${JSON_PATH}" | python3 -c 'import json,sys; print(json.load(sys.stdin)["richMenuId"])')

echo "Created rich menu: ${RICH_MENU_ID}"

curl -fsS -X POST "https://api-data.line.me/v2/bot/richmenu/${RICH_MENU_ID}/content" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: image/png' \
  --data-binary "@${IMAGE_PATH}" >/dev/null

echo 'Uploaded image.'

curl -fsS -X POST "https://api.line.me/v2/bot/user/all/richmenu/${RICH_MENU_ID}" \
  -H "Authorization: Bearer ${TOKEN}" >/dev/null

echo "Default rich menu set: ${RICH_MENU_ID}"