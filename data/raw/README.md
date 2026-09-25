# Raw IEC results

Original municipal election results from the Electoral Commission of South Africa (IEC):
https://results.elections.org.za/home/downloads/me-results

| File | Election | Notes |
|---|---|---|
| `2000_LGE.csv.zip` … `2016_LGE.csv.zip` | 2000, 2006, 2011, 2016 | National results files |
| `2021_provincial/*.csv.zip` | 2021 | Nine provincial files, combined in code by `01_cleaning_2021` |

Files are zipped because GitHub rejects files over 100 MB (and the website upload accepts files up to 25 MB). pandas reads `.csv.zip` files directly, so they never need to be unzipped. Do not combine the 2021 files in Excel: the combined data has 1,084,734 rows, more than Excel's limit of 1,048,576.
