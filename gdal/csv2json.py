import csv
import json
import re
import sys

if __name__ == '__main__':
    with open('resources/test.csv', encoding='iso-8859-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            geometry = json.loads(row.get('geometry'))
            osm_id = row.get("osm_id")
            osm_way_id = row.get("osm_way_id")
            osm_version = row.get("osm_version")
            osm_timestamp = row.get("osm_timestamp")
            all_tags = row.get("all_tags")
            all_tags = all_tags.replace('""', '\\"')
            all_tags = all_tags.replace('\r', '\\r')
            all_tags = all_tags.replace('\t', '\\t')
            all_tags = all_tags.replace('\\\\', 'DOUBLEBACKSLASH')

            tags = []
            pattern = r'(?:"(.*?[^\\\\])"=>"(.*?[^\\\\])"(,|$))'
            matches = re.findall(pattern, all_tags)
            for match in matches:
                k = match[0]
                v = match[1]
                if v.endswith('\\"'):
                    print("MATCHED '\\'", file=sys.stderr)  # Use print statement for debugging
                    v += '"'
                k = k.replace('DOUBLEBACKSLASH', '\\\\')
                v = v.replace('DOUBLEBACKSLASH', '\\\\')
                tags.append({"key": k, "value": v})
            json_tags = '[' + ','.join([f'{{"key":"{tag["key"]}","value":"{tag["value"]}"}}' for tag in tags]) + ']'
            try:
                json_tags = json.dumps(json.loads(json_tags))
                # print(json_tags)
            except json.JSONDecodeError as e:
                print(f"failed to JSON encode: {str(e)}, offending data:", file=sys.stderr)
                print(f"\torig: {all_tags}", file=sys.stderr)
                print(f"\tjson: {json_tags}", file=sys.stderr)

            genc = json.dumps(geometry, separators=(',', ':')).replace('"', '\\"')
            output = f'{{"geometry":"{genc}","osm_id":"{osm_id}","osm_way_id":"{osm_way_id}","osm_version":{osm_version},"osm_timestamp":"{osm_timestamp}","all_tags":{json_tags}}}'
            print(output)
