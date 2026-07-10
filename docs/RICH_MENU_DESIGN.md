# BPH LINE OA Rich Menu 設計說明

## 視覺方向

新版 rich menu 以「背包客青年旅館」為主軸，改掉原本較生硬的卡片感，改成旅人、城市地圖、上下舖、交誼空間、台北在地探索、聯絡與訂房的整體插畫語言。

## 品牌呼應

- 使用網站 Logo 的登山／背包客剪影概念作為每格右上角識別。
- 配色延續網站 Pantone 8 色：Stretch Limo、Cloud Dancer、Scarlet Smile、Bordeaux、Dragonfly、Graphite、Satin Slipper、Micron。
- 版型維持 LINE OA 常用 3 x 2 六格，方便精準對應 tap area。

## 六格內容

1. 旅店據點：城市地圖、路線與雙據點標籤。
2. 客房介紹：上下舖、閱讀燈與背包。
3. 設施服務：Wi‑Fi、交誼沙發、洗衣與咖啡。
4. 在地景點：台北城市、夜市燈籠、旅遊移動符號。
5. 聯絡我們：LINE 對話、Email、手機與櫃台。
6. 線上訂房：日曆、鑰匙、行李箱與快速預訂箭頭。

## LINE 規格

- 圖片：`richmenu/bph-rich-menu-main-2500x1686.png`
- 尺寸：2500 x 1686 px
- 點擊區域：`richmenu/bph-rich-menu-area-map.json`
- 建議檔案大小：低於 1 MB。

## 重新產圖

```bash
python3 tools/generate_richmenu_art.py
```

GitHub Actions 也會在相關檔案異動時自動執行產圖 workflow。