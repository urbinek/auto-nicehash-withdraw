import argparse
import datetime
import json
import os
import platform
import re
import requests
import sys
from pathlib import Path



def get_arguments():

    default_conf_path, default_log_path = get_default_path()

    # Declaration of argparse with return required values/arguments
    parser = argparse.ArgumentParser(description="Auto withdraw tool for NiceHash", add_help=True)
    parser.add_argument('--config', action='store', default='{}/config.json'.format(default_conf_path), required=False, help='Path to config file (default: {}/config.json)'.format(default_conf_path))
    parser.add_argument('--log-path', action='store', default='{}'.format(default_log_path), required=False, help='Path to log directory (default: {})'.format(default_log_path))
    parser.add_argument('--dry-run', action='store_true', default=False, required=False, help='Run script wihout any withdraws')
    parser.add_argument('--show-config', action='store_true', default=False, required=False, help='Show config and quit.')

    args = parser.parse_args()

    return args

def main():

    args = get_arguments()

    config = load_config(config_path=args.config)
    create_log_dirs(log_path=args.log_path)
    
    if args.show_config:
        display_obscured_conf(config=config)
        sys.exit(0)

    get_fees(config=config)
    

    
def get_fees(config):
    treshold_value = config["tresholds"]["maximumBcFee"]

    request = requests.get('https://api2.nicehash.com/main/api/v2/public/service/fee/info')
    fees = request.json()['withdrawal']['BITGO']['rules']['BTC']

    wallet_currency = fees['coin']
    nh_fee = fees['intervals'][0]['element']['value']
    bc_fee = format_output(num=fees['intervals'][0]['element']['sndValue'])

    fee_margin = format_output(num=(float(treshold_value) - float(bc_fee)))

    if treshold_value >= bc_fee:
        profit = 'positive'
    else:
        profit = 'negative'

    date = str(datetime.datetime.now())

    log = {
        'date': date,
        'wallet_currency': wallet_currency,
        'nh': {
            'nh_fee': nh_fee,
            'nh_fee_type': '%'
        },
        'bc': {
            'bc_fee': bc_fee,
            'nh_fee_type': 'btc'
        },
        'fee_margin': fee_margin,
        'profit': profit
    }

    print(log)

def get_default_path():
    if platform.system() == 'Linux':
        conf_path = '/etc/anw'
        log_path  = '/var/log/anw'
    elif platform.system() == 'Windows':
        conf_path = 'C:/ProgramData/anw'
        log_path  = 'C:/ProgramData/anw/log'
    elif platform.system() == 'Darwin':
        sys.exit("Lol, nope")
    else:
        sys.exit("Unsupported OS type.")

    return conf_path, log_path
 

def create_empty_config(config_path=None):
    config_json = {
        'source': {
            'name': 'Example API KEY',
            'apiKeyCode': 'kkkkkkkk-kkkk-kkkk-kkkk-kkkkkkkkkkkk',
            'apiSecretKeyCode': 'ssssssss-ssss-ssss-ssss-ssssssssssssssssssss-ssss-ssss-ssss-ssssssssssss',
            'organizationID': 'oooooooo-oooo-oooo-oooo-oooooooooooo'
        },

        'target': {
            'withdrawalAddressId ': 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
            'currency': 'BTC'
        },

        'tresholds': {
            'maximumBcFee': '0.00001000',
            'currency': 'BTC'
        }
    }

    with open(config_path, 'w') as outfile:
        json.dump(config_json, outfile, indent=4)
        return True

    return None


def load_config(config_path=None):
    print("Loading config file from '{}'".format(config_path))

    if not os.path.isfile(config_path):
        print("[WARNING]: Config file '{}' is missing. Creating new from config template, please update it for full functionality.".format(config_path))
        config_dir = os.path.dirname(os.path.abspath(config_path))
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        create_empty_config(config_path=config_path)
        
    with open(config_path) as config_json:
        config_path = json.load(config_json)
        return config_path

    return None


def format_output(num, output_type='btc'):
    if output_type == 'btc':
        return '{0:,.8f}'.format(num)
    elif output_type == 'mbtc':
        return '{0:,.5f}'.format(num)
    elif output_type == 'bit':
        return '{0:,.2f}'.format(num)
    elif output_type == 'gwei':
        return '{0:,.9f}'.format(num)
    elif output_type in ['satoshi', 'wei']:
        return '{:,}'.format(int(num))
    elif output_type == 'ether':
        return '{0:,.18f}'.format(num)
    else:
        raise Exception('Invalid unit: %s' % output_type)


def display_obscured_conf(config):

    print("name: \'{}\'".format(config["source"]["name"]))
    print("apiKeyCode: \'{}\'".format(re.sub('[0-9a-zA-Z]', '*', config["source"]["apiKeyCode"])))
    print("apiSecretKeyCode: \'{}\'".format(re.sub('[0-9a-zA-Z]', '*', config["source"]["apiSecretKeyCode"])))
    print("organizationID: \'{}\'".format(re.sub('[0-9a-zA-Z]', '*', config["source"]["organizationID"])))

def create_log_dirs(log_path=None):
    print("Logs will be saved under '{}'".format(log_path))

    if not os.path.isdir(log_path):
        print("[WARNING]: log directory '{}' is missing. Creating...".format(log_path))
        Path(log_path).mkdir(parents=True, exist_ok=True)
        return log_path

    return None

if __name__ == "__main__":
    main()
