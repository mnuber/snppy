##snppy.py
##
##SNPPy requires data from 23andme.com in the form of a .txt downloadable from their website.
##To use, see help.txt

import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("-f", "--file", required = True, help = "file to work with (required)")

updateGrp = argparser.add_mutually_exclusive_group()
updateGrp.add_argument("-u", "--update", required = False, help = "refreshes the SNP db from the list (very time consuming)", action = "store_true")
updateGrp.add_argument("-r", "--report", required = False, help = "creates an HTML/TXT report from the db", action = "store_true")
updateGrp.add_argument("-i", "--init", required = False, help = "setup SNPPy", action = "store_true")


args = vars(argparser.parse_args())

if args["update"]:
    from database_tools import snpedia_db
    snpedia_db.setup_snpedia(args['file'])
elif args["report"]:
    from database_tools import snpedia_db
    snpedia_db.report(args['file'])
elif args["init"]:
    from database_tools import create_dbs
    create_dbs.setup_snp_db(args['file'])
    create_dbs.setup_dna_db('./data/private/sample.txt', args['file'])
