import argparse
import json
import logging
import osmium
import sys
import time

from datetime import datetime


def osm_entity_to_dict(osm_entity):
    all_tags = [{"key": tag.k, "value": tag.v} for tag in osm_entity.tags]
    # change "k, v" to "key, value"
    return {"id": osm_entity.id, "all_tags": all_tags}


def osm_entity_to_dict_full(osm_entity):
    base_dict = osm_entity_to_dict(osm_entity)
    # add more fields: version, username, changeset, visible, osm_timestamp
    base_dict.update({
        "version": osm_entity.version,
        "username": osm_entity.user,
        "changeset": osm_entity.changeset,
        "visible": osm_entity.visible,
        "osm_timestamp": int(datetime.timestamp(osm_entity.timestamp)),
    })
    return base_dict


def osm_entity_node_dict(osm_node_entity):
    # add node-specific fields: latitude, longitude
    base_dict = osm_entity_to_dict_full(osm_node_entity)
    if osm_node_entity.location.valid():
        base_dict["latitude"] = osm_node_entity.location.lat
        base_dict["longitude"] = osm_node_entity.location.lon
    else:
        base_dict["latitude"] = None
        base_dict["longitude"] = None
    return base_dict


def osm_entity_way_dict(osm_way_entity):
    # add way-specific fields: nodes
    base_dict = osm_entity_to_dict_full(osm_way_entity)
    base_dict["nodes"] = [{"id": node.ref} for node in osm_way_entity.nodes]
    return base_dict


def osm_entity_relation_dict(osm_relation_entity):
    # add relation-specific fields: members
    base_dict = osm_entity_to_dict_full(osm_relation_entity)
    base_dict["members"] = [{"type": member.type, "id": member.ref, "role": member.role}
                            for member in iter(osm_relation_entity.members)]
    return base_dict


class NodeHandler(osmium.SimpleHandler):

    def __init__(self, file):
        osmium.SimpleHandler.__init__(self)
        self.file = file
        self.processing_counter = 0
        self.last_log_time = time.time()
        self.geo_json_factory = osmium.geom.GeoJSONFactory()

    def node(self, node):
        self.processing_counter = self.processing_counter + 1
        if self.processing_counter % 1000000 == 0:
            logging.info("nodes (processed {}) ".format(str(self.processing_counter))
                         + " " + str(time.time() - self.last_log_time))
            self.last_log_time = time.time()
        node_dict = osm_entity_node_dict(node)
        self.file.write(json.dumps(node_dict) + "\n")


class WayHandler(osmium.SimpleHandler):

    def __init__(self, file):
        osmium.SimpleHandler.__init__(self)
        self.file = file
        self.processing_counter = 0

        self.last_log_time = time.time()
        self.geo_json_factory = osmium.geom.GeoJSONFactory()

    def way(self, way):
        self.processing_counter = self.processing_counter + 1
        if self.processing_counter % 100000 == 0:
            logging.info("ways (processed {}) ".format(str(self.processing_counter))
                         + " " + str(time.time() - self.last_log_time))
            self.last_log_time = time.time()
        way_dict = osm_entity_way_dict(way)
        self.file.write(json.dumps(way_dict) + "\n")


class RelationHandler(osmium.SimpleHandler):

    def __init__(self, file):
        osmium.SimpleHandler.__init__(self)
        self.file = file
        self.processing_counter = 0

        self.last_log_time = time.time()
        self.geo_json_factory = osmium.geom.GeoJSONFactory()

    def relation(self, relation):
        self.processing_counter = self.processing_counter + 1
        if self.processing_counter % 100000 == 0:
            logging.info("relations (processed {}) ".format(str(self.processing_counter))
                         + " " + str(time.time() - self.last_log_time))
            self.last_log_time = time.time()
        relation_dict = osm_entity_relation_dict(relation)
        self.file.write(json.dumps(relation_dict) + "\n")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("type", help="'nodes', 'ways' or 'relations'")
    parser.add_argument("input_pbf", help="the path for input pbf file")
    parser.add_argument("output_path", help="output path")
    
    args = parser.parse_args()

    handler_dict = {
        "nodes": NodeHandler,
        "ways": WayHandler,
        "relations": RelationHandler
    }

    chosen_handler = handler_dict.get(args.type)
    if chosen_handler is None:
        print("Invalid type, please choose from 'nodes', 'ways' or 'relations'.")
        sys.exit(1)

    with open("{}/{}.jsonl".format(args.output_path, args.type), "w") as output_file:
        handler = chosen_handler(output_file)
        # handler.apply_file("resources/greater_london.osm.pbf")
        handler.apply_file(args.input_pbf)

