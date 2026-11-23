# Stage 時基、物理頻率、渲染節奏與 RTF

Isaac Sim 5.1.0 工程案例。區分 `Stage.GetTimeCodesPerSecond()` 的 USD 時基、`PhysicsScene` 的 `physxScene:timeStepsPerSecond` 物理步進頻率，以及應用和渲染的更新目標。載入後從 composed Stage 讀取各項設定。避免為了改渲染速度呼叫會重新 author `timeCodesPerSecond` 的方法；即使值相同，載入後重新寫入仍可能引發昂貴的場景重建。使用 Kit run-loop pacing 與 `timeline.set_target_framerate()` 控制執行期節奏。physics Hz 除以 render Hz 是平均比例，實際每畫面步數需量測。

以 `delta simulation time / delta monotonic wall time` 計算 RTF。另計算每秒 app update 數、各 section 的每幀平均和最大 wall time。暫停若仍納入時間窗，RTF 自然降低。`app.update()` 涵蓋原生呼叫及等待時間，app update rate 與 GPU 實際 present rate 應分開。`frame_total` 已包含該幀子區段，分析時避免重複加總。

效能統計可用選配分段計時，累計多幀後寫出 JSON Lines，附 cache hit/miss、handle 解析與更新次數。使用相同場景、物理速率、暖機區間及工作負載做 A/B；停止或時間軸倒退時重置統計視窗。
