# Backpackers Hostel LINE OA @：Google clasp 部署步驟與指令

本 repo 專門放 Backpackers Hostel / BPH 的 LINE OA Rich Menu、Google Apps Script 程式與部署指令。網站內容留在 `bph` repo；LINE OA 相關程式集中在 `bph_RichMenu`。

> 重點：不要用 GitHub Actions。正式流程使用 Google `clasp` 指令把 `src/` 推送到 Google Apps Script，再由 Apps Script 呼叫 LINE Messaging API 部署 rich menu。

## 0. 目錄結構

```txt
bph_RichMenu/
├── src/                              # Google Apps Script 原始碼
│   ├── appsscript.json
│   ├── Code.gs
│   ├── BphConfig.gs
│   ├── LineApi.gs
│   ├── RichMenuSetup.gs
│   └── Webhook.gs
├── richmenu/
│   ├── bph-rich-menu-main-2500x1686.png
│   └── bph-rich-menu-area-map.json
├── scripts/
│   ├── line-rich-menu-create.sh      # 備援：terminal 直接呼叫 LINE API
│   └── line-rich-menu-delete-all.sh  # 備援：清除 API 建立的 rich menu
├── tools/
│   └── generate_richmenu_art.py      # 手動重新產生 rich menu 圖
└── docs/
    └── DEPLOY_LINE_OA.md
```

## 1. LINE Developers 準備

1. 進入 LINE Developers Console。
2. 建立或選擇 Provider。
3. 建立 Messaging API channel。
4. 到 Messaging API 分頁取得：
   - Channel access token：給 Apps Script 呼叫 LINE Messaging API。
   - Channel secret：Webhook 嚴格簽章驗證時使用。
5. 在 LINE Official Account Manager 確認帳號狀態、加入好友測試、基本回覆設定。

## 2. 安裝與登入 clasp

```bash
git clone https://github.com/obmij/bph_RichMenu.git
cd bph_RichMenu
npm install
npx clasp login
```

如果尚未啟用 Google Apps Script API，先到 Google 帳號的 Apps Script API 設定頁啟用後，再重跑：

```bash
npx clasp login
```

## 3. 建立 Apps Script 專案

新建專案：

```bash
npx clasp create --type standalone --title "BPH Rich Menu" --rootDir src
```

建立完成後，repo 會產生 `.clasp.json`，內容應類似：

```json
{
  "scriptId": "YOUR_SCRIPT_ID",
  "rootDir": "src"
}
```

如果已經有既有 Apps Script 專案，使用：

```bash
cp .clasp.json.example .clasp.json
# 編輯 .clasp.json，填入既有 Apps Script ID
```

## 4. 推送 Apps Script 程式

```bash
npx clasp push
npx clasp open
```

推送後，Apps Script 專案內應看到：

```txt
Code.gs
BphConfig.gs
LineApi.gs
RichMenuSetup.gs
Webhook.gs
appsscript.json
```

## 5. 設定 Script Properties

在 Apps Script 編輯器：

1. 左側點「專案設定」。
2. 到「Script Properties」。
3. 新增以下屬性：

```txt
LINE_CHANNEL_ACCESS_TOKEN=你的 Messaging API Channel access token
LINE_CHANNEL_SECRET=你的 Channel secret
BPH_RICH_MENU_IMAGE_URL=https://raw.githubusercontent.com/obmij/bph_RichMenu/main/richmenu/bph-rich-menu-main-2500x1686.png
```

不要把 token 寫進 GitHub repo、README、commit、issue 或公開文件。

## 6. 授權 Apps Script

先在 Apps Script 編輯器手動執行一次：

```txt
setupBphRichMenu
```

第一次會要求授權，授權後可以繼續使用 clasp 指令執行。

## 7. 用 clasp 執行部署

授權完成後，可直接用 clasp 呼叫部署函式：

```bash
npx clasp run setupBphRichMenu
```

部署成功時，Apps Script Logger 會出現：

```txt
BPH rich menu deployed: richmenu-xxxxxxxxxxxxxxxx
```

`setupBphRichMenu()` 會依序執行：

