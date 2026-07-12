# LINE Webhook Verify：401 Unauthorized

## 結論

LINE 顯示：

```txt
The webhook returned an HTTP status code other than 200.(401 Unauthorized)
```

這不是 LINE token 問題，也不是 `doPost()` 回傳格式問題。這代表 LINE Platform 打到你的 Apps Script Web App URL 時，被 Google 擋在授權層，通常是以下其中一個：

1. Web App access 不是公開匿名存取。
2. 使用了 `/dev` test deployment URL；`/dev` 只允許有 Apps Script 編輯權限的人存取。
3. LINE Developers 貼到的不是 `/exec` 正式部署 URL。
4. 修改程式後沒有重新部署 Web App version。

LINE webhook 需要外部平台 POST 時拿到 HTTP 200；Google Apps Script Web App 要能被 LINE 存取，就必須公開到 `ANYONE_ANONYMOUS` 並使用 `/exec` URL。

## 已在 repo 修正的地方

`src/appsscript.json` 已加入：

```json
"webapp": {
  "access": "ANYONE_ANONYMOUS",
  "executeAs": "USER_DEPLOYING"
}
```

這會讓 clasp 部署 Web App 時使用公開匿名存取設定。

## 修正指令

```bash
git pull
npx clasp push --force
npx clasp deploy --description "BPH LINE OA Webhook public"
npx clasp deployments
```

在 `npx clasp deployments` 的輸出中找到最新 deployment ID，Web App URL 應為：

```txt
https://script.google.com/macros/s/DEPLOYMENT_ID/exec
```

把這個 `/exec` URL 貼到：

```txt
LINE Developers Console
→ Messaging API
→ Webhook settings
→ Webhook URL
```

不要使用 `/dev` URL。

## 先用 curl 檢查

把部署 URL 存成變數：

```bash
WEBHOOK_URL='https://script.google.com/macros/s/DEPLOYMENT_ID/exec'
```

GET 應回 200：

```bash
curl -i "$WEBHOOK_URL"
```

POST 也應回 200：

```bash
curl -i -X POST "$WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d '{"events":[]}'
```

預期要看到：

```txt
HTTP/2 200
```

如果 curl 都還是 401，代表 Web App deployment access 沒套到公開匿名，請重新部署或到 Apps Script UI 確認 deployment 設定。

## Apps Script UI 檢查

若 clasp deployment 還是 401，到 Apps Script 編輯器：

1. Deploy → Manage deployments。
2. 選 Web app deployment。
3. Edit。
4. Execute as：`Me`。
5. Who has access：`Anyone`。
6. Deploy。
7. 複製正式 Web app URL；必須以 `/exec` 結尾。
8. 到 LINE Developers 重新貼 Webhook URL。
9. 再按 Verify。

## 為什麼 `/dev` 不行

Apps Script 的 test deployment URL 以 `/dev` 結尾，只能由擁有 script 編輯權限的帳號存取；LINE Platform 當然沒有 Google 帳號登入權限，所以會收到 401。正式 webhook 必須使用 `/exec`。