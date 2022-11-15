#!/usr/bin/env python
# coding: utf-8

# In[386]:


# Import libraries
# Model design
import agentpy as ap
# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import IPython
import random


# In[496]:


# Define parameters
parameters = {
    'm': 5, # Height of the grid
    'n': 5, # Length of the grid
    'nRobots': 15, # Number of robots
    'pDirty': 0.6, # Percentage of grid dirty
    'tMax': 50 # Max running time
}


# In[529]:


class CleaningModel(ap.Model):
    def setup(self):
        # Create agents (Dirty cells)
        nDirty = int(self.p.pDirty * (self.p.m * self.p.n))
        dirtyCells = self.agents = ap.AgentList(self, nDirty)
        # Create agents (Cleaning Robots)
        cleaningRobots = self.other_agents = ap.AgentList(self, self.p.nRobots)
        # Create grid (Room)
        self.room = ap.Grid(self, (self.p.m, self.p.n), torus=False, track_empty=True)
        self.room.add_agents(dirtyCells, random=True, empty=True)
        self.room.add_agents(cleaningRobots, positions=[(1, 1)] * self.p.nRobots, empty=True)
        # Dynamic variable condition = 0:Clean 1:Robots 2:Dirty
        self.agents.condition = 2
        self.other_agents.condition = 1
        self.p.nMoves = 0
    
    def step(self):
        # Run for every cleaning robot
        for i in self.other_agents:
            # Calculate initial + final position
            posI = self.room.positions[i]
            posF = (posI[0]+random.randint(-1, 1), posI[1]+random.randint(-1, 1))
            while posF[0] >= self.p.m or posF[0] < 0 or posF[1] >= self.p.n or posF[1] < 0:
                posF = (posI[0]+random.randint(-1, 1), posI[1]+random.randint(-1, 1))
            # If current cell is dirty, clean to it
            if any(self.room.agents[posI].condition == 2):
                self.room.agents[posI].condition = 1
            # If current cell is clean and next cell is empty, move to it
            elif all(self.room.agents[posF].condition != 1):
                self.room.move_to(i, posF)
                self.room.agents[posF].condition = 1
                self.room.agents[posI].condition = 0
                self.p.nMoves += 1
            self.p.nDirty = 0
            for i in self.room.agents.condition:
                if i == 2:
                    self.p.nDirty += 1
        # Stop simulation at max running time
        if self.t == self.p.tMax or self.p.nDirty == 0:
            print(self.t) # Total time spent
            print((((self.p.n * self.p.m) - self.p.nDirty) / (self.p.n * self.p.m)) * 100) # Percentage of clean cells
            print(self.p.nMoves) # Total moves by agents
            self.stop()

    def end(self):
        # Document a measure at the end of the simulation
        self.report('Total time spent', self.t)
        self.report('Percentage of clean cells', (((self.p.n * self.p.m) - self.p.nDirty) / (self.p.n * self.p.m)) * 100)
        self.report('Total moves by agents', self.p.nMoves)


# In[530]:


# Create a single-run animation with custom colors
def animation_plot(model, ax):
    attr_grid = model.room.attr_grid('condition')
    color_dict = {0:'#ffffff', 1:'#4a4a4a', 2:'#efece8', None:'#ffffff'}
    ap.gridplot(attr_grid, ax=ax, color_dict=color_dict, convert=True)
    ax.set_title(f"Cleaning robot simulation\n"
                 f"Time-step: {model.t}, Dirty cells: "
                 f"{len(model.agents.select(model.agents.condition == 2))}")
fig, ax = plt.subplots()
model = CleaningModel(parameters)
animation = ap.animate(model, fig, ax, animation_plot)
IPython.display.HTML(animation.to_jshtml(fps=15))


# # M1.Actividad - Informe
# 
# TC2008B | Modelación de sistemas multiagentes con gráficas computacionales (Grupo 303)
# 
# **Spinning Seal FM**
# - A01366643 | Luisa Fernanda Castaños Arias
# - A01632621 | Héctor Rafael Álvarez Aceves
# - A01634610 | Rodolfo Arechiga
# - A01639224 | Fausto Alejandro Palma Cervantes
# 
# 14 de noviembre de 2022
# 
# En esta actividad fue importante identificar la relación que tienen la cantidad de robots que se usan y las dimensiones que se le dan a la cuadrícula. Al incrementar el tamaño de la cuadrícula además de que el tiempo de ejecución se disparara exponencialmente, la cantidad de almacenamiento necesaria para correr la simulación también creció. De cualquier modo, pudimos identificar que mientras más robots se tengan dentro de la simulación menos es el tiempo que dura: dado que se tienen más agentes para cubrir todo el espacio. Esto llevo a que en algunos intentos se terminara dicha simulación antes que el tiempo máximo indicado en los parámetros. Los resultados de las siguientes variables: tiempo de ejecución, porcentaje de celdas limpias y movimientos totales de los robots, se muestran al final de la simulación mediante prints.

# In[ ]:




