import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import random
import argparse

# def parse_args():
# 	'''PARAMETERS'''
# 	parser = argparse.ArgumentParser('boom')
# 	parser.add_argument('--N', type=int, default=16, help='no of oscillators')
# 	return parser.parse_args()

# args = parse_args()

# function to keep phase bounded between 0 and 2*pi
def keep_bounded(angle):
	if(angle>2*pi):
		angle = angle-2*pi
	if(theta[i][n+1]<0):
		angle = angle+2*pi

	return angle


# function for calculating adjacency matrix of m layers and N oscillators per layer
def adjacency(N,m):
	A = np.ones(N) - np.eye(N)
	I = np.eye(N)
	Ad = np.random.rand(m,m,N,N)

	for i in range(m):
		for j in range(m):
			if(i==j):
				Ad[i][j] = A
			else:
				Ad[i][j] = I

	Ad=Ad.reshape(m,m*N,N)


	Adj = Ad[0,:,:]

	for i in range(1,m):
		Adj=np.concatenate((Adj,Ad[i,:,:]),axis=1)

	return Adj

# function to plot phase value of order parameter at a given timestep t
def plot_order_parameter(t):

	x = np.cos(theta[:,t])
	y = np.sin(theta[:,t])

	x = np.append(x, [np.mean(x)])
	y = np.append(y, [np.mean(y)])

	c = np.chararray(N+1,unicode=True)

	for i in range(N+1):
		c[i] = 'b'

	c[N] = 'y'
	c_f[N] = 'y'

	axes = plt.gca()
	axes.set_xlim([-1.5,1.5])
	axes.set_ylim([-1.5,1.5])

	t1 = np.linspace(-1.5, 1.5, 100)
	t2 = np.zeros(100)
	axes.plot(t1, t2, linewidth =1, c='black')  # to plot x-axis
	axes.plot(t2, t1, linewidth =1, c='black')  # to plot y-axis

	t = np.linspace(0, 2*pi, 100)
	axes.plot(np.cos(t), np.sin(t), c='g', linewidth=1)    # to plot a unit circle
	# plt.scatter(x_i, y_i, c=c_i)
	plt.scatter(x, y, c=c_f)
	plt.show()


# magnitude of order parameter at a given timestep t
def order_para_mag(t):

	x = np.cos(theta[:,t])
	y = np.sin(theta[:,t])

	x = np.mean(x)
	y = np.mean(y)

	r = (x*x + y*y)**(1/2)

	return r

# calculates mean OP for t-th to (t+n)-th oscillation
def mean_order_parameter(t,n):
	a = []
	for i in range(n):
		a.append(order_para_mag(int((t+i)*N_t/100)))
	o = mean(a)
	return o


# omega = np.random.uniform(7.433, 7.667, N)    # Frequencies of 16 oscillators also come from random sampling of gaussinan with mean 2 and variance 0.5

omega_all = np.array([7.74334095, 7.60661757, 7.64509393, 7.13245997, 7.22316859,
       7.27505356, 7.30052216, 7.00394374, 7.7147747 , 7.1762493 ,
       7.41101836, 7.07184644, 7.84605506, 7.26146756, 7.11663017,
       7.95686032, 7.40357684, 7.67716534, 7.58827561, 7.98295863,
       7.21509378, 7.84335898, 7.83340062, 7.4992556 , 7.78140525,
       7.37500004, 7.31213251, 7.72541698, 7.30587977, 7.34463646,
       7.19432453, 7.97604975, 7.83659962, 7.44919356, 7.3881354 ,
       7.54963891, 7.78923156, 7.27670869, 7.25578913, 7.35169169,
       7.28180158, 7.3528294 , 7.51915414, 7.5532435 , 7.52461318,
       7.52883793, 7.07978764, 7.24459412, 7.91745028, 7.88082182])

# # One of the initial conditions for N = 16 case
# initial = np.array([4.86516572, 4.25427542, 5.62448612, 2.6363104 , 3.13918056,
#        5.52485543, 5.40279519, 2.47437502, 6.01973355, 5.94306109,
#        0.83500998, 3.21425546, 5.74718388, 6.02278303, 0.3968766 ,
#        2.48025589])

mean_OPs = []
list_of_eps = [0.02, 0.04, 0.06, 0.08, 0.1, 0.15, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
list_of_n = []

# for eps in list_of_eps:
for num in range(3,51):
	
	list_of_n.append(num)
	# setting the parameters
	pi = np.pi
	m = 1                    # number of layers
	N = num	                 # no of oscillators in one layer

	omega = omega_all[0:N]
	# print(omega.shape)

	omega_mean = np.mean(omega)         # mean value of freq distribution
	omega_var = 0.2        # variance of freq
	phase_lag = 0
	P = 2*pi/omega_mean   # P is the mean time period
	dt = P/400
	T = 100*P
	N_t = int(round(T/dt))       # no of time steps
	print(N_t)
	time_axis = np.linspace(0, N_t*dt, N_t+1)


	theta_mean = pi        # mean value of initial phase of osc
	theta_var = pi/20         # variance of initial phase
	theta = np.zeros([N*m, N_t+1], dtype = float)
	theta[:,0] = np.random.uniform(0, 2*pi, N)    # Initial condition of 16 oscillators come from random sampling
	# theta[:,0] = initial[0:N]


	Adj_matrix = adjacency(N,m)


	# N_t/2 = int(N_t/2)

	for n in range(int(N_t/4)):
		for i in range(N*m):
			theta[i][n+1] = theta[i][n] + dt*(omega[i])

			theta[i][n+1] = keep_bounded(theta[i][n+1])


	for n in range(int(N_t/4), N_t):
		for i in range(N*m):

			Adj_term = 0

			for j in range(N*m):
				Adj_term += Adj_matrix[i][j]*np.sin(theta[j][n]-theta[i][n]-phase_lag)	

			theta[i][n+1] = theta[i][n] + dt*(omega[i] + 1.4*Adj_term/(N+1))

			theta[i][n+1] = keep_bounded(theta[i][n+1])

	# for i in range(N):
	# 	plt.plot(theta[i])

	# plt.show()


	print("for n={}, mean of OPs of 80 to 100 osc ".format(N), mean_order_parameter(80,20))
	mean_OPs.append(mean_order_parameter(80,20))



with open("mean_OPs_vs_N.txt", "w") as output:
    output.write(str(mean_OPs))

plt.plot(list_of_n, mean_OPs)
plt.show()