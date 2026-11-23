# ROS 2 里程計、模擬時鐘與狀態新鮮度

Isaac Sim 5.1.0 工程案例。顯示移動機器人的前後速度時，訂閱既有 `nav_msgs/msg/Odometry`，取有正負號的 `twist.twist.linear.x`（m/s）。依 publisher namespace 與實際 topic 設定解析名稱。使用 Isaac Sim 原生 `isaacsim.ros2.bridge.ROS2Subscriber` 在 Session Layer 建立顯示用 OmniGraph，由 `OnTick` 降頻更新。比例、符號及 QoS 應與實際資料比對，可用 latest-only、相容的 QoS 做顯示快取。未收到有限值時，顯示預設值並用獨立狀態區分訊息未到與真正靜止。

把模擬時間發布到 `/clock` 時，先檢查場景內是否已有 publisher；訂閱端若使用 sim time，保持 clock 與播放狀態一致。監視端以接收時間判斷樣本新鮮度，暫停後舊值可保留顯示，但需標示過期。一次重啟後只把本次播放收到的樣本標為即時。

測試在獨立 ROS domain 發送正、負、零的 X 速度，另外給非零 Y/Z，確認顯示沒有使用三維速度絕對值。涵蓋 namespace 與絕對 topic、暫停重播、過期樣本及無訊息路徑。量測顯示訂閱對既有 publisher 頻率的影響。
