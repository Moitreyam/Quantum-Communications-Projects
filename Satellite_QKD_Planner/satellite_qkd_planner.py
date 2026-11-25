"""
Satellite QKD Mission Planning Tool
====================================
Interactive Streamlit dashboard for simulating a decoy-state BB84
satellite-to-ground free-space quantum key distribution link.

Physics: Gaussian beam diffraction, Beer-Lambert atmospheric absorption,
         detector dark counts, Ma/Lo decoy-state estimation, GLLP secure
         key rate, LEO orbital geometry.

Author : Moitreya M.
Stack  : Python 3.13 · NumPy · Matplotlib · Streamlit
"""

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ──────────────────────────────────────────────
# Layer 1 — Channel transmittance
# ──────────────────────────────────────────────

def geo_eff(w0, L, wavelength, a):
    """Geometric/diffraction collection efficiency (Gaussian beam)."""
    z_r = w0**2 * np.pi / wavelength
    w_l = w0 * np.sqrt(1 + (L / z_r)**2)
    eta_geo = 1 - np.exp(-2 * a**2 / w_l**2)
    return eta_geo


def atm_transm(T_zenith, elevation_rad):
    """Atmospheric transmittance via Beer-Lambert for a slant path."""
    sin_el = np.sin(elevation_rad)
    if np.isscalar(sin_el):
        if sin_el <= 0:
            return 0.0
    else:
        sin_el = np.where(sin_el <= 0, 1e-10, sin_el)
    return T_zenith ** (1 / sin_el)


def tot_transm(eta_geo, T_atm, eta_optics):
    """Total channel transmittance."""
    return eta_geo * T_atm * eta_optics


# ──────────────────────────────────────────────
# Layer 2 — Detector model & QBER
# ──────────────────────────────────────────────

def qber_calc(eta_total, eta_det, Y0, e_d):
    """QBER from signal detections + dark counts."""
    Y1 = Y0 + eta_total * eta_det
    if Y1 == 0:
        return 0.5
    qber = (e_d * eta_total * eta_det + 0.5 * Y0) / Y1
    return qber


def binary_entropy(x):
    """Binary (Shannon) entropy H₂(x)."""
    if x <= 0 or x >= 1:
        return 0.0
    return -x * np.log2(x) - (1 - x) * np.log2(1 - x)


# ──────────────────────────────────────────────
# Layer 3 — Decoy-state secure key rate
# ──────────────────────────────────────────────

def gain_qber(mu, eta, Y0, e_d):
    """Overall gain Q_μ and QBER E_μ for weak coherent pulses."""
    Q_mu = Y0 + 1 - np.exp(-eta * mu)
    if Q_mu == 0:
        return 0.0, 0.5
    E_mu = (e_d * (1 - np.exp(-eta * mu)) + 0.5 * Y0) / Q_mu
    return Q_mu, E_mu


def decoy_estimation(mu, nu, eta, Y0, e_d):
    """Ma/Lo decoy-state lower bound on Q₁ and upper bound on e₁."""
    Q_mu, E_mu = gain_qber(mu, eta, Y0, e_d)
    Q_nu, E_nu = gain_qber(nu, eta, Y0, e_d)

    denom = mu * nu - nu**2
    if denom == 0:
        return 0.0, 0.5, Q_mu, E_mu

    Q1 = (mu / denom) * (
        Q_nu * np.exp(nu)
        - Q_mu * np.exp(mu) * (nu**2 / mu**2)
        - Y0 * ((mu**2 - nu**2) / mu**2)
    )
    if Q1 <= 0:
        return 0.0, 0.5, Q_mu, E_mu

    e1 = (E_nu * Q_nu * np.exp(nu) - 0.5 * Y0) / (Q1 * nu)
    e1 = min(max(e1, 0.0), 0.5)

    return Q1, e1, Q_mu, E_mu


def secure_key_rate(Q1, e1, Q_mu, E_mu, f=1.16):
    """GLLP secure key rate R (bits / pulse)."""
    q = 0.5  # BB84 sifting factor
    R = q * (Q1 * (1 - binary_entropy(e1)) - Q_mu * f * binary_entropy(E_mu))
    return max(R, 0.0)


# ──────────────────────────────────────────────
# Layer 4 — Orbital geometry & pass integration
# ──────────────────────────────────────────────

def slant_range_calc(elevation_deg, h_km):
    """Slant range (m) from ground station to satellite."""
    R_earth = 6371  # km
    theta = np.radians(elevation_deg)
    L = -R_earth * np.sin(theta) + np.sqrt(
        (R_earth * np.sin(theta))**2 + 2 * R_earth * h_km + h_km**2
    )
    return L * 1000  # → metres


