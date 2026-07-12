# Backpackers Hostel LINE OA @ 部署步驟與指令

本 repo 專門放 Backpackers Hostel / BPH 的 LINE OA Rich Menu、Google Actions 部署流程與 Google Apps Script 程式。網站內容請留在 `bph` repo；LINE OA 相關程式集中在 `bph_RichMenu`。

> 重點：這不是本機安裝或測試環境。正式來源在 GitHub。首選部署路線是 GitHub Actions 直接部署到 LINE OA；Google Apps Script 作為 webhook / 輕量自動回覆與第二部署路線。

## 0. 目錄結構

```txt
bph_RichMenu/
├── .github/workflows/
│   ├── deploy-line-richmenu.yml       # 首選：GitHub Actions 直接部署 LINE rich menu
│   └── generate-richmenu.yml          # 產生 rich menu PNG
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
│   ├── line-rich-menu-create.sh      # 備援：terminal 直接部署 rich menu
│   └── line-rich-menu-delete-all.sh  # 備援：清除 API 建立的 rich menu
├── tools/
│   └── generate_richmenu_art.py      # 由 GitHub Actions 執行產圖
└── docs/
    ├── GITHUB_ACTIONS_DEPLOY.md
    ├── DEPLOY_LINE_OA.md
    └── RICH_MENU_DESIGN.md
```

## 1. LINE Developers 準備

1. 進入 LINE Developers Console。
2. 建立或選擇 Provider。
3. 建立 Messaging API channel。
4. 到 Messaging API 分頁取得：
   - Channel access token：給 GitHub Actions / Apps Script 呼叫 LINE Messaging API。
   - Channel secret：Webhook 嚴格簽章驗證時使用。
5. 在 LINE Official Account Manager 確認帳號狀態、加入好友測試、基本回覆設定。

## 2. 首選：GitHub Actions 直接部署 Rich Menu

這是建議路線：不建立任何本機測試環境，GitHub repo 直接作為正式部署來源。

### 2.1 設定 GitHub Secret

到 GitHub repo：

```txt
obmij/bph_RichMenu → Settings → Secrets and variables → Actions → New repository secret
```

新增：

```txt
Name: LINE_CHANNEL_ACCESS_TOKEN
Value: LINE Developers Console 裡 Messaging API channel 的 Channel access token
```

### 2.2 執行 workflow

到 GitHub repo：

```txt
Actions → Deploy BPH LINE Rich Menu → Run workflow
```

參數：

```txt
dry_run=false
set_default=true
```

workflow 會自動：

1. 檢查 token、JSON 與 PNG。
2. 驗證 LINE rich menu JSON。
3. 建立 rich menu object。
4. 上傳 `richmenu/bph-rich-menu-main-2500x1686.png`。
5. 設成所有好友的 default rich menu。
6. 建立或更新 alias：`bph-youth-hostel-2026`。
7. 在 GitHub Actions summary 顯示 rich menu ID。

完整文件：[`docs/GITHUB_ACTIONS_DEPLOY.md`](GITHUB_ACTIONS_DEPLOY.md)。

## 3. 第二路線：Google Apps Script 部署 Rich Menu / Webhook

若要把 webhook / 輕量回覆也放到 Apps Script，再做這段。

### 3.1 建立 Google Apps Script 專案

1. 進入 Google Apps Script。
2. 建立新專案，命名為 `BPH Rich Menu`。
3. 在 Apps Script 專案內建立與 GitHub `src/` 相同檔案：
   - `Code.gs`
   - `BphConfig.gs`
   - `LineApi.gs`
   - `RichMenuSetup.gs`
   - `Webhook.gs`
   - `appsscript.json`
4. 將 GitHub `src/` 內各檔內容複製到 Apps Script 專案。

### 3.2 設定 Apps Script Properties

在 Apps Script 編輯器：

1. 左側點「專案設定」。
2. 到「Script Properties」。
3. 新增以下屬性：

