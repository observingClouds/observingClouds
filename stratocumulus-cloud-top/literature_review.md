# Stratocumulus cloud-top processes and turbulence: a literature review

*Companion to the interactive notebook [`stratocumulus_cloud_top.py`](stratocumulus_cloud_top.py).*

---

## 1. Why the cloud top matters

Subtropical marine stratocumulus (Sc) cover roughly a fifth of the ocean surface and reflect much
more sunlight than the dark ocean underneath, while emitting at nearly the surface temperature. Their
net cloud radiative effect is therefore strongly negative, and small fractional changes matter for
climate sensitivity (Wood 2012; Bretherton 2015). Sc amount correlates with the strength of the
capping inversion, measured as lower-tropospheric stability (LTS; Klein & Hartmann 1993) or
estimated inversion strength (EIS; Wood & Bretherton 2006). The inversion matters so much because
the **thin (O(10 m)) layer at cloud top** is where the competing processes meet:

* **long-wave radiative cooling**, typically 40–100 W m⁻² deposited in the uppermost tens of metres
  of cloud, which is the main driver of turbulence (Lilly 1968; Nicholls 1989);
* **evaporative cooling** of cloudy air mixed with warm, dry inversion air (Randall 1980; Deardorff 1980);
* **wind shear** across the inversion (Wang et al. 2008; Katzwinkel et al. 2012; Mellado et al. 2014);
* **droplet sedimentation** and microphysics, which control how much liquid water is available to
  evaporate in the entrainment zone (Ackerman et al. 2004; Bretherton et al. 2007);
* and **entrainment**, the turbulent incorporation of free-tropospheric air. Entrainment deepens the
  boundary layer, warms and dries it, and largely sets cloud thickness and lifetime (Stevens 2002;
  Mellado 2017).

The central difficulty is a separation of scales. The inversion is a few metres to tens of metres
thick and the Kolmogorov scale is about 1 mm, while the energy-containing eddies have the size of the
boundary layer (z_i ≈ 1 km). Large-eddy simulation (LES) therefore does not resolve the processes
that set the entrainment rate, and climate models must parameterise them.

---

## 2. The mixed-layer framework

### 2.1 Lilly's model
Lilly (1968) laid the foundation. He treated the cloud-topped boundary layer as **well mixed** in
variables conserved under moist adiabatic processes (liquid-water static energy or θ_l, and total
water q_t), with a **zero-order jump** at z_i. Mass and heat budgets give

* dz_i/dt = w_e − D z_i (entrainment vs. large-scale subsidence),
* the jump conditions for the turbulent fluxes at z_i: (w′φ′)_{z_i} = −w_e Δφ,
* fluxes that are linear in height (because a well-mixed layer warms or moistens uniformly).

The system needs one more relation for **w_e**. Lilly bracketed it with a **minimum-entrainment**
bound (the buoyancy flux is nowhere negative) and a **maximum-entrainment** bound (the vertically
integrated buoyancy flux vanishes, so no TKE is left for dissipation). Schubert et al. (1979),
Deardorff (1976), Stage & Businger (1981) and many others built on this framework. Bretherton & Wyant
(1997) show that a good approximation to w_e for almost any closure is the energy-balance rate given
by Lilly's minimum-entrainment closure.

### 2.2 Efficiency closures
The most widely used family writes

$$ w_e = A\,\frac{w_*^3}{z_i\,\Delta b}, \qquad w_*^3 = 2.5\int_0^{z_i}\overline{w'b'}\,dz, $$

where Δb is the buoyancy jump and A an **entrainment efficiency**. For a dry convective layer
A ≈ 0.2 (Deardorff 1976). Nicholls & Turton (1986) fitted aircraft data and laboratory experiments
and proposed that evaporative cooling enhances A:

$$ A = a_1\left[1 + a_2\left(1-\frac{\Delta_m}{\Delta b}\right)\right], $$

