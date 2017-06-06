# budget-chatbot
Budget Chatbot Core Code - attached to a budget Google Spreadsheet - based on API.AI with Facebook Messenger + Heroku Integration

Webhook service that gets Api.ai classification JSON, possibly applies some processing involving a budget Google Spreadsheet, and returns a fulfillment response.


When integrated with Facebook Messenger, this can lead to interactions such as this simple example:
```
human: how much have I spent this month?
bluebot: $2,010

human: how many days left in the budget month?
bluebot: 10 days left in budget month including today.
```

# Deployment
https://heroku.com/deploy

# Notes
Certain files are excluded for privacy reasons, but core code is all included.

Intended to run on Python 3.