```txt
LINE_CHANNEL_ACCESS_TOKEN=你的 Messaging API Channel access token
LINE_CHANNEL_SECRET=你的 Channel secret
BPH_RICH_MENU_IMAGE_URL=https://raw.githubusercontent.com/obmij/bph_RichMenu/main/richmenu/bph-rich-menu-main-2500x1686.png
```

### 3.3 執行 Apps Script 部署函式

在 Apps Script 編輯器上方選擇函式：

```txt
setupBphRichMenu
```

按「執行」。第一次執行需授權。成功後 Logger 會出現：

```txt
BPH rich menu deployed: richmenu-xxxxxxxxxxxxxxxx
```

這個函式會依序執行：驗證 rich menu、建立 rich menu object、從 GitHub raw URL 下載正式 PNG、上傳圖片到 LINE、設成 default rich menu、建立或更新 alias。

## 4. 部署 Apps Script Web App Webhook

在 Apps Script 編輯器：

1. 點「部署」→「新增部署」。
2. 類型選「網頁應用程式」。
3. Execute as：選 `Me`。
4. Who has access：選 `Anyone`。
5. 部署後複製 Web app URL。
6. 到 LINE Developers Console → Messaging API → Webhook settings。
7. Webhook URL 貼上 Web app URL。
8. 開啟 `Use webhook`。
9. 點 `Verify` 測試。

Webhook 目前支援：

- `follow`：新好友加入時回覆歡迎訊息。
- 使用者輸入 `menu`、`選單`、`rich menu`：回覆如何打開選單。

## 5. 備援：用 terminal/curl 部署 Rich Menu

這不是本機測試環境，只是直接從 terminal 呼叫 LINE Messaging API。只有在 GitHub Actions 無法使用時才需要。

```bash
export LINE_CHANNEL_ACCESS_TOKEN='你的 Channel access token'

bash scripts/line-rich-menu-create.sh \
  richmenu/bph-rich-menu-area-map.json \
  richmenu/bph-rich-menu-main-2500x1686.png
```

## 6. Rich Menu 圖片來源

正式圖片在 GitHub：

```txt
richmenu/bph-rich-menu-main-2500x1686.png
```

GitHub Actions 會在 `tools/generate_richmenu_art.py` 或 rich menu 設定異動時重新產圖。

## 7. 驗收清單

- [ ] LINE OA 加好友後，下方顯示 `Backpackers Hostel` chat bar。
- [ ] 點開 rich menu 後六格清楚顯示。
- [ ] 點「旅店據點」會進入 BPH 據點頁。
- [ ] 點「客房介紹」會進入客房頁。
- [ ] 點「設施服務」會進入設施頁。
- [ ] 點「在地景點」會進入在地景點頁。
- [ ] 點「聯絡我們」會進入聯絡頁。
- [ ] 點「線上訂房」會進入訂房系統。
- [ ] 傳送 `menu` 或 `選單` 可收到 webhook 回覆。

## 8. 常見錯誤

### Missing GitHub Actions secret: LINE_CHANNEL_ACCESS_TOKEN

GitHub Secret 還沒設定，或 secret 名稱拼錯。名稱必須完全是 `LINE_CHANNEL_ACCESS_TOKEN`。

### 400: The image size is not allowed for richmenu

圖片不符合 LINE 規格。請確認：PNG 或 JPEG、寬度 800–2500 px、高度 250 px 以上、寬高比大於等於 1.45、檔案小於 1 MB。

### 400: An image has already been uploaded to the richmenu

LINE 不允許替換同一個 rich menu 物件的圖片。請重新建立 rich menu，再上傳新圖片。

### 401 Unauthorized

`LINE_CHANNEL_ACCESS_TOKEN` 錯誤、過期或沒有貼完整。

### 415 Unsupported Media Type

上傳 PNG 時 header 必須是 `Content-Type: image/png`。上傳 JPEG 時改用 `Content-Type: image/jpeg`。

### 中文網址跳轉異常

LINE request body 內的 URI 建議使用 UTF-8 percent-encoding。此 repo 的 `richmenu/bph-rich-menu-area-map.json` 已使用編碼後網址。