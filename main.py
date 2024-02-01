#!/usr/bin/env python
import time
from datetime import datetime
from colorama import Fore, Style
import logging
from rpi import RaspberryPi
import os


user = 'AXO'
today = datetime.now().strftime('%-d_%m_%Y_%H_%M')

# logging.basicConfig(filename=f'session_{user}_{today}.log', filemode='w', format='%(asctime)s - %(message)s',
#                     level=logging.ERROR, handlers=consoleHandler)

logFormatter = logging.Formatter('%(asctime)s - %(message)s')
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.ERROR)

fileHandler = logging.FileHandler(f'/home/pi/Desktop/logs/session_{user}_{today}.log')
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

logging.error('AXO FCT Test')

adapter = RaspberryPi(interface='JLINK', user=user)
logging.error(f'Initiating test for user {user}.')

while True:
    os.system('clear')

    print(f'{Fore.GREEN}<<< AXO Test adapter ready >>>{Style.RESET_ALL}\n\n')
    
    
    time.sleep(1)
    while adapter.check_dut_presence() and not adapter.errors:
        logging.error('DUT detected, test started')
        if not adapter.check_programmer():
            logging.error(f'Test 1/5 {Fore.RED}FAILED {Style.RESET_ALL}no JLlink was found or DUT not responding')
            adapter.finish_test()
            break
        else:
            logging.error(f'Test 1/5 {Fore.GREEN}PASS {Style.RESET_ALL}JLink was found')
        if not adapter.flash_modem_firmware():
            logging.error(f'Test 2/5 {Fore.RED}FAILED {Style.RESET_ALL}DUT not responding')
            adapter.finish_test()
            break
        else:
            logging.error(f'Test 2/5 {Fore.GREEN}PASS {Style.RESET_ALL}modem firmware flashed')
        if not adapter.flash_certificates():
            logging.error(f'Test 3/5 {Fore.RED}FAILED {Style.RESET_ALL}could not generate certificates or DUT not responding')
            adapter.finish_test()
            break
        else:
            logging.error(f'Test 3/5 {Fore.GREEN}PASS {Style.RESET_ALL}certificates provisioned for device {adapter.device_id}')
        if not adapter.flash_app_fw():
            logging.error(f'Test 4/5 {Fore.RED}FAILED {Style.RESET_ALL}no application firmware provided or DUT not responding ')
            adapter.finish_test()
            break
        else:
            logging.error(f'Test 4/5 {Fore.GREEN}PASS {Style.RESET_ALL}Application firmware flashed')
        if not adapter.verify_app_fw():
            logging.error(f'Test 5/5 {Fore.RED}FAILED {Style.RESET_ALL}device output does not match specification')
            adapter.finish_test()
            break
        else:
            logging.error(f'Test 5/5 {Fore.GREEN}PASS {Style.RESET_ALL}application firmware. Info: fw_version: {adapter.fw_ver}, IMSI: {adapter.imsi}')
        if adapter.print_label():
            logging.error(f'Test finished for DUT {adapter.device_id}. Result {Fore.GREEN}PASS{Style.RESET_ALL}')
            print('Test finished')
            adapter.finish_test()
            break
        else:
            print('Printing label FAILED, DUT PASS')
            adapter.finish_test()
            break
