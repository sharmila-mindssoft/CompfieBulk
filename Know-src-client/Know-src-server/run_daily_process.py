#!/usr/bin/python

# # run every 5 mins
# # PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin
# # */5 * * * * cd ~/Python/workspace/Compliance-Mirror/Src-server && python run_daily_process.py >> /processes/daily_process.log 2>&1

# # sudo chmod 777 run_daily_process.py


# from processes.daily_process import run_daily_process_country_wise
# from processes.auto_deletion_process import run_deletion_proess
from processes.auto_start_task import run_daily_process

def main() :
    run_daily_process()
    # run_deletion_proess()

if __name__ == "__main__" :
    main()
