TA-AlertToKV
----------------------------

       Original author: Greg Ford
       Current maintainer: Greg Ford
       Version: 0.0.1

Update History
----------------------------
       0.0.1 Dec 6, 2021
       --------
       First version

Using this App
----------------------------

Install the app. Setup a new KV - or pick an existing one to use. Configure a Splunk alert to use the newly-available action.

I recommend using `| table a, b, c | tojson` to store all required fields in a single text (json) field that will be written to the `data` value in the KV.

Mandatory parameters to the action include:
- collection
- app
- owner

Optional parameters:
- _time
- alert_title
- search_name
- severity
- data
- metadata

The `metadata` field is intended to store additional arbitrary fields to describe the status of the alert e.g. `{"status": "open", "escalated": False}`.