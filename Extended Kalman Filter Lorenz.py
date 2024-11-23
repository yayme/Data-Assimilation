import numpy as np
import matplotlib.pyplot as plt



class Extended_Kalman_filter:
    def __init__(self,initial_state,initial_covariance,process_noise,measurement_noise,dt):
        self.state=np.array(initial_state, dtype=float)
        self.P=np.array(initial_covariance, dtype=float) #P is the error covariance
        self.Q=np.array(process_noise, dtype=float)
        self.R=np.array(measurement_noise, dtype=float)
        self.dt=dt
    def predict(self):
        self.state=self.state+self.dt*system_dynamics(self.state)
        F=np.eye(3)+self.dt*system_jacobian(self.state)
        self.P=F@self.P@F.T+self.Q
    def update(self,z,H):
        # measurement residual
        y=z-H@self.state
        # innovation covariance
        S=H@self.P@H.T+self.R
        # kalman gain
        K=self.P@ H.T @np.linalg.inv(S)
        self.state=self.state+ K@y
        # I=np.eye(self.P.shape[0])
        self.P=self.P-K@H@self.P

def system_dynamics(state):
    x,y,z=state
    sigma,rho,beta=10,28,8/3
    dx=sigma*(y-x)
    dy=x*(rho-z)-y
    dz=x*y-beta*z
    return np.array([dx,dy,dz])
def system_jacobian(state):
    x,y,z=state
    sigma,rho,beta=10,28,8/3
    return np.array([
        [-sigma,sigma,0],
        [rho-z,-1,-x],
        [y,x,-beta]
    ])

# testing it out
dt=0.01
num_steps=1000
true_state=[1.0,1.0,1.0]
true_states=[true_state]

ekf=Extended_Kalman_filter(
    initial_state=[0.5,0.5,0.5],
    initial_covariance=np.eye(3)*10,
    process_noise=np.diag([0.1,0.1,0.1]),
    measurement_noise=np.array([[4.0]]),
    dt=dt
)



noise_measurements=[]
noise_measurements.append(true_states[0][0]+np.random.normal(0,2.0))

for k in range(1,num_steps):
    true_states_k=true_states[k-1]+dt*system_dynamics(true_states[k-1])
    true_states.append(true_states_k)
    noise_measurements.append(true_states[k][0]+np.random.normal(0,2.0))


estimated_states=[ekf.state]

for t in range(1,num_steps):
    ekf.predict()

    z=np.array([noise_measurements[t]])
    H=np.array([[1,0,0]]) #simple example. we are directly receiving position information
    ekf.update(z,H)

    estimated_states.append(ekf.state)

true_states=np.array(true_states)
estimated_states=np.array(estimated_states)
# plotting
from mpl_toolkits.mplot3d import Axes3D

fig=plt.figure(figsize=(10,8))
ax=fig.add_subplot(111,projection='3d')
ax.plot(true_states[:,0],true_states[:,1],true_states[:,2],label="true trajectory", color="g", linewidth=2)
ax.scatter(noise_measurements,np.zeros(len(noise_measurements)),np.zeros(len(noise_measurements)),
           label="noise measurements only in x", color="orange", alpha=0.5,s=10)
ax.plot(estimated_states[:,0],estimated_states[:,1],estimated_states[:,2],
        label="extended kalman filter esimation", color="r", linestyle="--",linewidth=2)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("extended kalman filter for lorenz system(3d visualization)")
ax.legend()
plt.show()
