#############     CALCULATION OF CONCRETE SHRINKAGE      #############
#############       ACCORDING TO RILEM TC-242-MDC        #############
#############       DOI 10.1617/s11527-014-0485-2        #############

### Model 4s - applicable without exact information about concrete mixture ###

__author__ = 'Katarzyna Zdanowicz'
__copyright__ = 'Copyright 2015, Katarzyna Zdanowicz'
__license__ = 'GPL'

import math
import sys

# UNITS
m = 1
cm = m/100
mm = m/1000
m2 = m*m
cm2 = cm*cm
mm2 = mm*mm

kg = 1000
N = 1
kN = N*1e3
kNm = N*m * 1e3		# also kN/m
Pa = N/m/m
kPa = Pa*1e3
MPa = Pa*1e6
GPa = Pa*1e9

###############################################################
###############               DATA              ###############
###############################################################

# Concrete
fcm = 27.6 * MPa 				# mean cylinder compressive strength at 28 days

cem_types = ["R", "RS", "SL"] 	# Cement type: Regular (R), Rapid Hardening (RS), Slow Hardening (SL)
cem_type = "R"
if cem_type not in cem_types:
    sys.exit('Check out cement type definition!')

## Comment on cement types: 
# ASTM Type I general purpose portland cement may be assumed as type R reactivity. ASTM Type II is a
# low heat cement and may be considered as SL. Type III, high early heat cements can be assumed as RS. 
# Types IV, V, Ia, IIa, and IIIa should be mapped to by their reactivity in the Model Code classiﬁcation Table.

# Geometry
specimen_types = ['infinite slab','infinite cylinder','infinite square prism','sphere','cube']
specimen = 'infinite slab' # ['infinite slab','infinite cylinder','infinite square prism','sphere','cube']
if specimen not in specimen_types:
    sys.exit('Check out specimen definition!')
V = 19.05 * mm**3 	# volume
S = 1 * mm**2 		# surface
UR = 4000 			# in absence of data, one can use U/R = 4000 K (P. 1.3)

# Environment
h = 0.50 			# relative humidity

t0 = 28 			# age when drying begins (in days)
tp = 28 			# age at loading (in days)
t = 112 			# age of concrete (in days)
T_cur = 20 			# curing temperature, between 20 and 30 Celsius degree
T_avg = 20 			# average environmental temperature before load
T = 20 				# environmental temperature in calculated moment

alfa_t = 1e-5 		# thermal coefficient of expansion
delta_T = T - T_avg	# temperature difference from the reference temperature at time t

# Loads
sigma = -11.03 * MPa	# applied compressive stress (creep)

###############################################################
###############       APPLICABILITY CHECK       ###############
###############################################################

if 15*MPa <= fcm <= 70 * MPa:
	pass
else:
	print('OUT OF APPLICABILITY RANGE: model not calibrated for such concrete compressive strength (fcm)')

if -25 <= T_avg <= 75:
	pass
else:
	print('OUT OF APPLICABILITY RANGE: model not calibrated for such average temperature (T_avg)')

if 20 <= T_cur <= 30:
	pass
else:
	print('OUT OF APPLICABILITY RANGE: model not calibrated for such curing temperature (T_cur)')

if 12e-3 <= V/S <= 120e-3:
	pass
else:
	print('OUT OF APPLICABILITY RANGE: model not calibrated for such volume/surface ratio (V/S)')


###############################################################
###############     TABELARISCHE PARAMETERS     ###############
###############################################################

# shrinkage parameters (Table 8)
if cem_type == "R":
	tau_s_cem = 0.027
	s_tf = 0.21
	eps_scem = 590e-6
	s_ef = -0.51

elif cem_type == "RS":
	tau_s_cem = 0.027
	s_tf = 1.55
	eps_scem = 830e-6
	s_ef = -0.84

elif cem_type == "SL":
	tau_s_cem = 0.032
	s_tf = -1.84
	eps_scem = 640e-6
	s_ef = -0.69

else:
	print('cem_type error')


# Creep parameters for model B4s (Table 9)
if cem_type == "R":
	s2 = 14.2e-3
	s3 = 0.976
	s4 = 4e-3
	s5 = 1.54e-3
	s2f = -1.58
	s3f = -1.61
	s4f = -1.16
	s5f = -0.45
	p5H = 8.0
	p1 = 0.70

elif cem_type == "RS":
	s2 = 29.9e-3
	s3 = 0.976
	s4 = 4e-3
	s5 = 41.8e-6
	s2f = -1.58
	s3f = -1.61
	s4f = -1.16
	s5f = -0.45
	p5H = 1.0
	p1 = 0.60

elif cem_type == "SL":
	s2 = 11.2e-3
	s3 = 0.976
	s4 = 4e-3
	s5 = 150e-6
	s2f = -1.58
	s3f = -1.61
	s4f = -1.16
	s5f = -0.45
	p5H = 8.0
	p1 = 0.80

else:
	print('cem_type error')

p5c = -0.85 # (Table 3)


# Aggregate dependent parameter scaling factors for shrinkage (Table 6)
k_ta = 1.0
k_ea = 1.0

# The specimen geometry shape parameter ks (Eq. 23)
k_s_dict= {'infinite slab': 1.0, 'infinite cylinder': 1.15, 'infinite square prism': 1.25, 'sphere': 1.30, 'cube':1.55}
k_s = k_s_dict[specimen]

###############################################################
###############           CALCULATIONS          ###############
###############            MODEL B4 s           ###############
###############################################################

# Elasticity modulus
E_28 = 4734 * math.sqrt(fcm/MPa) # ACI Ec_28

