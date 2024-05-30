const fs = require('fs');
const csv = require('csv-parser');

fs.createReadStream('resources/test.csv')
  .pipe(csv({ separator: ',', quote: '"' }))
  .on('data', (row) => {
    try {
      let geometry = JSON.parse(row['geometry']);
      let osm_id = row['osm_id'];
      let osm_way_id = row['osm_way_id'];
      let osm_version = row['osm_version'];
      let osm_timestamp = row['osm_timestamp'];
      let all_tags = row['all_tags'];

      all_tags = all_tags.replace(/""/g, '\\"');
      all_tags = all_tags.replace(/\r/g, '\\r');
      all_tags = all_tags.replace(/\t/g, '\\t');
      all_tags = all_tags.replace(/\\\\/g, 'DOUBLEBACKSLASH');

      let tags = [];
      let pattern = /"(.*?[^\\])"=>"(.*?[^\\])"(,|$)/g;
      let matches;
      while ((matches = pattern.exec(all_tags)) !== null) {
        let k = matches[1];
        let v = matches[2];
        if (v.endsWith('\\"')) {
          console.error("MATCHED '\\'");
          v += '"';
        }
        k = k.replace(/DOUBLEBACKSLASH/g, '\\\\');
        v = v.replace(/DOUBLEBACKSLASH/g, '\\\\');
        tags.push({ key: k, value: v });
      }

      let json_tags = JSON.stringify(tags);
      try {
        json_tags = JSON.stringify(JSON.parse(json_tags));
      } catch (e) {
        console.error("failed to JSON encode: " + e.message + ", offending data:");
        console.error("\torig: " + all_tags);
        console.error("\tjson: " + json_tags);
      }

      let genc = JSON.stringify(geometry).replace(/"/g, '\\"');
      let output = `{"geometry":"${genc}","osm_id":"${osm_id}","osm_way_id":"${osm_way_id}","osm_version":${osm_version},"osm_timestamp":"${osm_timestamp}","all_tags":${json_tags}}`;
      console.log(output);
    } catch (err) {
      console.error("Error processing row:", err);
    }
  })
  .on('end', () => {
    console.log('CSV file successfully processed');
  });
