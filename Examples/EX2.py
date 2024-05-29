from gem5.components.boards.riscv_board import RiscvBoard

from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator


# Setup the system memory.
memory = SingleChannelDDR3_1600()

# Setup a single core Processor.
processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING, isa=ISA.RISCV, num_cores=1
)

# Setup the board.
board = RiscvBoard(
    clk_freq="1GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=NoCache(),
)

# Set the Full System workload.
board.set_kernel_disk_workload(
    kernel=obtain_resource("riscv-bootloader-vmlinux-5.10"),
    disk_image=obtain_resource("riscv-disk-img"),
)

simulator = Simulator(board=board)
print("Beginning simulation!")

simulator.run(max_ticks=10**12)
