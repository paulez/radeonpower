#!/usr/bin/env python3

import argparse
import logging
from logging import debug, info, warning, error
import time
import re
import sys

DPM_FORCE_PERF_LEVEL = '/sys/class/drm/card0/device/power_dpm_force_performance_level'
DPM_SHADER_CLOCK = '/sys/class/drm/card0/device/pp_dpm_sclk'

def read_sys(path):
    return list(open(path, 'r'))

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
    performance_state = read_dpm_performance_state()[0].strip()
    if force or manual_state != performance_state:
        warning('Performance state is %s, setting to %s.',
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

def list_frequencies(args=None):
    for line in read_dpm_performance_state():
        print(line.strip())
    for line in read_dpm_shader_clock():
        print(line.strip())

def get_valid_frequency_index():
    freq = read_dpm_shader_clock()
    debug('Frequencies: %s', freq)
    pattern = re.compile("^([0-9]+)")
    idx = []
    for line in freq:
        debug('Line: %s', line)
        match = pattern.match(line)
        if match:
            idx.append(match.group(1))
    debug('Index: %s', idx)
    return idx

def set(args):
    frequency = args.frequency
    valid_frequencies = get_valid_frequency_index()
    if frequency in valid_frequencies:
        set_and_maintain_frequency(frequency)
    else:
        print_idx = ','.join(valid_frequencies)
        error('Frequency index %s is not valid, valid index are: %s',
              frequency, print_idx)
        return

def configure_debug(verbose_level):
    if verbose_level:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level)

def main(args):
    parser = argparse.ArgumentParser(
        description=__doc__)
    parser.add_argument('-v', '--verbose', help='Increase verbose level.',
                        action='store_true')

    subparsers = parser.add_subparsers()
    list_parser = subparsers.add_parser('list')
    list_parser.set_defaults(func=list_frequencies)

    set_parser = subparsers.add_parser('set')
    set_parser.add_argument('frequency', help='frequency index to set')
    set_parser.set_defaults(func=set)

    args = parser.parse_args(args)
    configure_debug(args.verbose)

    try:
        args.func(args)
    except AttributeError:
        list()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
