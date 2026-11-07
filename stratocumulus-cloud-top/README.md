# Stratocumulus cloud-top processes & turbulence

This folder contains:

| File | Contents |
|---|---|
| [`literature_review.md`](literature_review.md) | Literature review: the mixed-layer framework, entrainment closures, buoyancy reversal / CTEI, radiative and evaporative driving, sedimentation, shear, observations (DYCOMS-II, POST, ACTOS), LES/DNS, and open questions |
| [`stratocumulus_cloud_top.py`](stratocumulus_cloud_top.py) | Interactive [marimo](https://marimo.io) notebook for experimenting with the frameworks |

## Running the notebook

**In the browser, no install:** open [`open_in_marimo_app.html`](open_in_marimo_app.html), or copy the
`https://marimo.app/#code/...` link from [`marimo_app_link.txt`](marimo_app_link.txt). The whole notebook
is encoded in the link, which therefore reflects the notebook as of this commit. Alternatively
use [marimo.app/github.com/observingClouds/observingClouds/blob/ccr-25ef950d-596rpj/stratocumulus-cloud-top/stratocumulus_cloud_top.py](https://marimo.app/github.com/observingClouds/observingClouds/blob/ccr-25ef950d-596rpj/stratocumulus-cloud-top/stratocumulus_cloud_top.py),
which loads the file straight from GitHub.

**Locally:**

```bash
pip install marimo numpy matplotlib
marimo edit stratocumulus_cloud_top.py      # editable notebook
marimo run  stratocumulus_cloud_top.py      # app mode (code hidden)
# or, with uv, in an isolated environment using the inline script metadata:
uvx marimo edit --sandbox stratocumulus_cloud_top.py
```

## What you can explore

1. **Thermodynamic set-up**: DYCOMS-II RF01/RF02 presets or custom θ_l, q_t, z_i, inversion jumps,
   surface fluxes, the GCSS long-wave radiation parameters and droplet number.
2. **Mixing diagram and buoyancy reversal**: exact saturation-adjusted mixing line, χ\*, the
   saturated buoyancy jump, κ and a computed κ_crit on a Δq_t–Δθ_l stability diagram.
3. **Entrainment closures** applied to the same well-mixed buoyancy-flux budget
   B(z) = P(z) + w_e Q(z): Turton–Nicholls (a₂ = 60), Caldwell & Bretherton (a₂ = 25), Uchida et al.
   (a₂ = 110, sedimentation), dry CBL (A = 0.2), Lilly's minimum and maximum entrainment, a flux-ratio
   closure, and a custom closure with your own coefficients. Includes a sensitivity scan over the jumps.
4. **Mixed-layer model**: time integration with bulk surface fluxes, subsidence and free-tropospheric
   lapse rate. Compare z_i, cloud base, LWP, w_e, w\*, BIR (decoupling) and κ across closures.
5. **Inversion shear and turbulence scales**: bulk Richardson number, shear-layer thickness
   (≈ ⅓Δu²/Δb), Ozmidov, Kolmogorov and Taylor scales, buoyancy Reynolds number and DNS cost.

The physics kernel (thermodynamics and mixed-layer model) is plain NumPy inside the notebook, so the
file is self-contained.
