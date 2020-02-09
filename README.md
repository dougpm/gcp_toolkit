# gcp_toolkit: Something to make interacting with Google Cloud Platform APIs easier

## What is it?

**gcp_toolkit** is a Python package providing classes to make it easier to 
perform common operations on **Google Cloud Platform**, such as moving data from
a BigQuery table to Storage, or loading it into a **pandas** Data Frame for analysis.

## Main Features
Here are some features:

  - Moving data from BigQuery to Storage
  - Loading data from BigQuery into pandas Data Frame
  - Loading data from Storage into pandas Data Frame
  - Create "folder" in Storage bucket

## Usage guide
To use the toolkit, clone this repo into your project root folder (will deploy to PyPI in the future)

```sh
git clone https://github.com/dougpm/gcp_toolkit.git
```

Then import it in you code

```python
import gcp_toolkit as gtk

io = gtk.IO('your-bucket-name')

```

You can now use the classes method's such as:

```python
df = io.bucket_to_df('path/to/files')
```

A quick overview of functionalities will be available in the Documentation

## License

## Documentation
The official documentation is hosted on PyData.org: https://pandas.pydata.org/pandas-docs/stable

## Contributing 

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.
