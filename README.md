# bph_RichMenu

Backpackers Hostel / BPH 專用 LINE OA Rich Menu 與 Google Apps Script 部署 repo。

這個 repo 是 **GitHub 上的正式部署來源**。不是要你安裝一套本機測試環境；本機指令只作為備援。LINE OA 實際部署目標是：

1. LINE Developers / LINE Official Account
2. Google Apps Script
3. GitHub repo 內的 rich menu 圖與 Apps Script 程式

## 本次整理重點

- 將 LINE OA @ 相關 Apps Script 集中到 `src/`。
- 新增青年旅館風格 rich menu 產圖工具：`tools/generate_richmenu_art.py`。
- 新增並已由 GitHub Actions 產生正式圖片：`richmenu/bph-rich-menu-main-2500x1686.png`。
- 新增 6 格 tap area map：`richmenu/bph-rich-menu-area-map.json`。
- 新增 Apps Script 一鍵部署函式：`setupBphRichMenu()`。
- 新增 terminal/curl 部署腳本：`scripts/line-rich-menu-create.sh`，僅作備援。
- 新增完整部署文件：`docs/DEPLOY_LINE_OA.md`。

## Rich Menu 六格

1. 旅店據點
2. 客房介紹
3. 設施服務
4. 在地景點
5. 聯絡我們
6. 線上訂房

## GitHub-first 部署方式

到 Apps Script 建立專案後，把 `src/` 裡的 `.gs` 與 `appsscript.json` 放進 Apps Script，設定 Script Properties：

```txt
LINE_CHANNEL_ACCESS_TOKEN=你的 Messaging API Channel access token
LINE_CHANNEL_SECRET=你的 Channel secret
BPH_RICH_MENU_IMAGE_URL=https://raw.githubusercontent.com/obmij/bph_RichMenu/main/richmenu/bph-rich-menu-main-2500x1686.png
```

然後在 Apps Script 執行：

```txt
setupBphRichMenu
```

完整步驟請看：[`docs/DEPLOY_LINE_OA.md`](docs/DEPLOY_LINE_OA.md)。

## 備援 CLI 指令

只有當你要從 terminal 直接呼叫 LINE Messaging API 時才需要：

```bash
export LINE_CHANNEL_ACCESS_TOKEN='你的 Channel access token'
bash scripts/line-rich-menu-create.sh \
  richmenu/bph-rich-menu-area-map.json \
  richmenu/bph-rich-menu-main-2500x1686.png
```

這不是本機測試環境；只是把 GitHub repo 內的 LINE rich menu JSON 與圖片上傳到 LINE OA。