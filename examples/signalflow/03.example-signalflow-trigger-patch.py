#!/usr/bin/env python3

#--------------------------------------------------------------------------------
# Example: Sequencing the SignalFlow DSP package.
# 
# Requires signalflow: pip3 install signalflow
#
# In this example, a Cymbal patch is created at initialisation.
# Each event triggers the patch, causing its ASREnvelope to be re-triggered.
#--------------------------------------------------------------------------------

from isobar.io.signalflow import SignalFlowOutputDevice
from isobar.timelines.timeline import Timeline
from isobar.pattern.static import PLoop
from isobar.pattern.oscillator import PTri
from signalflow import Patch, WhiteNoise, SVFilter, ASREnvelope

class Cymbal (Patch):
    def __init__(self):
        super().__init__()
        noise = WhiteNoise()
        noise = SVFilter(noise, "high_pass", 5000)
        envelope = ASREnvelope(0, 0, 0.1)
        output = noise * envelope * 0.25
        self.set_output(output)
        self.set_trigger_node(envelope)

output_device = SignalFlowOutputDevice()

cymbal = Cymbal()
cymbal.play()

timeline = Timeline(120, output_device=output_device)
timeline.schedule({
    "type": "trigger",
    "patch": cymbal,
    "duration": PLoop(PTri(16, 0.5, 0.1)),
})
timeline.run()

