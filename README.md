# bph_RichMenu

Backpackers Hostel / BPH 專用 LINE OA Rich Menu 與 Google Apps Script 部署 repo。

這個 repo 是 **Google Apps Script / clasp 部署來源**。不要使用 GitHub Actions 部署；正式流程改為使用 Google `clasp` 指令將 `src/` 推送到 Apps Script，然後在 Apps Script 執行 `setupBphRichMenu()` 部署到 LINE OA。

## 本次整理重點

- 將 LINE OA @ 相關 Apps Script 集中到 `src/`。
- 保留青年旅館風格 rich menu 產圖工具：`tools/generate_richmenu_art.py`。
- 正式 rich menu 圖：`richmenu/bph-rich-menu-main-2500x1686.png`。
- 6 格 tap area map：`richmenu/bph-rich-menu-area-map.json`。
- Apps Script 一鍵部署函式：`setupBphRichMenu()`。
- 部署文件改為 Google clasp：`docs/DEPLOY_LINE_OA.md`。
- GitHub Actions 部署文件與 workflow 已移除；不要再使用 Actions 部署 LINE OA。

## Rich Menu 六格

1. 旅店據點
2. 客房介紹
3. 設施服務
4. 在地景點
5. 聯絡我們
6. 線上訂房

## Google clasp 部署流程

```bash
git clone https://github.com/obmij/bph_RichMenu.git
cd bph_RichMenu
npm install
npx clasp login
npx clasp create --type standalone --title "BPH Rich Menu" --rootDir src
npx clasp push
npx clasp open
```

在 Apps Script 專案設定 Script Properties：

```txt
LINE_CHANNEL_ACCESS_TOKEN=你的 Messaging API Channel access token
LINE_CHANNEL_SECRET=你的 Channel secret
BPH_RICH_MENU_IMAGE_URL=https://raw.githubusercontent.com/obmij/bph_RichMenu/main/richmenu/bph-rich-menu-main-2500x1686.png
```

第一次先在 Apps Script 編輯器手動執行 `setupBphRichMenu` 完成授權；之後可用 clasp 執行：

```bash
npx clasp run setupBphRichMenu
```

完整步驟請看：[`docs/DEPLOY_LINE_OA.md`](docs/DEPLOY_LINE_OA.md)。

## 備援：terminal 直接呼叫 LINE API

只有當你不想透過 Apps Script 執行 rich menu 建立時才需要：

```bash
export LINE_CHANNEL_ACCESS_TOKEN='你的 Channel access token'
bash scripts/line-rich-menu-create.sh \
  richmenu/bph-rich-menu-area-map.json \
  richmenu/bph-rich-menu-main-2500x1686.png
```

這不是本機測試環境；只是用 LINE Messaging API 直接部署 rich menu。