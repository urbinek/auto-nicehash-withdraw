import requests
import datetime
import json
import re

config_json_path = './config.json'


def main():

    # get tresholds from local config
    global config_json_path
    with open(config_json_path) as config_json:
        config = json.load(config_json)

    treshold_value = config["tresholds"]["maximumBcFee"]

    # get fees from cloud
    request = requests.get('https://api2.nicehash.com/main/api/v2/public/service/fee/info')
    fees = request.json()['withdrawal']['BITGO']['rules']['BTC']

    wallet_currency = fees['coin']
    nh_fee = format_output(num=fees['intervals'][0]['element']['value'])
    bc_fee = format_output(num=fees['intervals'][0]['element']['sndValue'])

    # calculate fee margin
    fee_margin = format_output(num=(float(treshold_value) - float(bc_fee)))

    # make big boy decisions
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

    print(f'{log}, <br>')


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


def display_obscured_conf():
    global config_json_path
    with open(config_json_path) as config_json:
        config = json.load(config_json)

    print("name: \'{}\'".format(config["source"]["name"]))

    print("apiKeyCode: \'{}\'".format(re.sub('[0-9a-zA-Z]', '*', config["source"]["apiKeyCode"])))
    print("apiSecretKeyCode: \'{}\'".format(re.sub('[0-9a-zA-Z]', '*', config["source"]["apiSecretKeyCode"])))
    print("organizationID: \'{}\'".format(re.sub('[0-9a-zA-Z]', '*', config["source"]["organizationID"])))


if __name__ == "__main__":
    main()