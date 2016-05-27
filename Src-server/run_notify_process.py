#!/usr/bin/python

# # run every 5 mins
# # PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin
# # */5 * * * * cd ~/Python/workspace/Compliance-Mirror/Src-server && python run_daily_process.py >> /processes/daily_process.log 2>&1

# # sudo chmod 777 run_daily_process.py

from processes.notify_email_daily import run_email_process

def main() :
    run_email_process()

if __name__ == "__main__" :
    main()