with Δ_m twice the average buoyancy over all mixtures of cloud and inversion air. Turton & Nicholls
(1987) and Bretherton & Wyant (1997) used a₁ = 0.2, a₂ = 60. Caldwell & Bretherton (2009) reduced a₂
to 25 to match DYCOMS-II and EPIC observations. Bretherton et al. (2007) showed in LES that droplet
**sedimentation** removes liquid water from the entrainment zone and makes entrainment less
efficient, and proposed damping the evaporative term by exp(−a_sed w_sed/w_*). Uchida et al. (2010)
retuned this against LES to a₂ = 110, a_sed = 9, with w_sed from a log-normal droplet size
distribution (σ_g = 1.2). For a piecewise-linear mixing line, 1 − Δ_m/Δb = χ*(1 − Δb_s/Δb), where
χ* is the saturation mixing fraction and Δb_s the saturated buoyancy jump. The notebook uses this identity.

Other closures include Lock (1998), Lewellen & Lewellen (1998), vanZanten et al. (1999), Moeng (2000)
and Lilly (2002a,b). They differ mainly in how they treat radiative cooling inside the entrainment
zone and the smoothness of the inversion. Stevens (2002) reviews them and argues that closures
expressed only in terms of a w_* scaling hide important physics: radiative and evaporative
processes act *within* the entrainment zone itself. He also notes that entrainment rates from
different closures, all applied to the same state, can differ by a factor of two to three.

### 2.3 Decoupling
When surface latent heat fluxes grow relative to cloud-top radiative cooling, for example over
warmer SSTs, the well-mixed assumption breaks down. Negative buoyancy fluxes appear below cloud base,
and the cloud layer **decouples** from the surface. Turton & Nicholls (1987) introduced the **buoyancy
integral ratio** (BIR), the negative sub-cloud buoyancy-flux area divided by the positive area. Bretherton & Wyant (1997)
used BIR > 0.15 as a decoupling threshold, where Turton & Nicholls had used 0.4. They identified the ratio of surface latent heat
flux to cloud radiative cooling as the main control. Decoupling, cumulus coupling and deepening are
the main route of the Sc-to-cumulus transition.

---

## 3. Buoyancy reversal and cloud-top entrainment instability (CTEI)

### 3.1 The original argument
Mixing a fraction χ of warm, dry inversion air into cloudy air evaporates liquid water and cools
the mixture. If the evaporative cooling is strong enough, some mixtures become **denser than the
cloud itself**. This is **buoyancy reversal**. Randall (1980) and Deardorff (1980) argued that this
leads to runaway entrainment: negatively buoyant mixtures sink, generate TKE, entrain more and break
up the cloud (**CTEI**). In terms of the inversion jumps, the criterion is equivalent to

$$ \kappa \equiv 1 + \frac{c_p\,\Delta\theta_l}{L_v\,\Delta q_t} > \kappa_{crit}, \qquad \kappa_{crit}\approx 0.2\text{–}0.25 $$

for typical subtropical temperatures and pressures (the notebook computes κ_crit exactly for the
current state).

### 3.2 Refinements and the "CTEI paradox"
Many observed, persistent Sc decks sit inside the region that the Randall–Deardorff criterion calls
unstable (Kuo & Schubert 1988; Stevens et al. 2003). Later studies tightened the criterion or recast it:

* **Siems et al. (1990)** found in laboratory and numerical experiments that buoyancy reversal alone
  produces only weak mixing unless it is strong.
* **MacVean & Mason (1990)** and **Duynkerke (1993)** used energetic arguments and derived more
  restrictive conditions under which entrainment genuinely releases enough energy to run away.
  These conditions are rarely met in observed Sc.
* **Yamaguchi & Randall (2008)** ran LES of evaporatively driven entrainment. Deck break-up needed
  κ well above the classical threshold.
* **Mellado (2010)** and **Mellado et al. (2009)** used DNS of the evaporatively driven cloud-top
  mixing layer. Buoyancy reversal produces turbulence whose intensity scales with the (small)
  buoyancy-reversal magnitude, but it is too weak to destroy a deck on relevant timescales without
  other forcing.
* **van der Dussen et al. (2014)** derived the LWP budget of a well-mixed, adiabatic Sc layer.
  The LWP tendency decreases as κ grows because the entrained air is increasingly dry, and an equilibrium
  κ_eq exists beyond which the cloud thins. κ_eq depends on other factors, notably the moisture flux at cloud base.
