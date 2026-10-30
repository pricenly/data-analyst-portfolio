# Bundled dataset

`SampleSuperstore.csv` is the public **Sample Superstore** dataset, widely used
for analytics practice.

- Original source: <https://www.kaggle.com/datasets/vivek468/superstore-dataset-final>
- Records: 10,800 rows, 21 columns, orders from 2015 to 2018
- The file also contains an appended Returns block (806 rows with empty
  order fields); `eda_notebook.py` removes it and reports the count.

It is committed here so the project runs with a single command. Do not treat
these records as client data or as evidence of any company's performance.
