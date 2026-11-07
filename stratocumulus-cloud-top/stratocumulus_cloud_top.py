# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "matplotlib>=3.7",
#     "numpy>=1.26",
# ]
# ///
"""Interactive explorer for stratocumulus cloud-top processes and turbulence.

Run with:  marimo edit stratocumulus_cloud_top.py   (or `marimo run ...` for app mode)
"""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="Stratocumulus cloud-top lab")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from types import SimpleNamespace

    plt.rcParams.update(
        {
            "figure.dpi": 110,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": "#e4e3df",
            "grid.linewidth": 0.6,
            "axes.edgecolor": "#8a8984",
            "axes.labelcolor": "#2b2b29",
            "xtick.color": "#52514e",
            "ytick.color": "#52514e",
            "font.size": 9.5,
            "legend.frameon": False,
            "lines.linewidth": 2.0,
        }
    )
    # Fixed categorical order (colour follows the entity, never its rank)
    SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
    INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8984"
    return INK, INK2, MUTED, SERIES, SimpleNamespace, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stratocumulus cloud-top lab ☁️

    Stratocumulus are maintained by a delicate balance at a sharp, typically 5–50 m thick
    inversion: **long-wave radiative cooling** and **evaporative cooling** at cloud top drive
    the turbulence that keeps the layer well mixed, while that same turbulence **entrains**
    warm, dry free-tropospheric air that deepens the boundary layer and thins the cloud.

    This notebook goes with the literature review in
    [`literature_review.md`](literature_review.md). Use it to try out the main frameworks:

    1. **Thermodynamic set-up**: start from a field-campaign preset (DYCOMS-II) or your own values.
    2. **Mixing diagram & buoyancy reversal**: Randall (1980)/Deardorff (1980) cloud-top
       entrainment instability (CTEI), the stability parameter κ, χ\*, and the saturated buoyancy jump.
    3. **Entrainment closures**: Lilly (1968), Turton & Nicholls (1987), Caldwell & Bretherton (2009),
       Uchida et al. (2010) and others, applied to the *same* buoyancy-flux budget of a well-mixed layer.
    4. **Mixed-layer model**: integrate a Lilly-type model forward in time and compare
       closures, decoupling diagnostics (BIR) and LWP evolution.
    5. **Shear and small-scale turbulence at the inversion**: Richardson numbers, shear-layer
       thickness, Ozmidov/Kolmogorov scales and what they imply for LES/DNS.

    > **Caveat**: this is a teaching tool. The mixed-layer model leaves out drizzle, the diurnal cycle of
    > short-wave absorption and decoupled structure; check any quantitative statement against the
    > cited papers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "📚 Literature in one screen (expand)": mo.md(r"""
    | Theme | Key idea | Key references |
    |---|---|---|
    | Mixed-layer framework | Well-mixed conserved variables (θ_l, q_t); jumps at z_i; w_e closes the system | Lilly 1968; Deardorff 1976; Schubert et al. 1979; Bretherton & Wyant 1997; Stevens 2002 (review); Caldwell & Bretherton 2009 |
    | Radiative driving | LW cooling of ≈ 40–100 W m⁻² concentrated in the top tens of metres generates negatively buoyant downdrafts | Lilly 1968; Nicholls 1989; Stevens et al. 2005; de Lozar & Mellado 2015 |
    | Buoyancy reversal / CTEI | Mixing dry inversion air into cloud can make mixtures *denser* than both end-members; κ = 1 + c_p Δθ_l /(L_v Δq_t) | Randall 1980; Deardorff 1980; Kuo & Schubert 1988; Siems et al. 1990; MacVean & Mason 1990; Duynkerke 1993; Yamaguchi & Randall 2008; Mellado 2010 |
    | Persistence despite CTEI | Observed decks often sit in the "unstable" region; κ controls LWP tendency rather than immediate break-up | Kuo & Schubert 1988; Stevens et al. 2003; van der Dussen et al. 2014; Xiao et al. 2011 |
    | Entrainment closures | w_e = A w\*³/(z_i Δb) with evaporative enhancement; flux-ratio/energy closures | Nicholls & Turton 1986; Turton & Nicholls 1987; Lock 1998; Moeng 2000; Lilly 2002; Stevens 2002; Uchida et al. 2010 |
    | Sedimentation & microphysics | Droplet sedimentation removes liquid from the entrainment zone → less evaporative enhancement | Ackerman et al. 2004; Bretherton et al. 2007; de Lozar & Mellado 2017; Schulz & Mellado 2019 |
    | Observations | DYCOMS-II, POST, ACTOS: entrainment rates 2–7 mm s⁻¹, a turbulent EIL, holes and filaments | Stevens et al. 2003a,b; Faloona et al. 2005; Gerber et al. 2005, 2013; Katzwinkel et al. 2012; Malinowski et al. 2013; Jen-La Plante et al. 2016 |
    | Shear at cloud top | Shear builds a marginally stable layer, Ri ≈ 0.25–0.7, thickness ≈ ⅓ Δu²/Δb | Wang et al. 2008; Katzwinkel et al. 2012; Mellado et al. 2014; Kopec et al. 2016; Schulz & Mellado 2018 |
    | Small scales & numerics | η ≈ 1 mm vs z_i ≈ 1 km; LES needs Δz ≲ 5 m at the inversion; DNS for the EIL physics | Moeng et al. 1996; Stevens et al. 2005; Mellado 2017; Mellado et al. 2018 |
    | Climate relevance | Low-cloud amount scales with inversion strength (LTS/EIS); entrainment & aerosol feedbacks | Klein & Hartmann 1993; Wood & Bretherton 2006; Wood 2012; Bretherton 2015; Schneider et al. 2019 |
    """)
        }
    )
    return


