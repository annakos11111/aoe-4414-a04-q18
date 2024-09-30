# eci_to_ecef.py
#
# Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km
# Finds ECEF vector from ECI vector
# Parameters:
# year, month, day, hour, minute, second : time 
# eci_x_km, eci_y_km, eci_z_km : ECI position
# Output:
# ecef_x_km, ecef_y_km, ecef_z_km

# Written by Anna Kosnic
#
# import Python modules
import sys # argv
import math as m

# "constants"
R_E_KM = 6378.1363
E_E = 0.081819221456
w = 7.292115e-5

# helper functions
def calc_denom(ecc, lat):
    return m.sqrt(1-ecc**2 *(m.sin(lat))**2)

# initialize script arguments
year        = 0
month       = 0
day         = 0
hour        = 0
minute      = 0
second      = float('nan')
eci_x_km    = float('nan')
eci_y_km    = float('nan')
eci_z_km    = float('nan')


# parse script arguments
if len(sys.argv)==10:
    year     = int(sys.argv[1])
    month    = int(sys.argv[2])
    day      = int(sys.argv[3])
    hour     = int(sys.argv[4])
    minute   = int(sys.argv[5])
    second   = float(sys.argv[6])
    eci_x_km = float(sys.argv[7])
    eci_y_km = float(sys.argv[8])
    eci_z_km = float(sys.argv[9])
else:
    print(\
        'Usage: '\
        'python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km'\
            )
    exit()


# script below
# finding fractional julian date
jd = day - 32075 + \
    int(1461*(year + 4800 + int((month - 14)/12))/4) + \
    int(367*(month - 2 - (int((month - 14)/12)*12))/12) - \
    int(3*int((year + 4900 + int((month - 14)/12))/100)/4)

jd_mid = jd - 0.5
d_frac = (second + 60*(minute + 60*hour))/86400
jd_frac = jd_mid + d_frac

# finding GMST angle in radians
tut1 = (jd_frac - 2451545.0)/36525
gmst_sec = 67310.54841 + (876600*60*60 + 8640184.812866)*tut1 + 0.093104*tut1**2 + -6.2e-6*tut1**3
gmst_rad = m.fmod(gmst_sec%86400 * w + 2*m.pi,2*m.pi)

# rotating ECI vector
ecef = [m.cos(-gmst_rad)*eci_x_km - m.sin(-gmst_rad)*eci_y_km, m.sin(-gmst_rad)*eci_x_km + m.cos(-gmst_rad)*eci_y_km, eci_z_km]
ecef_x_km = ecef[0]
ecef_y_km = ecef[1]
ecef_z_km = ecef[2]

print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)