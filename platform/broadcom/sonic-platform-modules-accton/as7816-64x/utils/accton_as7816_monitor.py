#!/usr/bin/env python
#
# Copyright (C) 2017 Accton Technology Corporation
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# ------------------------------------------------------------------
# HISTORY:
#    mm/dd/yyyy (A.D.)
#    11/13/2017: Polly Hsu, Create
#    1/10/2018: Jostar modify for as7716_32
#    5/02/2019: Roy Lee modify for as7816_64x
# ------------------------------------------------------------------

try:
    import getopt
    import sys
    import logging
    import logging.config
    import time  # this is only being used as part of the example
    import signal
    from collections import namedtuple
    from as7816_64x.fanutil import FanUtil
    from as7816_64x.thermalutil import ThermalUtil
except ImportError as e:
    raise ImportError('%s - required module not found' % str(e))

# Deafults
VERSION = '1.0'
FUNCTION_NAME = 'accton_as7816_monitor'
DUTY_MAX = 100
DUTY_DEF = 40

FANDUTY_BY_LEVEL={
    'LV_5' : DUTY_DEF,
    'LV_7' : 52,
    'LV_9' : 64,
    'LV_B' : 76,
    'LV_D' : 88,
    'LV_F' : DUTY_MAX,
}
FANLEVEL_BY_DUTY={
    DUTY_DEF : 'LV_5',
    52 : 'LV_7',
    64 : 'LV_9',
    76 : 'LV_B',
    88 : 'LV_D',
    DUTY_MAX : 'LV_F',
}

NA_L = 0
NA_H = 999999
Threshold = namedtuple('Threshold', ['val', 'next_lv'])


UP_TH_F2B = {  #order :0x4D,0x4E,0x48,0x49,0x4A,0x4B
    'LV_5': Threshold([57000,60000,40000,39000,36000,38000], 'LV_7'),
    'LV_7': Threshold([62000,64000,46000,45000,43000,44000], 'LV_B'),
    'LV_9': Threshold([ NA_L, NA_L, NA_L, NA_L, NA_L, NA_L], 'LV_B'), # NA, force to change level.
    'LV_B': Threshold([ NA_H, NA_H,51000,49000,48000,49000], 'LV_D'),
    'LV_D': Threshold([67000,70000,55000,54000,53000,54000], 'LV_F'),
    'LV_F': Threshold([ NA_H, NA_H, NA_H, NA_H, NA_H, NA_H], 'LV_F')  # Won't go any higher.
}
DOWN_TH_F2B = {
    'LV_5': Threshold([ NA_L, NA_L, NA_L, NA_L, NA_L, NA_L], 'LV_5'), # Won't go any lower.
    'LV_7': Threshold([55000,58000,38000,37000,34000,36000], 'LV_5'),
    'LV_9': Threshold([ NA_H, NA_H, NA_H, NA_H, NA_H, NA_H], 'LV_7'), # NA, force to change level.
    'LV_B': Threshold([60000,62000,43000,42000,40000,41000], 'LV_7'),
    'LV_D': Threshold([65000,68000,49000,47000,46000,47000], 'LV_B'),
    'LV_F': Threshold([ NA_H, NA_H,53000,52000,51000,52000], 'LV_D')
}
UP_TH_B2F = {
    'LV_5': Threshold([52000,41000,34000,27000,26000,26000], 'LV_7'),
    'LV_7': Threshold([ NA_H, NA_H,38000,32000,31000,31000], 'LV_9'),
    'LV_9': Threshold([57000,48000,42000,37000,37000,36000], 'LV_B'),
    'LV_B': Threshold([61000,52000,46000,42000,42000,42000], 'LV_D'),
    'LV_D': Threshold([66000,57000,51000,47000,47000,47000], 'LV_F'),
    'LV_F': Threshold([ NA_H, NA_H, NA_H, NA_H, NA_H, NA_H], 'LV_F')  # Won't go any higher.
}
DOWN_TH_B2F = {
    'LV_5': Threshold([ NA_L, NA_L, NA_L, NA_L, NA_L, NA_L], 'LV_5'), # Won't go any lower.
    'LV_7': Threshold([50000,39000,32000,25000,24000,24000], 'LV_5'),
    'LV_9': Threshold([55000,45000,36000,30000,29000,29000], 'LV_7'),
    'LV_B': Threshold([ NA_H, NA_H,40000,35000,34000,34000], 'LV_9'),
    'LV_D': Threshold([59000,50000,44000,40000,40000,40000], 'LV_B'),
    'LV_F': Threshold([63000,55000,48000,45000,45000,45000], 'LV_D')
}

global log_file
global log_level


test_temp = 0
test_temp_list = [0, 0, 0, 0, 0, 0]
test_temp_revert = 0
temp_test_data = 0


