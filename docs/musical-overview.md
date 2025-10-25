# Isobar Musical Overview

## Core Concepts
- **Timeline**: Central clock generating musical events at a tempo or synced externally.
- **Pattern**: Declarative generator producing a value stream (notes, durations, velocities, controls) each tick.
- **Event**: Concrete realisation assembled from one or more pattern outputs (eg. note + duration + amplitude).
- **OutputDevice**: Target for events (MIDI, MIDI file, OSC, optional SignalFlow audio graph, etc.).

## Musical Abstractions
- **Pitch Layers**: Arithmetic (PSeries, PRange, PGeom), tonal mapping (PDegree, scales, keys), permutations, arpeggiators.
- **Rhythm Layers**: Euclidean rhythms (PEuclidean), stutters (PStutter), loops / ping‑pong (PLoop, PPingPong), subsequences, resets.
- **Dynamics & Expression**: Velocity sequences plus stochastic modulation (PBrown added to fixed pattern) for evolving dynamics.
- **Form & Structure**: Pattern concatenation, collapse / skipping rests, padding to bar lengths, creep / permutation for variation.
- **Algorithmic Generators**: L‑systems (PLSystem), Markov chains (PMarkov), random walks (PWalk), white / brown noise sources.
- **Control & Modulation**: Warp patterns (tempo curves), fade patterns (gradual note introduction), scalar transforms (normalise, map, wrap).

## Pattern Operations
- **Functional Composition**: Arithmetic operators overload (+, -, *, /, %, **, shifts, comparisons) combining or shaping streams.
- **Temporal Manipulation**: Reset triggers (PReset), counters, impulse generators, ping‑pong reversal, reversible finite sequences.
- **Selection & Filtering**: Choices with weights (PChoice), sampled subsets, skip / flip probability, nearest note / key filtering.
- **Stateful Behaviour**: Brownian drift, Markov transitions, L‑system evolution provide memory and emergent variation.

## Scheduling & Execution
- **Mapping**: `timeline.schedule({...})` binds semantic keys ("note", "duration", "amplitude", etc.) to patterns; each tick pulls next values.
- **Concurrency**: Multiple tracks can be scheduled; each track maintains its own pattern state while sharing the timeline clock.
- **Lifecycle**: Tracks auto‑remove when finite patterns exhaust (unless looped); timeline runs foreground or background.
- **Latency Handling**: Output devices can specify added latency separately from beat-based delays.

## Musical Capabilities
- **Generative Scales / Arpeggios**: Build complex melodic lines by stacking transformations (degree mapping, transposition, palindrome looping).
- **Algorithmic Rhythm**: Euclidean distribution, permutations, probability skips create non-trivial grooves.
- **Adaptive Dynamics**: Combining deterministic accents with stochastic walks produces organic velocity contours.
- **Structural Variation**: Pattern generators that mutate (Markov, L‑system) enable evolving motifs without manual scripting.

## Extensibility
- **Optional Backends**: SignalFlow DSP graph or SuperCollider for synthesis; remains optional to keep core MIDI workflow lean.
- **Custom Patterns**: Users can wrap functions (PFunc), dictionaries, arrays, or create new pattern subclasses for domain needs.
- **Output Abstraction**: Uniform interface allows swapping devices (live MIDI, file rendering, OSC) without changing pattern logic.

## Typical Workflow
1. Define pitch pattern: start with series or scale degrees, then transform (loop, ping‑pong, transpose).
2. Define rhythm & dynamics: attach duration pattern and amplitude pattern (sequence + stochastic modulation).
3. Schedule: pass a dict of property → pattern into `Timeline.schedule`.
4. Run: invoke `timeline.run()` to stream events to chosen output device.

## Design Strengths
- **Declarative**: Musical intent expressed as composable pattern objects rather than imperative loops.
- **Layered Variation**: Independent pitch, rhythm, and dynamics layers encourage rich emergent combinations.
- **Algorithmic Breadth**: Built‑in stochastic, formal grammar, and probabilistic generators cover wide generative techniques.

## Outcome
Facilitates rapid prototyping of algorithmic pieces: concise code establishes evolving melodies, rhythms, and dynamics with minimal explicit state management.
