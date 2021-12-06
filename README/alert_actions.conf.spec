[create_alert_in_kv]
param.app = <string>
* The app containing the target collection
param.collection = <string>
* The target collection name
param.owner = <string>
* The target collection owner. Defaults to 'nobody' if not provided
param._time = <string>
* The time of the alert (or the underlying event)
param.alert_title = <string>
* The title of the alert, which could be parameterised
param.search_name = <string>
* The search name that triggered the alert
param.severity = <string>
* The severity associated with the alert
param.data = <string>
* The event fields as a json string, potentially formed using the tojson command
param.metadata = <string>
* Additional alert status fields as a json string, potentially formed using the tojson command