# Get data from BigQuery
# Insert data to Graph
    
from google.cloud import bigquery

class GetBigQueryData:

    def __init__(self, table_id: str):
        # Construct a BigQuery client object.
        self.client = bigquery.Client()
        self.table_id = table_id
        # TODO(developer): Set table_id to the ID of the table to create.
        # table_id = "your-project.your_dataset.your_table_name"

    def run_job(self):
        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("post_abbr", "STRING"),
                bigquery.SchemaField("date", "DATE"),
            ],
            skip_leading_rows=1,
            time_partitioning=bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="date",  # Name of the column to use for partitioning.
                expiration_ms=7776000000,  # 90 days.
            ),
        )
        uri = "gs://cloud-samples-data/bigquery/us-states/us-states-by-date.csv"

        load_job = self.client.load_table_from_uri(
            uri, self.table_id, job_config=job_config
        )  # Make an API request.

        load_job.result()  # Wait for the job to complete.

        table = self.client.get_table(self.table_id)
        print("Loaded {} rows to table {}".format(table.num_rows, self.table_id))
