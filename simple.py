# import all gem'5 objects
import m5 
from m5.objects import * #imports all SimObjects

#Instantiate a system
# "System" is a Python class wrapper for the System C++ SimObject

system = System()

# Initialze a clock and voltage domain
# "clk_domain" is a *parameter* of the System SimObject 
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
# gem5 is smart enough automatically convert units
system.clk_domain.voltage_domain = VoltageDomain()

# let's set up the memory system
system.mem_mode = 'timing'
# You want to use *timing* for simulations, the options are things 'atomic' 'functional'(debug)

# All systems need memory!
system.mem_ranges = [AddrRange('512MB')]

# Let's create a CPU
system.cpu = TimingSimpleCPU()

# Now, we need a memory bus
system.membus = SystemXBar()

# Hook up CPU
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
# Next, some BS to get things right
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

# Now, you must create a memory controller and add a specific DRAM interface. Code from gem5-20.1.
system.mem_ctrl = MemCtrl()

# Finally, let's make the memory controller
system.mem_ctrl.dram = DDR3_1600_8x8()

# Set up physical memory ranges
system.mem_ctrl.dram.range = system.mem_ranges[0]

# Connect memory to bus
system.mem_ctrl.port = system.membus.mem_side_ports

# Now tell the system what we want it to do 
process = Process()
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello']
system.cpu.workload = process
system.cpu.createThreads()

# Now, we're almost done
# Create a root object
root = Root(full_system = False, system = system)

# Instantiate all of the C++
m5.instantiate()

# We're ready to run!

print("Beginning simulation!")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