@app.cell
def _(SimpleNamespace, np):
    # ======================================================================
    # Physics kernel: thermodynamics, mixing diagram, mixed-layer model
    # ======================================================================
    Rd, Rv, cp, Lv, g = 287.04, 461.5, 1004.0, 2.5e6, 9.81
    p00, rho_w = 1.0e5, 1000.0
    eps = Rd / Rv
    delta = Rv / Rd - 1.0
    kap = Rd / cp

    def exner(p):
        return (p / p00) ** kap

    def esat(T):
        """Saturation vapour pressure over liquid water (Bolton 1980) [Pa]."""
        return 611.2 * np.exp(17.67 * (T - 273.15) / (T - 29.65))

    def qsat(T, p):
        es = esat(T)
        return eps * es / (p - (1.0 - eps) * es)

    def saturation_adjust(thl, qt, p, n_iter=8):
        """T, q_l, q_v from liquid-water potential temperature, total water and pressure."""
        thl, qt, p = np.broadcast_arrays(np.asarray(thl, float), np.asarray(qt, float), np.asarray(p, float))
        Tl = thl * exner(p)
        T = Tl.copy()
        for _ in range(n_iter):  # Newton iteration for T = Tl + Lv/cp (qt - qs(T))
            qs = qsat(T, p)
            dqs = qs * 17.67 * (273.15 - 29.65) / (T - 29.65) ** 2
            T = T - (T - Tl - Lv / cp * (qt - qs)) / (1.0 + Lv / cp * dqs)
        ql = qt - qsat(T, p)
        sat = ql > 0
        T = np.where(sat, T, Tl)
        ql = np.where(sat, ql, 0.0)
        return T, ql, qt - ql

    def theta_v(thl, qt, p):
        T, ql, qv = saturation_adjust(thl, qt, p)
        return T / exner(p) * (1.0 + delta * qv - ql), ql

    def kappa_param(dthl, dqt):
        """Inversion stability parameter κ = 1 + c_p Δθ_l / (L_v Δq_t)."""
        return 1.0 + cp * dthl / (Lv * dqt) if dqt != 0 else np.nan

    def mixing_line(thl, qt, dthl, dqt, p, n=401):
        """Buoyancy (relative to cloud-top air) of mixtures with a fraction χ of inversion air."""
        chi = np.linspace(0.0, 1.0, n)
        thv_m, ql_m = theta_v(thl + chi * dthl, qt + chi * dqt, p)
        thv0 = thv_m[0]
        b = g * (thv_m - thv0) / thv0
        if ql_m[0] <= 0:
            chi_star = 0.0
        elif (ql_m > 0).all():
            chi_star = 1.0
        else:
            k = int(np.argmax(ql_m <= 0))
            q0, q1 = ql_m[k - 1], ql_m[k]
            chi_star = chi[k - 1] + (chi[k] - chi[k - 1]) * q0 / (q0 - q1)
        b_star = float(np.interp(chi_star, chi, b))
        db = float(b[-1])
        dm = 2.0 * np.trapezoid(b, chi)  # Turton & Nicholls (1987) "Δ_m"
        E = 1.0 - dm / db if db > 0 else np.nan  # = χ*(1 - Δb_s/Δb) for a piecewise-linear mixing line
        return dict(chi=chi, b=b, ql=ql_m, chi_star=chi_star, b_star=b_star, db=db, dm=dm, E=E,
                    dbs=b_star / chi_star if chi_star > 0 else np.nan, thv0=thv0)

    def kappa_crit(thl, qt, dqt, p):
        """κ at which the mixture at χ* is neutrally buoyant (onset of buoyancy reversal)."""
        lo, hi = 0.0, 60.0
        f = lambda dth: mixing_line(thl, qt, dth, dqt, p, n=801)["b_star"]
        if f(lo) > 0 or f(hi) < 0:
            return np.nan
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
        return kappa_param(0.5 * (lo + hi), dqt)

    def ml_profiles(thl, qt, zi, ps, nz=150):
        """Vertical structure of a well-mixed layer with uniform θ_l and q_t.

        The grid is split at the lifting condensation level so that cloud base is a grid point,
        which keeps the vertical integrals (w*, BIR) smooth as cloud base moves."""
        pres = lambda zz: p00 * ((ps / p00) ** kap - g * zz / (cp * thl)) ** (1.0 / kap)
        ql_at = lambda zz: saturation_adjust(thl, qt, pres(zz))[1]
        if ql_at(zi) <= 0:
            zb, z = zi, np.linspace(0.0, zi, nz)
        else:
            if ql_at(0.0) > 0:
                zb = 0.0
            else:
                lo, hi = 0.0, zi
                for _ in range(40):
                    mid = 0.5 * (lo + hi)
                    lo, hi = (lo, mid) if ql_at(mid) > 0 else (mid, hi)
                zb = hi
            n1 = int(np.clip(round(nz * zb / zi), 3, nz - 6)) if zb > 0 else 0
            z = np.concatenate([np.linspace(0.0, zb, n1, endpoint=False), np.linspace(zb, zi, nz - n1)])
        p = pres(z)
        T, ql, qv = saturation_adjust(np.full(z.size, thl), np.full(z.size, qt), p)
        rho = p / (Rd * T * (1 + delta * qv - ql))
        lwp = np.trapezoid(rho * ql, z)
        # buoyancy-flux coefficients ∂θv/∂θl, ∂θv/∂qt; one-sided differences that stay in the
        # local regime (clear below cloud base, saturated from cloud base up)
        dth, dq = 0.01, 1e-6
        cld = z >= zb
        sgn = np.where(cld, -1.0, 1.0)  # cloudy: lower θl / add qt stays saturated
        thv_c, _ = theta_v(thl, qt, p)
        c_th = (theta_v(thl + sgn * dth, qt, p)[0] - thv_c) / (sgn * dth)
        c_q = (theta_v(thl, qt - sgn * dq, p)[0] - thv_c) / (-sgn * dq)
        return dict(z=z, p=p, T=T, ql=ql, rho=rho, zb=zb, lwp=lwp, c_th=c_th, c_q=c_q,
                    ql_top=ql[-1], p_top=p[-1], rho_sfc=rho[0], rho_top=rho[-1])

    def rad_flux(prof, F0, F1, klw):
        """Net upward LW flux [W m-2], GCSS DYCOMS-II form: F0 e^{-κQ(z,zi)} + F1 e^{-κQ(0,z)}."""
        z, rq = prof["z"], prof["rho"] * prof["ql"]
        Qb = np.concatenate([[0.0], np.cumsum(0.5 * (rq[1:] + rq[:-1]) * np.diff(z))])
        return F0 * np.exp(-klw * (Qb[-1] - Qb)) + F1 * np.exp(-klw * Qb)

    def sed_velocity(ql_top, rho, Nd_cm3, sigma_g=1.2):
        """Cloud-top sedimentation velocity, w_sed = c r² exp(5 ln² σg) (Ackerman et al. 2009; Uchida et al. 2010)."""
        if ql_top <= 0:
            return 0.0
        r = (3 * rho * ql_top / (4 * np.pi * rho_w * Nd_cm3 * 1e6)) ** (1 / 3)
        return 1.19e8 * r**2 * np.exp(5 * np.log(sigma_g) ** 2)

    def flux_decomposition(prof, shf, lhf, FR, dthl, dqt, thv0):
        """Buoyancy flux B(z) = P(z) + w_e Q(z) [m² s⁻³] for a well-mixed layer.

        Total (turbulent + radiative) fluxes are linear in z; turbulent = total - radiative."""
        z, rho = prof["z"], prof["rho"]
        s = z / z[-1]
        pi = exner(prof["p"])
        rho_t, pi_t = prof["rho_top"], exner(prof["p_top"])
        Fs_P = (shf + FR[0]) * (1 - s) + FR[-1] * s - FR  # W m-2
        Fs_Q = -rho_t * cp * pi_t * dthl * s
        Fq_P = lhf / Lv * (1 - s) / rho
        Fq_Q = -rho_t * dqt * s / rho
        P = g / thv0 * (prof["c_th"] * Fs_P / (rho * cp * pi) + prof["c_q"] * Fq_P)
        Q = g / thv0 * (prof["c_th"] * Fs_Q / (rho * cp * pi) + prof["c_q"] * Fq_Q)
        return P, Q

    def bir(z, B, zb):
        """Buoyancy integral ratio (Turton & Nicholls 1987; Bretherton & Wyant 1997)."""
        neg_sub = (z < zb) & (B < 0)
        neg = -np.trapezoid(np.where(neg_sub, B, 0.0), z)
        pos = np.trapezoid(np.where(neg_sub, 0.0, B), z)
        return max(neg / pos, 0.0) + 0.0 if pos > 0 else np.inf  # "+ 0.0" turns -0.0 into 0.0

    def area_ratio(z, B):
        neg = -np.trapezoid(np.minimum(B, 0.0), z)
        pos = np.trapezoid(np.maximum(B, 0.0), z)
        return neg / pos if pos > 0 else np.inf

    def solve_entrainment(prof, P, Q, db, E, closure, wsed=0.0):
        """Entrainment velocity w_e [m/s], w*³ and efficiency A for a closure specification."""
        z = prof["z"]
        zi = z[-1]
        Wp, Wq = 2.5 * np.trapezoid(P, z), 2.5 * np.trapezoid(Q, z)
        kind, A, we, note = closure["kind"], np.nan, np.nan, ""
        if not db > 0:
            return dict(we=np.nan, wstar3=np.nan, A=np.nan, note="Δb ≤ 0: no stable inversion")
        if kind == "efficiency":
            Efac = max(E, 0.0) if np.isfinite(E) else 0.0
            sed = 1.0
            for _ in range(40):
                A = closure["a1"] * (1 + closure["a2"] * Efac * sed)
                den = zi * db - A * Wq
                if den <= 0:
                    return dict(we=np.nan, wstar3=np.nan, A=A,
                                note="runaway: entrainment feeds w*³ faster than Δb resists (CTEI-like)")
                we = A * Wp / den
                ws = np.cbrt(max(Wp + we * Wq, 1e-12))
                sed = np.exp(-closure.get("ased", 0.0) * wsed / ws)
            we = max(we, 0.0)
        elif kind == "lilly_max":
            if Wq < 0:
                we = max(-Wp / Wq, 0.0)
            else:
                note = "∫B grows with w_e (buoyancy reversal): no upper bound"
        elif kind == "lilly_min":
            zb = prof["zb"] if prof["zb"] < zi else 0.9 * zi
            m = (z < zb) & (Q < 0)
            if m.any():
                we = max(float(np.min(P[m] / -Q[m])), 0.0)
            else:
                note = "no level where entrainment reduces B below cloud base"
        elif kind == "ratio":
            k = closure["k"]
            hi = max(-Wp / Wq, 0.0) if Wq < 0 else 0.2
            if area_ratio(z, P + hi * Q) < k:
                note = "target ratio never reached"
            else:
                lo = 0.0
                for _ in range(60):
                    mid = 0.5 * (lo + hi)
                    lo, hi = (mid, hi) if area_ratio(z, P + mid * Q) < k else (lo, mid)
                we = 0.5 * (lo + hi)
        w3 = Wp + we * Wq if np.isfinite(we) else np.nan
        if kind != "efficiency":
            A = we * zi * db / w3 if (np.isfinite(w3) and w3 > 1e-6) else np.nan
        return dict(we=we, wstar3=w3, A=A, note=note)

    def diagnose(st, closure, nz=150):
        """Steady-state diagnosis of w_e for the state dictionary `st`."""
        prof = ml_profiles(st["thl"], st["qt"], st["zi"], st["ps"], nz=nz)
        FR = rad_flux(prof, st["F0"], st["F1"], st["klw"])
        mix = mixing_line(st["thl"], st["qt"], st["dthl"], st["dqt"], prof["p_top"])
        P, Q = flux_decomposition(prof, st["shf"], st["lhf"], FR, st["dthl"], st["dqt"], mix["thv0"])
        wsed = sed_velocity(prof["ql_top"], prof["rho_top"], st["Nd"])
        sol = solve_entrainment(prof, P, Q, mix["db"], mix["E"], closure, wsed)
        B = P + sol["we"] * Q if np.isfinite(sol["we"]) else np.full_like(P, np.nan)
        return dict(prof=prof, mix=mix, P=P, Q=Q, B=B, FR=FR, wsed=wsed,
                    bir=bir(prof["z"], B, prof["zb"]) if np.isfinite(sol["we"]) else np.nan, **sol)

    def run_mlm(st, closure, sst, V, D, gamma_th, F_clear, hours=48.0, dt=600.0, nz=100, drizzle=True):
        """Forward-Euler integration of a Lilly (1968)-type mixed-layer model.

        Bulk surface fluxes with C_T = 1e-3 (1 + 0.07 V) (Bretherton & Wyant 1997);
        free troposphere θ_l⁺(z) = θ_l + Δθ_l + Γ (z - z_i0), q_t⁺ = q_t + Δq_t.
        Optional drizzle sink: cloud-base rain rate R = 0.37 (LWP/N_d)^1.75 mm/day
        (Comstock et al. 2004), assumed to reach the surface (its effect on the buoyancy-flux
        profile is neglected)."""
        thl, qt, zi = st["thl"], st["qt"], st["zi"]
        ps, zi0 = st["ps"], st["zi"]
        thl_ft_zi0, qt_ft = st["thl"] + st["dthl"], st["qt"] + st["dqt"]
        CT = 1e-3 * (1 + 0.07 * V)
        th_sfc, qs_sfc = sst / exner(ps), qsat(sst, ps)
        nt = int(round(hours * 3600 / dt))
        keys = ["t", "zi", "zb", "lwp", "we", "wstar", "bir", "kappa", "shf", "lhf", "rain"]
        out = {k: np.full(nt + 1, np.nan) for k in keys}
        status = "ok"
        for n in range(nt + 1):
            prof = ml_profiles(thl, qt, zi, ps, nz=nz)
            rho0 = prof["rho_sfc"]
            shf = rho0 * cp * CT * V * (th_sfc - thl)
            lhf = rho0 * Lv * CT * V * (qs_sfc - qt)
            dthl = thl_ft_zi0 + gamma_th * (zi - zi0) - thl
            dqt = qt_ft - qt
            FR = rad_flux(prof, st["F0"], st["F1"], st["klw"])
            mix = mixing_line(thl, qt, dthl, dqt, prof["p_top"], n=201)
            P, Q = flux_decomposition(prof, shf, lhf, FR, dthl, dqt, mix["thv0"])
            wsed = sed_velocity(prof["ql_top"], prof["rho_top"], st["Nd"])
            sol = solve_entrainment(prof, P, Q, mix["db"], mix["E"], closure, wsed)
            if not np.isfinite(sol["we"]):
                status = f"stopped at t = {n * dt / 3600:.1f} h: {sol['note']}"
                break
            we = sol["we"]
            B = P + we * Q
            rain = 0.37 * (prof["lwp"] * 1e3 / st["Nd"]) ** 1.75 / 86400.0 if drizzle else 0.0  # kg m-2 s-1
            rec = dict(rain=rain * 86400.0, t=n * dt / 3600, zi=zi, zb=min(prof["zb"], zi), lwp=prof["lwp"], we=we,
                       wstar=np.cbrt(sol["wstar3"]), bir=bir(prof["z"], B, prof["zb"]),
                       kappa=kappa_param(dthl, dqt), shf=shf, lhf=lhf)
            for k, v in rec.items():
                out[k][n] = v
            if n == nt:
                break
            rcp = np.mean(prof["rho"]) * cp * np.mean(exner(prof["p"]))
            top = FR[-1] - prof["rho_top"] * cp * exner(prof["p_top"]) * we * dthl
            thl += dt * (shf + FR[0] - top - F_clear + Lv * rain) / (rcp * zi)
            qt += dt * (lhf / Lv + prof["rho_top"] * we * dqt - rain) / (np.mean(prof["rho"]) * zi)
            zi += dt * (we - D * zi)
        return out, status

    sc = SimpleNamespace(
        Rd=Rd, Rv=Rv, cp=cp, Lv=Lv, g=g, exner=exner, qsat=qsat, theta_v=theta_v,
        saturation_adjust=saturation_adjust, kappa_param=kappa_param, mixing_line=mixing_line,
        kappa_crit=kappa_crit, ml_profiles=ml_profiles, rad_flux=rad_flux, sed_velocity=sed_velocity,
        flux_decomposition=flux_decomposition, bir=bir, solve_entrainment=solve_entrainment,
        diagnose=diagnose, run_mlm=run_mlm,
    )
    return (sc,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 · Thermodynamic set-up

    The boundary layer is assumed well mixed in the conserved variables θ_l and q_t up to the
    inversion height z_i. Across the inversion they jump by Δθ_l > 0 and Δq_t < 0. Radiation uses the
    idealised GCSS DYCOMS-II long-wave formula
    $F_R(z) = F_0\,e^{-\kappa_{lw} Q(z, z_i)} + F_1\,e^{-\kappa_{lw} Q(0,z)}$ (Stevens et al. 2005),
    where Q is the liquid-water path above or below z.
    """)
    return


@app.cell
def _():
    PRESETS = {
        "DYCOMS-II RF01 (nocturnal, non-drizzling; Stevens et al. 2005)": dict(
            thl=289.0, qt=9.0, zi=840.0, ps=1017.8, dthl=8.5, dqt=-7.5, shf=15.0, lhf=115.0,
            F0=70.0, F1=22.0, klw=85.0, Nd=140.0, sst=292.5, obs_we=(4.0, 0.8)),
        "DYCOMS-II RF02 (drizzling; Ackerman et al. 2009)": dict(
            thl=288.3, qt=9.45, zi=795.0, ps=1017.8, dthl=6.7, dqt=-4.45, shf=16.0, lhf=93.0,
            F0=70.0, F1=22.0, klw=85.0, Nd=55.0, sst=292.5, obs_we=(6.0, 1.5)),
        "Strong buoyancy reversal (illustrative)": dict(
            thl=289.0, qt=9.0, zi=800.0, ps=1017.8, dthl=6.0, dqt=-8.0, shf=12.0, lhf=110.0,
            F0=70.0, F1=22.0, klw=85.0, Nd=100.0, sst=292.0, obs_we=None),
        "Moist free troposphere, no buoyancy reversal (illustrative)": dict(
            thl=289.0, qt=9.0, zi=800.0, ps=1017.8, dthl=8.0, dqt=-2.0, shf=12.0, lhf=90.0,
            F0=70.0, F1=22.0, klw=85.0, Nd=100.0, sst=292.0, obs_we=None),
    }
    return (PRESETS,)


@app.cell
def _(PRESETS, mo):
    preset = mo.ui.dropdown(options=list(PRESETS), value=list(PRESETS)[0], label="**Preset**")
    preset
    return (preset,)


@app.cell
def _(PRESETS, mo, preset):
    _p = PRESETS[preset.value]
    _s = lambda lo, hi, st, v, lab: mo.ui.slider(lo, hi, step=st, value=v, label=lab, show_value=True, debounce=True)
    state_ui = mo.ui.dictionary(
        {
            "thl": _s(280.0, 300.0, 0.1, _p["thl"], "θ_l BL [K]"),
            "qt": _s(4.0, 14.0, 0.05, _p["qt"], "q_t BL [g/kg]"),
            "zi": _s(300.0, 2000.0, 5.0, _p["zi"], "z_i [m]"),
            "ps": _s(1000.0, 1030.0, 0.5, _p["ps"], "p_s [hPa]"),
            "dthl": _s(0.5, 20.0, 0.1, _p["dthl"], "Δθ_l [K]"),
            "dqt": _s(-12.0, 0.0, 0.05, _p["dqt"], "Δq_t [g/kg]"),
            "shf": _s(-20.0, 60.0, 1.0, _p["shf"], "SHF [W/m²]"),
            "lhf": _s(0.0, 250.0, 1.0, _p["lhf"], "LHF [W/m²]"),
            "F0": _s(0.0, 120.0, 1.0, _p["F0"], "F₀ cloud-top LW [W/m²]"),
            "F1": _s(0.0, 60.0, 1.0, _p["F1"], "F₁ cloud-base LW [W/m²]"),
            "klw": _s(20.0, 200.0, 1.0, _p["klw"], "κ_lw [m²/kg]"),
            "Nd": _s(10.0, 500.0, 5.0, _p["Nd"], "N_d [cm⁻³]"),
        }
    )
    mo.hstack(
        [
            mo.vstack([mo.md("**Boundary layer**"), state_ui["thl"], state_ui["qt"], state_ui["zi"], state_ui["ps"]]),
            mo.vstack([mo.md("**Inversion & surface**"), state_ui["dthl"], state_ui["dqt"], state_ui["shf"], state_ui["lhf"]]),
            mo.vstack([mo.md("**Radiation & microphysics**"), state_ui["F0"], state_ui["F1"], state_ui["klw"], state_ui["Nd"]]),
        ],
        wrap=True,
        gap=2,
    )
    return (state_ui,)


@app.cell
def _(PRESETS, mo, preset, sc, state_ui):
    _v = state_ui.value
    st = dict(_v)
    st["qt"] = _v["qt"] * 1e-3
    st["dqt"] = _v["dqt"] * 1e-3
    st["ps"] = _v["ps"] * 100.0
    st["obs_we"] = PRESETS[preset.value]["obs_we"]
    st["sst"] = PRESETS[preset.value]["sst"]

    base_prof = sc.ml_profiles(st["thl"], st["qt"], st["zi"], st["ps"])
    base_mix = sc.mixing_line(st["thl"], st["qt"], st["dthl"], st["dqt"], base_prof["p_top"])
    kappa_now = sc.kappa_param(st["dthl"], st["dqt"])
    kappa_c = sc.kappa_crit(st["thl"], st["qt"], st["dqt"], base_prof["p_top"]) if st["dqt"] < 0 else float("nan")
    _cloudy = base_prof["lwp"] > 0
    mo.hstack(
        [
            mo.stat(f"{base_prof['zb']:.0f} m" if _cloudy else "no cloud", label="Cloud base z_b",
                    caption=f"cloud depth {st['zi'] - base_prof['zb']:.0f} m" if _cloudy else ""),
            mo.stat(f"{base_prof['lwp'] * 1e3:.0f} g/m²", label="LWP (adiabatic)",
                    caption=f"q_l at top {base_prof['ql_top'] * 1e3:.2f} g/kg"),
            mo.stat(f"{base_mix['db'] / sc.g * base_mix['thv0']:.2f} K", label="Δθ_v across inversion",
                    caption=f"Δb = {base_mix['db'] * 100:.1f} cm s⁻²"),
            mo.stat(f"{kappa_now:.2f}", label="κ = 1 + c_pΔθ_l/(L_vΔq_t)",
                    caption=f"buoyancy reversal if κ > {kappa_c:.2f}"),
        ],
        widths="equal",
    )
    return base_mix, base_prof, kappa_c, kappa_now, st


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 · Mixing diagram, buoyancy reversal and CTEI

    Mix a fraction χ of inversion air into cloud-top air and saturation-adjust the mixture.
    Its buoyancy b(χ), relative to the cloudy air, is piecewise linear with a kink at **χ\***,
    the fraction that just evaporates all liquid water. If $b(\chi^*) < 0$, some mixtures are
    denser than the cloud. This is **buoyancy reversal**, the basis of Randall's (1980) and
    Deardorff's (1980) cloud-top entrainment instability (CTEI). For typical conditions it is
    equivalent to

    $$\kappa \equiv 1 + \frac{c_p\,\Delta\theta_l}{L_v\,\Delta q_t} > \kappa_{crit} \approx 0.2\text{–}0.25 .$$

    Observed decks, however, often persist well inside the "unstable" region (Kuo & Schubert 1988;
    Stevens et al. 2003). Later work treats κ as controlling how fast entrainment dries and thins the
    cloud (LWP tendency) rather than as a switch for instant break-up (van der Dussen et al. 2014;
    Xiao et al. 2011). The **evaporative-enhancement factor**
    $E = 1-\Delta_m/\Delta b = \chi^*(1-\Delta b_s/\Delta b)$ (Turton & Nicholls 1987; Uchida et al. 2010)
    is the input to the entrainment closures in §3.
    """)
    return