def key_per_pass(max_elev_deg, h_km, pulse_rate,
                 w0, wavelength, a, T_zenith,
                 eta_optics, eta_det, Y0, e_d,
                 mu, nu, f):
    """Integrate secure key bits over one symmetric LEO pass."""
    min_elev = 10  # degrees — below this, atmosphere kills the link
    if max_elev_deg <= min_elev:
        return 0.0

    elevations_up   = np.linspace(min_elev, max_elev_deg, 100)
    elevations_down = np.linspace(max_elev_deg, min_elev, 100)
    elevations = np.concatenate([elevations_up, elevations_down])

    total_time = 300  # seconds (typical LEO pass duration)
    dt = total_time / len(elevations)

    total_bits = 0.0
    for elev in elevations:
        L = slant_range_calc(elev, h_km)
        eta_g  = geo_eff(w0, L, wavelength, a)
        T_atm  = atm_transm(T_zenith, np.radians(elev))
        eta_total = tot_transm(eta_g, T_atm, eta_optics)
        Q1, e1, Q_mu, E_mu = decoy_estimation(mu, nu, eta_total, Y0, e_d)
        rate = secure_key_rate(Q1, e1, Q_mu, E_mu, f)
        total_bits += rate * pulse_rate * dt

    return total_bits


# ══════════════════════════════════════════════
#  Streamlit UI
# ══════════════════════════════════════════════

st.set_page_config(page_title="Satellite QKD Mission Planner",
                   page_icon="🛰️", layout="wide")

st.title("🛰️ Satellite QKD Mission Planning Tool")
st.markdown(
    "Interactive simulator for a **decoy-state BB84** satellite-to-ground "
    "free-space QKD link.  Adjust parameters in the sidebar and watch the "
    "link budget, QBER, secure key rate and mission yield update in real time."
)

# ── Sidebar parameters ──────────────────────
st.sidebar.header("⚙️ System Parameters")

st.sidebar.subheader("Orbit & Geometry")
h_km       = st.sidebar.slider("Orbit altitude (km)", 200, 2000, 500, 50)
elev_deg   = st.sidebar.slider("Elevation angle (°)", 10, 90, 30, 5)

st.sidebar.subheader("Transmitter Optics")
w0         = st.sidebar.slider("Beam waist w₀ (cm)", 1, 20, 5, 1) / 100  # → m
wavelength = st.sidebar.selectbox("Wavelength (nm)", [785, 850, 1550], index=1) * 1e-9

st.sidebar.subheader("Receiver")
a          = st.sidebar.slider("Telescope radius (cm)", 10, 100, 50, 5) / 100
T_zenith   = st.sidebar.slider("Zenith transmittance", 0.5, 1.0, 0.8, 0.05)
eta_optics = st.sidebar.slider("Receiver optics efficiency", 0.1, 1.0, 0.5, 0.05)

st.sidebar.subheader("Detector")
eta_det    = st.sidebar.slider("Detector efficiency", 0.05, 0.50, 0.20, 0.05)
Y0_exp     = st.sidebar.slider("Dark count rate (10^x)", -8, -4, -6, 1)
Y0         = 10.0 ** Y0_exp
e_d        = st.sidebar.slider("Misalignment error e_d", 0.005, 0.05, 0.02, 0.005)

st.sidebar.subheader("Protocol")
mu         = st.sidebar.slider("Signal intensity μ", 0.1, 1.0, 0.5, 0.05)
nu         = st.sidebar.slider("Decoy intensity ν", 0.01, 0.3, 0.1, 0.01)
f_ec       = st.sidebar.slider("Error correction factor f", 1.0, 1.5, 1.16, 0.01)

st.sidebar.subheader("System")
pulse_rate = st.sidebar.selectbox(
    "Pulse rate (MHz)", [10, 50, 100, 200, 500, 1000], index=2
) * 1e6

# ── Compute link budget at current elevation ──
L_slant    = slant_range_calc(elev_deg, h_km)
eta_g      = geo_eff(w0, L_slant, wavelength, a)
T_atm_val  = atm_transm(T_zenith, np.radians(elev_deg))
eta_total  = tot_transm(eta_g, T_atm_val, eta_optics)
loss_dB    = -10 * np.log10(eta_total) if eta_total > 0 else 999

qber_val   = qber_calc(eta_total, eta_det, Y0, e_d)
Q1, e1, Q_mu, E_mu = decoy_estimation(mu, nu, eta_total, Y0, e_d)
R_val      = secure_key_rate(Q1, e1, Q_mu, E_mu, f_ec)

# ── Link budget summary ─────────────────────
st.header("📊 Link Budget at Current Operating Point")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Slant Range", f"{L_slant/1000:.1f} km")
c2.metric("Total Loss", f"{loss_dB:.1f} dB")
c3.metric("QBER", f"{qber_val*100:.2f} %")
c4.metric("Key Rate", f"{R_val:.2e} bits/pulse")

# Loss breakdown
st.subheader("Loss Breakdown")
geo_loss_dB  = -10*np.log10(eta_g) if eta_g > 0 else 999
atm_loss_dB  = -10*np.log10(T_atm_val) if T_atm_val > 0 else 999
opt_loss_dB  = -10*np.log10(eta_optics) if eta_optics > 0 else 999

b1, b2, b3 = st.columns(3)
b1.metric("Geometric Loss", f"{geo_loss_dB:.1f} dB")
b2.metric("Atmospheric Loss", f"{atm_loss_dB:.1f} dB")
b3.metric("Optics Loss", f"{opt_loss_dB:.1f} dB")

