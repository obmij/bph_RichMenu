/**
 * Optional Apps Script web app endpoint for LINE webhook health checks.
 * Apps Script web apps don't expose request headers to doPost(), so this file is intentionally minimal.
 * For production-grade webhook signature validation, deploy the webhook on Cloud Run / Cloud Functions.
 */
function doGet() {
  return jsonOutput_({ ok: true, service: 'bph-richmenu', timestamp: new Date().toISOString() });
}

function doPost(e) {
  const bodyText = e && e.postData && e.postData.contents ? e.postData.contents : '{}';
  let body;
  try {
    body = JSON.parse(bodyText);
  } catch (error) {
    return jsonOutput_({ ok: false, error: 'Invalid JSON' });
  }

  const events = body.events || [];
  events.forEach(function(event) {
    if (event.type === 'follow' && event.replyToken) {
      replyText_(event.replyToken, '歡迎加入 Backpackers Hostel！下方選單可查看旅店據點、客房、設施、在地景點與線上訂房。');
    }
    if (event.type === 'message' && event.message && event.message.type === 'text' && event.replyToken) {
      const text = String(event.message.text || '').trim();
      if (/^(menu|選單|rich menu)$/i.test(text)) {
        replyText_(event.replyToken, '請點開下方 Backpackers Hostel 選單。需要訂房請選「線上訂房」。');
      }
    }
  });

  return jsonOutput_({ ok: true });
}

function replyText_(replyToken, text) {
  return lineApiRequest_('/v2/bot/message/reply', 'post', {
    replyToken: replyToken,
    messages: [{ type: 'text', text: text }]
  });
}

function jsonOutput_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}