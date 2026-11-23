# 讀取即時世界座標與變換快取失效

Isaac Sim 5.1.0 工程案例。關閉 USD pose writeback 後，輸出攝影機追蹤、標籤或故障框需要即時 pose。對動態 prim 找出最近且有效的剛體祖先，取 PhysX 的 position、quaternion 及 authored scale 組合世界矩陣，套用由 USD 解析的 prim 到剛體固定偏移。在 OpenUSD `Gf.Matrix4d` 的乘法慣例中，`child_world = child_to_body * body_world`。沒有剛體祖先時，可透過 `usdrt.Usd.Stage.Attach(context.get_stage_id())` 取對應 prim 的 Fabric hierarchy world matrix。Fabric 尚未產生值、靜態物件或 timeline 停止時，可走 `UsdGeom.XformCache` 的 composed USD 路徑。

快取剛體 handle、固定局部偏移和 Fabric accessor，每次重新讀取 pose 或矩陣值。Handle 可能在播放／停止、物理重建或 Stage 更換後失效。`Usd.Notice.ObjectsChanged` 可在 callback 收集 resync 與 `xformOp:*`、`xformOpOrder`、API schema、references 等有關變更，交給更新迴圈依受影響祖先和 prim 路徑做失效處理。缺少的 Fabric accessor 或尚未註冊的 handle 要容許重查。

測試移動剛體、旋轉父節點、修改子節點偏移、移除／重建 Prim 並停止後重播，比對 PhysX/Fabric 即時 pose、子節點座標及 handle 是否重新解析。`omni.isaac.dynamic_control` 是此版本既有讀取方式，屬已棄用介面，移植時應查目標版本支援的替代 API。
