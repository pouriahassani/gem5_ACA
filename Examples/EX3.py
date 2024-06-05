from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.isas import ISA
# from gem5.resources.resource import CustomResource
from gem5.resources.resource import AbstractResource
from gem5.simulate.simulator import Simulator
from typing import Dict
from warnings import warn
class CustomResource(AbstractResource):
    """
    A custom gem5 resource. This can be used to encapsulate a resource provided
    by a gem5 user as opposed to one available within the gem5 resources
    repository.

    .. warning::

        This class is deprecated and will be removed in future releases of gem5.
        Please use the correct AbstractResource subclass instead.
    """

    def __init__(self, local_path: str, metadata: Dict = {}):
        """
        :param local_path: The path of the resource on the host system.
        :param metadata: Add metadata for the custom resource. **Warning:**
                         As of v22.1.1, this parameter is not used.
        """
        warn(
            "The `CustomResource` class is deprecated. Please use an "
            "`AbstractResource` subclass instead."
        )
        if bool(metadata):  # Empty dicts cast to False
            warn(
                "the `metadata` parameter was set via the `CustomResource` "
                "constructor. This parameter is not used."
            )
        super().__init__(local_path=local_path)

# Setup the system memory.
memory = SingleChannelDDR3_1600()

# Setup a single core Processor.
processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING, isa=ISA.RISCV, num_cores=1
)

# Setup the board.
board = SimpleBoard(
    clk_freq="1GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=NoCache(),
)
binary = "/workspace/gem5_ACA/Examples/mul"
# Create a CustomResource object.
binary_resource = CustomResource(local_path=binary)
# Set the syscall enulation mode with hello world workload.
board.set_se_binary_workload(binary_resource)

simulator = Simulator(board=board)
print("Beginning simulation!")
simulator.run()
print("end simulation!")
