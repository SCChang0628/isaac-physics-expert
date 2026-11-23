# 從編輯器匯出 USDA 場景與關聯資料

Isaac Sim 5.1.0 工程案例。從已驗證的編輯器狀態形成一致的資料快照，用同一份識別碼映射產生地圖 JSON、導航 YAML 及場景 USDA。重新儲存或另存時優先保留穩定的物件識別碼，切換場景後核對新結果中的對應。工作執行緒處理序列化與檔案寫入，UI 接收進度和各步驟錯誤；匯出入口應處理同一專案正在執行模擬的狀態。

載入前儘早驗證參考資產路徑、Stage up axis、`metersPerUnit`、物理場景與 OmniGraph extension 需求。保存的 USDA 場景用於下次啟動，暫時視覺、圖及初始化覆寫可使用 Session Layer，當期 PhysX/Fabric pose 另有獨立讀取路徑。測試另存複本再重新開啟，比對資產 reference、座標、ID 與 graph 節點解析，也涵蓋匯出一半遇到 I/O 錯誤及重試。
