# GitHub Actions 部署 BPH LINE OA Rich Menu

這是目前最乾淨的正式部署方式：不用本機環境、不用下載 zip、不用從 terminal 執行腳本。GitHub repo 是正式來源，GitHub Actions 直接呼叫 LINE Messaging API。

## 1. 設定 GitHub Secret

到 GitHub repo：

```txt
obmij/bph_RichMenu → Settings → Secrets and variables → Actions → New repository secret
```

新增：

```txt
Name: LINE_CHANNEL_ACCESS_TOKEN
Value: LINE Developers Console 裡 Messaging API channel 的 Channel access token
```

不要把 token 寫進 README、issue、commit、Apps Script 檔案或任何公開內容。

## 2. 執行部署 workflow

到 GitHub repo：

```txt
Actions → Deploy BPH LINE Rich Menu → Run workflow
```

參數：

```txt
dry_run=false
set_default=true
```

按下 `Run workflow` 後，workflow 會自動：

1. 檢查 `LINE_CHANNEL_ACCESS_TOKEN` 是否存在。
2. 檢查 rich menu JSON 與 PNG 是否存在。
3. 檢查 PNG 是否小於 1 MB。
4. 呼叫 LINE `/v2/bot/richmenu/validate` 驗證 JSON。
5. 建立 rich menu object。
6. 上傳 `richmenu/bph-rich-menu-main-2500x1686.png`。
7. 將 rich menu 設成所有好友的 default rich menu。
8. 建立或更新 alias：`bph-youth-hostel-2026`。
9. 在 workflow summary 顯示 rich menu ID。

## 3. 只驗證不部署

若只是想確認 JSON 與 token 正常：

```txt
Actions → Deploy BPH LINE Rich Menu → Run workflow
dry_run=true
set_default=true
```

`dry_run=true` 只會驗證，不會建立、不會上傳、不會設成 default。

## 4. 驗收

部署成功後：

1. 用手機加入或打開 BPH LINE OA。
2. 下方 chat bar 應顯示 `Backpackers Hostel`。
3. 點開後應看到六格：旅店據點、客房介紹、設施服務、在地景點、聯絡我們、線上訂房。
4. 每格應連到對應 BPH 網站或訂房系統。

## 5. 常見錯誤

### Missing GitHub Actions secret: LINE_CHANNEL_ACCESS_TOKEN

GitHub Secret 還沒設定，或 secret 名稱拼錯。名稱必須完全是：

```txt
LINE_CHANNEL_ACCESS_TOKEN
```

### 401 Unauthorized

LINE Channel access token 無效、過期、貼錯 channel，或多了空白。

### Rich menu image must be smaller than 1 MB for LINE

圖片超過 LINE rich menu 限制。重新執行 `Generate BPH Rich Menu Artwork` workflow，或壓縮 PNG 後再 commit。

### 400 The request body has 1 error

通常是 `richmenu/bph-rich-menu-area-map.json` 的 bounds、URL 或 action 格式錯誤。先用 `dry_run=true` 檢查。