# Meta-CAD tools evaluation — what survives a fresh CI runner?

Closes #6.

## Why this exists

In [PR #2 comment 4309337047][c1] I dismissed Rhino/Grasshopper, Fusion 360
Generative Design, nTop, and Onshape FeatureScript with one line:

> chosen over Rhino/Grasshopper, Fusion Generative Design, nTop, Onshape
> FeatureScript because it's pure-Python and pip-installable — none of the
> others survive the "freshly-cloned repo on a CI runner" test

That was lazy. This directory is the receipt: I actually attempted each tool
inside the agent sandbox (Ubuntu 24.04, dotnet 8/9/10 SDKs, sudo+apt, curl,
no GUI, no vendor credentials) and recorded what happened. The verdicts below
are now backed by the install/build/runtime logs in [`logs/`](logs/) and the
small working examples checked in beside this file.

[c1]: https://github.com/vertical-cloud-lab/powder-excavator/pull/2#issuecomment-4309337047

## Scoreboard

| Tool | Authoring on Linux runner | Headless evaluation on Linux runner | What it would take to use in CI |
|------|---------------------------|-------------------------------------|---------------------------------|
| **CadQuery** (current pick) | ✅ `pip install cadquery` | ✅ pure-Python kernel | Nothing — already works |
| **OpenSCAD** | ✅ `apt install openscad` | ✅ `openscad -o out.stl in.scad` | Nothing — already works |
| **rhino3dm** (NURBS lib only) | ✅ `pip install rhino3dm` (8.17.0) | ✅ pure-Python NURBS IO | Nothing — already works |
| **Rhino Compute** front-end (`rhino.compute`) | ✅ `dotnet build` succeeds | ✅ proxy *runs* on Linux | Pair with a worker (next row) |
| **Rhino Compute** worker (`compute.geometry`) | ✅ `dotnet build` succeeds | ❌ runtime needs `libRhinoLibrary.so` | Windows host **or** Wine + Rhino-Win + license; **or** point at a paid hosted Compute |
| **Grasshopper** (`.gh` definitions) | ⚠️ no Linux authoring tool; can be authored on Windows then evaluated via Compute | ⚠️ same as Compute worker | Same as Compute worker |
| **Onshape FeatureScript** | ✅ author `.fs` as text | ⚠️ validation/exec is server-side | `ONSHAPE_ACCESS_KEY` + `ONSHAPE_SECRET_KEY` GitHub secrets + a free Onshape account |
| **nTop Automate** (Linux headless) | ⚠️ tarball gated by login at app.ntop.com | ⚠️ ditto + paid license | Vendor-issued tarball + license file uploaded as encrypted GitHub secrets; commercial subscription |
| **Fusion 360 / Generative Design** | ❌ 1.4 GB Win-only PE32 GUI installer; no Linux build, no headless mode | ❌ Generative Design is paid cloud, no public REST | Effectively impossible to bolt onto this repo's CI |

Two of those rows — Onshape FeatureScript and nTop Automate — are clearly
**not** "doesn't survive a fresh CI runner". They survive perfectly well if the
maintainer is willing to add a vendor account and put the credentials in
`Settings → Secrets`. That's a different conversation than I had in PR #2 and
the dismissal was wrong. Details below per tool.

---

## 1. Rhino / Grasshopper / Rhino Compute

There are three layers and the answer is different for each.

### 1a. `rhino3dm` — the open NURBS kernel as a Python library
Pure-Python, pip-installable, BSD-licensed, no Rhino install, no license:

```
$ pip install rhino3dm   # 8.17.0
$ python rhino3dm_demo.py
Wrote /tmp/.../trough.3dm: ok=True, size=10335 bytes
Re-read ok, objects=4
  - Extrusion       bbox min=-12.0,-40.0,-12.56  max=12.56,0.0,1.18
  - Extrusion       bbox min=-10.4,-40.0,-10.88  max=10.88,0.0,1.02
  - LineCurve       bbox min=0.0,-2.0,16.0  max=0.0,42.0,16.0
  - TextDot         bbox min=0.0,20.0,-17.0  max=0.0,20.0,-17.0
```

[`rhino3dm_demo.py`](rhino3dm_demo.py) builds the trough as two extruded NURBS
half-arcs plus a pivot reference line, writes a real `.3dm` file, and
round-trips it. So **for IO and basic NURBS authoring, "no Rhino on Linux"
is no longer true** — you just don't get the parametric/Grasshopper layer
on top.

### 1b. `compute.rhino3d` (the .NET REST server) — partially Linux-native
Cloned + built both the proxy and the worker on this Ubuntu runner with stock
`dotnet 9`:

```
$ git clone --depth=1 https://github.com/mcneel/compute.rhino3d.git
$ cd compute.rhino3d/src/rhino.compute && dotnet build -c Release
  rhino.compute -> .../rhino.compute.dll
  Build succeeded.    0 Warning(s)    0 Error(s)
$ dotnet rhino.compute.dll --urls=http://127.0.0.1:8081
RC  [INF] Rhino compute started
RC  [INF] Now listening on: http://127.0.0.1:8081
RC  [INF] Application started.
```

So the front-end **builds and runs on Linux** — it's just an
ASP.NET Core reverse-proxy that load-balances geometry workers. The worker
also builds:

```
$ cd ../compute.geometry && dotnet build -c Release
  compute.geometry -> .../compute.geometry.dll
  Build succeeded.    5 Warning(s)    0 Error(s)
```

…but fails at startup because there is no Linux build of Rhino itself:

```
$ dotnet compute.geometry.dll --urls=http://127.0.0.1:8082
Unhandled exception. System.DllNotFoundException: Unable to load shared
library '/usr/lib/rhino3d/libRhinoLibrary.so' or one of its dependencies.
   at RhinoInside.Resolver.PrepareRhinoEnv()
   at compute.geometry.Program.Main(String[] args)
```

The Rhino Compute README confirms: *"Compute is built on top of Rhino 8 for
Windows and can run anywhere Rhino 8 for Windows can run."* So the realistic
deployments today are:

1. Spin up a Windows host (or Windows container/VM) for `compute.geometry`,
   keep `rhino.compute` on Linux in front of it. Doable in CI but heavy.
2. Run the worker under Wine with a Rhino-for-Windows install + license.
   Possible per community projects (`cryinkfly/Rhinoceros-3D-for-Linux`,
   `aaronsb/rhino-wine`), but not "fresh-clone on a Linux runner" simple.
3. Pay for a hosted Compute service and treat it as a remote dependency from
   this repo's CI. That's plausible — see `compute_rhino3d` below.

### 1c. `compute_rhino3d` — Python client to a Compute server
Pip-installable (0.12.2), works against any Compute server URL:

```python
import compute_rhino3d.Util as U, compute_rhino3d.Mesh as MeshM
U.url    = "https://my.compute.host/"
U.apiKey = "..."
mesh_list = MeshM.CreateFromBrep(my_brep)   # POSTs /rhino/geometry/mesh/createfrombrep-brep
```

I pointed the client at a dead URL just to verify the request path is well-formed:

```
ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=65530):
  ... url: /rhino/geometry/mesh/createfrombrep-brep ...
  [Errno 111] Connection refused
```

So there is a real plug-and-play Python path **iff** somebody (us or a vendor)
runs the Windows-side worker. For our purposes that's a maintained dependency,
not something CI bootstraps from scratch.

**Net for the manuscript:** "no Rhino on Linux" was overstated. We can author
NURBS in pure Python, run the orchestrator on Linux, and call out to a hosted
worker. The thing that cleanly *doesn't* work in this CI is "headless
Grasshopper-evaluation on a Linux runner with no external services."

---

## 2. Onshape FeatureScript

I was wrongest about this one. Authoring is just text; evaluation is a REST API
call to `cad.onshape.com`. The Python client is pip-installable:

```
$ pip install onshape-client     # 1.6.3
```

Authoring works fine on the runner — see [`excavator_trough.fs`](excavator_trough.fs),
a real Custom-Feature `.fs` file that defines `troughRadius`, `troughLength`,
`wallThickness` with `LengthBoundSpec` annotations (Onshape will render them as
sliders), sketches the half-annulus profile, and extrudes it.

Anonymous REST is firewalled off, as expected:

```
$ python onshape_rest_probe.py
HTTPError 401 Unauthorized: {"message":"Unauthenticated API request","status":401}
```

…but with `ONSHAPE_ACCESS_KEY` + `ONSHAPE_SECRET_KEY` in
`Settings → Secrets and variables → Actions`, a CI job can:

1. Create a fresh Onshape document via `POST /api/v6/documents`.
2. Push the contents of `excavator_trough.fs` into a Feature Studio via
   `POST /api/v6/featurestudios/{did}/w/{wid}/e/{eid}` — this returns
   FeatureScript compile diagnostics, which is the "validation/feedback"
   half of #6.
3. Insert the custom feature into a Part Studio and call
   `POST /api/v6/partstudios/{...}/features` to actually evaluate it.
4. Pull back STEP/STL via `GET /api/v6/partstudios/{...}/stl` and run the
   same DFM checks we run on CadQuery output.

Free-tier Onshape accounts can do all of this; the only non-trivial part is
that public free documents are world-visible by design. This is a perfectly
reasonable second-source CAD pipeline to add to CI when @sgbaird wants it —
say the word and I'll wire it up.

---

## 3. Fusion 360 / Generative Design

This one really does not survive a Linux CI runner. Concrete evidence:

```
$ curl -O https://dl.appstreaming.autodesk.com/.../Fusion%20Admin%20Install.exe
  -> 1.4 GB
$ file Fusion360ClientInstaller.exe
  PE32 executable (GUI) Intel 80386, for MS Windows, 5 sections
$ wine Fusion360ClientInstaller.exe /S
  wine: failed to open L"C:\\windows\\syswow64\\rundll32.exe": c0000135
  ShellExecuteEx failed: Internal error.
```

Even past the wine multilib problem, two structural blockers remain:

* Fusion 360 is a streaming GUI client, not a headless renderer. There is no
  `fusion --batch foo.f3d` mode and no Linux build at all.
* **Generative Design** specifically is a *cloud* job inside Autodesk's
  paid subscription, billed by tokens; there is no public REST endpoint to
  submit a study from outside the GUI. Autodesk's "Design Automation for
  Inventor/Revit" APS service does not cover Fusion Generative Design.

So for the powder-excavator CI loop, Fusion Generative Design is a hard no.
The right Autodesk-adjacent option (if we ever want one) is Inventor +
APS Design Automation, which is its own evaluation.

---

## 4. nTop / nTop Automate

Also wrongly dismissed. nTop *does* publish a Linux headless build —
**nTop Automate for Linux** — distributed as a tarball you extract anywhere,
intended exactly for HPC and CI batch use. From nTop's own support article
([support.ntop.com #16750988785299](https://support.ntop.com/hc/en-us/articles/16750988785299-nTop-Automate-for-Linux-Update)):

> nTop Automate for Linux is the headless (no GUI) version intended for
> large automated/batch workflows and HPC environments… reached general
> availability and can be directly downloaded by authorized users from the
> official user dashboard at https://app.ntop.com/.

What stops it on *this* runner is that the dashboard is login-walled and
requires a paid commercial license:

```
$ curl -I https://app.ntop.com/
HTTP/2 200 — single-page React app behind login; no anonymous downloads
$ pip install ntop_api
ERROR: No matching distribution found for ntop_api
```

But "can't pip install it" ≠ "can't run it in CI". The realistic CI shape is:

1. Buy / extend the existing nTop seat with an Automate license.
2. Drop the `nTop Automate` tarball into a private GCS/S3 bucket (or
   GitHub Releases on a private repo).
3. CI: download the tarball, extract, mount the licence file from
   `secrets.NTOP_LICENSE`, run `ntopcl my_workflow.ntop --output mesh.stl`.
4. Feed the resulting lattice/TPMS geometry through the same DFM checks.

This is the same operational shape as a paid CodeQL or Coverity license in
CI, not exotic. nTop is the best-of-class generative tool in the list and
it's worth doing this if we ever push the trough geometry past what
CadQuery's BREP kernel handles cleanly (e.g. lattice infill of the arms).

---

## 5. Genuine non-Python alternative: OpenSCAD

To not just be "Python with extra steps", I also ran OpenSCAD end-to-end
on this same runner — installs from the distro repo, no Python, no license:

```
$ sudo apt install openscad      # OpenSCAD version 2021.01
$ openscad -o trough.stl excavator_trough.scad
   Halfedges: 732   Edges: 366   Halffacets: 248   Facets: 124   Volumes: 2
$ head -2 trough.stl
solid OpenSCAD_Model
  facet normal -0.760414 0 0.649439
```

[`excavator_trough.scad`](excavator_trough.scad) is a working hollowed
half-cylinder trough, 124 facets, ~80 KB STL. OpenSCAD is the cleanest
"non-Python, fully open, fully CI-compatible" option if we ever want to
replace or dual-source the CadQuery model.

---

## Revised recommendation

Drop the original blanket dismissal and replace it with:

* **Primary CAD authoring + CI DFM**: keep CadQuery (best fresh-runner story,
  unifies authoring + DFM + tests in one Python codebase).
* **Non-Python second source**: OpenSCAD is a one-liner to add and gives
  us a sanity check that geometry behaves the same in two kernels.
* **Generative / NURBS path** (if we ever need it):
  * **Onshape FeatureScript** via `onshape-client` + repo secrets — easiest
    to stand up; gives us real generative parametric features and cloud
    rendering for free.
  * **nTop Automate** for actual generative / lattice work — needs a paid
    license but is genuinely Linux-headless-ready; the right tool if we
    take the bimodal compliant-mechanism scoop (#4) seriously.
  * **Rhino + Grasshopper via Rhino Compute** — viable as a hosted service,
    not viable as something CI builds from scratch on Linux.
* **Fusion 360 Generative Design**: don't pursue. Cloud-token-billed,
  GUI-only authoring, no headless API, no Linux. Inventor + APS Design
  Automation would be the Autodesk-side option to revisit, separately.

If/when @sgbaird wants any of the cloud paths actually wired into this repo,
say which one(s) and I'll do the secrets wiring + workflow in a follow-up PR.

## Files

| File | What it is |
|------|------------|
| [`rhino3dm_demo.py`](rhino3dm_demo.py) | Pure-Python NURBS authoring → real `.3dm` file |
| [`excavator_trough.fs`](excavator_trough.fs) | Real Onshape FeatureScript Custom Feature for the trough |
| [`onshape_rest_probe.py`](onshape_rest_probe.py) | Probe of the Onshape REST API showing 401 anonymous response |
| [`excavator_trough.scad`](excavator_trough.scad) | OpenSCAD model that builds an STL on this runner |
| [`logs/`](logs/) | Captured install / build / runtime output for every claim above |
