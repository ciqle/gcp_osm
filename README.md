# gcp_osm [WIP]
Load openstreetmap to GCP bigquery

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
Within GDAL `ogr2ogr` will be responsible for generating these datasets.

### Step 1.1: Generate CSV files of 5 GDAL datasets

### Step 1.2: Transform the CSV files into JSONL
