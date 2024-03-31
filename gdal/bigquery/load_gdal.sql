
-- Create points table
create or replace external table `${project_id}.${dataset}.global-points-external` (
    osm_id INTEGER,
    osm_version INTEGER,
    osm_way_id INTEGER,
    osm_timestamp TIMESTAMP,
    geometry STRING,
    all_tags ARRAY<STRUCT<key STRING, value STRING>>
)
OPTIONS (
    format = 'NEWLINE_DELIMITED_JSON',
    uris = ['${gcs_path_for_gdal}/global-points.geojson.csv.jsonl'],
    max_bad_records = 10000
);

create or replace table `${project_id}.${dataset}.global-points`
as
select
    osm_id,
    osm_version,
    osm_way_id,
    osm_timestamp,
    SAFE.ST_GEOGFROMGEOJSON(geometry, make_valid => TRUE) as geometry,
    all_tags
from
    `${project_id}.${dataset}.global-points-external`;

drop table `${project_id}.${dataset}.global-points-external`;

-- Create lines table
create or replace external table `${project_id}.${dataset}.global-lines-external` (
    osm_id INTEGER,
    osm_version INTEGER,
    osm_way_id INTEGER,
    osm_timestamp TIMESTAMP,
    geometry STRING,
    all_tags ARRAY<STRUCT<key STRING, value STRING>>
)
OPTIONS (
    format = 'NEWLINE_DELIMITED_JSON',
    uris = ['${gcs_path_for_gdal}/global-lines.geojson.csv.jsonl'],
    max_bad_records = 10000
);

create or replace table `${project_id}.${dataset}.global-lines`
as
select
    osm_id,
    osm_version,
    osm_way_id,
    osm_timestamp,
    SAFE.ST_GEOGFROMGEOJSON(geometry, make_valid => TRUE) as geometry,
    all_tags
from
    `${project_id}.${dataset}.global-lines-external`;

drop table `${project_id}.${dataset}.global-lines-external`;

-- Create multilinestrings table
create or replace external table `${project_id}.${dataset}.global-multilinestrings-external` (
    osm_id INTEGER,
    osm_version INTEGER,
    osm_way_id INTEGER,
    osm_timestamp TIMESTAMP,
    geometry STRING,
    all_tags ARRAY<STRUCT<key STRING, value STRING>>
)
OPTIONS (
    format = 'NEWLINE_DELIMITED_JSON',
    uris = ['${gcs_path_for_gdal}/global-multilinestrings.geojson.csv.jsonl'],
    max_bad_records = 10000
);

create or replace table `${project_id}.${dataset}.global-multilinestrings`
as
select
    osm_id,
    osm_version,
    osm_way_id,
    osm_timestamp,
    SAFE.ST_GEOGFROMGEOJSON(geometry, make_valid => TRUE) as geometry,
    all_tags
from
    `${project_id}.${dataset}.global-multilinestrings-external`;

drop table `${project_id}.${dataset}.global-multilinestrings-external`;

-- Create other_relations table
create or replace external table `${project_id}.${dataset}.global-other_relations-external` (
    osm_id INTEGER,
    osm_version INTEGER,
    osm_way_id INTEGER,
    osm_timestamp TIMESTAMP,
    geometry STRING,
    all_tags ARRAY<STRUCT<key STRING, value STRING>>
)
OPTIONS (
    format = 'NEWLINE_DELIMITED_JSON',
    uris = ['${gcs_path_for_gdal}/global-other_relations.geojson.csv.jsonl'],
    max_bad_records = 10000
);

create or replace table `${project_id}.${dataset}.global-other_relations`
as
select
    osm_id,
    osm_version,
    osm_way_id,
    osm_timestamp,
    SAFE.ST_GEOGFROMGEOJSON(geometry, make_valid => TRUE) as geometry,
    all_tags
from
    `${project_id}.${dataset}.global-other_relations-external`;

drop table `${project_id}.${dataset}.global-other_relations-external`;

-- Create multilinestrings table
create or replace external table `${project_id}.${dataset}.global-multipolygons-external` (
    osm_id INTEGER,
    osm_version INTEGER,
    osm_way_id INTEGER,
    osm_timestamp TIMESTAMP,
    geometry STRING,
    all_tags ARRAY<STRUCT<key STRING, value STRING>>
)
OPTIONS (
    format = 'NEWLINE_DELIMITED_JSON',
    uris = ['${gcs_path_for_gdal}/global-multipolygons.geojson.csv.jsonl'],
    max_bad_records = 10000
);

create or replace table `${project_id}.${dataset}.global-multipolygons`
as
select
    osm_id,
    osm_version,
    osm_way_id,
    osm_timestamp,
    SAFE.ST_GEOGFROMGEOJSON(geometry, make_valid => TRUE) as geometry,
    all_tags
from
    `${project_id}.${dataset}.global-multipolygons-external`;

drop table `${project_id}.${dataset}.global-multipolygons-external`;
