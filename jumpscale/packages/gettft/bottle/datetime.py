from jumpscale.loader import j

from bottle import Bottle, HTTPResponse

app = Bottle()


@app.route("/prices/date", method="GET")
def get_next_date():
    current_time = j.data.time.utcnow()
    # est is ahead utc with 4 hours means 160000 est is 200000 utc
    if int(current_time.strftime("%H%M%S")) < 140000:
        # date of today
        res = current_time.format("D MMMM YYYY")
    else:
        # date of tomorrow
        next_time = j.data.time.get(current_time.timestamp + 24 * 60 * 60)
        res = next_time.format("D MMMM YYYY")
    return HTTPResponse(
        j.data.serializers.json.dumps({"date": res}),
        status=200,
        headers={"Content-Type": "application/json"},
    )
