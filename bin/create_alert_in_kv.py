import json
import requests
import urllib.parse, urllib.error
import sys, os

sys.path.append(os.path.join(os.environ['SPLUNK_HOME'],'etc','apps','SA-VSCode','bin'))
import splunk_debug as dbg
# dbg.enable_debugging(timeout=10)

payload = json.loads(sys.stdin.read())
server_uri=payload.get('server_uri')
config = payload.get('configuration', dict())

collection = urllib.parse.quote(config.get('collection'))
app=urllib.parse.quote(config.get('app') if 'app' in config else payload.get('app'))
owner=urllib.parse.quote(config.get('owner') if 'owner' in config else 'nobody')

# Use all other fields as part of our new row
new_record = {k: config[k] for k in config.keys() - {'collection', 'app', 'owner'}}

# Build the URL for the Splunkd REST endpoint
kv_url = f'{server_uri}/servicesNS/{owner}/{app}/storage/collections/data/{collection}?output_mode=json'
print('DEBUG Built kvstore url=%s' % kv_url, file=sys.stderr)

headers = {
    'Authorization': 'Splunk %s' % payload.get('session_key'),
    'Content-Type': 'application/json'}

print('INFO Adding to kvstore collection=%s with data=%s' % (
    collection, json.dumps(new_record)), file=sys.stderr)

try:
    response = requests.post(url=kv_url, json=new_record, headers=headers, verify=False)
    print('DEBUG server response:', str(response.json()), file=sys.stderr)
except requests.exceptions.RequestException as e:
    print('ERROR Failed to add record:', json.dumps(json.loads(e.read())), file=sys.stderr)
    sys.exit(3)