# ══════════════════════════════════════════════
#  Money Plots
# ══════════════════════════════════════════════

st.header("📈 Money Plots")

eta_sweep = np.logspace(-1, -7, 300)
loss_sweep = -10 * np.log10(eta_sweep)

qber_curve = []
rate_curve = []
for eta in eta_sweep:
    qber_curve.append(qber_calc(eta, eta_det, Y0, e_d))
    Q1_s, e1_s, Qmu_s, Emu_s = decoy_estimation(mu, nu, eta, Y0, e_d)
    rate_curve.append(secure_key_rate(Q1_s, e1_s, Qmu_s, Emu_s, f_ec))

qber_curve = np.array(qber_curve)
rate_curve = np.array(rate_curve)

# ── Plot 1: QBER vs Channel Loss ─────────────
fig1, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.plot(loss_sweep, qber_curve * 100, 'b-', linewidth=2)
ax1.axhline(y=11, color='r', linestyle='--', linewidth=1, label='BB84 threshold (11%)')
ax1.axvline(x=loss_dB, color='g', linestyle=':', linewidth=1.5, label=f'Operating point ({loss_dB:.1f} dB)')
ax1.set_xlabel('Channel Loss (dB)')
ax1.set_ylabel('QBER (%)')
ax1.set_title('Money Plot 1 — QBER vs Channel Loss')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 70)
ax1.set_ylim(0, 55)
st.pyplot(fig1)

# ── Plot 2: Secure Key Rate vs Channel Loss ──
fig2, ax2 = plt.subplots(figsize=(8, 4.5))
rate_plot = np.where(rate_curve > 0, rate_curve, np.nan)
ax2.semilogy(loss_sweep, rate_plot, 'b-', linewidth=2)
ax2.axvline(x=loss_dB, color='g', linestyle=':', linewidth=1.5, label=f'Operating point ({loss_dB:.1f} dB)')
ax2.set_xlabel('Channel Loss (dB)')
ax2.set_ylabel('Secure Key Rate (bits/pulse)')
ax2.set_title('Money Plot 2 — Decoy-State BB84 Key Rate vs Channel Loss')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 70)
st.pyplot(fig2)

# ── Plot 3: Key per Pass vs Max Elevation ─────
elev_range = np.arange(15, 91, 5)
bits_per_pass = []
for el in elev_range:
    bits = key_per_pass(el, h_km, pulse_rate,
                        w0, wavelength, a, T_zenith,
                        eta_optics, eta_det, Y0, e_d,
                        mu, nu, f_ec)
    bits_per_pass.append(bits)

bits_per_pass = np.array(bits_per_pass)

fig3, ax3 = plt.subplots(figsize=(8, 4.5))
ax3.plot(elev_range, bits_per_pass / 1e6, 'b-o', linewidth=2, markersize=4)
ax3.axvline(x=elev_deg, color='g', linestyle=':', linewidth=1.5, label=f'Current pass ({elev_deg}°)')
ax3.set_xlabel('Maximum Elevation Angle (°)')
ax3.set_ylabel('Secure Key Bits per Pass (Mbits)')
ax3.set_title('Money Plot 3 — Secret Key Generated per LEO Pass')
ax3.legend()
ax3.grid(True, alpha=0.3)
st.pyplot(fig3)

# ══════════════════════════════════════════════
#  Mission Summary
# ══════════════════════════════════════════════

st.header("🎯 Mission Summary")

current_pass_bits = key_per_pass(elev_deg, h_km, pulse_rate,
                                 w0, wavelength, a, T_zenith,
                                 eta_optics, eta_det, Y0, e_d,
                                 mu, nu, f_ec)

passes_per_day = 4  # typical LEO visibility from one ground station
daily_key = current_pass_bits * passes_per_day
aes_keys  = daily_key / 256 if daily_key > 0 else 0
voice_hrs = daily_key / (64000 * 3600) if daily_key > 0 else 0  # 64 kbps voice

m1, m2, m3, m4 = st.columns(4)
m1.metric("Key per Pass", f"{current_pass_bits/1e6:.2f} Mbits")
m2.metric("Daily Key (4 passes)", f"{daily_key/1e6:.2f} Mbits")
m3.metric("AES-256 Keys / Day", f"{aes_keys:,.0f}")
m4.metric("Voice Encryption (hrs)", f"{voice_hrs:.1f}")

if R_val > 0:
    st.success("✅ System can generate secure key at this operating point.")
else:
    st.error("❌ No secure key at this loss level — channel too lossy.")

# ── Footer ───────────────────────────────────
st.markdown("---")
st.markdown(
    "*Physics: Gaussian beam model · Beer-Lambert atmosphere · "
    "Ma/Lo decoy-state estimation · GLLP secure key rate · "
    "LEO orbital geometry*"
)
st.markdown(
    "Built as part of the **Quantum Communications Projects** portfolio.  "
    "[GitHub](https://github.com/Moitreyam/Quantum-Communications-Projects)"
)
