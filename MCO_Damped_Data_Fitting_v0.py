#
# MCO_Damped_Data_Fitting_v0.py
#
# This file will generate a plot of univariate data
# with a fit to a function that 
# the user defines.
#
# Here we assume a linearly damped harmonic oscillator model 
# will fit the data.
#
# Written by:
#
# Ernest R. Behringer
# Department of Physics and Astronomy
# Eastern Michigan University
# Ypsilanti, MI 48197
# (734) 487-8799
# ebehringe@emich.edu
#
# 20190709 by ERB Using curve_fit from scipy.optimize.  Beware filename path!
#

# import the commands needed to make the plot and fit the data
from pylab import figure,xlim,xlabel,ylim,ylabel,grid,show,plot,legend,title
from numpy import exp,cos,pi,linspace,loadtxt
from scipy.optimize import curve_fit

# Read the data to be fit. Using an absolute path name that you'll have to change. 
filename = 'damped_undriven.dat'
t_meas,phi_meas = loadtxt(filename, dtype=float, delimiter='\t', skiprows=2, unpack=True)

# Define the fit function: A*exp(-beta*t)*cos(omegad*t - phi0)
#
def fit_func(t, A, phi0, beta, omegad):
    return A*exp(-beta*t)*cos(omegad*t - phi0)

# Initial values of A, phi0, beta, and omegad
A_i = 0.5 # in rad
phi0_i = 0.0 # in rad
beta_i = 0.2 # in Hz
omegad_i = 2.0*pi/0.55 # in rad/s
# Assign the initial values to be the values
A = A_i
phi0 = phi0_i
beta = beta_i
omegad = omegad_i

print(A, phi0, beta, omegad)

# Run curve_fit to optimize the fit parameters.
# The first argument is the name of the fit function.
# The second argument is the name of the array of independent data values.
# The third argument is the name of the array of dependent data values.
curve_fit_opt, curve_fit_cov = curve_fit(fit_func, t_meas, phi_meas)

# Assign the (optimized) fit parameters
A_opt = curve_fit_opt[0]
phi0_opt = curve_fit_opt[1]
beta_opt = curve_fit_opt[2]
omegad_opt = curve_fit_opt[3]

print(A_opt, phi0_opt, beta_opt, omegad_opt)
print(curve_fit_cov[0][0],curve_fit_cov[1][1],curve_fit_cov[2][2],curve_fit_cov[3][3])

# Generate the arrays needed to make a smooth plot of the fit function
t_fit = linspace(min(t_meas),max(t_meas),10001)
phi_guess = fit_func(t_fit, A_i, phi0_i, beta_i,omegad_i)
phi_fit = fit_func(t_fit, A_opt, phi0_opt, beta_opt, omegad_opt)

# Start a figure.  This command creates a separate window for the plot.
figure('Angular Position versus Time')

# Define the limits of the horizontal axis
xlim(min(t_meas),max(t_meas))

# Label the horizontal axis, with units
xlabel("$t$ [s]", size = 16)

# Define the limits of the vertical axis
ylim(min(phi_meas),max(phi_meas))

# Label the vertical axis, with units
ylabel("Angular Position $\\phi$ [rad]", size = 16)

# Make a grid on the plot
grid(True)

# Generate the plot.  The plot symbols will be green (g) circles (o).
#plot(theta_points,irradiance_points,"go",label="Noisy")
plot(t_meas,phi_meas,"k.",label="Data")
plot(t_fit,phi_guess,"r--",label="Guess")
plot(t_fit,phi_fit,"b",label="Fit")
legend(loc=3)

# Make title
title('Optimized values: $A = $%.2f rad, $\\phi_0 = $%.2f rad, $\\beta = $%.2f s$^{-1}$, $\\omega_d = $%.2f rad/s'%(A_opt,phi0_opt,beta_opt,omegad_opt))

# Show the plot
show()