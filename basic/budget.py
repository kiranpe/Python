#!/usr/bin/env python3

host_charge = 0.51

per_day = 24 * host_charge
per_month = 30 * host_charge

per_20servers_day = 20 * per_day
per_20servers_month = 20 * per_month

budget = 918
operate_days = budget / per_day

print("Cost to operate one server per day: ${:.2f}".format(per_day))
print("Cost to operate one server per month: ${:.2f}".format(per_month))
print("Cost to operate twenty servers per day: ${:.2f}".format(per_20servers_day))
print("Cost to operate twenty servers per month: ${:.2f}".format(per_20servers_month))
print("One Server operate with budget ${0:.2f} and cost for day ${1:.2f}: {2:.0f} days".format(budget,per_day,operate_days))
