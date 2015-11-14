#############     CALCULATION OF CONCRETE SHRINKAGE     #############
#############       ACCORDING TO RILEM TC-242-MDC       #############
#############       DOI 10.1617/s11527-014-0485-2       #############

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

#####################################################################
###############                  DATA                 ###############
#####################################################################

# Concrete
fcm = 27.6 * MPa 				# mean cylinder compressive strength at 28 days

cem_types = ["R", "RS", "SL"] 	# Cement type: Regular (R), Rapid Hardening (RS), Slow Hardening (SL)
cem_type = "R"
if cem_type not in cem_types:
    sys.exit('Check out cement type definition!')

## Comment on cement types: 
## ASTM Type I general purpose portland cement may be assumed as type R reactivity. ASTM Type II is a
## low heat cement and may be considered as SL. Type III, high early heat cements can be assumed as RS.
## Types IV, V, Ia, IIa, and IIIa should be mapped to by their reactivity in the Model Code classiﬁcation Table.

c = 0.2193			# cement content (mass per 1m3 of concrete, in T)
wc = 0.60 			# (w/c) - water - cement ratio (by weight)
ac = 7.0 			# (a/c) - aggregate - cement ratio (by weight)
ro = 2.350 			# mass density of concrete in T/m3

# Geometry
specimen_types = ['infinite slab','infinite cylinder','infinite square prism','sphere','cube']
specimen = 'infinite slab' # ['infinite slab','infinite cylinder','infinite square prism','sphere','cube']
if specimen not in specimen_types:
    sys.exit('Check out specimen definition!')

V = 1.9e7 * mm**3 	# volume
S = 1e6 * mm**2		# surface
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
sigma = -11.03 * MPa	# applied stress (compressive - negative)

# Aggregate data - NOT NECESSARY, CAN BE LEFT EMPTY
agg_types = ['Diabase', 'Quartzite', 'Limestone', 'Sandstone', 'Granite', 'Quartz Diorite']
agg_type = '' 				# empty agg_type field
#agg_type = 'Limestone' 	# defined agg_type field


#####################################################################
###############          APPLICABILITY CHECK          ###############
#####################################################################

if 0.22 <= wc <= 0.87:
	pass
else:
	print('OUT OF APPLICABILITY RANGE: model not calibrated for such w/c ratio (wc)')
	
if 1.0 <= ac <= 13.2:
	pass
else:
	print('OUT OF APPLICABILITY RANGE: model not calibrated for such a/c ratio (ac)')

if 15 * MPa <= fcm <= 70 * MPa:
	pass
else:
	print('OUT OF APPLICABILITY RANGE: model not calibrated for such concrete compressive strength (fcm)')

if 0.200 <= c <= 1.5:
	pass
else:
	print('OUT OF APPLICABILITY RANGE: model not calibrated for such cement content (c)')

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


#####################################################################
###############            TABLE PARAMETERS           ###############
#####################################################################

# shrinkage parameters for model B4 (Table 1)
if cem_type == "R":
	tau_cem = 0.016
	pta = -0.33
	ptw = -0.06
	ptc = -0.10
	eps_cem = 360e-6
	pea = -0.80
	pew = 1.10
	pec = 0.11

elif cem_type == "RS":
	tau_cem = 0.080
	pta = -0.33
	ptw = -2.40
	ptc = -2.70
	eps_cem = 860e-6
	pea = -0.80
	pew = -0.27
	pec = 0.11

elif cem_type == "SL":
	tau_cem = 0.010
	pta = -0.33
	ptw = 3.55
	ptc = 3.80
	eps_cem = 410e-6
	pea = -0.80
	pew = 1.00
	pec = 0.11

else:
	print('cem_type error')


# autogenous shrinkage parameters for model B4 (Table 2)
if cem_type == "R":
	tau_au_cem = 1.00
	r_tw = 3.00
	r_t = -4.50
	r_alfa = 1.00
	eps_au_cem = 210e-6
	r_ea = -0.75
	r_ew = -3.50

elif cem_type == "RS":
	tau_au_cem = 41.00 # ???
	r_tw = 3.00
	r_t = -4.50
	r_alfa = 1.40
	eps_au_cem = -84e-6
	r_ea = -0.75
	r_ew = -3.50

elif cem_type == "SL":
	tau_au_cem = 1.00
	r_tw = 3.00
	r_t = -4.50
	r_alfa = 1.00
	eps_au_cem = 0e-6
	r_ea = -0.75
	r_ew = -3.50

