import argparse
import sys

# from common.methods import *
from common.methods import get_arguments
from common.methods import get_default_path
from common.methods import get_fees
from common.methods import load_config
from common.methods import create_log_dirs
from common.methods import display_obscured_conf

import nicehash
host = 'https://api2.nicehash.com'


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