* **Xiao et al. (2011)** found in LES that the Sc-to-cumulus transition is most likely when
  buoyancy reversal coincides with decoupling driven by strong surface evaporation.

The current view is that buoyancy reversal is not by itself an instability that destroys the cloud.
κ is better read as an indicator of how strongly entrainment dries and thins the cloud. Its effect
depends on radiative forcing, surface fluxes, shear and microphysics.

---

## 4. Radiative and evaporative driving within the entrainment zone

Long-wave cooling in Sc is concentrated within roughly one optical e-folding length of cloud top,
about 1/(κ_lw ρ q_l) ≈ 10–30 m. Some of it falls inside the **entrainment interfacial layer
(EIL)**, where mixtures of cloud and inversion air are cooled directly. Moeng (2000), Lock (1998) and
Stevens (2002) emphasise that this "direct" radiative cooling of entrained air helps sustain the
entrainment flux. The LES intercomparisons for DYCOMS-II RF01 (Stevens et al. 2005) and RF02
(Ackerman et al. 2009) used an idealised radiation scheme of the form
F_R(z) = F₀ e^{−κ Q(z,∞)} + F₁ e^{−κ Q(0,z)} + (free-troposphere term), with F₀ = 70 W m⁻², F₁ = 22 W m⁻²,
κ = 85 m² kg⁻¹. This scheme is reused in the notebook. Both studies found entrainment rates highly sensitive to
numerics. Many LES over-entrained relative to the observed ≈ 4 mm s⁻¹ (RF01) and ≈ 6 mm s⁻¹ (RF02),
mainly because of spurious mixing at an under-resolved inversion.

**de Lozar & Mellado (2013, 2015)** used DNS of a cloud-top mixing layer driven by radiative and
evaporative cooling, and separated the contributions of radiation, evaporation and diffusion to the
entrainment velocity. Radiative cooling alone in a "smoke cloud" sustains reasonable in-cloud
turbulence but entrains too slowly. Eddies much larger than a few optical lengths contribute little
to entrainment. Evaporative cooling enhances entrainment through small-scale mixing within the EIL.

---

## 5. Sedimentation, drizzle and aerosol

Entrainment links the cloud top to aerosol-cloud interactions:

* **Ackerman et al. (2004)** showed in LES that more droplets (smaller, more numerous droplets that
  evaporate faster and sediment slower) can *increase* entrainment and reduce LWP when the overlying
  air is dry. This partly offsets the Twomey brightening.
* **Bretherton et al. (2007)** isolated **sedimentation** as the main mechanism. Faster sedimentation
  (fewer, larger droplets) removes liquid from the entrainment zone and reduces evaporative enhancement.
  The result is weaker entrainment and higher LWP.
* **de Lozar & Mellado (2017)** found with DNS that sedimentation reduces the entrainment velocity
  even more than LES had suggested.
* **Schulz & Mellado (2019)** found that the sedimentation effect (up to ≈ 40 % reduction) can fully
  compensate the shear enhancement of entrainment (up to ≈ 40 %) under subtropical conditions. Entrainment
  parameterisations should therefore weight both effects similarly.
* **Glassmeier et al. (2021)** showed that the slow, entrainment-mediated LWP adjustment of Sc
  takes days. This complicates inferences from short-lived ship tracks.

At the droplet scale, mixing of cloudy and dry air ranges from **homogeneous** (all droplets
partially evaporate) to **extreme inhomogeneous** (some droplets evaporate completely, others are untouched).
Which regime applies depends on the ratio of the turbulent mixing time to the droplet evaporation time
(Baker et al. 1980; Burnet & Brenguier 2007; Lehmann et al. 2009). This affects the droplet size
distribution near the cloud top and hence the radiative and sedimentation properties.

---

## 6. Turbulence at the inversion: observations

### 6.1 Field campaigns
* **FIRE** (Albrecht et al. 1988) and **ASTEX** (Albrecht et al. 1995) provided the first systematic
  turbulence and microphysics data in Sc and in the Sc-to-cumulus transition.
