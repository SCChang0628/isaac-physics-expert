# PhysX Fabric 輸出、USD 回寫與 Session Layer

Isaac Sim 5.1.0 / Kit 107.3 工程案例。使用 `isaacsim.core.utils.extensions.enable_extension('omni.physx.fabric')` 啟用 Fabric。透過 `carb.settings` 與 `omni.physxfabric.bindings._physxFabric` 啟用 `SETTING_FABRIC_ENABLED`、`SETTING_FABRIC_UPDATE_TRANSFORMATIONS`、`SETTING_FABRIC_UPDATE_VELOCITIES` 和 `SETTING_FABRIC_UPDATE_JOINT_STATES`。依賴關節回授的 OmniGraph 也要確認仍能取得 Fabric 狀態。透過 `omni.physx.bindings._physx` 關閉 `SETTING_UPDATE_TO_USD` 及 `SETTING_UPDATE_VELOCITIES_TO_USD`，並將 `/persistent/omnigraph/updateToUsd` 設為 `False`。

用 `stage.SetEditTarget(stage.GetSessionLayer())` 或 `Usd.EditContext(stage, stage.GetSessionLayer())` 安排執行期間的初始化、外觀及暫存圖。這些 USD authored opinions 與 PhysX 每幀輸出是不同的資料。修改場景檔的「儲存／匯出」是另一個明確的操作。Fabric 方案下，`UsdGeom.XformCache` 仍會反映 composed USD 上的 authored 變換。攝影機、標籤、故障框等執行期讀取端應透過即時 PhysX 姿態或 Fabric world matrix 取座標。

驗證時先記錄 root layer 的 `ExportToString()`，再讓物體移動，同時檢查 Fabric 姿態確實改變、authored USD 姿態維持原值、root layer 快照一致。若只比較 root layer，物體根本沒進入模擬時也可能通過。完整範例見同目錄 `fabric-writeback-test.md`。