@app.cell
def _(mo):
    kappa_user = mo.ui.slider(0.2, 1.2, step=0.05, value=0.7, label="Extra κ reference line (e.g. a break-up threshold)", show_value=True)
    kappa_user
    return (kappa_user,)


@app.cell
def _(INK, INK2, MUTED, PRESETS, SERIES, base_mix, base_prof, kappa_c, kappa_now, kappa_user, np, plt, sc, st):
    _fig, (_a1, _a2) = plt.subplots(1, 2, figsize=(10.5, 4.0), gridspec_kw=dict(width_ratios=[1.1, 1]))
    # --- (a) mixing line
    _m = base_mix
    _a1.axhline(0, color=MUTED, lw=1)
    _a1.plot(_m["chi"], _m["b"] * 100, color=SERIES[0], label="b(χ), saturation-adjusted")
    _a1.plot([0, 1], [0, _m["db"] * 100], color=MUTED, lw=1.2, ls="--", label="no-evaporation (linear) mixing")
    _a1.fill_between(_m["chi"], _m["b"] * 100, 0, where=_m["b"] < 0, color=SERIES[1], alpha=0.25, lw=0,
                     label="negatively buoyant mixtures")
    _a1.plot([_m["chi_star"]], [_m["b_star"] * 100], "o", ms=8, color=SERIES[1], mec="white", mew=2)
    _a1.annotate(f"χ* = {_m['chi_star']:.3f}\nb(χ*) = {_m['b_star'] * 100:+.2f} cm s⁻²",
                 (_m["chi_star"], _m["b_star"] * 100), xytext=(0.55, 0.12), textcoords="axes fraction",
                 color=INK, fontsize=9, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    _zoom = min(1.0, max(4 * _m["chi_star"], 0.15))
    _a1.set_xlim(0, _zoom)
    _ylo = min(_m["b"].min() * 100 * 1.4, -0.2)
    _a1.set_ylim(_ylo, max(_m["b"][_m["chi"] <= _zoom].max() * 100 * 1.15, 0.5))
    _a1.set_xlabel("mixing fraction of inversion air χ  (zoomed)")
    _a1.set_ylabel("buoyancy relative to cloud  [cm s⁻²]")
    _a1.set_title("Mixing line at cloud top", loc="left", fontsize=10.5, color=INK)
    _a1.legend(loc="upper left", fontsize=8)

    # --- (b) Δq_t – Δθ_l stability diagram
    _dq = np.linspace(-12, -0.2, 60)
    _a2.fill_between(_dq, 0, 20, color="#f4f3f0", lw=0)
    for _kv, _lab, _c, _ls in [(kappa_c, f"κ_crit = {kappa_c:.2f} (buoyancy reversal, this p,T)", SERIES[1], "-"),
                               (kappa_user.value, f"κ = {kappa_user.value:.2f} (user line)", SERIES[6], "--")]:
        _dth = (_kv - 1) * sc.Lv * (_dq * 1e-3) / sc.cp
        _a2.plot(_dq, _dth, color=_c, ls=_ls, label=_lab)
    _dth_c = (kappa_c - 1) * sc.Lv * (_dq * 1e-3) / sc.cp
    _a2.fill_between(_dq, 0, _dth_c, color=SERIES[1], alpha=0.12, lw=0)
    _a2.text(-11.5, 1.0, "buoyancy reversal\n(CTEI-'unstable')", color=INK2, fontsize=8.5)
    for _i, (_name, _p) in enumerate([(n, p) for n, p in PRESETS.items() if n.startswith("DYCOMS")]):
        _a2.plot(_p["dqt"], _p["dthl"], "s", ms=8, color=SERIES[2 + _i], mec="white", mew=2, label=_name.split(" (")[0])
    _a2.plot(st["dqt"] * 1e3, st["dthl"], "o", ms=10, color=SERIES[0], mec="white", mew=2, label=f"current state (κ = {kappa_now:.2f})")
    _a2.set_xlim(-12, 0)
    _a2.set_ylim(0, 20)
    _a2.set_xlabel("Δq_t  [g/kg]")
    _a2.set_ylabel("Δθ_l  [K]")
    _a2.set_title("Inversion-jump stability diagram", loc="left", fontsize=10.5, color=INK)
    _a2.legend(loc="upper right", fontsize=7.5)
    _fig.tight_layout()
    _fig
    return


@app.cell
def _(base_mix, kappa_c, kappa_now, mo):
    _m = base_mix
    _rev = _m["b_star"] < 0
    mo.callout(
        mo.md(
            f"""**χ\\*** = {_m['chi_star']:.3f} · **Δb** = {_m['db']*100:.2f} cm s⁻² · **Δb_s** (saturated jump)
    = {_m['dbs']*100:+.2f} cm s⁻² · **evaporative enhancement E** = {_m['E']:.3f}.
    κ = {kappa_now:.2f} {'>' if kappa_now > kappa_c else '<'} κ_crit = {kappa_c:.2f} → **{'buoyancy reversal: the Randall–Deardorff criterion predicts CTEI' if _rev else 'no buoyancy reversal: mixtures are positively buoyant'}**."""
        ),
        kind="warn" if _rev else "success",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 · Entrainment closures on a common buoyancy-flux budget

    In a well-mixed layer the turbulent fluxes of θ_l and q_t are linear in height between the
    surface and the inversion, minus the radiative flux. The buoyancy flux therefore decomposes
    **exactly** as $B(z) = P(z) + w_e\,Q(z)$, and $w_*^3 = 2.5\int_0^{z_i} B\,dz$. Each closure picks
    a different w_e:

    | Closure | Condition |
    |---|---|
    | Efficiency (Nicholls & Turton 1986; Turton & Nicholls 1987) | $w_e = A\,w_*^3/(z_i\Delta b)$, $A = a_1[1 + a_2 E\,e^{-a_{sed} w_{sed}/w_*}]$ |
    | — TN87 / Bretherton & Wyant 1997 | a₁ = 0.2, a₂ = 60 |
    | — Caldwell & Bretherton 2009 | a₁ = 0.2, a₂ = 25 |
    | — Uchida et al. 2010 (LES-tuned) | a₁ = 0.2, a₂ = 110, a_sed = 9 (sedimentation; Bretherton et al. 2007) |
    | — Dry CBL (Deardorff 1976) | A = 0.2 |
    | Lilly (1968) minimum entrainment | sub-cloud buoyancy flux nowhere negative (min B = 0) |
    | Lilly (1968) maximum entrainment | no net TKE production: ∫B dz = 0 (upper bound) |
    | Flux-ratio closure | −(negative area)/(positive area) of B = k (flux-partitioning family; see Stevens 2002) |

    The **buoyancy integral ratio** BIR (negative sub-cloud area / positive area) indicates
    **decoupling** when it exceeds ≈ 0.15 (Bretherton & Wyant 1997; Turton & Nicholls 1987 used 0.4).
    """)
    return


@app.cell
def _(mo):
    CLOSURE_NAMES = [
        "TN87: a₂ = 60",
        "CB09: a₂ = 25",
        "Uchida+10: a₂ = 110, sed.",
        "Dry CBL: A = 0.2",
        "Lilly min (min B = 0)",
        "Lilly max (∫B = 0)",
        "Flux ratio k",
        "Custom efficiency",
    ]
    closure_select = mo.ui.multiselect(
        options=CLOSURE_NAMES,
        value=["TN87: a₂ = 60", "CB09: a₂ = 25", "Uchida+10: a₂ = 110, sed.", "Dry CBL: A = 0.2", "Lilly min (min B = 0)", "Custom efficiency"],
        label="Closures to compare",
    )
    custom_a1 = mo.ui.slider(0.05, 1.0, step=0.01, value=0.2, label="custom a₁", show_value=True, debounce=True)
    custom_a2 = mo.ui.slider(0.0, 150.0, step=1.0, value=40.0, label="custom a₂", show_value=True, debounce=True)
    custom_ased = mo.ui.slider(0.0, 20.0, step=0.5, value=9.0, label="custom a_sed", show_value=True, debounce=True)
    ratio_k = mo.ui.slider(0.02, 0.6, step=0.01, value=0.2, label="flux-ratio k", show_value=True, debounce=True)
    mo.vstack([closure_select, mo.hstack([custom_a1, custom_a2, custom_ased, ratio_k], wrap=True)])
    return CLOSURE_NAMES, closure_select, custom_a1, custom_a2, custom_ased, ratio_k


@app.cell
def _(CLOSURE_NAMES, custom_a1, custom_a2, custom_ased, ratio_k):
    CLOSURES = dict(
        zip(
            CLOSURE_NAMES,
            [
                dict(kind="efficiency", a1=0.2, a2=60.0, ased=0.0),
                dict(kind="efficiency", a1=0.2, a2=25.0, ased=0.0),
                dict(kind="efficiency", a1=0.2, a2=110.0, ased=9.0),
                dict(kind="efficiency", a1=0.2, a2=0.0, ased=0.0),
                dict(kind="lilly_min"),
                dict(kind="lilly_max"),
                dict(kind="ratio", k=ratio_k.value),
                dict(kind="efficiency", a1=custom_a1.value, a2=custom_a2.value, ased=custom_ased.value),
            ],
        )
    )
    return (CLOSURES,)


@app.cell
def _(CLOSURES, CLOSURE_NAMES, closure_select, sc, st):
    diag = {n: sc.diagnose(st, CLOSURES[n]) for n in CLOSURE_NAMES if n in closure_select.value}
    return (diag,)


@app.cell
def _(CLOSURE_NAMES, INK, INK2, MUTED, SERIES, base_prof, diag, np, plt, st):
    _fig, (_a1, _a2) = plt.subplots(1, 2, figsize=(10.5, 4.6), gridspec_kw=dict(width_ratios=[1.15, 1]))
    _z = base_prof["z"]
    _a1.axvline(0, color=MUTED, lw=1)
    if base_prof["lwp"] > 0:
        _a1.axhspan(base_prof["zb"], st["zi"], color="#eef3fb", lw=0)
        _a1.text(0.02, st["zi"] - 15, "cloud layer", transform=_a1.get_yaxis_transform(), ha="left", va="top", color=MUTED, fontsize=8.5)
    _names, _we, _cols = [], [], []
    for _n, _d in diag.items():
        _c = SERIES[CLOSURE_NAMES.index(_n)]
        if np.all(np.isfinite(_d["B"])):
            _a1.plot(_d["B"] * 1e4, _z, color=_c, label=_n)
        _names.append(_n)
        _we.append(_d["we"] * 1e3)
        _cols.append(_c)
    _a1.set_xlabel("buoyancy flux B  [10⁻⁴ m² s⁻³]")
    _a1.set_ylabel("height  [m]")
    _a1.set_ylim(0, st["zi"])
    _a1.set_title("Buoyancy-flux profiles implied by each closure", loc="left", fontsize=10.5, color=INK)
    _a1.legend(fontsize=7.5, loc="lower left")

    _y = np.arange(len(_names))
    _a2.barh(_y, np.nan_to_num(_we), color=_cols, height=0.6, edgecolor="white", linewidth=2)
    for _yy, _w in zip(_y, _we):
        _a2.text((_w if np.isfinite(_w) else 0) + 0.3, _yy, f"{_w:.1f}" if np.isfinite(_w) else "n/a", va="center", fontsize=8.5, color=INK)
    if st["obs_we"] is not None:
        _o, _e = st["obs_we"]
        _a2.axvspan(_o - _e, _o + _e, color=MUTED, alpha=0.18, lw=0)
        _a2.axvline(_o, color=MUTED, lw=1.5, ls="--")
        _a2.text(_o, 1.0, f"observed {_o:.0f}±{_e:g}", ha="center", va="bottom", fontsize=8, color=INK2,
                 transform=_a2.get_xaxis_transform())
    _a2.set_yticks(_y, _names, fontsize=8)
    _a2.invert_yaxis()
    _a2.set_xlabel("entrainment velocity w_e  [mm s⁻¹]")
    _a2.set_title("Entrainment rate", loc="left", fontsize=10.5, color=INK, pad=14)
    _a2.grid(axis="y", visible=False)
    _fig.tight_layout()
    _fig
    return


@app.cell
def _(diag, mo, np, st):
    _rows = []
    for _n, _d in diag.items():
        _rows.append(
            {
                "closure": _n,
                "w_e [mm/s]": round(float(_d["we"] * 1e3), 2) if np.isfinite(_d["we"]) else None,
                "w* [m/s]": round(float(np.cbrt(_d["wstar3"])), 2) if np.isfinite(_d["wstar3"]) else None,
                "A": round(float(_d["A"]), 2) if np.isfinite(_d["A"]) else None,
                "BIR": round(float(_d["bir"]), 3) if np.isfinite(_d["bir"]) else None,
                "decoupled? (BIR>0.15)": (bool(_d["bir"] > 0.15) if np.isfinite(_d["bir"]) else None),
                "dz_i/dt [mm/s] (D = 3.75e-6 s⁻¹)": round(float((_d["we"] - 3.75e-6 * st["zi"]) * 1e3), 2) if np.isfinite(_d["we"]) else None,
                "note": _d["note"],
            }
        )
    _any = next(iter(diag.values()), None)
    mo.vstack(
        [
            mo.ui.table(_rows, selection=None, label="Closure diagnostics"),
            mo.md(
                f"Cloud-top sedimentation velocity w_sed = **{_any['wsed']*100:.2f} cm/s** for N_d = {st['Nd']:.0f} cm⁻³ "
                "(enters only the closures with a_sed > 0). Typical observed Sc entrainment rates are 2–7 mm/s."
            ) if _any else mo.md("Select at least one closure."),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sensitivity scan

    How does w_e respond to the inversion jumps? The scan runs over Δθ_l (Δq_t fixed) or over Δq_t
    (Δθ_l fixed) for the selected closures. Watch the efficiency closures blow up as κ grows: more
    evaporative enhancement and a smaller Δb. This is the mixed-layer analogue of the CTEI feedback.
    """)
    return


@app.cell
def _(mo):
    scan_var = mo.ui.radio(options=["Δθ_l", "Δq_t"], value="Δθ_l", label="scan variable", inline=True)
    scan_var
    return (scan_var,)


@app.cell
def _(CLOSURES, CLOSURE_NAMES, INK, MUTED, SERIES, closure_select, np, plt, scan_var, sc, st):
    if scan_var.value == "Δθ_l":
        _xs = np.linspace(2.0, 16.0, 36)
        _mk = lambda x: {**st, "dthl": x}
        _xlab = "Δθ_l  [K]"
        _xnow = st["dthl"]
    else:
        _xs = np.linspace(-11.0, -0.5, 36)
        _mk = lambda x: {**st, "dqt": x * 1e-3}
        _xlab = "Δq_t  [g/kg]"
        _xnow = st["dqt"] * 1e3
    _fig, (_a1, _a2) = plt.subplots(1, 2, figsize=(10.5, 3.6))
    for _n in CLOSURE_NAMES:
        if _n not in closure_select.value:
            continue
        _w = []
        for _x in _xs:
            _d = sc.diagnose(_mk(_x), CLOSURES[_n], nz=80)
            _w.append(_d["we"] * 1e3)
        _a1.plot(_xs, _w, color=SERIES[CLOSURE_NAMES.index(_n)], label=_n)
    _kap = [sc.kappa_param(_mk(_x)["dthl"], _mk(_x)["dqt"]) for _x in _xs]
    _a2.plot(_xs, _kap, color=INK)
    for _a in (_a1, _a2):
        _a.axvline(_xnow, color=MUTED, ls=":", lw=1.2)
        _a.set_xlabel(_xlab)
    _a1.set_ylabel("w_e  [mm s⁻¹]")
    _a1.set_ylim(0, min(np.nanmax(_a1.get_ylim()[1]), 60))
    _a1.set_title("Entrainment velocity vs inversion jump", loc="left", fontsize=10.5, color=INK)
    _a1.legend(fontsize=7.5)
    _a2.set_ylabel("κ")
    _a2.set_title("Inversion stability parameter κ", loc="left", fontsize=10.5, color=INK)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 · Mixed-layer model: time evolution

    A Lilly (1968)-type model: $\partial_t \theta_l$, $\partial_t q_t$ from flux divergences,
    $\mathrm{d}z_i/\mathrm{d}t = w_e - D z_i$, bulk surface fluxes over a fixed SST, the GCSS
    radiation above, a free troposphere with lapse rate Γ above the initial inversion
    (initial jumps from §1), and an optional drizzle sink that depends on LWP and N_d. Every closure sees identical forcing, so the spread between the curves
    reflects the closure alone. Runs stop early if a closure has no finite solution, for example
    runaway entrainment once buoyancy reversal dominates.
    """)
    return


@app.cell
def _(CLOSURE_NAMES, mo, st):
    _s = lambda lo, hi, stp, v, lab: mo.ui.slider(lo, hi, step=stp, value=v, label=lab, show_value=True, debounce=True)
    mlm_ui = mo.ui.dictionary(
        {
            "sst": _s(285.0, 302.0, 0.1, st["sst"], "SST [K]"),
            "V": _s(1.0, 15.0, 0.5, 7.0, "wind speed V [m/s]"),
            "D": _s(0.0, 8.0, 0.05, 3.75, "divergence D [10⁻⁶ s⁻¹]"),
            "gamma": _s(0.0, 10.0, 0.1, 5.0, "FT lapse Γ [K/km]"),
            "Fclear": _s(0.0, 60.0, 1.0, 0.0, "extra clear-sky cooling [W/m²]"),
            "hours": _s(6.0, 120.0, 6.0, 48.0, "duration [h]"),
            "drizzle": mo.ui.checkbox(value=True, label="drizzle sink (Comstock et al. 2004)"),
        }
    )
    mlm_closures = mo.ui.multiselect(
        options=CLOSURE_NAMES,
        value=["TN87: a₂ = 60", "CB09: a₂ = 25", "Uchida+10: a₂ = 110, sed.", "Lilly min (min B = 0)"],
        label="Closures to integrate",
    )
    mo.vstack([mo.hstack(list(mlm_ui.elements.values()), wrap=True), mlm_closures])
    return mlm_closures, mlm_ui


@app.cell
def _(CLOSURES, CLOSURE_NAMES, mlm_closures, mlm_ui, sc, st):
    _v = mlm_ui.value
    mlm_runs = {}
    for _n in CLOSURE_NAMES:
        if _n in mlm_closures.value:
            mlm_runs[_n] = sc.run_mlm(st, CLOSURES[_n], sst=_v["sst"], V=_v["V"], D=_v["D"] * 1e-6,
                                     gamma_th=_v["gamma"] * 1e-3, F_clear=_v["Fclear"], hours=_v["hours"],
                                     drizzle=_v["drizzle"])
    return (mlm_runs,)


@app.cell
def _(CLOSURE_NAMES, INK, MUTED, SERIES, mlm_runs, mo, plt):
    _fig, _ax = plt.subplots(2, 3, figsize=(11, 6.0), sharex=True)
    _ax = _ax.ravel()
    _titles = ["Cloud top (solid) and base (dashed) [m]", "Liquid water path [g m⁻²]", "Entrainment velocity [mm s⁻¹]",
               "Convective velocity w* [m s⁻¹]", "Buoyancy integral ratio (decoupling)", "Inversion parameter κ"]
    for _n, (_o, _status) in mlm_runs.items():
        _c = SERIES[CLOSURE_NAMES.index(_n)]
        _ax[0].plot(_o["t"], _o["zi"], color=_c, label=_n)
        _ax[0].plot(_o["t"], _o["zb"], color=_c, ls="--", lw=1.4)
        _ax[1].plot(_o["t"], _o["lwp"] * 1e3, color=_c)
        _ax[2].plot(_o["t"], _o["we"] * 1e3, color=_c)
        _ax[3].plot(_o["t"], _o["wstar"], color=_c)
        _ax[4].plot(_o["t"], _o["bir"], color=_c)
        _ax[5].plot(_o["t"], _o["kappa"], color=_c)
    _ax[4].axhline(0.15, color=MUTED, ls="--", lw=1.2)
    _ax[4].text(0.01, 0.15, " BW97 threshold 0.15", va="bottom", fontsize=8, color=MUTED, transform=_ax[4].get_yaxis_transform())
    for _a, _t in zip(_ax, _titles):
        _a.set_title(_t, loc="left", fontsize=9.5, color=INK)
    for _a in _ax[3:]:
        _a.set_xlabel("time [h]")
    _ax[0].legend(fontsize=7.5, loc="best")
    _fig.tight_layout()
    _msgs = [f"- **{_n}**: {_s}" for _n, (_, _s) in mlm_runs.items() if _s != "ok"]
    mo.vstack([_fig, mo.callout(mo.md("\n".join(_msgs)), kind="warn") if _msgs else mo.md("")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5 · Shear and small-scale turbulence at the inversion

    Aircraft and helicopter observations (Katzwinkel et al. 2012; Malinowski et al. 2013; Jen-La Plante
    et al. 2016) show a **turbulent entrainment interfacial layer (EIL)** a few to tens of metres thick
    above the cloud, often held at **marginal stability** by wind shear: the bulk Richardson number
    $Ri_b = \Delta b\, h / \Delta u^2$ hovers around 0.2–0.7. DNS suggest a shear-layer thickness
    $h \approx \tfrac13\,\Delta u^2/\Delta b$ (Mellado et al. 2014). Shear enhances entrainment only
    above a critical velocity jump (Schulz & Mellado 2018), and sedimentation can cancel the effect
    (Schulz & Mellado 2019).

    The scales separate widely, from the **Kolmogorov scale η ≈ 1 mm** to z_i ≈ 1 km. The
    long-wave cooling is deposited over an **optical e-folding length** of order 10–20 m, and
    de Lozar & Mellado (2013) argue that eddies larger than a few optical lengths do little of the
    entraining. That is why LES needs Δz ≲ 5 m near the inversion (Stevens et al. 2005) and why DNS
    of the cloud-top layer has become a key tool (Mellado 2017; Mellado et al. 2018).
    """)
    return


