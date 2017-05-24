Dump SQL Server Table to CSV File
=================================

This script requires `python3` and `pip3`.


Installation
------------

Use `pip3 -r requirements.txt` to install dependencies.


Usage
-----

Run `./sql2csv.py --help` to see command-line options.

To dump the whole table, use
```bash
    ./sql2csv.py --server='xx.xx.xx.xx\INSTANCE' \
    --db='DATABSE'        \
    --user='DOMAIN\USER'  \
    --password='PASSWORD' \
    --table='TABLE'       \
    --output='table.csv'
```

If a subset of the table is required, provide optional `--where='....'` clause.
Note that proper shell quoting is required if where clause contains spaces or
special symbols such as <, >, ".

For example:
```bash
    ./sql2csv.py ...other options... --where='name <> "foobar"'
```

