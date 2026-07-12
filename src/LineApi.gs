/**
 * Minimal LINE Messaging API client for Google Apps Script.
 */
const LINE_API_BASE = 'https://api.line.me';
const LINE_API_DATA_BASE = 'https://api-data.line.me';
const LINE_RICH_MENU_MAX_IMAGE_BYTES = 1000000; // LINE rich menu image max: 1 MB.

function lineApiRequest_(path, method, payload, options) {
  options = options || {};
  const url = (options.dataApi ? LINE_API_DATA_BASE : LINE_API_BASE) + path;
  const params = {
    method: method || 'get',
    muteHttpExceptions: true,
    headers: {
      Authorization: 'Bearer ' + getLineAccessToken_()
    }
  };

  if (payload !== undefined && payload !== null) {
    if (options.rawBytes) {
      params.contentType = options.contentType || 'application/octet-stream';
      params.payload = payload;
    } else {
      params.contentType = 'application/json';
      params.payload = JSON.stringify(payload);
    }
  }

  const response = UrlFetchApp.fetch(url, params);
  const status = response.getResponseCode();
  const text = response.getContentText();
  if (status < 200 || status >= 300) {
    throw new Error('LINE API error ' + status + ' ' + String(method || 'get').toUpperCase() + ' ' + path + ': ' + text);
  }
  return text ? JSON.parse(text) : {};
}

function downloadImageBlob_(url) {
  const response = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
  const status = response.getResponseCode();
  if (status < 200 || status >= 300) {
    throw new Error('Failed to download rich menu image: ' + status + ' ' + response.getContentText());
  }
  return response.getBlob();
}

function normalizeImageContentType_(blob, url) {
  const contentType = String(blob.getContentType() || '').toLowerCase();
  if (contentType === 'image/png' || contentType === 'image/jpeg') return contentType;

  const path = String(url || '').split('?')[0].toLowerCase();
  if (path.endsWith('.png')) return 'image/png';
  if (path.endsWith('.jpg') || path.endsWith('.jpeg')) return 'image/jpeg';

  throw new Error('Rich menu image must be PNG or JPEG. Actual content type: ' + (contentType || '(unknown)'));
}

function prepareBphRichMenuImage_() {
  const url = getBphRichMenuImageUrl_();
  const blob = downloadImageBlob_(url);
  const bytes = blob.getBytes();
  const byteLength = bytes.length;
  const contentType = normalizeImageContentType_(blob, url);

  if (byteLength > LINE_RICH_MENU_MAX_IMAGE_BYTES) {
    throw new Error(
      'Rich menu image is too large before upload: ' + byteLength +
      ' bytes. LINE rich menu image max is 1 MB. Compress or replace BPH_RICH_MENU_IMAGE_URL before running setup.'
    );
  }

  Logger.log('Rich menu image validated: ' + byteLength + ' bytes, ' + contentType + ', ' + url);
  return { bytes: bytes, byteLength: byteLength, contentType: contentType, url: url };
}

function deleteRichMenuById_(richMenuId) {
  return lineApiRequest_('/v2/bot/richmenu/' + richMenuId, 'delete');
}