[![Documentation Status](https://readthedocs.org/projects/gcp-toolkit/badge/?version=latest)](https://gcp-toolkit.readthedocs.io/en/latest/?badge=latest)
# gcp_toolkit: Something to make interacting with Google Cloud Platform APIs easier

## What is it?

**gcp_toolkit** is a Python package that makes it easier to 
perform common operations on **Google Cloud Platform**, such as moving data from
a BigQuery table to Storage or loading it into a **pandas** Data Frame for analysis.

## Main Features
Here are some features:

  - Moving data from BigQuery to Storage
  - Loading data from BigQuery into pandas Data Frame
  - Loading data from pandas Data Frame into BigQuery
  - Loading data from Storage into pandas Data Frame
  - Create folder in Storage bucket

## Usage guide
To use the toolkit, clone this repo into your project root folder and copy the gcp_toolkit package:

```sh
git clone https://github.com/dougpm/gcp_toolkit.git && \
cp -r gcp_toolkit/gcp_toolkit gcp_toolkit2 && \
cp gcp_toolkit/requirements.txt . && \
pip install -r requirements.txt && \ 
rm -rf gcp_toolkit && \
mv gcp_toolkit2 gcp_toolkit
```

Then import it in your code:

```python
import gcp_toolkit as gtk

io = gtk.IO('your-bucket-name', 'your-dataset-name')
```

You can now use methods like:
```python
df = io.bucket_to_df('path/to/bucket/files/files_prefix*')
```

A complete description of funcionalities is available in the [Documentation](https://gcp-toolkit.readthedocs.io/en/latest/tutorial.html).

## License

## Documentation

Documentation is availabe [here](https://gcp-toolkit.readthedocs.io/en/latest/)

## Contributing 

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.
