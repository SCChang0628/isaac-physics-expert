# Linux CPU 親和性與 Isaac Sim Worker 預算

Isaac Sim 5.1.0 工程案例。先讀 `os.sched_getaffinity(0)` 得到程序實際允許的 logical CPUs，才能處理容器、cpuset 和非連續 ID。透過 `/sys/devices/system/cpu` topology 查同一實體核心的 SMT 兄弟；共用一個核心的執行緒盡量留在同一區。保留一組 CPU 給控制程序共用，其餘給模擬。可依核心類型與工作量調整，單一實體核心則容許共用。手動覆寫時檢查範圍、空集合及預期互斥。

在 `SimulationApp` 建立 worker 前設定 affinity，並讓 worker 上限跟可用 CPU 數量一致。控制程序共用同一池，避免每個程序各自釘住同一核心或重新計算分配。當任一相關程序仍在運行時沿用同一份配置。以固定場景比較 RTF、app update rate、控制回應延遲及負載，依實測決定是否保留該分配。
