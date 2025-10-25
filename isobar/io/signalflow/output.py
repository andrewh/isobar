from ..output import OutputDevice

import logging
import inspect

logger = logging.getLogger(__name__)

try:
    from signalflow import AudioGraph, Patch, PatchSpec
    _signalflow_available = True
except (ModuleNotFoundError, ImportError):
    AudioGraph = Patch = PatchSpec = None  # type: ignore
    _signalflow_available = False

if _signalflow_available:
    class SignalFlowOutputDevice(OutputDevice):
        def __init__(self, graph=None):
            super().__init__()
            if graph:
                self.graph = graph
            else:
                self.graph = AudioGraph.get_shared_graph()
                if self.graph is None:
                    self.graph = AudioGraph(start=True)
            logger.info("Opened SignalFlow output")
            self.patches = []

        def create(self, patch_spec, patch_params, output=None):
            if inspect.isclass(patch_spec):
                patch = patch_spec(**patch_params)
            elif isinstance(patch_spec, PatchSpec):
                patch = Patch(patch_spec, patch_params)
            else:
                raise RuntimeError("patch property is of invalid type")
            patch.set_auto_free(True)
            if output:
                if patch.add_to_graph():
                    output.add_input(patch)
            else:
                self.graph.play(patch)

        def trigger(self, patch, trigger_name=None, trigger_value=None):
            if trigger_name is not None and trigger_value is not None:
                patch.trigger(trigger_name, trigger_value)
            elif trigger_name is not None:
                patch.trigger(trigger_name)
            else:
                patch.trigger()
else:
    class SignalFlowOutputDevice(OutputDevice):
        def __init__(self, *args, **kwargs):
            raise RuntimeError("SignalFlowOutputDevice requires the 'signalflow' package to be installed")
