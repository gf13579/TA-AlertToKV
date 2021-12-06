import json
import requests
import urllib.parse
import urllib.error
import urllib3
import sys, os

sys.path.append(os.path.join(os.environ['SPLUNK_HOME'],'etc','apps','SA-VSCode','bin'))
import splunk_debug as dbg
dbg.enable_debugging(timeout=10)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

payload = json.loads(sys.stdin.read())
server_uri=payload.get('server_uri')
search_name=payload.get('search_name')
config = payload.get('configuration', dict())

collection = urllib.parse.quote(config.get('collection'))
app = urllib.parse.quote(config.get('app') if 'app' in config else payload.get('app'))
owner = urllib.parse.quote(config.get('owner') if 'owner' in config else 'nobody')
owner = 'nobody' if owner == '' else owner

# Use all other fields as part of our new row
new_record = {k: config[k] for k in config.keys() - {'collection', 'app', 'owner'}}
new_record['search_name'] = search_name

# Build the URL for the Splunkd REST endpoint
kv_url = f'{server_uri}/servicesNS/{owner}/{app}/storage/collections/data/{collection}?output_mode=json'
# kv_url = f'{server_uri}/servicesNS/{owner}/{app}/storage/collections/data/{collection}/batch_save?output_mode=json'
print('DEBUG create_alert_in_kv: create_alert_in_kv: Built kvstore url=%s' % kv_url, file=sys.stderr)


headers = {
    'Authorization': 'Splunk %s' % payload.get('session_key'),
    'Content-Type': 'application/json'}

print('INFO create_alert_in_kv: Adding to kvstore collection=%s with data=%s' % (
    collection, json.dumps(new_record)), file=sys.stderr)

try:
    response = requests.post(url=kv_url, json=new_record, headers=headers, verify=False)
    print('DEBUG create_alert_in_kv: server response:', str(response.json()), file=sys.stderr)
except requests.exceptions.RequestException as e:
    print('ERROR create_alert_in_kv: Failed to add record:', json.dumps(json.loads(e.read())), file=sys.stderr)
    sys.exit(3)