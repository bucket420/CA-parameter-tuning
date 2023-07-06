import numpy as np
import subprocess
import os
from utils import get_metrics, write_csv, read_csv
import uproot
import json

class Particle:
    def __init__(self, lb=-10, ub=10, num_objectives=2, velocity=None, position=None, 
                 best_position=None, best_fitness=None):
        if position is not None:
            self.velocity = velocity
            self.position = position
            self.fitness = None
            self.best_position = best_position
            self.best_fitness = best_fitness
        else:
            self.position = np.random.uniform(lb, ub)
            self.velocity = np.zeros_like(self.position)
            self.best_position = self.position
            self.best_fitness = np.ones(num_objectives) #inf for minimization
            self.fitness = np.ones(num_objectives)

    def update_velocity(self, global_best_position, w=0.5, c1=1, c2=1):
        r1 = np.random.uniform(0, 1)
        r2 = np.random.uniform(0, 1)
        cognitive = c1 * r1 * (self.best_position - self.position)
        social = c2 * r2 * (global_best_position - self.position)
        self.velocity = w * self.velocity + cognitive + social

    def update_position(self, lb, ub):
        self.position = np.clip(self.position + self.velocity, lb, ub)
    
    def evaluate_fitness(self, uproot_file, id):
        self.fitness = np.array(get_metrics(uproot_file, id))
        
        # sometimes tracks overflow happens which leads to perfect fitness but the result is actually bad
        if self.best_fitness[0] == 0 or self.best_fitness[1] == 0:
            self.fitness = np.array([1.0, 1.0])
            
        if all(self.fitness < self.best_fitness):
            self.best_fitness = self.fitness
            self.best_position = self.position

class PSO:
    def __init__(self, lb, ub, num_objectives=2, num_particles=50, w=0.5, c1=1, c2=1, 
                 num_iterations=100, state_json=None, max_iter_no_improv=None, tol=None):
        if not state_json:
            self.num_particles = num_particles
            self.lb = lb
            self.ub = ub
            self.w = w
            self.c1 = c1
            self.c2 = c2
            self.num_iterations = num_iterations
            self.num_objectives = num_objectives
            self.max_iter_no_improv = max_iter_no_improv
            self.tol = tol
            self.particles = [Particle(lb, ub) for _ in range(num_particles)]
            self.global_best_position = np.zeros_like(lb)
            self.global_best_fitness = np.ones(num_objectives)
            self.state = {
                "num_objectives": self.num_objectives,
                "num_particles": self.num_particles,
                "num_iterations": self.num_iterations,
                "max_iter_no_improv": self.max_iter_no_improv,
                "tol": self.tol,
                "lb": self.lb,
                "ub": self.ub,
                "w": self.w,
                "c1": self.c1,
                "c2": self.c2,
                "global_best_position": self.global_best_position.tolist(),
                "global_best_fitness": self.global_best_fitness.tolist(),
                "iteration": 0
            }
            write_csv('parameters.csv', [self.particles[i].position for i in range(self.num_particles)])
            with open('history/pso_state.json', 'w') as f:
                json.dump(self.state, f, indent=4)
        else:
            with open(state_json) as f:
                self.state = json.load(f)
            self.num_particles = self.state["num_particles"]
            self.lb = self.state["lb"]
            self.ub = self.state["ub"]
            self.w = self.state["w"]
            self.c1 = self.state["c1"]
            self.c2 = self.state["c2"]
            self.num_iterations = self.state["num_iterations"]
            self.num_objectives = self.state["num_objectives"]
            self.max_iter_no_improv = self.state["max_iter_no_improv"]
            self.tol = self.state["tol"]
            self.global_best_fitness = np.array(self.state["global_best_fitness"], dtype=float)
            self.global_best_position = np.array(self.state["global_best_position"], dtype=float)
            num_params = len(self.lb)
            particles_state = read_csv('history/particles_state.csv')
            self.particles = [Particle(
                                lb=self.lb, 
                                ub=self.ub, 
                                num_objectives=self.num_objectives,
                                position=np.array(particles_state[i][:num_params], dtype=float),
                                velocity=np.array(particles_state[i][num_params:2*num_params], dtype=float),
                                best_position=np.array(particles_state[i][2*num_params:3*num_params], dtype=float),
                                best_fitness=np.array(particles_state[i][3*num_params:], dtype=float)
                             ) for i in range(self.num_particles)]
            

    def optimize(self):
        uproot_file = None
        # clear old data, probably not the best way to do this
        if not self.state["iteration"]:
            os.system("rm -rf history/parameters/*")
            os.system("rm -rf history/validation/*")
            os.system("rm -rf history/pareto_front/*")
            
        for i in range(self.num_iterations):
            write_csv('history/parameters/iteration' + str(self.state["iteration"]) + '.csv', [self.particles[i].position for i in range(self.num_particles)])
            validation_result = "history/validation/iteration" + str(self.state["iteration"]) + ".root"
            subprocess.run(['cmsRun','reconstruction.py', "outputFileName=" + validation_result])
            
            for j, particle in enumerate(self.particles):
                uproot_file = uproot.open(validation_result)
                particle.evaluate_fitness(uproot_file, j)
                if all(particle.fitness < self.global_best_fitness): 
                    self.global_best_fitness = particle.fitness
                    self.global_best_position = particle.position
            uproot_file.close()
                
            pareto_front = self.get_pareto_front()
            write_csv('history/pareto_front/iteration' + str(self.state["iteration"]) + '.csv', 
                      [np.concatenate([pareto_front[self.state["iteration"]].position, pareto_front[i].fitness]) for i in range(len(pareto_front))])  

            for j, particle in enumerate(self.particles):
                particle.update_velocity(self.global_best_position, self.w, self.c1, self.c2)
                particle.update_position(self.lb, self.ub)
                
            write_csv('parameters.csv', [self.particles[i].position for i in range(self.num_particles)])
            write_csv('history/particles_state.csv', 
                      [np.concatenate([particle.position, particle.velocity, particle.best_position, particle.best_fitness]) 
                       for particle in self.particles])

            self.state["iteration"] += 1
            self.state["global_best_position"] = self.global_best_position.tolist()
            self.state["global_best_fitness"] = self.global_best_fitness.tolist()
            with open('history/pso_state.json', 'w') as f:
                json.dump(self.state, f, indent=4)  

    def get_pareto_front(self):
        pareto_front = []
        for particle in self.particles:
            dominated = False
            for other_particle in self.particles:
                if all(particle.fitness > other_particle.fitness):
                    dominated = True
                    break
            if not dominated:
                pareto_front.append(particle)
        # Sort the Pareto front by crowding distance
        # crowding_distances = self.calculate_crowding_distance(pareto_front)
        # pareto_front.sort(key=lambda x: crowding_distances[x], reverse=True)
        return pareto_front

    def calculate_crowding_distance(self, pareto_front):
        crowding_distances = {particle: 0 for particle in pareto_front}
        for objective_index in range(self.num_objectives):
            # Sort the Pareto front by the current objective function
            pareto_front_sorted = sorted(pareto_front, key=lambda x: x.fitness[objective_index])
            crowding_distances[pareto_front_sorted[0]] = np.inf
            crowding_distances[pareto_front_sorted[-1]] = np.inf
            for i in range(1, len(pareto_front_sorted)-1):
                crowding_distances[pareto_front_sorted[i]] += (
                    pareto_front_sorted[i+1].fitness[objective_index] -
                    pareto_front_sorted[i-1].fitness[objective_index]
                )
        return crowding_distances
