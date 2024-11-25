import numpy as np
import matplotlib.pyplot as plt



class Kalman_filter:
    def __init__(self,initial_state,initial_covariance,process_noise,measurement_noise):
        self.state=initial_state
        self.P=initial_covariance #P is the error covariance
        self.Q=process_noise
        self.R=measurement_noise
    def predict(self, F):
        self.state=F@self.state #state transition
        self.P=F@self.P@F.T+self.Q
    def update(self,z,H):
        # measurement residual
        y=z-H@self.state
        # innovation covariance
        S=H@self.P@H.T+self.R
        # kalman gain
        K=self.P@ H.T @np.linalg.inv(S)
        self.state=self.state+ K@y
        self.P=self.P-K@H@self.P

# testing it out
N=1000
num_steps=50
true_position=0
initial_state=np.array([0])
initial_covariance=np.array([[10]])

process_noise=np.array([[0.1]])
measurement_noise=np.array([[2]])
# measurment with white noise
def measurement_model(true_position):
    return true_position+np.random.normal(0,2)

def motion_model(state):
    return state+np.random.normal(0,0.5)

kf=Kalman_filter(initial_state,initial_covariance,process_noise,measurement_noise)

true_positions=[true_position]
estimated_positions=[]
predicted_positions=[]

for t in range(num_steps):
    true_position=motion_model(true_position)
    true_positions.append(true_position)
    F=np.array([[1]]) #Testing with simple motion model
    kf.predict(F)

    z=measurement_model(true_position)
    H=np.array([[1]]) #simple example. we are directly receiving position information
    kf.update(z,H)

    estimated_positions.append(kf.state[0])
    predicted_positions.append(kf.state[0])


# plotting
plt.figure(figsize=(10,6))
plt.plot(true_positions, label="true position", color="b", linestyle="-", linewidth=2)
plt.plot(estimated_positions,label="estimated positoins using kalman filter", color="r",linestyle="--",linewidth=2)
plt.scatter(range(num_steps),predicted_positions,color='g',s=10,label="predicted positions")
plt.xlabel('time')
plt.ylabel('position')
plt.title('kalman filter: position estimation ')
plt.legend()
plt.show()

