/**
 * Minimal LINE Messaging API client for Google Apps Script.
 */
const LINE_API_BASE = 'https://api.line.me';
const LINE_API_DATA_BASE = 'https://api-data.line.me';

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

function downloadImageBytes_(url) {
  const response = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
  const status = response.getResponseCode();
  if (status < 200 || status >= 300) {
    throw new Error('Failed to download rich menu image: ' + status + ' ' + response.getContentText());
  }
  return response.getBlob().getBytes();
}