import simpy
import matplotlib.pyplot as plt
plt.close('all')

from my_functions import my_nsl, my_ol

class MooreMachine:
    def __init__(self, env):
        
        
        self.env = env
        
        # model settings
        self.tpd_NSL = 0.2
        self.tpd_OL = 0.1
        self.tpd_reg = 0.1
        
        # states
        self.ps = 0b000  # Initial state (000 in binary)
        self.ns = 0b000
        
        # signal
        self.clk = 0
        
        # synchronous reset
        self.sr = 0b0
        
        # asynchronous reset
        self.ar = 0b0
        
        # period
        self.period = 0b111
        
        # compare
        self.compare = 0b011
        
        # outputs
        self.outputs = 0b0
        
        # simpy store resource
        self.S_reg_OL = simpy.Store(env)
        self.S_reg_NSL = simpy.Store(env)
        
        # sampling variables
        self.time = []
        self.wav_ps = []
        self.wav_ns = []
        self.wav_clk = []
        self.wav_outputs = []
        self.wav_sr = []
        self.wav_ar = []
        
        # running processes
        env.process(self.next_state_logic()) 
        env.process(self.output_logic())  
        env.process(self.register())  
        env.process(self.clock())
        env.process(self.run())
        env.process(self.probe())

    def next_state_logic(self):
        while True:
            yield self.S_reg_NSL.get()
            yield self.env.timeout(self.tpd_NSL)

            self.ns = my_nsl(self.ps,self.sr)
            

    def register(self):
        # Update the current state
        while True:
            yield self.env.timeout(self.tpd_reg)  # Wait for 1 time unit before the next transition
            
            self.ps = self.ns
            self.S_reg_OL.put(True)
            self.S_reg_NSL.put(True)
            
            yield self.env.timeout(1-self.tpd_reg)  # Wait for 1 time unit before the next transition

    def output_logic(self):
        while True:
            yield self.S_reg_OL.get()
            yield self.env.timeout(self.tpd_OL)  # Update at every resolution tick
            self.outputs, self.sr = my_ol(self.ps, self.period, self.compare, self.sr, self.ar)
            
    def run(self):
        yield self.env.timeout(0.5)
        while True:
            print(f"Time: {self.env.now}, State: {self.ps:03b}, Output: {self.outputs:03b}")
            yield self.env.timeout(1)  
    
    def clock(self):
        self.clk = 1
        while True:
            yield self.env.timeout(0.5)
            self.clk = 0
            yield self.env.timeout(0.5)
            self.clk = 1

    def probe(self):
        while True:
            self.time.append(self.env.now)
            self.wav_ps.append(self.ps)
            self.wav_ns.append(self.ns)
            self.wav_outputs.append(self.outputs)
            self.wav_clk.append(self.clk)
            self.wav_sr.append(self.sr)
            self.wav_ar.append(self.ar)
            yield self.env.timeout(0.01)  
            
    def plot_states_and_output(self):
        plt.figure(figsize=(14, 8))
        
        # Define the time ticks based on the simulation time
        time_ticks = range(0, int(self.time[-1]) + 1, 1)
    
        plt.subplot(5, 1, 1)
        plt.step(self.time, self.wav_outputs, where='post', color='green')
        plt.ylabel('Outputs')
        plt.xticks(time_ticks)
        plt.title('Waveforms')
        plt.grid(True)
        
        plt.subplot(5, 1, 2)
        plt.step(self.time, self.wav_sr, where='post', color ='purple')
        plt.ylabel('SR')
        plt.xticks(time_ticks)
        plt.grid(True)
        
        plt.subplot(5, 1, 3)
        plt.step(self.time, self.wav_ns, where='post')
        plt.ylabel('Next State')
        plt.xticks(time_ticks)
        plt.grid(True)
    
        plt.subplot(5, 1, 4)
        plt.step(self.time, self.wav_ps, where='post', color='blue')
        plt.ylabel('Present State')
        plt.xticks(time_ticks)
        plt.grid(True)
        
        plt.subplot(5, 1, 5)
        plt.step(self.time, self.wav_clk, where='post', color='red')
        plt.ylabel('Clock')
        plt.xlabel('Time (units)')
        plt.xticks(time_ticks)
        plt.grid(True)
    
        plt.tight_layout()
        plt.show()


# Create a SimPy environment
env = simpy.Environment()
# Create a Moore machine instance
counter = MooreMachine(env)

# Run the simulation for 10 time units
env.run(until=20)

# After the simulation, plot the waveforms
counter.plot_states_and_output()