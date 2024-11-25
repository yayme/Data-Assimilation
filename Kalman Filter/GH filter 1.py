import numpy as np
import matplotlib.pyplot as plt
# number of particles
N=1000
# simple motion model
def motion(x):
    return x+np.random.normal(0,0.5)
# measurement with non-gaussian noise
def measurement_model(true_position):
    return true_position+np.random.laplace(0,1)
# laplace noise for demonstration
def gh_filter(true_position, particles, weights):
    # propagation step
    for i in range(len(particles)):
        particles[i]=motion(particles[i])

    measurement=measurement_model(true_position)
    for i in range(len(particles)):
        # likelihood based on laplace noise
        weights[i]=np.exp(-np.abs(particles[i]-measurement)/1.0)
    weights/=np.sum(weights)
    # resampling step
    indices=np.random.choice(range(N), size=N, p=weights)
    particles[:]=[particles[i] for i in indices]
    # estimated position=mean of particles
    estimated_position=np.mean(particles)
    return estimated_position,particles,weights

# simulation
true_position=0
true_positions=[true_position]
particles=np.random.uniform(-10,10,N)
weights=np.ones(N)/N
# weight initialized as 1/N to each
num_steps=50
estimated_positions=[]

for t in range(num_steps):
    true_position=motion(true_position)
    true_positions.append(true_position)
    estimated_position,particles, weights=gh_filter(true_position, particles, weights)
    estimated_positions.append(estimated_position)

    # plotting
plt.figure(figsize=(10,6))
plt.plot(true_positions, label="true position", color="g",linestyle='-', linewidth=2)
plt.plot(estimated_positions, label="Estimated Position (G-H Filter)", color='r',linestyle='--', linewidth=2)
plt.scatter(range(num_steps), estimated_positions, color='r', s=10,label="particles")
plt.xlabel('time stop')
plt.ylabel('position')
plt.title('G-H filter: non-gaussian position estimation')
plt.legend()
plt.show()
