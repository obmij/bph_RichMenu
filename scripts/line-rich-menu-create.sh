#!/usr/bin/env bash
set -euo pipefail

TOKEN="${LINE_CHANNEL_ACCESS_TOKEN:?Set LINE_CHANNEL_ACCESS_TOKEN first.}"
JSON_PATH="${1:-richmenu/bph-rich-menu-area-map.json}"
IMAGE_PATH="${2:-richmenu/bph-rich-menu-main-2500x1686.png}"
MAX_IMAGE_BYTES=1000000

if [[ ! -f "$JSON_PATH" ]]; then
  echo "Missing rich menu JSON: $JSON_PATH" >&2
  exit 1
fi
if [[ ! -f "$IMAGE_PATH" ]]; then
  echo "Missing rich menu image: $IMAGE_PATH" >&2
  echo "Run: python3 tools/generate_richmenu_art.py" >&2
  exit 1
fi

IMAGE_BYTES=$(wc -c < "$IMAGE_PATH" | tr -d ' ')
if [[ "$IMAGE_BYTES" -gt "$MAX_IMAGE_BYTES" ]]; then
  echo "Rich menu image is too large: ${IMAGE_BYTES} bytes. LINE rich menu image max is 1 MB." >&2
  echo "Compress or replace ${IMAGE_PATH} before uploading." >&2
  exit 1
fi

echo "Rich menu image validated: ${IMAGE_BYTES} bytes."

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

if [[ "${IMAGE_PATH,,}" == *.jpg || "${IMAGE_PATH,,}" == *.jpeg ]]; then
  CONTENT_TYPE='image/jpeg'
else
  CONTENT_TYPE='image/png'
fi

if ! curl -fsS -X POST "https://api-data.line.me/v2/bot/richmenu/${RICH_MENU_ID}/content" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: ${CONTENT_TYPE}" \
  --data-binary "@${IMAGE_PATH}" >/dev/null; then
  echo "Image upload failed. Deleting incomplete rich menu ${RICH_MENU_ID}." >&2
  curl -fsS -X DELETE "https://api.line.me/v2/bot/richmenu/${RICH_MENU_ID}" \
    -H "Authorization: Bearer ${TOKEN}" >/dev/null || true
  exit 1
fi

echo 'Uploaded image.'

curl -fsS -X POST "https://api.line.me/v2/bot/user/all/richmenu/${RICH_MENU_ID}" \
  -H "Authorization: Bearer ${TOKEN}" >/dev/null

echo "Default rich menu set: ${RICH_MENU_ID}"