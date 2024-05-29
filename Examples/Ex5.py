from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator


# Setup the system memory.
memory = SingleChannelDDR3_1600()

# Here we setup a MESI Two Level Cache Hierarchy.
cache_hierarchy = MESITwoLevelCacheHierarchy(
    l1d_size="4kB",
    l1d_assoc=8,
    l1i_size="16kB",
    l1i_assoc=8,
    l2_size="256kB",
    l2_assoc=16,
    num_l2_banks=1,
)

# Setup a single core Processor.
processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING, isa=ISA.RISCV, num_cores=1
)

# Setup the board.
board = SimpleBoard(
    clk_freq="1GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Set the syscall emulator mode for running binary found in the id of: riscv-stc
board.set_se_binary_workload(
    obtain_resource(resource_id="riscv-stc")
    )

simulator = Simulator(board=board)
print("Beginning simulation!")
simulator.run()
