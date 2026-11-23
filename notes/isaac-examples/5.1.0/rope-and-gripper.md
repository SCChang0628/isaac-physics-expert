# 升降繩索視覺、Surface Gripper 與原生 OmniGraph 節點

Isaac Sim 5.1.0 / Kit 107.3 工程案例。繩索節點讀取上端與吊具的即時剛體 pose，將上端點轉到吊具局部座標。沿局部 Z 計算兩端距離及中心，對等效高度為 1 的繩索網格更新 `xformOp:scale` 與 `xformOp:translate`。長度近零時限制最小值。以 Session Layer 更新視覺，兩端 pose 應與 Fabric 畫面一致。可快取靜態尺度及 handle，重建後重新讀取。

抓取節點以 Surface Gripper 的狀態和 PhysX 剛體 live pose 核對實際附著物件。使用距離、方向以及夾爪狀態防止拉錯候選物，將吸附與釋放視為狀態轉移。對應的關節回授宜取即時物理讀值，避免關閉 USD 回寫後停在起始值。用無窗測試驅動兩個升降高度，核對繩索長度、相應關節回授及夾爪釋放後載具落下。

部署原生節點時，先為目標 Kit、OS 與架構建置，再於開啟含該節點的 USD 前啟用 extension。USD 保存 OmniGraph 節點類型名稱，原生程式庫由 extension 提供。更新原生程式庫可先產生新檔，原子替換後重啟程序，避免截斷執行中已載入的檔案。
