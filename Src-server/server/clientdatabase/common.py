import datetime
from dateutil import relativedelta
from server.clientdatabase.tables import *
from server.common import (
    string_to_datetime
)
from server.clientdatabase.general import (
    convert_datetime_to_date
)


def get_last_7_years():
    seven_years_list = []
    end_year = datetime.datetime.now().year - 1
    start_year = end_year - 5
    iter_value = start_year
    while iter_value <= end_year:
        seven_years_list.append(iter_value)
        iter_value += 1
    return seven_years_list


def get_country_domain_timelines(
    db, country_ids, domain_ids, years, client_id=None
):
    country_wise_timelines = []
    for country_id in country_ids:
        domain_wise_timeline = []
        for domain_id in domain_ids:
            columns = "period_from, period_to"
            condition = "country_id = %s and domain_id = %s "
            condition_val = [country_id, domain_id]
            rows = db.get_data(
                tblClientConfigurations, columns,
                condition, condition_val
            )
            if len(rows) > 0:
                period_from = rows[0]["period_from"]
                period_to = rows[0]["period_to"]
                start_end_dates = []
                for year in years:
                    start_year = year
                    end_year = year+1
                    start_date_string = None
                    end_date_string = None
                    start_date_string = "1-%s-%s" % (
                        db.string_months[period_from],
                        start_year
                    )
                    start_date = string_to_datetime(start_date_string)
                    end_date_string = "%s-%s-%s" % (
                        db.end_day_of_month[period_to],
                        db.string_months[period_to],
                        end_year
                    )
                    end_date = string_to_datetime(end_date_string)
                    r = relativedelta.relativedelta(
                        convert_datetime_to_date(end_date),
                        convert_datetime_to_date(start_date)
                    )
                    if r.years > 0:
                        end_date = (
                            end_date - relativedelta.relativedelta(years=1)
                        )
                    start_end_dates.append(
                        {
                            "year": year,
                            "start_date": start_date,
                            "end_date": end_date
                        }
                    )
                domain_wise_timeline.append(
                    [domain_id, start_end_dates]
                )
        country_wise_timelines.append([country_id, domain_wise_timeline])
    return country_wise_timelines


def calculate_ageing_in_hours(ageing):
        day = ageing.days
        print day
        hour = 0
        # if day > 0:
        #     hour += day * 24
        hour += (ageing.seconds / 3600)
        minutes = (ageing.seconds / 60 % 60)
        if day == 0:
            summary = "%s:%s Hour(s)" % (hour, minutes)
        else :
            summary = "%s Day(s) %s:%s Hour(s)" % (day, hour, minutes)
        return summary


def calculate_years(month_from, month_to):
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    if month_from == 1 and month_to == 12:
        single_years = []
        single_years.append([current_year])
        for i in range(1, 7):
            single_years.append([current_year - i])
        return single_years
    else:
        double_years = []
        if current_month in [int(m) for m in range(month_from, 12+1)]:
            first_year = current_year
            second_year = current_year + 1
            years = [first_year, second_year]
            # print first_year, second_year, years
        elif current_month in [int(m) for m in range(1, month_to+1)]:
            first_year = current_year - 1
            second_year = current_year
            # print first_year, second_year

        for i in range(1, 8):
            if i == 1:
                years = [first_year, second_year]
                # print years
            else:
                first_year = current_year - i
                second_year = first_year + 1
                years = [first_year, second_year]
                # print years

            double_years.append(years)
        # print double_years
        return double_years
