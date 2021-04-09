import argparse
import sys

# from common.methods import *
from common.methods import get_default_path
from common.methods import get_fees
from common.methods import load_config
from common.methods import create_log_dirs
from common.methods import display_obscured_conf

import nicehash
host = 'https://api2.nicehash.com'


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

    config = load_config(config_path=args.config, log=args.quiet)
    create_log_dirs(log_path=args.log_path, log=args.quiet)
    
    if args.show_config:
        display_obscured_conf(config_path=args.config)
        sys.exit(0)

    get_fees(config=config)

if __name__ == "__main__":
    main()
