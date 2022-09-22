#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
import socket
import datetime
from collections import Counter
from hashlib import sha1
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

now = datetime.datetime.now()
yyyymmdd = now.strftime('%Y-%m-%d')
nowstr = now.isoformat()

hostname = socket.gethostname()
try:
    ip_address = socket.gethostbyname(hostname)
except socket.gaierror:
    ip_address = '127.0.0.1'

print('Running inspec')

proc = subprocess.Popen(
    ('inspec', 'exec', '--chef-license=accept', '/usr/local/src/inspec/profiles/base', '--reporter', 'json:/tmp/inspec_output.json'),
    stdout=sys.stdout,
    stderr=sys.stdout
)
rc = proc.wait()

if not os.path.exists('/tmp/inspec_output.json'):
    print('/tmp/inspec_output.json doest exist')
    sys.exit(1)

with open('/tmp/inspec_output.json', 'r') as fp:
    data = json.load(fp)

results = []
success_counter = Counter()
fail_counter = Counter()

for profile in data['profiles']:
    name = profile['name']

    profile_base = {
        'name': name,
        'title': profile['title'],
        'version': profile['version'],
        'host': hostname,
        'ip': ip_address,
    }

    for control in profile['controls']:
        for result in control['results']:
            status = result['status']
            if status in ('passed', 'failed'):
                rec = {
                    'control_id': control['id'],
                    'control_title': control['title'],
                    'status': status,
                    '@timestamp': result['start_time']
                }
                rec.update(profile_base)
                id_ = sha1(str(rec).encode()).hexdigest()
                results.append((id_, json.dumps(rec)))

                if status == 'passed':
                    success_counter[name] += 1
                else:
                    fail_counter[name] += 1
            elif status == 'skipped':
                continue
            else:
                print('Unknown status: {0}'.format(status))


summary_results = []

for key in (set(success_counter.keys()) | set(fail_counter.keys())):
    success = success_counter[key]
    fail = fail_counter[key]
    total = success + fail
    success_perc = success / total

    rec = json.dumps({
        '@timestamp': nowstr,
        'inspec_profile': key,
        'host': hostname,
        'ip': ip_address,
        'success_percentange': round(success_perc, 2)
    })
    id_ = sha1(str(rec).encode()).hexdigest()
    summary_results.append((id_, rec))


auth = ('inspec', 'M5pcZ6lsvnOsh8UzLHFl')
es_url = 'https://elasticsearch.uksouth.bink.sh:9200'
# es_url = 'https://localhost:9200'

for i in range(0, len(summary_results), 10):
    index = 'inspec-summary-{0}'.format(yyyymmdd)
    bulk = ''
    for id_, item in summary_results[i:i+10]:
        bulk += json.dumps({"index": {"_index": index, "_id": id_}}) + '\n'
        bulk += item + '\n'

    resp = requests.post(es_url + '/{0}/_bulk'.format(index), auth=auth, data=bulk, verify=False, headers={'Content-Type': 'application/x-ndjson'})
    if resp.status_code == 200:
        print('Submitted bulk summary data')
    else:
        print('Got non-200 status: {0}'.format(resp.status_code))
        print('Response: {0}'.format(resp.text))


for i in range(0, len(results), 10):
    index = 'inspec-results-{0}'.format(yyyymmdd)
    bulk = ''
    for id_, item in results[i:i+10]:
        bulk += json.dumps({"index": {"_index": index, "_id": id_}}) + '\n'
        bulk += item + '\n'

    resp = requests.post(es_url + '/{0}/_bulk'.format(index), auth=auth, data=bulk, verify=False, headers={'Content-Type': 'application/x-ndjson'})
    if resp.status_code == 200:
        print('Submitted bulk results data')
    else:
        print('Got non-200 status: {0}'.format(resp.status_code))
        print('Response: {0}'.format(resp.text))