@app.cell
def _(mo):
    du = mo.ui.slider(0.0, 10.0, step=0.1, value=2.0, label="velocity jump Δu [m/s]", show_value=True)
    c_h = mo.ui.slider(0.1, 1.0, step=0.01, value=0.33, label="h = c Δu²/Δb, c =", show_value=True)
    log_eps_cloud = mo.ui.slider(-6.0, -2.0, step=0.1, value=-3.0, label="log₁₀ ε in cloud [m²/s³]", show_value=True)
    log_eps_eil = mo.ui.slider(-7.0, -2.0, step=0.1, value=-4.0, label="log₁₀ ε in EIL [m²/s³]", show_value=True)
    mo.hstack([du, c_h, log_eps_cloud, log_eps_eil], wrap=True)
    return c_h, du, log_eps_cloud, log_eps_eil


@app.cell
def _(INK, INK2, MUTED, SERIES, base_mix, base_prof, c_h, du, log_eps_cloud, log_eps_eil, mo, np, plt, st):
    _nu = 1.5e-5
    _db = max(base_mix["db"], 1e-6)
    _eps_c, _eps_i = 10 ** log_eps_cloud.value, 10 ** log_eps_eil.value
    _h = max(c_h.value * du.value**2 / _db, 0.0)
    _N2 = _db / max(_h, 1.0)  # stratification across the EIL (h floored at 1 m)
    _LO = np.sqrt(_eps_i / _N2**1.5)  # Ozmidov scale
    _eta_c = (_nu**3 / _eps_c) ** 0.25
    _eta_i = (_nu**3 / _eps_i) ** 0.25
    _u = (_eps_c * st["zi"]) ** (1 / 3)
    _lam = np.sqrt(15 * _nu * _u**2 / _eps_c)
    _Re_lam = _u * _lam / _nu
    _Reb = _eps_i / (_nu * _N2)
    _rho_ql = base_prof["rho_top"] * base_prof["ql_top"]
    _lrad = 1.0 / (st["klw"] * _rho_ql) if _rho_ql > 0 else np.nan
    _ndns = (st["zi"] / _eta_c) ** 3

    _fig, (_a1, _a2) = plt.subplots(1, 2, figsize=(10.5, 3.8), gridspec_kw=dict(width_ratios=[1, 1.3]))
    _hh = np.linspace(0.5, 150, 300)
    _Ri = _db * _hh / max(du.value, 1e-3) ** 2
    _a1.axhspan(0, 0.25, color=SERIES[1], alpha=0.12, lw=0)
    _a1.axhspan(0.2, 0.7, color=SERIES[0], alpha=0.10, lw=0)
    _a1.plot(_hh, _Ri, color=INK)
    _a1.axhline(0.25, color=SERIES[1], lw=1.2, ls="--")
    _a1.text(148, 0.12, "Ri < ¼: KH-unstable", ha="right", fontsize=8, color=INK2)
    _a1.text(148, 0.62, "ACTOS range 0.2–0.7", ha="right", fontsize=8, color=INK2)
    if _h > 0:
        _a1.plot([_h], [c_h.value], "o", ms=9, color=SERIES[0], mec="white", mew=2)
        _a1.annotate(f"h = {_h:.0f} m", (_h, c_h.value), xytext=(8, 8), textcoords="offset points", fontsize=8.5, color=INK)
    _a1.set_xlim(0, 150)
    _a1.set_ylim(0, 2)
    _a1.set_xlabel("EIL thickness h [m]")
    _a1.set_ylabel("bulk Ri = Δb h / Δu²")
    _a1.set_title("Shear-layer stability", loc="left", fontsize=10.5, color=INK)

    _scales = [("Kolmogorov η (cloud)", _eta_c), ("Kolmogorov η (EIL)", _eta_i), ("Taylor λ (cloud)", _lam),
               ("Ozmidov L_O (EIL)", _LO), ("LW optical length", _lrad), ("shear layer h", _h),
               ("LES Δz ≈ 5 m", 5.0), ("z_i", st["zi"])]
    _scales = [(n, v) for n, v in _scales if np.isfinite(v) and v > 0]
    _scales.sort(key=lambda t: t[1])
    for _i, (_n, _v) in enumerate(_scales):
        _a2.plot([1e-4, _v], [_i, _i], color="#e4e3df", lw=2)
        _a2.plot([_v], [_i], "o", ms=8, color=SERIES[0], mec="white", mew=2)
        _a2.text(_v * 1.4, _i, f"{_v:.3g} m", va="center", fontsize=8, color=INK2)
    _a2.set_yticks(range(len(_scales)), [n for n, _ in _scales], fontsize=8.5)
    _a2.set_xscale("log")
    _a2.set_xlim(1e-4, 1e5)
    _a2.set_xlabel("length scale [m]")
    _a2.set_title("Scale ladder of cloud-top turbulence", loc="left", fontsize=10.5, color=INK)
    _a2.grid(axis="y", visible=False)
    _fig.tight_layout()

    mo.vstack(
        [
            _fig,
            mo.hstack(
                [
                    mo.stat(f"{_h:.1f} m", label="shear-layer thickness h", caption=f"N = {np.sqrt(_N2):.3f} s⁻¹ across EIL"),
                    mo.stat(f"{_Reb:.2g}", label="buoyancy Reynolds ε/(νN²)", caption="> ~20: turbulence survives stratification" if _Reb > 20 else "low: viscously damped / intermittent"),
                    mo.stat(f"{_Re_lam:.2g}", label="Re_λ (cloud)", caption=f"u' ≈ (ε z_i)^⅓ = {_u:.2f} m/s"),
                    mo.stat(f"{_ndns:.1e}", label="DNS points for (z_i/η)³", caption="largest DNS today ≈ 10¹²"),
                ],
                widths="equal",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Ideas for experiments

    * **CTEI paradox**: pick the *strong buoyancy reversal* preset (κ ≈ 0.7). The Randall–Deardorff
      criterion flags instability, yet most closures still give a finite entrainment rate and the
      mixed-layer cloud persists for a while. Lower Δθ_l toward 5 K and watch the efficiency closures lose
      their finite solution. This is the mixed-layer analogue of CTEI runaway, and the scan in §3 shows it too.
      Compare LWP tendencies for κ ≈ 0.3, 0.5 and 0.7 (van der Dussen et al. 2014).
    * **Sedimentation–entrainment feedback**: with the Uchida+10 closure and the drizzle sink off, vary
      N_d from 30 to 300 cm⁻³. Fewer, larger droplets sediment faster, entrain less and give *higher* LWP
      (Bretherton et al. 2007). Turn drizzle on to see the opposing drizzle effect (Uchida et al. 2010).
    * **Decoupling**: raise SST or wind speed in §4 and watch the BIR cross 0.15 as the latent heat flux
      grows relative to radiative cooling (Bretherton & Wyant 1997).
    * **Free-tropospheric humidity**: lower Δq_t toward 0 g/kg (a moist free troposphere) and compare
      with Ackerman et al. (2004).
    * **Radiative forcing**: set F₀ to zero (e.g. under an overlying cloud layer). Entrainment collapses
      in every closure, because cloud-top cooling is the main source of turbulence in Sc.

    ### Key references (full list in `literature_review.md`)
    Lilly (1968) *QJRMS* 94 · Randall (1980) *JAS* 37 · Deardorff (1980) *JAS* 37 · Nicholls & Turton (1986) *QJRMS* 112 ·
    Turton & Nicholls (1987) *QJRMS* 113 · Bretherton & Wyant (1997) *JAS* 54 · Stevens (2002) *QJRMS* 128 ·
    Stevens et al. (2005) *MWR* 133 · Bretherton et al. (2007) *GRL* 34 · Ackerman et al. (2009) *MWR* 137 ·
    Caldwell & Bretherton (2009) *J. Climate* 22 · Uchida et al. (2010) *ACP* 10 · Wood (2012) *MWR* 140 ·
    Katzwinkel et al. (2012) *BLM* 145 · Mellado et al. (2014) *JAS* 71 · van der Dussen et al. (2014) *JAS* 71 ·
    de Lozar & Mellado (2015) *JAS* 72 · Mellado (2017) *Annu. Rev. Fluid Mech.* 49 · Schulz & Mellado (2018, 2019).
    """)
    return


if __name__ == "__main__":
    app.run()
