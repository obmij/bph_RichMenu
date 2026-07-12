/**
 * Rich menu deployment commands.
 * Run richMenuSetup() or setup() from Apps Script editor after setting Script Properties.
 */
function validateBphRichMenu() {
  const body = getBphRichMenuObject_();
  return lineApiRequest_('/v2/bot/richmenu/validate', 'post', body);
}

function checkBphRichMenuImage() {
  const image = prepareBphRichMenuImage_();
  return {
    ok: true,
    bytes: image.byteLength,
    maxBytes: LINE_RICH_MENU_MAX_IMAGE_BYTES,
    contentType: image.contentType,
    url: image.url
  };
}

function createBphRichMenu_() {
  const body = getBphRichMenuObject_();
  const result = lineApiRequest_('/v2/bot/richmenu', 'post', body);
  if (!result.richMenuId) throw new Error('No richMenuId returned by LINE.');
  return result.richMenuId;
}

function uploadBphRichMenuImage_(richMenuId, preparedImage) {
  const image = preparedImage || prepareBphRichMenuImage_();
  return lineApiRequest_(
    '/v2/bot/richmenu/' + richMenuId + '/content',
    'post',
    image.bytes,
    { dataApi: true, rawBytes: true, contentType: image.contentType }
  );
}

function setDefaultBphRichMenu_(richMenuId) {
  return lineApiRequest_('/v2/bot/user/all/richmenu/' + richMenuId, 'post');
}

function upsertBphRichMenuAlias_(richMenuId) {
  const aliasId = BPH_DEFAULTS.aliasId;
  try {
    return lineApiRequest_('/v2/bot/richmenu/alias', 'post', {
      richMenuAliasId: aliasId,
      richMenuId: richMenuId
    });
  } catch (error) {
    return lineApiRequest_('/v2/bot/richmenu/alias/' + aliasId, 'post', {
      richMenuId: richMenuId
    });
  }
}

function setupBphRichMenu() {
  validateBphRichMenu();
  const image = prepareBphRichMenuImage_();
  let richMenuId = null;

  try {
    richMenuId = createBphRichMenu_();
    uploadBphRichMenuImage_(richMenuId, image);
    setDefaultBphRichMenu_(richMenuId);
    upsertBphRichMenuAlias_(richMenuId);
    PropertiesService.getScriptProperties().setProperty('BPH_ACTIVE_RICH_MENU_ID', richMenuId);
    Logger.log('BPH rich menu deployed: ' + richMenuId);
    return richMenuId;
  } catch (error) {
    if (richMenuId) {
      try {
        deleteRichMenuById_(richMenuId);
        Logger.log('Deleted incomplete rich menu after deployment failure: ' + richMenuId);
      } catch (cleanupError) {
        Logger.log('Failed to clean up incomplete rich menu ' + richMenuId + ': ' + cleanupError.message);
      }
    }
    throw error;
  }
}

function listBphRichMenus() {
  return lineApiRequest_('/v2/bot/richmenu/list', 'get');
}

function getDefaultBphRichMenuId() {
  return lineApiRequest_('/v2/bot/user/all/richmenu', 'get');
}

function clearDefaultBphRichMenu() {
  return lineApiRequest_('/v2/bot/user/all/richmenu', 'delete');
}

function deleteAllRichMenusCreatedByApi() {
  try {
    clearDefaultBphRichMenu();
  } catch (error) {
    Logger.log('Default rich menu clear skipped: ' + error.message);
  }
  const result = listBphRichMenus();
  const deleted = [];
  (result.richmenus || []).forEach(function(menu) {
    deleteRichMenuById_(menu.richMenuId);
    deleted.push(menu.richMenuId);
  });
  Logger.log('Deleted rich menus: ' + JSON.stringify(deleted));
  return deleted;
}