* **DYCOMS-II** (Stevens et al. 2003a) measured entrainment with several independent methods
  (flux-jump, conserved scalars, ozone/DMS budgets; Stevens et al. 2003b; Faloona et al. 2005).
  Rates ranged from about 1 to 7 mm s⁻¹. These measurements became benchmarks for LES (Stevens et al. 2005;
  Ackerman et al. 2009) and for single-column models (Zhu et al. 2005). Gerber et al. (2005) described "holes" and
  entrainment-related structure at cloud top.
* **VOCALS-REx** (Wood et al. 2011) sampled the south-east Pacific Sc deck and its transitions; Carman et
  al. (2012) used it to constrain entrainment and the EIL.
* **POST** (Physics of Stratocumulus Top; Gerber et al. 2013; Malinowski et al. 2013;
  Jen-La Plante et al. 2016) flew high-rate, slow-flight sampling through the Sc top off California.
  Mixing across the capping inversion takes place in a turbulent inversion layer (TIL) above the
  cloud. Shear-generated turbulence there is often strong, and turbulence is anisotropic and
  intermittent at the cloud edge.
* **ACTOS** helicopter-borne measurements (Katzwinkel et al. 2012) found a **self-limiting,
  shear-induced turbulent inversion layer** 37–85 m thick, with nearly linear profiles of θ, wind,
  humidity and aerosol. The bulk Richardson number increased from ≈ 0.2 to ≈ 0.7 as the layer grew, which is
  consistent with shear production balanced by buoyancy suppression. Eddy sizes were limited to around the
  Ozmidov scale, and mixing was more like "nibbling" than large-eddy engulfment.

### 6.2 Shear
LES (Wang et al. 2008; Kopec et al. 2016) and DNS (Mellado et al. 2014; Schulz & Mellado 2018)
agree on several points:
* shear thickens the EIL and promotes Kelvin–Helmholtz mixing;
* DNS give a background shear-layer thickness of about (1/3)Δu²/Δb, i.e. a bulk Ri near 1/3
  (Mellado et al. 2014);
* shear markedly enhances entrainment only when the velocity jump exceeds a critical value
  (≈ 1–4 m s⁻¹ in Schulz & Mellado 2018), and can then thin the cloud;
* shear-enhanced mixing can make buoyancy reversal comparable to other forcing mechanisms
  (Mellado et al. 2014).

---

## 7. Numerical modelling: LES, DNS and their gap

* **LES intercomparisons** (Moeng et al. 1996; Stevens et al. 2005; Ackerman et al. 2009) show that
  vertical resolution near the inversion, advection schemes and subgrid models strongly affect
  entrainment. Δz ≲ 5 m near the inversion is a common minimum, and results often fail to converge
  even then.
* **DNS** resolves the Kolmogorov scale but only over small domains of O(1–10 m). It has clarified
  the physics of buoyancy reversal (Mellado 2010), radiative–evaporative interactions (de Lozar &
  Mellado 2015), sedimentation (de Lozar & Mellado 2017) and shear (Mellado et al. 2014; Schulz &
  Mellado 2018, 2019).
* **Mellado (2017)** reviews cloud-top entrainment from a fluid-dynamics perspective. **Mellado et al.
  (2018)** argue that DNS and LES are complementary ("better together"). DNS can calibrate the
  small-scale entrainment physics that LES must parameterise near the inversion.
* **Mixed-layer models** remain valuable as conceptual tools. Examples include multiple equilibria
  and slow manifolds (Bretherton et al. 2010), climate-change responses (Caldwell & Bretherton 2009)
  and the sensitivity to free-tropospheric humidity and subsidence (van der Dussen et al. 2016).
  Their results depend strongly on the entrainment closure (Uchida et al. 2010). This is the
  dependence the notebook lets you explore.

---

## 8. Climate relevance and open questions

* Low-cloud feedback in GCMs is dominated by how Sc and the Sc-to-cumulus transition respond to
  warming. The response involves changes in inversion strength, free-tropospheric humidity,
  subsidence and greenhouse-gas radiative cooling, all of which act through cloud-top entrainment
  (Bretherton 2015). LES suggest that very high CO₂ could break up Sc decks by weakening cloud-top
  radiative cooling (Schneider et al. 2019).
