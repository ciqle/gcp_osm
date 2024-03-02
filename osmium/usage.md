## How to parse PBF to jsonl:

`nohup python3 pbf_parser.py nodes planet-231218.osm.pbf 2>&1 > nodes.log &`

`nohup python3 pbf_parser.py ways planet-231218.osm.pbf 2>&1 > nodes.log &`

`nohup python3 pbf_parser.py relations planet-231218.osm.pbf 2>&1 > nodes.log &`