# 北海岸小旅行

入口為 index.html，保留原本卡片、導航、打卡、分享功能。六站文字、三張輪播圖的標記、餐廳及旅人筆記皆為靜態 HTML；沒有 JavaScript 仍可閱讀、滑圖與開啟地圖。

## 自動更新

GitHub Pages 從 main 分支根目錄發布。日常修改 index.html 後會自動部署。

天氣由瀏覽器直接讀取 Open-Meteo（模式估計與預報，非現地測站），使用 Asia/Taipei。每 15 分鐘及返回頁面時重新整理。跨日或讀取失敗不顯示過期天氣。

scripts/update_tides.py 讀取氣象署公開 30 日鄉鎮潮汐表，檢核日期、欄位及筆數後產生 data/tides.json。石門對應麟山鼻、富基，淡水對應海堤與沙灘。潮高相對當地平均海平面，非即時測站水位；乾潮不等於安全下水。

.github/workflows/refresh-tides.yml 每 6 小時及手動執行更新。無 API key。頁面優先讀取 raw.githubusercontent.com/Oloid666/north-coast-trip/main/data/tides.json（支援 CORS），失敗時使用內嵌快照；快照沒有當天資料就顯示查詢提示。這讓 GITHUB_TOKEN 提交資料後，不依賴 Pages 重建即可更新潮汐。GitHub 排程可能延遲，公開 repo 長期無活動時可能停用，請在 Actions 檢查。若 push 遭拒，檢查 Settings → Actions → General → Workflow permissions 是否允許 Read and write。

## 圖片、來源與位置

每站附照片作者、CC 授權與來源。Wikimedia Commons 照片由外部縮圖載入，失敗時明確標示並回退到原創插畫；原有插畫已內嵌。新增 6 幅 AI 情境插畫放於 assets/road-cycle-scenes.png，與 HTML 同次部署。

- 第 1、2 站：景點照片。
- 第 3 站：龍舌蘭植物品種照片，不是小院子店內實拍。
- 第 4 站：位置仍待確認。藍海大道主題情境插畫，附公開旅人文章，不把推測當確定位置。
- 第 5 站：金色水岸觀海長堤海堤段，與淡水老街河岸、八里觀海長堤不同。使用清楚標示的主題插畫，另附新北官方實景與入口連結。
- 第 6 站：沙崙周邊海岸照片，不宣稱是海上皇宮外觀或指定座標現場照。辨位使用甲山林官方作品頁 https://construction.jsl.com.tw/case/237（淡水濱海路三段571號），建案照片請以官方頁核對，不搬運未取得授權的建案照片。沙灘導航仍是 25.191273, 121.419416，不導向私人社區入口。

餐廳為區域順遊候選，非即時距離排序；未列未查證評分、價格或營業狀態。第 4 站定位未確認，餐廳不宣稱就在拍照點旁。旅遊 tips 整理公開旅人分享並附來源，仍以現場公告為準。

## 互動與驗證

原生橫向 scroll-snap 三圖輪播、按鈕及鍵盤切圖、點圖放大（含 Escape、焦點限制與返回）、專屬動畫、親子小任務、localStorage 打卡、系統分享／複製／LINE 分享。尊重 prefers-reduced-motion。

已檢查 JavaScript 語法、靜態六站／18 圖／12 餐廳、地圖座標、重複 ID；以 DOM 測試確認輪播、動畫清理、打卡資料異常、放大操作、分享回退、天氣離線與過期處理、潮汐日期檢查。雲端執行環境啟動失敗，最後改以 GitHub 工具完成；尚無 Safari、LINE 內瀏覽器實機排版驗證。
