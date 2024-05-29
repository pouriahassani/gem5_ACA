from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_switchable_processor import (
    SimpleSwitchableProcessor,
)
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator


# Setup the system memory.
memory = SingleChannelDDR3_1600(size="3GB")

# Here we setup the processor. This is a special switchable processor in which
# a starting core type and a switch core type must be specified. Once a
# configuration is instantiated a user may call `processor.switch()` to switch
# from the starting core types to the switch core types. In this simulation
# we start with ATOMIC cores to simulate the OS boot, then switch to the
# Out-of-order (O3) cores for the command we wish to run after boot.
processor = SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.ATOMIC,
    switch_core_type=CPUTypes.O3,
    isa=ISA.X86,
    num_cores=1,
)

# Here we setup the board. The X86Board allows for Full-System X86 simulations.
board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=NoCache(),
)

# Here we set the Full System workload.
# The `set_kernel_disk_workload` function for the X86Board takes a kernel, a
# disk image, and, optionally, a command to run.

# This is the command to run after the system has booted. The first `m5 exit`
# will stop the simulation so we can switch the CPU cores from ATOMIC to O3
# and continue the simulation to run the echo command, sleep for a second,
# then, again, call `m5 exit` to terminate the simulation. After simulation
# has ended you may inspect `m5out/system.pc.com_1.device` to see the echo
# output.
command = (
    "m5 exit;"
    + "echo 'This is running on O3 CPU cores.';"
    + "sleep 1;"
    + "m5 exit;"
)

board.set_kernel_disk_workload(
    kernel=obtain_resource("x86-linux-kernel-4.4.186"),
    disk_image=obtain_resource("x86-ubuntu-18.04-img"),
    readfile_contents=command,
)

simulator = Simulator(board=board)

# Runs up to the first `m5 exit` command.
print("Start booting the OS")
simulator.run()
# Here we can do things to modify the configuration. In this case we switch
# the CPU cores from the ATOMIC CPU cores to the O3 cores. This reason for this
# is to simulate the OS boot with the ATOMIC CPU cores, which are faster, then
# switch to the O3 cores to run the command we want to run on the O3 cores.
processor.switch()
print("Finished booting the OS")

# Then to resume the simulation we call `simulator.run()` to continue the
# simulation until the second, and last, `m5 exit` command.print("finished booting the OS")
print("Start execuitng the commands on the O3 core")
simulator.run()
print("Finished execuitng the commands on the O3 core")

