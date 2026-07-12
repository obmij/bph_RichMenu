/**
 * BPH / Backpackers Hostel LINE OA configuration.
 * Store secrets in Apps Script Properties, never in source control.
 */
const BPH_SCRIPT_PROPERTIES = {
  LINE_CHANNEL_ACCESS_TOKEN: 'LINE_CHANNEL_ACCESS_TOKEN',
  LINE_CHANNEL_SECRET: 'LINE_CHANNEL_SECRET',
  BPH_RICH_MENU_IMAGE_URL: 'BPH_RICH_MENU_IMAGE_URL'
};

const BPH_DEFAULTS = {
  richMenuImageUrl: 'https://raw.githubusercontent.com/obmij/bph_RichMenu/main/richmenu/bph-rich-menu-main-2500x1686.png',
  richMenuName: 'BPH Youth Hostel Rich Menu 2026',
  // LINE requires chatBarText to be no longer than 14 characters.
  chatBarText: 'BPH Hostel',
  aliasId: 'bph-youth-hostel-2026'
};

const BPH_SITE_URLS = {
  locations: 'https://www.bph.com.tw/%E8%A5%BF%E9%96%80%E5%BA%97.html',
  rooms: 'https://www.bph.com.tw/%E5%AE%A2%E6%88%BF%E4%BB%8B%E7%B4%B9_%E8%A5%BF%E9%96%80%E5%BA%97.html',
  facilities: 'https://www.bph.com.tw/%E8%A8%AD%E6%96%BD%E6%9C%8D%E5%8B%99_%E8%A5%BF%E9%96%80%E5%BA%97.html',
  localGuide: 'https://www.bph.com.tw/%E5%9C%A8%E5%9C%B0%E6%99%AF%E9%BB%9E.html',
  contact: 'https://www.bph.com.tw/%E8%81%AF%E7%B5%A1%E6%88%91%E5%80%91_%E8%A5%BF%E9%96%80%E5%BA%97.html',
  booking: 'https://res.windsurfercrs.com/ibe/index.aspx?propertyID=17484&nono=1&adults=2&lang=zh-tw'
};

function getScriptProperty_(key, fallback) {
  const value = PropertiesService.getScriptProperties().getProperty(key);
  if (value) return value;
  if (fallback !== undefined) return fallback;
  throw new Error('Missing Script Property: ' + key);
}

function getLineAccessToken_() {
  return getScriptProperty_(BPH_SCRIPT_PROPERTIES.LINE_CHANNEL_ACCESS_TOKEN);
}

function getBphRichMenuImageUrl_() {
  return getScriptProperty_(BPH_SCRIPT_PROPERTIES.BPH_RICH_MENU_IMAGE_URL, BPH_DEFAULTS.richMenuImageUrl);
}

function getBphRichMenuObject_() {
  return {
    size: { width: 2500, height: 1686 },
    selected: true,
    name: BPH_DEFAULTS.richMenuName,
    chatBarText: BPH_DEFAULTS.chatBarText,
    areas: [
      {
        bounds: { x: 0, y: 0, width: 833, height: 843 },
        action: { type: 'uri', label: '旅店據點', uri: BPH_SITE_URLS.locations }
      },
      {
        bounds: { x: 833, y: 0, width: 833, height: 843 },
        action: { type: 'uri', label: '客房介紹', uri: BPH_SITE_URLS.rooms }
      },
      {
        bounds: { x: 1666, y: 0, width: 834, height: 843 },
        action: { type: 'uri', label: '設施服務', uri: BPH_SITE_URLS.facilities }
      },
      {
        bounds: { x: 0, y: 843, width: 833, height: 843 },
        action: { type: 'uri', label: '在地景點', uri: BPH_SITE_URLS.localGuide }
      },
      {
        bounds: { x: 833, y: 843, width: 833, height: 843 },
        action: { type: 'uri', label: '聯絡我們', uri: BPH_SITE_URLS.contact }
      },
      {
        bounds: { x: 1666, y: 843, width: 834, height: 843 },
        action: { type: 'uri', label: '線上訂房', uri: BPH_SITE_URLS.booking }
      }
    ]
  };
}