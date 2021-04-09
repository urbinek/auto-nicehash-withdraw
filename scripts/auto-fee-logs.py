from common.methods import create_log_dirs
from common.methods import display_obscured_conf
from common.methods import get_arguments
from common.methods import get_default_path
from common.methods import get_fees
from common.methods import load_config
import json
import os
import sys


def main():

    args = get_arguments()

    config = load_config(config_path=args.config, log=args.quiet)
    create_log_dirs(log_path=args.log_path, log=args.quiet)
    
    fee = get_fees(config=config)

    log_file_path = '{}/auto-fee-logs.json'.format(args.log_path)
    log = "{}".format(json.dumps(fee))

    try: 
        with open(log_file_path, 'a') as logs:
            logs.write("{},\n".format(log))
            logs.close()
        print(fee)
    except Exception as e:
        print("[ERROR] An error occoured during saving log file!")
        print("[ERROR] {}".format(e))
        sys.exit(e)
    
if __name__ == "__main__":
    main()
