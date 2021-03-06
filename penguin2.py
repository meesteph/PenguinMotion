import numpy as np
import scipy as sp
import random

# Computational Parameters
a = 1.           # Average size of the penguins
dev_a = a/10.    # Deviation of the average size

N_xy = 8        # Number of penguins in the x and  y direction
N_z = 10         # Number of penguins in the z direction

dev_i = 0.01
dev_j = 0.01
dev_or = 0.25*np.pi

class Penguin(object):

	def __init__(self, radius, position, alignment, boundary):
		"""
		Arguments:
			radius		:=	float representing penguin radius
			position	:=	numpy array representing penguin position (x, y, z)
			alignment	:=	numpy array representing alignment unit vector
			boundary	:=	boolean value, True if boundary penguin, False if bulk penguin
		"""

		self.radius = radius
		self.position = position
		self.alignment = alignment
		self.boundary = boundary

	def get_distance(self, penguin2):

		return np.dot((self.position - penguin2.position),(self.position - penguin2.position))

	def net_force(self, F_self, F_in, k, penguin_list, a):
		"""
		Arguments:
			F_self			:=	multiplicative strength factor of penguin self-propulsion
			F_in			:=	multiplicative strength factor of the penguin boundary force
			k				:=	spring constant relating to the repulsive force of overlapping penguins
			penguin_list	:=	python list containing all penguins in the system
			a 				:=	average radius of all penguins in the system
		"""

		critical_radius = a
                neighbour_radius = 1.3 * a
		F_selfPropulsion = F_self * self.alignment

		F_repulsion = 0 

		if (self.boundary == True):

			F_boundary = F_in * self.alignment

		else:

			F_boundary = 0
                above_plane = []
		for i in range(len(penguin_list)):

			if (penguin_list[i] != self):

				r = self.get_distance(penguin_list[i])
				r_mag = np.linalg.norm(r)
				if (r < neighbour_radius):
				        #Repulstion force if neighbours are too close
				        if (r < critical_radius):
					   F_repulsion += -k * r
					#Boundary determination
					#alignment [a b c], position [x_0, y_0, z_0], neighbour at [x, y, z]
                                        #Plane defined by: a(x-x_0)+b(y-y_0)+c(z-z_0)=0
					plane = self.alignment[0]*(penguin_list[i].position[0] - self.position[0]) + self.alignment[1]*(penguin_list[i].position[1] - self.position[1]) + self.alignment[2]*(penguin_list[i].position[2] - self.position[2])
                                        #print(i, plane)
                                        if plane > 0:
                                            above_plane.append(0)
                                        else:
                                            above_plane.append(1)
                print(above_plane)
                if (all(j == 0 for j in above_plane)) or (all (j == 1 for j in above_plane)):
                    self.boundary = True
                else:
                    self.boundary = False
	def net_torque(self, T_in, T_n, T_align, penguin_list, a):
		"""
		Arguments:
			T_in 			:=	multiplicative strength factor of the boundary torque term
			T_n				:=	multiplicative strength factor of the random torque term
			T_align			:=	multiplicative strength factor of the alignment torque term
			penguin_list	:=	python list containing all penguins in the system
			a 				:=	average radius of all penguins in the system
		"""

		critical_radius = a
		T_alignment = np.zeros(3)

		if (self.boundary == True):

			distance_sum = np.zeros(3)

			for i in range(len(penguin_list)):

				r = self.get_distance(penguin_list[i])
				r_mag = np.linalg.norm(r)

				if (penguin_list[i] != self) and (penguin_list[i].boundary == True):

					distance_sum += self.get_distance(penguin_list[i])

				if (penguin_list[i] != self) and (r_mag < critical_radius):

					T_alignment += T_align * (self.alignment - penguin_list[i].alignment)

			exterior_bisector = distance_sum / np.linalg.norm(distance_sum)

			delta_theta = self.alignment - exterior_bisector

			T_boundary = T_in * delta_theta

		else:

			T_boundary = 0

		eta = random.uniform(-1.0,1.0)

		T_noise = eta * T_n

		return T_boundary + T_noise + T_alignment
		
##############################################################################
########################INITIALIZING##########################################
##############################################################################

# Placing all the penguins on a cuboid grid, with small deviations on the grid points
Penguin_list = []

for i in range(N_xy):
    for j in range(N_xy):
        for k in range(N_z):
            Penguin_list.append(Penguin(np.random.normal(a,dev_a),
                    np.array([np.random.normal(i,dev_i),np.random.normal(j,dev_j),k]),
                    np.array([np.random.normal(0,1),np.random.normal(0,1),1]), False))
cnt = 0
for penguin in Penguin_list:
    penguin.net_force(1,1,1,Penguin_list,1)
    if penguin.boundary:
        cnt += 1
    
print(cnt)
