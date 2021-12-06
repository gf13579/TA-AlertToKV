import json
import requests
import urllib.parse
import urllib.error
import urllib3
import sys, os
import gzip
import csv
import re

sys.path.append(os.path.join(os.environ['SPLUNK_HOME'],'etc','apps','SA-VSCode','bin'))
import splunk_debug as dbg
dbg.enable_debugging(timeout=10)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

payload = json.loads(sys.stdin.read())
server_uri=payload.get('server_uri')
results_file = payload.get('results_file')
search_name=payload.get('search_name')
config = payload.get('configuration', dict())

collection = urllib.parse.quote(config.get('collection'))
app = urllib.parse.quote(config.get('app') if 'app' in config else payload.get('app'))
owner = urllib.parse.quote(config.get('owner') if 'owner' in config else 'nobody')
owner = 'nobody' if owner == '' else owner

# Build the URL for the Splunkd REST endpoint
# kv_url = f'{server_uri}/servicesNS/{owner}/{app}/storage/collections/data/{collection}?output_mode=json'
kv_url = f'{server_uri}/servicesNS/{owner}/{app}/storage/collections/data/{collection}/batch_save?output_mode=json'
print('DEBUG create_alert_in_kv: create_alert_in_kv: Built kvstore url=%s' % kv_url, file=sys.stderr)

# Process the events, removing internal fields and rendering mv as a json list
dicts_to_add = []
# rows = []
with gzip.open(results_file, 'rt') as zip_file:
    # rows = [row for row in csv.DictReader(zip_file)]
    reader = csv.DictReader(zip_file)
    for row in reader:
        for k in row.keys():
            if k.startswith('__mv_') and row[k] != '':
                non_mv_name = re.sub(r"^__mv_", "", k)
                if non_mv_name in row.keys():
                    row[non_mv_name] = row[k].strip('$')
                    row[non_mv_name] = str(row[non_mv_name].split('$;$'))
        new_dict = {key:row[key] for key in row.keys() if not key.startswith('__mv')}
        dicts_to_add.append(new_dict)

# Use all other fields as part of our new row
# dbg.set_breakpoint()

print(f'INFO create_alert_in_kv: dicts_to_add is {str(dicts_to_add)}')

alert_info = {k: config[k] for k in config.keys() - {'collection', 'app', 'owner'}}
for d in dicts_to_add:
    print('INFO create_alert_in_kv: Updating d. Config is {}'.format(str(config)))
    d.update(alert_info)
    d['search_name'] = search_name

# if dicts_to_add: print(f'INFO create_alert_in_kv keys: {dicts_to_add[0].keys()}')

headers = {
    'Authorization': 'Splunk %s' % payload.get('session_key'),
    'Content-Type': 'application/json'}

# print('INFO create_alert_in_kv: Adding to kvstore collection=%s with data=%s' % (collection, json.dumps(dicts_to_add)), file=sys.stderr)

try:
    response = requests.post(url=kv_url, json=dicts_to_add, headers=headers, verify=False)
    print('DEBUG create_alert_in_kv: server response:', str(response.json()), file=sys.stderr)
#except requests.exceptions.RequestException as e:
except Exception as e:
    print('ERROR create_alert_in_kv: Failed to add records:', json.dumps(json.loads(e.read())), file=sys.stderr)
    sys.exit(3)
