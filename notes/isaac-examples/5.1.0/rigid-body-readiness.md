# 動態剛體、碰撞體、重力與 PhysX 就緒

Isaac Sim 5.1.0 工程案例。檢查 composed Stage 上的 `UsdPhysics.RigidBodyAPI`、`rigidBodyEnabled`、`kinematicEnabled` 及 `physxRigidBody:disableGravity`。場景需要有效 `UsdPhysics.Scene`。多個 PhysicsScene 時明確指定 `simulationOwner`，核對剛體和碰撞體屬於預期場景。碰撞體透過 `UsdPhysics.CollisionAPI` 解析並確認啟用，巢狀剛體的碰撞體歸最近剛體祖先。保留 USD 的重力預設語意，包含代表依 stage up axis 推導方向的零向量，並檢查顯式值是否有效。

Schema 檢查之後，播放 timeline、等待至少幾次 app update，再確認 PhysX 已註冊有效 handle。準備狀態可週期重查，暫停時清掉 ready。上層等待要有逾時，並回傳具體失敗原因。驗證案例包含自由落體、Surface Gripper 吸附和釋放後再落下，對照 PhysX/Fabric 的位置及 composed USD 的 authored pose。使用記憶體 Stage 或獨立資產副本。