* Myers & Norris (2013) show that stronger subsidence reduces marine boundary-layer cloudiness at
  fixed inversion strength. A shallower boundary layer and the entrainment response are the likely
  explanation.

**Open questions**
1. A physically based entrainment closure that combines radiative, evaporative, shear and
   sedimentation effects and converges with resolution.
2. How the EIL thickness is set, and how it couples to large eddies (engulfment vs nibbling).
3. How cloud-top mixing (homogeneous vs inhomogeneous) feeds back on droplet spectra, drizzle and
   radiation.
4. Under which combinations of κ, decoupling and precipitation decks actually break up (CTEI vs
   transition vs open cells).
5. Robust observational estimates of w_e and its variability on climate-relevant timescales.

---

## 9. Mapping to the notebook

| Notebook section | Literature it illustrates |
|---|---|
| §1 Set-up & presets | DYCOMS-II RF01/RF02 (Stevens et al. 2005; Ackerman et al. 2009) |
| §2 Mixing diagram, κ, χ* | Randall 1980; Deardorff 1980; Siems et al. 1990; Duynkerke 1993; van der Dussen et al. 2014 |
| §3 Entrainment closures | Lilly 1968; Deardorff 1976; Nicholls & Turton 1986; Turton & Nicholls 1987; Bretherton & Wyant 1997; Bretherton et al. 2007; Caldwell & Bretherton 2009; Uchida et al. 2010; Stevens 2002 |
| §4 Mixed-layer model | Lilly 1968; Bretherton & Wyant 1997; Caldwell & Bretherton 2009; Uchida et al. 2010 |
| §5 Shear & scales | Katzwinkel et al. 2012; Mellado et al. 2014; Schulz & Mellado 2018, 2019; de Lozar & Mellado 2013; Mellado 2017; Mellado et al. 2018 |

---

## References

*Note: the bibliographic details were compiled from memory. Only the papers central to the
notebook's formulas and numbers were checked against the publications or their abstracts
(Uchida et al. 2010; Bretherton & Wyant 1997; Bretherton et al. 2007; Katzwinkel et al. 2012;
Mellado et al. 2014; Schulz & Mellado 2019; van der Dussen et al. 2014; de Lozar & Mellado 2015;
Xiao et al. 2011). Please verify the others before citing them formally.*

