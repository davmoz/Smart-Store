/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event Event payload.
 * @param {!Object} context Metadata for the event.
 */
exports.helloPubSub = (event, context) => {
    const message = event.data
        ? Buffer.from(event.data, 'base64').toString()
        : 'Hello, World';

    // Big Query init
    const {BigQuery} = require('@google-cloud/bigquery');
    const bigquery = new BigQuery({
        projectId: 'pycom-iot',
    });

    // Define datasets and tables
    const datasetId = "mydata"; //Enter your BigQuery dataset name here
    const tableId = 'device_payload';

    // Parse data
    const jsonData = JSON.parse(message);
    const payload_in_hex = jsonData['data'];
    rows = [jsonData]

    let data_decoded;
    if (jsonData.hasOwnProperty('seqNumber')) {

        /**
         * Payload is: TTHHPPPPAAAAMMMM where
         * T = Temperature (1 byte, 8 bits)
         * H = Humidity (1 byte, 8 bits)
         * P = Pressure (2 bytes, 16 bits)
         * A = Air Quality (2 byte, 16 bits)
         * M = Movement last hour (2 bytes, 16 bits)
         */
        const temp = parseInt(payload_in_hex.substring(0, 2), 16);
        const humidity = parseInt(payload_in_hex.substring(2, 4), 16);
        const pressure = parseInt(payload_in_hex.substring(4, 8), 16);
        const air_quality = parseInt(payload_in_hex.substring(8, 12), 16);
        const count_last_hour = parseInt(payload_in_hex.substring(12, 16), 16);

        data_decoded = {};
        data_decoded['Temperature'] = temp;
        data_decoded['Humidity'] = humidity;
        data_decoded['Pressure'] = pressure;
        data_decoded['Air_Quality'] = air_quality;
        data_decoded['Movement'] = count_last_hour;
        data_decoded['Timestamp'] = jsonData['time'];
        data_decoded['full_payload'] = message;
        const parsed_data = [data_decoded];

        bigquery
            .dataset(datasetId)
            .table(tableId)
            .insert(parsed_data).then((foundErrors) => {
            parsed_data.forEach((row) => console.log('Inserted: ', row));

            if (foundErrors && foundErrors.insertErrors !== undefined) {
                foundErrors.forEach((err) => {
                    console.log('Error: ', err);
                })
            }

        })
            .catch((err) => {
                console.error('FROM device_payload INSERT:', err);
            });
    }
};
