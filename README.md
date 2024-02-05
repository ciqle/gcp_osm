# gcp_osm [WIP]
Load openstreetmap to GCP bigquery

## Step 0: Download OpenStreetMap release from source site
Source file is available on [Planet OSM](https://planet.openstreetmap.org/). The entire full pbf file should be downloaded firstly beforehands.

## Step 1: Load GDAL datasets
(Backgrounds please see [this link](https://gdal.org/drivers/vector/osm.html))
GDAL datasets contain 5 layers:
* points : "node" features that have significant tags attached.
* lines : "way" features that are recognized as non-area.
* multilinestrings : "relation" features that form a multilinestring(type = 'multilinestring' or type = 'route').
* multipolygons : "relation" features that form a multipolygon (type = 'multipolygon' or type = 'boundary'), and "way" features that are recognized as area.
* other_relations : "relation" features that do not belong to the above 2 layers.

### Prerequisites
On your local machine you will firstly need to [install GDAL](https://gdal.org/download.html), recommend to install it with Anaconda.
Within GDAL suite, `ogr2ogr` will be responsible for generating these datasets.

### Step 1.1: Generate CSV files of 5 GDAL datasets
Input: PBF file as geospatial info source, `osmconf.ini` as configuration
The command should be like:

`ogr2ogr -skipfailures -f CSV <path_of_output_csv> <path_of_input_pbf_file> --config OSM_CONFIG_FILE <path_of_osmconf.ini> --config OGR_INTERLEAVED_READING YES --config GDAL_CACHEMAX 20000 --config OSM_MAX_TMPFILE_SIZE 40000 -dialect sqlite -sql "select AsGeoJSON(geometry) AS geometry, osm_id,NULL AS osm_way_id,osm_version,osm_timestamp, replace(all_tags,X'0A','') as all_tags from <layer_type> where ST_IsValid(geometry) = 1"`

For `multipolygons` layer especially the sql would be different: substituting `NULL as osm_way_id` with `osm_way_id`, which means osm_way_id is present only for `multipolygon` layer.

### Step 1.2: Transform the CSV files into JSONL
