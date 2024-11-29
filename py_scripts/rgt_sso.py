import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

'''
    Parameters:
    - mu_E (float): Earth's standard gravitational parameter in m^3/s^2 (default: 3.986e14 m^3/s^2).
    - R_E (float): Earth's radius in meters (default: 6371 km).
    - J2 (float): Earth's second zonal harmonic coefficient (default: 1.08263e-3).
    - omega_E (float): SS drift, ~1 deg/ day
    - omega_E (float): Earth's angular velocity in rad/s (default: 7.292115e-5 rad/s).
'''

# Constants and variables
mu_E = 3.986e14        # Gravitational parameter of Earth (m^3/s^2)
R_E = 6371e3           # Earth's radius (meters)
J2 = 1.08263e-3        # Second zonal harmonic coefficient
omega_ES = 1.9909681837564945e-07 # SS Omega drift
omega_E = 7.2921159e-5  # Earth's angular velocity (rad/s)

# f(h)
def f(h, tau):
    term1 = np.sqrt(mu_E / (R_E + h)**3)
    term2 = (J2 * R_E**2 * np.sqrt(mu_E) / (R_E + h)**(7/2)) * \
            ((8 / 3) * ((R_E + h)**7 * omega_ES**2 / (J2**2 * R_E**4 * mu_E)) + (3 / 2))
    term3 = (omega_ES - omega_E) * tau
    return term1 + term2 + term3

# f'(h)
def f_prime(h):
    numerator = -18 * J2 * R_E**2 * mu_E * (R_E + h)**2 + \
                112 * (R_E + h)**7 * omega_ES**2 + \
                63 * J2**2 * R_E**4 * mu_E
    denominator = 12 * J2 * R_E**2 * np.sqrt(mu_E) * (R_E + h)**(9/2)
    return numerator / denominator

# Initial guess h_0 (spherical Earth)
def initial_guess(tau):
    return (mu_E / (tau**2 * omega_E**2))**(1/3) - R_E

# Newton-Raphson!!
def newton_raphson(h0, tau, tolerance=0.0001, max_iterations=500):
    h = h0
    for iteration in range(max_iterations):

        fh = f(h, tau)
        fph = f_prime(h)
        
        if abs(fh) < tolerance:
            return h

        if fph == 0:
            raise ValueError("Derivative is zero. No solution found.")
        
        h = h - fh / fph
    
    raise ValueError("Newton-Raphson did not converge within the maximum number of iterations.")

def sun_sync_inclination(height):
    """
    Compute the inclination for a Sun-synchronous orbit at a given height.
    
    Parameters:
    - height (float): Orbital altitude above Earth's surface in meters.
    
    Returns:
    - inclination (float): Inclination in degrees.
    """
    # Compute semi-major axis (orbital radius for circular orbit)
    a = R_E + height
    
    # Compute cos(i)
    # cos_i = -(2 / 3) * (a**3 / (J2 * R_E**2)) * (omega_E / np.sqrt(mu_E))
    
    cos_i = - (a / 12352000)**(7/2)

    # Ensure the value of cos_i is valid for arccos (within -1 to 1)
    if not -1 <= cos_i <= 1:
        raise ValueError(f"cos(i) is out of bounds: {cos_i}. Check inputs for consistency.")
    
    # Compute inclination in radians and convert to degrees
    inclination_rad = np.arccos(cos_i)
    inclination_deg = np.degrees(inclination_rad)
    
    return inclination_deg

def add_to_results(results, new_solution):
    for existing_solution in results:
        if abs(round(existing_solution[2], 5) - new_solution[2]) < 0.00001 and abs(round(existing_solution[3], 5) - new_solution[3]) < 0.00001:
            return False
    results.append(new_solution)
    return True

results = []
non_converged = 1

# ND : Days to repeat orbit
# NS : Number of orbits until repetition
for NS in range(10, 350):
    for ND in np.arange(1,21,1):
    
        tau = NS / ND

        # Solve for h
        try:
            h_0 = initial_guess(tau)
            # print("initial guess: ", h_0)
            h_solution = newton_raphson(h_0, tau)

            inc = sun_sync_inclination(h_solution)

            if inc < 105 and h_solution > 300e3 and h_solution < 3000e3:
                add_to_results(results, [ND, NS, h_solution / 1000.0, inc])

            # print(NS, ND, h_solution, sun_sync_inclination(h_solution))

        except ValueError as e:
            non_converged = non_converged + 1
            # print(e)

        
print("Non converged: ", non_converged)
# print(list(results))

# Extract x, y, z coordinates
ND, NS, h, inc = zip(*results)

# Create a 3D scatter plot
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.scatter(ND, h, inc, c='b', marker='o', s=2)

# Reverse the x-axis direction
ax.invert_xaxis()

# Set axis labels
ax.set_xlabel('ND')
ax.set_ylabel('Orbit height [km]')
ax.set_zlabel('inclination [°]')

# Title
ax.set_title('SSO w/ RGT')

for result in results:
    print(result[0], result[1], result[2], result[3], sep=",")

# Show the plot
plt.show()