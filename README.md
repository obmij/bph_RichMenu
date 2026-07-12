# bph_RichMenu

Backpackers Hostel / BPH 專用 LINE OA Rich Menu、GitHub Actions 部署流程與 Google Apps Script 程式 repo。

這個 repo 是 **GitHub 上的正式部署來源**。不是本機測試環境；正式部署目標是：

1. LINE Developers / LINE Official Account
2. GitHub Actions：直接部署 LINE rich menu
3. Google Apps Script：選用 webhook / 輕量自動回覆
4. GitHub repo 內的 rich menu 圖、area map 與 Apps Script 程式

## 本次整理重點

- 將 LINE OA @ 相關 Apps Script 集中到 `src/`。
- 新增青年旅館風格 rich menu 產圖工具：`tools/generate_richmenu_art.py`。
- 新增並已由 GitHub Actions 產生正式圖片：`richmenu/bph-rich-menu-main-2500x1686.png`。
- 新增 6 格 tap area map：`richmenu/bph-rich-menu-area-map.json`。
- 新增 **GitHub Actions 正式部署 workflow**：`.github/workflows/deploy-line-richmenu.yml`。
- 新增 Apps Script 一鍵部署函式：`setupBphRichMenu()`，作為第二部署路線。
- 新增完整部署文件：`docs/GITHUB_ACTIONS_DEPLOY.md`、`docs/DEPLOY_LINE_OA.md`。

## Rich Menu 六格

1. 旅店據點
2. 客房介紹
3. 設施服務
4. 在地景點
5. 聯絡我們
6. 線上訂房

## 首選：GitHub Actions 雲端部署

在 GitHub repo 設定 Secret：

```txt
Settings → Secrets and variables → Actions → New repository secret
Name: LINE_CHANNEL_ACCESS_TOKEN
Value: LINE Developers Console 的 Messaging API Channel access token
```

然後執行：

```txt
Actions → Deploy BPH LINE Rich Menu → Run workflow
dry_run=false
set_default=true
```

workflow 會直接驗證 JSON、建立 rich menu、上傳 GitHub repo 內的 PNG、設成 LINE OA default rich menu，並建立 alias `bph-youth-hostel-2026`。

完整步驟請看：[`docs/GITHUB_ACTIONS_DEPLOY.md`](docs/GITHUB_ACTIONS_DEPLOY.md)。

## 第二路線：Google Apps Script

若要把 webhook / 輕量回覆也放到 Apps Script，請看：[`docs/DEPLOY_LINE_OA.md`](docs/DEPLOY_LINE_OA.md)。

Apps Script 的主要部署函式仍是：

```txt
setupBphRichMenu
```

## 備援 CLI 指令

CLI 只作備援；正式部署請優先用 GitHub Actions。