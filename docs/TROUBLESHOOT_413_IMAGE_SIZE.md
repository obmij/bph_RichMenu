# 413 Request Entity Too Large：Rich Menu 圖片太大

## 原因

LINE rich menu image 的官方限制是：

- PNG 或 JPEG
- width：800–2500 px
- height：250 px 以上
- aspect ratio：width / height >= 1.45
- max file size：1 MB

如果圖片超過 1 MB，就不能拿去做 LINE rich menu image。若直接呼叫 upload endpoint，可能會得到 `413 Request Entity Too Large` 或 rich menu image size error。

## 本 repo 的修正

Apps Script 現在會先下載 `BPH_RICH_MENU_IMAGE_URL`，檢查：

1. MIME type 必須是 `image/png` 或 `image/jpeg`。
2. 檔案大小必須小於等於 `1000000` bytes。
3. 檢查通過後才會建立 rich menu object。
4. 如果建立後上傳失敗，會嘗試刪除未完成的 rich menu，避免留下半成品。

因此後續不會再先建立 rich menu、再讓 LINE upload endpoint 才報 413。

## 先檢查圖片，不部署

推送最新 Apps Script 後：

```bash
npx clasp push --force
npx clasp run checkRichMenuImage
```

或在 Apps Script 編輯器選擇：

```txt
checkRichMenuImage
```

成功會回傳：

```json
{
  "ok": true,
  "bytes": 942195,
  "maxBytes": 1000000,
  "contentType": "image/png",
  "url": "..."
}
```

## 壓縮圖片

如果圖片超過 1 MB，請先壓縮後再更新 GitHub raw image 或 `BPH_RICH_MENU_IMAGE_URL`。

範例：把任何來源圖轉成 2500 x 1686、160 色 PNG：

```bash
python3 - <<'PY'
from PIL import Image
from pathlib import Path

src = Path('source-rich-menu.png')
out = Path('richmenu/bph-rich-menu-main-2500x1686.png')
W, H = 2500, 1686
im = Image.open(src).convert('RGB')
scale = max(W / im.width, H / im.height)
im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
left = (im.width - W) // 2
top = (im.height - H) // 2
im = im.crop((left, top, left + W, top + H))
im = im.quantize(colors=160, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
out.parent.mkdir(parents=True, exist_ok=True)
im.save(out, optimize=True)
print(out, out.stat().st_size, 'bytes')
if out.stat().st_size > 1000000:
    raise SystemExit('Still too large for LINE rich menu image')
PY
```

接著：

```bash
git add richmenu/bph-rich-menu-main-2500x1686.png
git commit -m "assets: compress rich menu image under LINE limit"
git push
npx clasp push --force
npx clasp run checkRichMenuImage
npx clasp run richMenuSetup
```

## 注意

`/v2/bot/richmenu/validate` 只驗證 rich menu JSON，不會驗證圖片檔案大小；圖片大小必須在 upload 前自行檢查。