1. 驗證 rich menu JSON。
2. 建立 rich menu object。
3. 從 GitHub raw URL 下載正式 rich menu PNG。
4. 上傳圖片到 LINE。
5. 設成所有好友的 default rich menu。
6. 建立或更新 alias：`bph-youth-hostel-2026`。

## 8. 更新程式後重新部署

修改 `src/` 任何檔案後：

```bash
npx clasp push
npx clasp run setupBphRichMenu
```

如果只改 webhook 內容、但不用重建 LINE rich menu，可以只 push：

```bash
npx clasp push
```

## 9. 部署 Apps Script Web App Webhook

```bash
npx clasp deploy --description "BPH LINE OA Webhook"
```

接著在 Apps Script 編輯器確認 Web App 部署設定：

1. Execute as：選 `Me`。
2. Who has access：選 `Anyone`。
3. 複製 Web app URL。
4. 到 LINE Developers Console → Messaging API → Webhook settings。
5. Webhook URL 貼上 Web app URL。
6. 開啟 `Use webhook`。
7. 點 `Verify` 測試。

Webhook 目前支援：

- `follow`：新好友加入時回覆歡迎訊息。
- 使用者輸入 `menu`、`選單`、`rich menu`：回覆如何打開選單。

## 10. Rich Menu 圖片來源

正式圖片在 GitHub：

```txt
richmenu/bph-rich-menu-main-2500x1686.png
```

若需要重新產生圖片，才使用：

```bash
python3 -m pip install pillow
python3 tools/generate_richmenu_art.py
npx clasp push
```

## 11. 驗收清單

- [ ] LINE OA 加好友後，下方顯示 `Backpackers Hostel` chat bar。
- [ ] 點開 rich menu 後六格清楚顯示。
- [ ] 點「旅店據點」會進入 BPH 據點頁。
- [ ] 點「客房介紹」會進入客房頁。
- [ ] 點「設施服務」會進入設施頁。
- [ ] 點「在地景點」會進入在地景點頁。
- [ ] 點「聯絡我們」會進入聯絡頁。
- [ ] 點「線上訂房」會進入訂房系統。
- [ ] 傳送 `menu` 或 `選單` 可收到 webhook 回覆。

## 12. 備援：terminal 直接呼叫 LINE API

只有在 Apps Script/clasp 不可用時才用這個。這不是主路線。

```bash
export LINE_CHANNEL_ACCESS_TOKEN='你的 Channel access token'

bash scripts/line-rich-menu-create.sh \
  richmenu/bph-rich-menu-area-map.json \
  richmenu/bph-rich-menu-main-2500x1686.png
```

清掉 API 建立的 rich menu：

```bash
export LINE_CHANNEL_ACCESS_TOKEN='你的 Channel access token'
bash scripts/line-rich-menu-delete-all.sh
```

## 13. 常見錯誤

### Apps Script API has not been used

Google 帳號尚未啟用 Apps Script API。啟用後重新執行：

```bash
npx clasp login
```

### No script found. Please create or clone a script first.

`.clasp.json` 不存在或 scriptId 錯誤。先執行：

```bash
npx clasp create --type standalone --title "BPH Rich Menu" --rootDir src
```

或確認 `.clasp.json` 的 scriptId。

### Missing Script Property: LINE_CHANNEL_ACCESS_TOKEN

Apps Script 專案尚未設定 Script Properties，或 key 名稱拼錯。

### 400: The image size is not allowed for richmenu

圖片不符合 LINE 規格。請確認：PNG 或 JPEG、寬度 800–2500 px、高度 250 px 以上、寬高比大於等於 1.45、檔案小於 1 MB。

### 400: An image has already been uploaded to the richmenu

LINE 不允許替換同一個 rich menu 物件的圖片。請重新建立 rich menu，再上傳新圖片。

### 401 Unauthorized

`LINE_CHANNEL_ACCESS_TOKEN` 錯誤、過期或沒有貼完整。

### 415 Unsupported Media Type

上傳 PNG 時 header 必須是 `Content-Type: image/png`。上傳 JPEG 時改用 `Content-Type: image/jpeg`。