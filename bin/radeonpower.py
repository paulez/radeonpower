#!/usr/bin/env python3

import logging
import time

DPM_FORCE_PERF_LEVEL = '/sys/class/drm/card0/device/power_dpm_force_performance_level'
DPM_SHADER_CLOCK = '/sys/class/drm/card0/device/pp_dpm_sclk'

def read_sys(path):
    with open(path, 'r') as sys_file:
        sys_state = sys_file.read()
    return sys_state.strip()

def write_sys(path, value):
    with open(path, 'w') as sys_file:
        sys_file.write(value)

def read_dpm_performance_state():
    return read_sys(DPM_FORCE_PERF_LEVEL)

def read_dpm_shader_clock():
    return read_sys(DPM_SHADER_CLOCK)

def set_dpm_performance_state(value):
    return write_sys(DPM_FORCE_PERF_LEVEL, value)

def set_dpm_shader_clock(value):
    return write_sys(DPM_SHADER_CLOCK, value)

def set_frequency(frequency_index, force=False):
    manual_state = 'manual'
    performance_state = read_dpm_performance_state()
    if force or manual_state != performance_state:
        logging.warning('Performance state is %s, setting to %s.',
                performance_state, manual_state)
        set_dpm_performance_state(manual_state)
        set_dpm_shader_clock(frequency_index)
    else:
        logging.info('frequency set to manual, nothing to do.')

def set_and_maintain_frequency(frequency_index):
    set_frequency(frequency_index, force=True)
    while(True):
        time.sleep(60)
        set_frequency(frequency_index)

logging.basicConfig(level=logging.INFO)
set_and_maintain_frequency('3')
