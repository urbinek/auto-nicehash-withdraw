from common.methods import create_dir
from common.methods import display_obscured_conf
from common.methods import draw_graphs_from_rrd
from common.methods import get_arguments
from common.methods import get_default_path
from common.methods import get_fees
from common.methods import load_config
from common.methods import save_fee_in_json
from common.methods import save_fee_in_rrd
import json
import os
import sys


def main():

    args = get_arguments()

    if args.quiet:
        print("Loading:\t'{}'".format(args.config))
    config = load_config(config_path=args.config, quiet=args.quiet)
   
    if args.quiet: 
        print("Log path:\t'{}'".format(args.log_path))
    create_dir(path=args.log_path, quiet=args.quiet)

    if args.quiet: 
        print("Web path:\t'{}'".format(args.www_log_path))
    create_dir(path=args.www_log_path, quiet=args.quiet)
    

    log_file_path = '{}/auto-fee-logs.json'.format(args.www_log_path)
    if args.quiet:
        print("Fee logs:\t'{}'".format(log_file_path))
    create_dir(path=args.www_log_path, quiet=args.quiet)

    db_file_path = '{}/bc_btc_fee.rrd'.format(args.db_log_path)
    if args.quiet:
        print("RRD db:\t\t'{}'".format(db_file_path))
    create_dir(path=args.db_log_path, quiet=args.quiet)

    if args.quiet:
        print("Fetching current bc fees...")
    fees = get_fees(config=config)
    print(fees)

    save_fee_in_json(fees=fees, log_file_path=log_file_path)

    save_fee_in_rrd(fee=fees['blockchain']['fee'], db_file_path=db_file_path)
   
    if args.quiet:
        print("Drawing graphs...")
    draw_graphs_from_rrd(graph_dir='/www', db_file_path=db_file_path)

if __name__ == "__main__":
    main()
