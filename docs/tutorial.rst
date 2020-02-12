Tutorial
========

With an activated Python 3 virtual env, clone the repository into your project root folder, install required libraries and copy the package from inside:

.. code-block:: bash

    git clone https://github.com/dougpm/gcp_toolkit.git && \
    cp -r gcp_toolkit/gcp_toolkit gcp_toolkit2 && \
    cp gcp_toolkit/requirements.txt . && \
    pip install -r requirements.txt && \ 
    rm -rf gcp_toolkit && \
    mv gcp_toolkit2 gcp_toolkit

io module
---------

**Using the IO class:**

.. code-block:: python

    import gcp_toolkit as gtk

    io = gtk.IO('your-bucket-name', 'your-dataset-name')

This automatically creates google.cloud.storage and google.cloud.bigquery Client instances,
but you can pass your own to the constructor if you need to specify details.

**Note:** You must have Create Table permissions on the specified dataset.


**Loading data from BigQuery into a pandas Data Frame:**

.. code-block:: python

    df = io.bq_to_df('SELECT fields FROM dataset.table_name')

**Loading data from pandas Data Frame into BigQuery:**

.. code-block:: python

    io.df_to_bq(df, 'dataset.table_name')

**Loading data from Storage bucket into pandas Data Frame:**

.. code-block:: python

    df = io.bucket_to_df('path/to/bucket/files/files_prefix*')

**Moving data from BigQuery to Storage:**

.. code-block:: python

    df = io.bq_to_bucket('SELECT fields FROM dataset.table_name', 
                         'path/to/files/file_name')

**Note:** The above may fail occasionally due to the table being to big to be extracted to a single file.
In that case, you must add a '*' wildcard to the file name, like so:

.. code-block:: python

    df = io.bq_to_bucket('SELECT fields FROM dataset.table_name', 
                         'path/to/files/file_name*')