- Ackerman, A. S., M. P. Kirkpatrick, D. E. Stevens, and O. B. Toon, 2004: The impact of humidity above stratiform clouds on indirect aerosol climate forcing. *Nature*, **432**, 1014–1017.
- Ackerman, A. S., and Coauthors, 2009: Large-eddy simulations of a drizzling, stratocumulus-topped marine boundary layer. *Mon. Wea. Rev.*, **137**, 1083–1110.
- Albrecht, B. A., D. A. Randall, and S. Nicholls, 1988: Observations of marine stratocumulus clouds during FIRE. *Bull. Amer. Meteor. Soc.*, **69**, 618–626.
- Albrecht, B. A., C. S. Bretherton, D. Johnson, W. H. Schubert, and A. S. Frisch, 1995: The Atlantic Stratocumulus Transition Experiment—ASTEX. *Bull. Amer. Meteor. Soc.*, **76**, 889–904.
- Baker, M. B., R. G. Corbin, and J. Latham, 1980: The influence of entrainment on the evolution of cloud droplet spectra: I. A model of inhomogeneous mixing. *Quart. J. Roy. Meteor. Soc.*, **106**, 581–598.
- Bretherton, C. S., 2015: Insights into low-latitude cloud feedbacks from high-resolution models. *Phil. Trans. Roy. Soc. A*, **373**, 20140415.
- Bretherton, C. S., and M. C. Wyant, 1997: Moisture transport, lower-tropospheric stability, and decoupling of cloud-topped boundary layers. *J. Atmos. Sci.*, **54**, 148–167.
- Bretherton, C. S., P. N. Blossey, and J. Uchida, 2007: Cloud droplet sedimentation, entrainment efficiency, and subtropical stratocumulus albedo. *Geophys. Res. Lett.*, **34**, L03813, doi:10.1029/2006GL027648.
- Bretherton, C. S., J. Uchida, and P. N. Blossey, 2010: Slow manifolds and multiple equilibria in stratocumulus-capped boundary layers. *J. Adv. Model. Earth Syst.*, **2**, 14.
- Burnet, F., and J.-L. Brenguier, 2007: Observational study of the entrainment-mixing process in warm convective clouds. *J. Atmos. Sci.*, **64**, 1995–2011.
- Caldwell, P., and C. S. Bretherton, 2009: Response of a subtropical stratocumulus-capped mixed layer to climate and aerosol changes. *J. Climate*, **22**, 20–38.
- Carman, J. K., and Coauthors, 2012: Observational constraints on entrainment and the entrainment interface layer in stratocumulus. *Atmos. Chem. Phys.*, **12**, 11135–11152.
- de Lozar, A., and J. P. Mellado, 2013: Direct numerical simulations of a smoke cloud-top mixing layer as a model for stratocumuli. *J. Atmos. Sci.*, **70**, 2356–2375.
- de Lozar, A., and J. P. Mellado, 2015: Mixing driven by radiative and evaporative cooling at the stratocumulus top. *J. Atmos. Sci.*, **72**, 4681–4700, doi:10.1175/JAS-D-15-0087.1.
- de Lozar, A., and J. P. Mellado, 2017: Reduction of the entrainment velocity by cloud droplet sedimentation in stratocumulus. *J. Atmos. Sci.*, **74**, 751–765.
- Deardorff, J. W., 1976: On the entrainment rate of a stratocumulus-topped mixed layer. *Quart. J. Roy. Meteor. Soc.*, **102**, 563–582.
- Deardorff, J. W., 1980: Cloud top entrainment instability. *J. Atmos. Sci.*, **37**, 131–147.
- Duynkerke, P. G., 1993: The stability of cloud top with regard to entrainment: Amendment of the theory of cloud-top entrainment instability. *J. Atmos. Sci.*, **50**, 495–502.
- Faloona, I., and Coauthors, 2005: Observations of entrainment in eastern Pacific marine stratocumulus using three conserved scalars. *J. Atmos. Sci.*, **62**, 3268–3285.
- Gerber, H., and Coauthors, 2005: Holes and entrainment in stratocumulus. *J. Atmos. Sci.*, **62**, 443–459.
- Gerber, H., G. Frick, S. P. Malinowski, H. Jonsson, D. Khelif, and S. K. Krueger, 2013: Entrainment rates and microphysics in POST stratocumulus. *J. Geophys. Res. Atmos.*, **118**, 12 094–12 109.
- Glassmeier, F., F. Hoffmann, J. S. Johnson, T. Yamaguchi, K. S. Carslaw, and G. Feingold, 2021: Aerosol-cloud-climate cooling overestimated by ship-track data. *Science*, **371**, 485–489.
- Jen-La Plante, I., and Coauthors, 2016: Physics of Stratocumulus Top (POST): turbulence characteristics. *Atmos. Chem. Phys.*, **16**, 9711–9725.
- Katzwinkel, J., H. Siebert, and R. A. Shaw, 2012: Observation of a self-limiting, shear-induced turbulent inversion layer above marine stratocumulus. *Bound.-Layer Meteor.*, **145**, 131–143, doi:10.1007/s10546-011-9683-4.
- Klein, S. A., and D. L. Hartmann, 1993: The seasonal cycle of low stratiform clouds. *J. Climate*, **6**, 1587–1606.
- Kopec, M. K., S. P. Malinowski, and Z. P. Piotrowski, 2016: Effects of wind shear and radiative cooling on the stratocumulus-topped boundary layer. *Quart. J. Roy. Meteor. Soc.*, **142**, 3222–3233.
- Kuo, H.-C., and W. H. Schubert, 1988: Stability of cloud-topped boundary layers. *Quart. J. Roy. Meteor. Soc.*, **114**, 887–916.
- Lehmann, K., H. Siebert, and R. A. Shaw, 2009: Homogeneous and inhomogeneous mixing in cumulus clouds: Dependence on local turbulence structure. *J. Atmos. Sci.*, **66**, 3641–3659.
- Lewellen, D. C., and W. S. Lewellen, 1998: Large-eddy boundary layer entrainment. *J. Atmos. Sci.*, **55**, 2645–2665.
- Lilly, D. K., 1968: Models of cloud-topped mixed layers under a strong inversion. *Quart. J. Roy. Meteor. Soc.*, **94**, 292–309.
- Lilly, D. K., 2002a,b: Entrainment into mixed layers. Parts I and II. *J. Atmos. Sci.*, **59**, 3340–3352; 3353–3361.
- Lock, A. P., 1998: The parametrization of entrainment in cloudy boundary layers. *Quart. J. Roy. Meteor. Soc.*, **124**, 2729–2753.
- MacVean, M. K., and P. J. Mason, 1990: Cloud-top entrainment instability through small-scale mixing and its parameterization in numerical models. *J. Atmos. Sci.*, **47**, 1012–1030.
- Malinowski, S. P., and Coauthors, 2013: Physics of Stratocumulus Top (POST): turbulent mixing across capping inversion. *Atmos. Chem. Phys.*, **13**, 12171–12186.
- Mellado, J. P., 2010: The evaporatively driven cloud-top mixing layer. *J. Fluid Mech.*, **660**, 5–36.
- Mellado, J. P., 2017: Cloud-top entrainment in stratocumulus clouds. *Annu. Rev. Fluid Mech.*, **49**, 145–169.
- Mellado, J. P., B. Stevens, H. Schmidt, and N. Peters, 2009: Buoyancy reversal in cloud-top mixing layers. *Quart. J. Roy. Meteor. Soc.*, **135**, 963–978.
- Mellado, J. P., B. Stevens, and H. Schmidt, 2014: Wind shear and buoyancy reversal at the top of stratocumulus. *J. Atmos. Sci.*, **71**, 1040–1057, doi:10.1175/JAS-D-13-0189.1.
- Mellado, J. P., C. S. Bretherton, B. Stevens, and M. C. Wyant, 2018: DNS and LES for simulating stratocumulus: Better together. *J. Adv. Model. Earth Syst.*, **10**, 1421–1438.
- Moeng, C.-H., 2000: Entrainment rate, cloud fraction, and liquid water path of PBL stratocumulus clouds. *J. Atmos. Sci.*, **57**, 3627–3643.
- Moeng, C.-H., and Coauthors, 1996: Simulation of a stratocumulus-topped planetary boundary layer: Intercomparison among different numerical codes. *Bull. Amer. Meteor. Soc.*, **77**, 261–278.
- Myers, T. A., and J. R. Norris, 2013: Observational evidence that enhanced subsidence reduces subtropical marine boundary layer cloudiness. *J. Climate*, **26**, 7507–7524.
- Nicholls, S., 1989: The structure of radiatively driven convection in stratocumulus. *Quart. J. Roy. Meteor. Soc.*, **115**, 487–511.
- Nicholls, S., and J. D. Turton, 1986: An observational study of the structure of stratiform cloud sheets: Part II. Entrainment. *Quart. J. Roy. Meteor. Soc.*, **112**, 461–480.
- Randall, D. A., 1980: Conditional instability of the first kind upside-down. *J. Atmos. Sci.*, **37**, 125–130.
- Schneider, T., C. M. Kaul, and K. G. Pressel, 2019: Possible climate transitions from breakup of stratocumulus decks under greenhouse warming. *Nat. Geosci.*, **12**, 163–167.
- Schubert, W. H., J. S. Wakefield, E. J. Steiner, and S. K. Cox, 1979: Marine stratocumulus convection. Part I: Governing equations and horizontally homogeneous solutions. *J. Atmos. Sci.*, **36**, 1286–1307.
- Schulz, B., and J. P. Mellado, 2018: Wind shear effects on radiatively and evaporatively driven stratocumulus tops. *J. Atmos. Sci.*, **75**, 3245–3263.
- Schulz, B., and J. P. Mellado, 2019: Competing effects of droplet sedimentation and wind shear on entrainment in stratocumulus. *J. Adv. Model. Earth Syst.*, **11**, 1830–1846, doi:10.1029/2019MS001617.
- Siems, S. T., C. S. Bretherton, M. B. Baker, S. Shy, and R. E. Breidenthal, 1990: Buoyancy reversal and cloud-top entrainment instability. *Quart. J. Roy. Meteor. Soc.*, **116**, 705–739.
- Stage, S. A., and J. A. Businger, 1981: A model for entrainment into a cloud-topped marine boundary layer. Part I: Model description and application to a cold-air outbreak episode. *J. Atmos. Sci.*, **38**, 2213–2229.
- Stevens, B., 2002: Entrainment in stratocumulus-topped mixed layers. *Quart. J. Roy. Meteor. Soc.*, **128**, 2663–2690.
- Stevens, B., and Coauthors, 2003a: Dynamics and chemistry of marine stratocumulus—DYCOMS-II. *Bull. Amer. Meteor. Soc.*, **84**, 579–593.
- Stevens, B., and Coauthors, 2003b: On entrainment rates in nocturnal marine stratocumulus. *Quart. J. Roy. Meteor. Soc.*, **129**, 3469–3493.
- Stevens, B., and Coauthors, 2005: Evaluation of large-eddy simulations via observations of nocturnal marine stratocumulus. *Mon. Wea. Rev.*, **133**, 1443–1462.
- Turton, J. D., and S. Nicholls, 1987: A study of the diurnal variation of stratocumulus using a multiple mixed layer model. *Quart. J. Roy. Meteor. Soc.*, **113**, 969–1009.
- Uchida, J., C. S. Bretherton, and P. N. Blossey, 2010: The sensitivity of stratocumulus-capped mixed layers to cloud droplet concentration: do LES and mixed-layer models agree? *Atmos. Chem. Phys.*, **10**, 4097–4109.
- van der Dussen, J. J., S. R. de Roode, and A. P. Siebesma, 2014: Factors controlling rapid stratocumulus cloud thinning. *J. Atmos. Sci.*, **71**, 655–664, doi:10.1175/JAS-D-13-0114.1.
- van der Dussen, J. J., S. R. de Roode, S. Dal Gesso, and A. P. Siebesma, 2015: An LES model study of the influence of the free tropospheric thermodynamic conditions on the stratocumulus response to a climate perturbation. *J. Adv. Model. Earth Syst.*, **7**, 670–691.
- van der Dussen, J. J., S. R. de Roode, and A. P. Siebesma, 2016: How large-scale subsidence affects stratocumulus transitions. *Atmos. Chem. Phys.*, **16**, 691–701.
- vanZanten, M. C., P. G. Duynkerke, and J. W. M. Cuijpers, 1999: Entrainment parameterization in convective boundary layers. *J. Atmos. Sci.*, **56**, 813–828.
- Wang, S., J.-C. Golaz, and Q. Wang, 2008: Effect of intense wind shear across the inversion on stratocumulus clouds. *Geophys. Res. Lett.*, **35**.
- Wood, R., 2012: Stratocumulus clouds. *Mon. Wea. Rev.*, **140**, 2373–2423.
- Wood, R., and C. S. Bretherton, 2006: On the relationship between stratiform low cloud cover and lower-tropospheric stability. *J. Climate*, **19**, 6425–6432.
- Wood, R., and Coauthors, 2011: The VAMOS Ocean-Cloud-Atmosphere-Land Study Regional Experiment (VOCALS-REx): goals, platforms, and field operations. *Atmos. Chem. Phys.*, **11**, 627–654.
- Xiao, H., C.-M. Wu, and C. R. Mechoso, 2011: Buoyancy reversal, decoupling and the transition from stratocumulus to shallow cumulus topped marine boundary layers. *Clim. Dyn.*, **37**, 971–984, doi:10.1007/s00382-010-0882-3.
- Yamaguchi, T., and D. A. Randall, 2008: Large-eddy simulation of evaporatively driven entrainment in cloud-topped mixed layers. *J. Atmos. Sci.*, **65**, 1481–1504.
- Zhu, P., and Coauthors, 2005: Intercomparison and interpretation of single-column model simulations of a nocturnal stratocumulus-topped marine boundary layer. *Mon. Wea. Rev.*, **133**, 2741–2758.
