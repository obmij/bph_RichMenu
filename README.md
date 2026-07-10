# bph_RichMenu

Backpackers Hostel / BPH 專用 LINE OA Rich Menu 與 Google Apps Script 部署 repo。

## 本次整理重點

- 將 LINE OA @ 相關 Apps Script 集中到 `src/`。
- 新增青年旅館風格 rich menu 產圖工具：`tools/generate_richmenu_art.py`。
- 新增 6 格 tap area map：`richmenu/bph-rich-menu-area-map.json`。
- 新增 Apps Script 一鍵部署函式：`setupBphRichMenu()`。
- 新增 terminal/curl 部署腳本：`scripts/line-rich-menu-create.sh`。
- 新增完整部署文件：`docs/DEPLOY_LINE_OA.md`。
- 新增 GitHub Actions：推送後可自動產生 `richmenu/bph-rich-menu-main-2500x1686.png`。

## Rich Menu 六格

1. 旅店據點
2. 客房介紹
3. 設施服務
4. 在地景點
5. 聯絡我們
6. 線上訂房

## 快速部署

```bash
git clone https://github.com/obmij/bph_RichMenu.git
cd bph_RichMenu
npm install
npx clasp login
npx clasp create --type standalone --title "BPH Rich Menu"
npx clasp push
```

到 Apps Script 設定 `LINE_CHANNEL_ACCESS_TOKEN` 後執行：

```txt
setupBphRichMenu
```

完整步驟請看：[`docs/DEPLOY_LINE_OA.md`](docs/DEPLOY_LINE_OA.md)

## 重新產生 rich menu 圖

```bash
python3 tools/generate_richmenu_art.py
```

圖片需維持 2500 x 1686 px，且小於 1 MB。