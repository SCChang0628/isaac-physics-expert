# 以自由落體測試 Fabric 與 Root Layer

Isaac Sim 5.1.0。用安裝目錄的 `python.sh test_writeback.py` 執行下列程式，預期 `PASS`。

```python
from isaacsim import SimulationApp

app = SimulationApp({
    "headless": True,
    "width": 320,
    "height": 240,
    "limit_cpu_threads": 4,
})
try:
    import carb
    import omni.timeline
    import omni.usd
    import usdrt
    from isaacsim.core.utils.extensions import enable_extension
    from pxr import Gf, UsdGeom, UsdPhysics

    context = omni.usd.get_context()
    context.new_stage()
    stage = context.get_stage()
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage, 1)
    UsdPhysics.Scene.Define(stage, "/PhysicsScene")
    cube = UsdGeom.Cube.Define(stage, "/Cube")
    translate = cube.AddTranslateOp()
    translate.Set(Gf.Vec3d(0, 0, 3))
    UsdPhysics.RigidBodyAPI.Apply(cube.GetPrim())
    UsdPhysics.CollisionAPI.Apply(cube.GetPrim())
    before = stage.GetRootLayer().ExportToString()
    stage.SetEditTarget(stage.GetSessionLayer())
    enable_extension("omni.physx.fabric")
    settings = carb.settings.get_settings()
    settings.set_bool("/physics/fabricEnabled", True)
    settings.set_bool("/physics/fabricUpdateTransformations", True)
    settings.set_bool("/physics/updateToUsd", False)

    timeline = omni.timeline.get_timeline_interface()
    timeline.play()
    timeline.commit()
    for _ in range(60):
        app.update()

    rt = usdrt.Usd.Stage.Attach(context.get_stage_id())
    xform = usdrt.Rt.Xformable(rt.GetPrimAtPath("/Cube"))
    matrix = xform.GetFabricHierarchyWorldMatrixAttr().Get()
    assert matrix is not None and matrix.ExtractTranslation()[2] < 2.9
    assert translate.Get()[2] == 3
    assert stage.GetRootLayer().ExportToString() == before
    print("PASS", flush=True)
finally:
    app.close()
```