def E(t):
	E_t = E_28 * math.sqrt(t/(4 + (6/7) * t)) # Eq. 19
	return E_t

# Humidity dependence, Eq. 20
if h <= 0.98:
	kh = 1 - h**3
elif 0.98 < h <= 1:
	kh = 12.94 * (1 - h) - 0.2
else:
	print('error h')
# print('kh =',kh)

# Equivalent times at different temperatures
beta_th = math.exp( (UR) * (1/293 - 1/(T_cur+273)) ) # URh = UR
beta_ts = math.exp( (UR) * (1/293 - 1/(T_avg+273)) ) # URs = UR
beta_tc = math.exp( (UR) * (1/293 - 1/(T_avg+273)) ) # URc = UR

# Temperature corrected ages: (Eq. 8 - 10)
# equivalent times for shrinkage:
tt = (t - t0) * beta_ts
t0t = t0 * beta_th
# equivalent times for creep:
tpd = t0 * beta_th + (tp - t0) * beta_ts
td = tpd + (t - tp) * beta_tc

###########################################
# Drying shrinkage calculations
###########################################

## Drying shrinkage halftime
tau_0 = tau_s_cem * (fcm/(40*MPa))**s_tf # drying shrinkage halftime Eq.45
D = 2*V/S # effective thickness (Eq. 21)
tau_sh = tau_0 * k_ta * (k_s * D / mm)**2 # Eq.21
#print('tau_sh =',tau_sh,' tau_0 =',tau_0)

## Final drying shrinkage
eps_0 = eps_scem * (fcm/(40*MPa))**s_ef # shrinkage Eq. 44

## Shrinkage correction for the effect of ageing on elastic stiffness
E1 = E(7 * beta_th + 600 * beta_ts)
E2 = E(t0t + tau_sh * beta_ts)
eps_sh_inf = -eps_0 * k_ea * (E1 / E2) # Eq. 17
#print('eps_0 =',eps_0,'eps_sh_inf =',eps_sh_inf)

## Time curve
St = math.tanh(math.sqrt(tt / tau_sh)) # Eq. 15

## Drying shrinkage
eps_sh = eps_sh_inf * kh * St # Eq. 14
print('Drying shrinkage (eps_sh) =',"%.8f" % eps_sh)

###########################################
# Autogenous shrinkage calculations
###########################################

#autogenous shrinkage parameters (Table 7)
tau_au_cem = 2.26
r_tf = 0.27
eps_au_cem = 78.2e-6
r_ef = 1.03
alfa_s = 1.73
r_t = -1.73

# Autogenous shrinkage halftime
tau_au = tau_au_cem * (fcm/(40*MPa))**r_tf # Eq. 48	

## Final autogenous shrinkage
eps_au_inf = -eps_au_cem * (fcm/(40*MPa))**r_ef # final autogenous shrinkage Eq. 47

## Autogenous shrinkage
eps_au = eps_au_inf * (1 + (tau_au / (t + t0))**alfa_s)**r_t # autogenous shrinkage in time # Eq. 46
print('Autogenous shrinkage (eps_au) =',"%.8f" % eps_au)

###########################################
# Average creep calculations
###########################################

# Model parameters 
q1 = p1 / E_28 # instantaneous compliance, Eq. 28
q2 = (s2 / GPa) * (fcm/(40*MPa))**s2f # aging viscoelastic creep, Eq. 40
q3 = s3 * q2 * (fcm/(40*MPa))**s3f # non-aging viscoelastic creep Eq. 41
q4 = (s4 / GPa) * (fcm/(40*MPa))**s4f # flow, Eq. 42    -->  !!!!!!!!!!!!! In the example s4 = 6.9e-3 - why???
q5 = (s5 / GPa) * (fcm/(40*MPa))**s5f * (abs(kh * eps_sh_inf))**p5c # drying creep Eq. 43

# Basis creep compliance, Eq. 31 - 35
Qf = (0.086 * tpd ** (2/9) + 1.21 * tpd ** (4/9)) ** (-1)
Z = (tpd ** (-0.5)) * math.log(1 + ((td - tpd) ** (0.1)))
r_tp = 1.7 * tpd ** 0.12 + 8
Q = Qf * (1 + (Qf / Z)**r_tp)**(-1/r_tp) # Eq. 32

C0 = ((q2 * Q) + (q3 * math.log(1 + ((td - tpd) ** (0.1)))) + (q4 * math.log(td/tpd)) ) * 10**6

# Drying creep compliance, Eq. 36 - 38
t0pd = max(tpd,t0t)
if td >= t0pd:
	Ht = 1 - (1 - h) * math.tanh(math.sqrt((td - t0t) / tau_sh))
	Hct = 1 - (1 - h) * math.tanh(math.sqrt((t0pd - t0t) / tau_sh))
	Cd = q5 * max((math.exp(-p5H * Ht) - math.exp(-p5H * Hct)), 0) ** 0.5 * 10**6
elif td < t0d:
	Cd = 0
else:
	print('error Cd')

# Total creep compliance function
Rt =  math.exp( (UR) * (1/293 - 1/(T_avg+273)) ) # Eq. 39
J = q1 + Rt * C0 + Cd # Eq. 27
print('Average creep (J*sigma) =', "%.8f" % (J * sigma * 10**(-6)))


###########################################
# Temperature influence calculations
###########################################

T_infl = alfa_t * delta_T
print('Temperature influence (T_infl) =',"%.8f" % T_infl)


###########################################
# Total strain calculations
###########################################

eps_tot = (J * sigma * 10**(-6)) + eps_sh + eps_au + alfa_t * delta_T # Eq. 12
print('Total strain (eps_tot) =', "%.8f" % eps_tot)
