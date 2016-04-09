#!/usr/bin/python

from processes.daily_process import run_daily_process_country_wise
from processes.notify_email_daily import run_email_process

def main() :
    run_daily_process_country_wise()
    run_email_process()

if __name__ == "__main__" :
    main()
