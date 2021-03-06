# TA-AlertToKV

Author: Greg Ford

## Update History

| Version | Date         | Comments       |
| ------- | ------------ | -------------- |
| 0.0.1   | Dec 6, 2021  | First version  |
| 0.0.2   | May 23, 2022 | Logging. Fixes |

## Using this App

Install the app. Setup a new KV - or pick an existing one to use. Configure a Splunk alert to use the newly-available action.

If your collection has the following fields, they will be populated: _time, alert_title, data (see below), metadata, search_name severity.

Choose whether to store the event data using the fields from your search results (e.g. `| table a b c`) or to render all of the event data as a single json string in a kv field called `data`. If doing the latter, you can unpack the json at search time using `| inputlookup your_lookup | eval _raw=data | spath | fields - _raw, data`

Mandatory parameters to the action include:
- collection
- app
- owner

Optional parameters:
- alert_title
- severity
- metadata

The `metadata` field is intended to support additional arbitrary fields to describe the status of the alert e.g. `{"status": "open", "escalated": False}`.

## KV Collection Definition

Recommended alert KV definition for collections.conf:

```conf
[acme_alert_kv]
field._time = time
field.alert_title = string
field.data = string
field.search_name = string
field.severity = string
field.metadata = string
```

Recommended lookup definition for transforms.conf:

```conf
[acme_alert_kv_lookup]
collection = sc_alert_kv
external_type = kvstore
fields_list = _time,alert_title,data,metadata,search_name,severity,_key
```

## Troubleshooting

High level error messages:

```
index=_internal sendmodalert
```

App-level error messages:

```
index=_internal source="*/ta-alerttokv.log"
```

To create a test alert - and send detailed error messages to search.log:

```
| makeresults | sendalert create_alert_in_kv param.collection=your_kv param.app=your_app param.owner=Nobody param.storage_format=json
```

