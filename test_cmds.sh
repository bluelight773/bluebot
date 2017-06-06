# TODO: Should turn into Python tests, but for now a list of curl commands
# Assuming we've run python app.py

curl -H "Content-type: application/json" -X POST -d '{"result":{"action":"days.left.in.this.month"}}' http://localhost:5000/webhook

curl -H "Content-type: application/json" -X POST -d '{"result":{"action":"money.spent.this.month"}}' http://localhost:5000/webhook

curl -H "Content-type: application/json" -X POST -d '{"result":{"action":"money.left.this.month", "parameters":{"budget_type":"basic budget"}}}' http://localhost:5000/webhook
curl -H "Content-type: application/json" -X POST -d '{"result":{"action":"money.left.this.month", "parameters":{"budget_type":"bonus budget"}}}' http://localhost:5000/webhook
curl -H "Content-type: application/json" -X POST -d '{"result":{"action":"money.left.this.month", "parameters":{"budget_type":"overall budget"}}}' http://localhost:5000/webhook