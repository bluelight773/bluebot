#!/usr/bin/env python
"""Flask service to handle some basic budget queries for bluelight based on a Google Spreadsheet.
Integrated with FB Messenger Bluebot chatbot.

Originally based on: https://github.com/api-ai/apiai-weather-webhook-sample
"""

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# For calendar computations
import maya
import calendar

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from settings import BUDGET_SS_KEY, BUDGET_WS_NAME

# These are the main entity synonyms used
BUDGET_OVERALL = "overall budget"
BUDGET_BASIC = "basic budget"
BUDGET_BONUS = "bonus budget"

BUDGET_TYPES = {BUDGET_OVERALL, BUDGET_BASIC, BUDGET_BONUS}
# Flask app should start in global layout
app = Flask(__name__)

# Ensure access to the budget doc
scope = ['https://spreadsheets.google.com/feeds']

# Assumes file is in workind dir
credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(os.path.dirname(os.path.realpath(__file__)),
    'bluebot-cff2f5041231.json'), scope)

gc = gspread.authorize(credentials)

# Open budget worksheet
spreadsheet = gc.open_by_key(BUDGET_SS_KEY)
budget_ws = spreadsheet.worksheet(BUDGET_WS_NAME)



@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def _form_standard_response_dict(text):
    """Forms a dictionary with speech, displayText values equal to text and a source of bluebot-webhook"""
    return {
        "speech": text,
        "displayText": text,
        # "data": data,
        # "contextOut": [],
        "source": "bluebot-webhook"
    }

def processRequest(req):
    # Supporting budget queries
    result = req.get("result")
    action = result.get("action")

    # Handle different actions
    if action == "days.left.in.this.month":
        today_month_day = maya.now().day
        today_month = maya.now().month
        today_year = maya.now().year
        if today_month_day < 16:
            num_days_left = 15 - today_month_day + 1
        else:
            # This will count days left in this month and add 15 from the next month
            num_days_left = calendar.monthrange(today_year, today_month)[1] - today_month_day + 1 + 15
        return _form_standard_response_dict("{} days left in budget month including today.".format(num_days_left))

    elif action == "money.spent.this.month":
        # Row 2, Col 3 (C2) has amount spent this month
        amount_spent_this_month_str = budget_ws.cell(2, 3).value
        return _form_standard_response_dict(amount_spent_this_month_str)

    elif action == "money.left.this.month":
        budget_type = req.get("result").get("parameters").get("budget_type")
        if not budget_type:
            budget_type = BUDGET_OVERALL

        amount_left_in_basic_budget_str = budget_ws.cell(2, 7).value
        amount_left_in_bonus_budget_str = budget_ws.cell(2, 11).value
        amount_left_in_summed_budget_str = budget_ws.cell(2, 5).value
        if budget_type == BUDGET_BASIC:
            return _form_standard_response_dict(
                "Amount left in Basic Budget:\n{}\n\nNote: Negative means we're beyond budget :(".format(
                    amount_left_in_basic_budget_str))
        elif budget_type == BUDGET_BONUS:
            return _form_standard_response_dict(
                "Amount left in Bonus Budget:\n{}\n\nNote: Negative means we're beyond budget :(".format(
                    amount_left_in_bonus_budget_str))
        elif budget_type == BUDGET_OVERALL:
            return _form_standard_response_dict(
                "Amount left:"
                "\n-Summed Budget: {}\n-Basic Budget: {}\n-Bonus Budget: {}\n\n"
                "Note: Negative means we're beyond budget :(".format(
                amount_left_in_summed_budget_str, amount_left_in_basic_budget_str, amount_left_in_bonus_budget_str))

        # Some error as budget isn't one of the expected values.
        else:
            return _form_standard_response_dict(
                "Not clear as to which budget you want to know about: Basic Budget, Bonus Budget, Overall Budget.")

    else:
        return {}



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')