def get_temperature(thermal, idx):
    global test_temp_list
    global test_temp
    global temp_test_data
    global test_temp_revert

    start_idx = thermal.get_idx_thermal_start()
    last_idx = start_idx + thermal.get_num_thermals() - 1

    if test_temp == 0:
        return thermal._get_thermal_node_val(idx)

    temp = test_temp_list[idx - start_idx] + temp_test_data

    if idx == last_idx:
        if test_temp_revert == 0:
            temp_test_data = temp_test_data+2000
        else:
            temp_test_data = temp_test_data-2000
    temp = (temp/1000)*1000
    logging.debug('set test temp %d to thermal%d', temp, idx)
    return temp

# Make a class we can use to capture stdout and sterr in the log
class accton_as7816_monitor(object):
    # static temp var
    _ori_temp = 0
    _new_perc = 0
    _ori_perc = 0

    def __init__(self, log_file, log_level):
        """Needs a logger and a logger level."""

        self.thermal = ThermalUtil()
        self.fan = FanUtil()
        self.is_fan_f2b = self.fan.get_fan_dir(self.fan.get_idx_fan_start()) == 0
        self.up_th = UP_TH_F2B if self.is_fan_f2b == True else UP_TH_B2F
        self.down_th = DOWN_TH_F2B if self.is_fan_f2b == True else DOWN_TH_B2F

        # set up logging to file
        logging.basicConfig(
            filename=log_file,
            filemode='w',
            level=log_level,
            format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )

        # set up logging to console
        if log_level == logging.DEBUG:
            console = logging.StreamHandler()
            console.setLevel(log_level)
            formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)

        logging.debug('SET. logfile:%s / loglevel:%d', log_file, log_level)

    def manage_fans(self):
        thermal = self.thermal
        fan = self.fan
        for x in range(fan.get_idx_fan_start(), fan.get_num_fans()+1):
            fan_status = fan.get_fan_status(x)
            if fan_status is None:
                logging.debug('INFO. SET new_perc to %d (FAN stauts is None. fan_num:%d)', DUTY_MAX, x)
                return False
            if fan_status is False:             
                logging.debug('INFO. SET new_perc to %d (FAN fault. fan_num:%d)', DUTY_MAX, x)
                fan.set_fan_duty_cycle(DUTY_MAX)
                return True
            #logging.debug('INFO. fan_status is True (fan_num:%d)', x)
 
        #Find if current duty matched any of define duty. 
        #If not, set it to highest one.
        cur_duty_cycle = fan.get_fan_duty_cycle()
        fanlevel = FANLEVEL_BY_DUTY.get(cur_duty_cycle, 'LV_F')

        # decide target level by thermal sensor input.
        can_level_up = False
        can_level_down = True
        start_idx = thermal.get_idx_thermal_start()
        end_idx = start_idx + thermal.get_num_thermals()
        for i in range(start_idx, end_idx):
            temp = get_temperature(thermal, i)
            th_idx = i - start_idx
            high = self.up_th[fanlevel].val[th_idx]
            low = self.down_th[fanlevel].val[th_idx]
            # perform level up if anyone is higher than high_th.
            if  temp >= high:
                can_level_up = True
                break
            # cancel level down if anyone is higher than low_th.
            if temp > low:
                can_level_down = False

        if can_level_up:
            next_fanlevel = self.up_th[fanlevel].next_lv
        elif can_level_down:
            next_fanlevel = self.down_th[fanlevel].next_lv
        else:
            next_fanlevel = fanlevel
        new_duty_cycle = FANDUTY_BY_LEVEL.get(next_fanlevel, DUTY_MAX)


        if(new_duty_cycle != cur_duty_cycle):
            logging.debug('set fanduty from %d to %d', cur_duty_cycle , new_duty_cycle)
            fan.set_fan_duty_cycle(new_duty_cycle)
        return True

def handler(signum, frame):
    fan = FanUtil()
    logging.debug('INFO:Cause signal %d, set fan speed max.', signum)
    fan.set_fan_duty_cycle(DUTY_MAX)
    sys.exit(0)

def main(argv):
    global test_temp
    log_file = '%s.log' % FUNCTION_NAME
    log_level = logging.INFO
    if len(sys.argv) != 1:
        try:
            opts, args = getopt.getopt(argv,'hdlt:',['lfile='])
        except getopt.GetoptError:
            print('Usage: %s [-d] [-l <log_file>]' % sys.argv[0])
            return 0
        for opt, arg in opts:
            if opt == '-h':
                print('Usage: %s [-d] [-l <log_file>]' % sys.argv[0])
                return 0
            elif opt in ('-d', '--debug'):
                log_level = logging.DEBUG
            elif opt in ('-l', '--lfile'):
                log_file = arg

        if sys.argv[1] == '-t':
            if len(sys.argv) != 8:
                print("temp test, need input 6 temp")
                return 0
            i = 0
            for x in range(2, 8):
                test_temp_list[i] = int(sys.argv[x])*1000
                i = i+1
            test_temp = 1
            log_level = logging.DEBUG
            print(test_temp_list)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    monitor = accton_as7816_monitor(log_file, log_level)

    # Loop forever, doing something useful hopefully:
    while True:
        monitor.manage_fans()
        time.sleep(10)

if __name__ == '__main__':
    main(sys.argv[1:])