else:
	print('cem_type error')


# creep parameters for model B4 (Table 3 Part 1)
if cem_type == "R":
	p1 = 0.70
	p2 = 58.6e-3
	p3 = 39.3e-3
	p4 = 3.4e-3
	p5 = 777e-6
	p5H = 8.0

elif cem_type == "RS":
	p1 = 0.60
	p2 = 17.4e-3
	p3 = 39.3e-3
	p4 = 3.4e-3
	p5 = 94.6e-6
	p5H = 1.0

elif cem_type == "SL":
	p1 = 0.80
	p2 = 40.5e-3
	p3 = 39.3e-3
	p4 = 3.4e-3
	p5 = 496e-6
	p5H = 8.0 # comment in the recommendations: "lacing data, assumed"

else:
	print('cem_type error')

# creep parameters for model B4 (Table 3 part 2)
p2w = 3.00
p3a = -1.10
p3w = 0.40
p4a = -0.90
p4w = 2.45
p5e = -0.85
p5a = -1.00
p5w = 0.78


# Aggregate dependent parameter scaling factors for shrinkage (Table 6)
if agg_type == 'Diabase':
	k_ta = 0.06
	k_ea = 0.76
elif agg_type == 'Quartzite':
	k_ta = 0.59
	k_ea = 0.71
elif agg_type == 'Limestone':
	k_ta = 1.80
	k_ea = 0.95
elif agg_type == 'Sandstone':
	k_ta = 2.30
	k_ea = 1.60
elif agg_type == 'Granite':
	k_ta = 4.00
	k_ea = 1.05
elif agg_type == 'Quartz Diorite':
	k_ta = 15.0
	k_ea = 2.20
elif agg_type == '':
	k_ta = 1.0
	k_ea = 1.0
else:
	print('error agg_type')


# The specimen geometry shape parameter ks (Eq. 23)
k_s_dict= {'infinite slab': 1.0, 'infinite cylinder': 1.15, 'infinite square prism': 1.25, 'sphere': 1.30, 'cube':1.55}
k_s = k_s_dict[specimen]


#####################################################################
###############              CALCULATIONS             ###############
###############                MODEL B4               ###############
#####################################################################

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
tau_0 = tau_cem * (ac / 6) ** pta * (wc / 0.38) ** ptw * ((6.5 * c) / ro) ** ptc # Eq. 22
D = 2*V/S # effective thickness (Eq. 21)
tau_sh = tau_0 * k_ta * (k_s * D / mm)**2 # Eq.21
#print('tau_sh =',tau_sh,' tau_0 =',tau_0)

## Final drying shrinkage
eps_0 = eps_cem * (ac / 6) ** pea * (wc / 0.38) ** pew * ((6.5 * c) / ro) ** pec # Eq. 16

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

alfa = r_alfa * (wc / 0.38) # Eq. 24

# Autogenous shrinkage halftime
tau_au = tau_au_cem * (wc / 0.38) ** r_tw # Eq. 26

## Final autogenous shrinkage
eps_au_inf = -eps_au_cem * (ac / 6) ** r_ea	* (wc / 0.38) ** r_ew # Eq. 25

## Autogenous shrinkage
eps_au = eps_au_inf * (1 + (tau_au / (tt - t0t)) ** alfa ) ** r_t # Eq. 24
print('Autogenous shrinkage (eps_au) =',"%.8f" % eps_au)


###########################################
# Average creep calculations
###########################################

# Model parameters 
q1 = p1 / E_28 # instantaneous compliance, Eq. 28
q2 = (p2 / GPa) * (wc / 0.38)**p2w # aging viscoelastic creep, Eq. 40
q3 = p3 * q2 * (ac / 6)**p3a * (wc / 0.38)**p3w # non-aging viscoelastic creep Eq. 41
q4 = (p4 / GPa) * (ac / 6)**p4a * (wc / 0.38)**p4w # flow, Eq. 42
q5 = (p5 / GPa) * (ac / 6)**p5a * (wc / 0.38)**p5w * (abs(kh * eps_sh_inf))**p5e # drying creep Eq. 43

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

eps_tot = (J * sigma * 10**(-6)) + eps_sh + eps_au + T_infl  # Eq. 12
print('Total strain (eps_tot) =', "%.8f" % eps_tot)


