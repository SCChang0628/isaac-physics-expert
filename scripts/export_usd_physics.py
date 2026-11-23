"""Read-only composed USD physics snapshot.

Run with an Isaac Sim Python that provides pxr, e.g. ~/isaacsim/python.sh.
No simulation, playback, writes to USD, or parameter changes.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="Original scene .usd[a/c]")
    parser.add_argument("--output", type=Path, required=True, help="JSON output path (prefer data/)")
    parser.add_argument("--max-items", type=int, default=12000)
    args = parser.parse_args()

    from pxr import Usd, UsdPhysics  # Isaac Sim bundled OpenUSD runtime

    stage = Usd.Stage.Open(str(args.input.expanduser().resolve()))
    if stage is None:
        raise RuntimeError("Could not open USD Stage, check references and file paths")
    out = []
    for prim in stage.Traverse():
        kinds = []
        if prim.IsA(UsdPhysics.Scene):
            kinds.append("PhysicsScene")
        if prim.HasAPI(UsdPhysics.RigidBodyAPI):
            kinds.append("RigidBody")
        if prim.HasAPI(UsdPhysics.CollisionAPI):
            kinds.append("Collision")
        if prim.HasAPI(UsdPhysics.ArticulationRootAPI):
            kinds.append("ArticulationRoot")
        if prim.IsA(UsdPhysics.Joint):
            kinds.append("Joint")
        # Metadata may be stored on Xform / ordinary prims too.
        attrs = {}
        for a in prim.GetAttributes():
            name = a.GetName()
            if not any(key in name.lower() for key in
                       ("physics:", "physx", "material:binding", "angularvelocity")):
                continue
            try:
                val = a.Get()
                string_value = str(val)
                if len(string_value) < 450:
                    attrs[name] = string_value
            except Exception:
                continue
        if not kinds and not attrs:
            continue
        out.append({"path": str(prim.GetPath()), "type": prim.GetTypeName(),
                    "physics_types": kinds, "attributes": attrs})
        if len(out) >= args.max_items:
            print(f"Reached --max-items={args.max_items}; snapshot truncated")
            break
    payload = {"source": str(args.input.expanduser().resolve()),
               "notice": "Read-only composed USD snapshot. Values are informational, not validated.",
               "physics_prims": out}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(out)} physics prims to {args.output}")


if __name__ == "__main__":
    main()
