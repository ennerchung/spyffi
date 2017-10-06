#!/usr/bin/env python

from SPyFFI.Observation import Observation, default

# start from the default settings
inputs = default

inputs['camera']['label'] = 'tranist'
inputs['catalog']['name'] = 'testpattern'
inputs['camera']['subarray'] = 400
inputs['camera']['variablefocus'] = False
inputs['expose']['jitterscale'] = 1.0
inputs['expose']['skipcosmics'] = True
inputs['catalog']['testpatternkw']['randomizemagnitudes'] = True
inputs['observation']['cadencestodo'] = {120:16}
o = Observation(inputs)

o.create()
