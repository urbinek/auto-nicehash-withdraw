from datetime import datetime
from pathlib import Path
import argparse
import json
import os
import platform
import re
import requests
import rrdtool
import sys


def get_arguments():

    default_conf_path, default_log_path, default_www_log_path, default_db_log_path = get_default_path()

    # Declaration of argparse with return required values/arguments
    parser = argparse.ArgumentParser(description="Auto withdraw tool for NiceHash", add_help=True)
    parser.add_argument('--config', action='store', default='{}/config.json'.format(default_conf_path), required=False, help='Path to config file (default: {}/config.json)'.format(default_conf_path))
    parser.add_argument('--log-path', action='store', default='{}'.format(default_log_path), required=False, help='Path to log directory (default: {})'.format(default_log_path))
    parser.add_argument('--www-log-path', action='store', default='{}'.format(default_www_log_path), required=False, help='Path to www log directory (default: {})'.format(default_www_log_path))
    parser.add_argument('--db-log-path', action='store', default='{}'.format(default_db_log_path), required=False, help='Path to db directory (default: {})'.format(default_db_log_path))
    parser.add_argument('--dry-run', action='store_true', default=False, required=False, help='Run script wihout any withdraws')
    parser.add_argument('--quiet', action='store_false', default=True, required=False, help='Supress some log output.')
    parser.add_argument('--show-config', action='store_true', default=False, required=False, help='Show config and quit.')

    args = parser.parse_args()

    return args

def get_default_path():
    if platform.system() == 'Linux':
        conf_path    = '/etc/anw'
        log_path     = '/var/log/anw'
        www_log_path = '/www'
        db_log_path  = '/db'
    elif platform.system() == 'Windows':
        conf_path     = 'C:/ProgramData/anw'
        log_path      = 'C:/ProgramData/anw/log'
        www_log_path  = 'C:/ProgramData/anw/www'
        db_log_path   = 'C:/ProgramData/anw/db'
    elif platform.system() == 'Darwin':
        sys.exit("Lol, nope")
    else:
        sys.exit("Unsupported OS type.")

    return conf_path, log_path, www_log_path, db_log_path


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


def load_config(config_path=None, quiet=True):
    if not os.path.isfile(config_path):
        if quiet:
            print("[WARNING]: Config file '{}' is missing. Creating new from config template, please update it for full functionality.".format(config_path))
        config_dir = os.path.dirname(os.path.abspath(config_path))
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        create_empty_config(config_path=config_path)

    with open(config_path) as config_json:
        config_path = json.load(config_json)
        return config_path

    return None


def display_obscured_conf(config_path=None):
    print("name: \'{}\'".format(config_path["source"]["name"]))
    print("apiKeyCode: \'{}\'".format(re.sub('[0-9a-zA-Z]', '*', config_path["source"]["apiKeyCode"])))
    print("apiSecretKeyCode: \'{}\'".format(re.sub('[0-9a-zA-Z]', '*', config_path["source"]["apiSecretKeyCode"])))
    print("organizationID: \'{}\'".format(re.sub('[0-9a-zA-Z]', '*', config_path["source"]["organizationID"])))


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


def create_dir(path=None, quiet=True):
    if not os.path.isdir(path):
        if quiet:
            print("[WARNING]: '{}' directory is missing. Creating...".format(path))
        Path(path).mkdir(parents=True, exist_ok=True)
    return path


def get_fees(config):

    treshold_value = config["tresholds"]["maximumBcFee"]

    request = requests.get('https://api2.nicehash.com/main/api/v2/public/service/fee/info')
    fees = request.json()['withdrawal']['BITGO']['rules']['BTC']

    coin = fees['coin']
    nh_fee = fees['intervals'][0]['element']['value']
    bc_fee = format_output(num=fees['intervals'][0]['element']['sndValue'])

    fee_margin = format_output(num=(float(treshold_value) - float(bc_fee)))

    if treshold_value >= bc_fee:
        profit = 'positive'
    else:
        profit = 'negative'

    date = str(datetime.now())

    log = {
        "date": date,
        "coin": coin,
        "nicehash": {
            "fee": nh_fee,
            "type": "%"
        },
        "blockchain": {
            "fee": bc_fee,
            "type": "btc"
        },
        "margin": fee_margin,
        "profit": profit
    }

    return log

def save_fee_in_json(fees, log_file_path):
    try:
        log = "{}".format(json.dumps(fees))
        with open(log_file_path, 'a') as logs:
            logs.write("{},\n".format(log))
            logs.close()
    except Exception as e:
        print("[ERROR] An error occoured during saving log file!")
        print("[ERROR] {}".format(e))
        sys.exit(e)


def save_fee_in_rrd(fee, db_file_path):
    try:
        if not os.path.isfile(db_file_path):
            rrdtool.create(db_file_path,
                '--step', '1200',
                'DS:{}:GAUGE:1800:U:U'.format("bc_btc_fee"),
                'RRA:MAX:0.5:1:2232'
            )
        else:
            rrdtool.update(db_file_path,
                'N:{}'.format(fee)
            )
    except Exception as e:
        print("[ERROR] An error occoured during saving db file!")
        print("[ERROR] {}".format(e))
        sys.exit(e)

def draw_graphs_from_rrd(graph_dir, db_file_path):

    periods = {
        'day': 'MINUTE:10:HOUR:1:MINUTE:120:0:%R',
        'week': 'HOUR:12:DAY:1:DAY:1:0:%A',
        'month': 'WEEK:1:WEEK:1:DAY:1:0:%d'
    }

    for period in periods:
        graphv_args = [
            '--imgformat', 'SVG',
            '--width', '600',
            '--height', '150',
            '--slope-mode',
            '--disable-rrdtool-tag',
            '--start', 'end-1{}'.format(period),
            '--end', 'now',
            '--font', 'DEFAULT:8:Noto Sans',
            '--font', 'TITLE:10:BOLD:Noto Sans',
            '--color', 'CANVAS#31373D',
            '--color', 'BACK#1F262D',
            '--color', 'FONT#FFFFFF',
            '--color', 'MGRID#6A6E73',
            '--color', 'GRID#6A6E73',
            '--color', 'ARROW#FFDD00',
            '--border', '0',
            '--title', 'BC BTC Fee - Last {}'.format(period),
            '--watermark', '{}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")),
            '--vertical-label', 'BTC',
            '--units-exponent', '0',
            '--alt-y-grid',
            '--left-axis-format', f'%.8lf',
            '--units-length', '10',
            '--x-grid', '{}'.format(periods[period]),
            '--right-axis', '1:0',
            '--right-axis-format', f'%.8lf',
            '--right-axis-label', 'BTC',
            'DEF:btc_fee={}:{}:LAST'.format(db_file_path, "bc_btc_fee"),
            'LINE2:btc_fee#FFDD00:  Fee',
            f'GPRINT:btc_fee:LAST:Current\: %0.8lf BTC\t',
            f'GPRINT:btc_fee:MIN:Min\: %0.8lf BTC\t',
            f'GPRINT:btc_fee:MAX:Max\: %0.8lf BTC',
            'TEXTALIGN:center'
        ]

        result = rrdtool.graph('{}/bc_btc_fee-{}.svg'.format(graph_dir, period), graphv_args)

    return result