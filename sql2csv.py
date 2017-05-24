#!/usr/bin/env python3
from argparse import ArgumentParser
from sys import stderr
import csv
import pymssql

options = None
conn = None
cursor = None

def parse_options():
    parser = ArgumentParser()
    parser.add_argument('--server', metavar="SERVER", help="Database server; use SERVER\\instance syntax to specify instance")
    parser.add_argument('--db', metavar="DATABASE", help="Database name")
    parser.add_argument('--user', metavar="USER", help="Database name; use DOMAIN\\user if domain is required")
    parser.add_argument('--password', metavar="PASSWORD", help="Database password")
    parser.add_argument('--table', metavar="TABLE", help="Table name")
    parser.add_argument('--where', metavar="WHERE", help="SQL select WHERE clause to select subset of the table, for example --where='f1 > 100 AND f2 < 200'")

    parser.add_argument('-o', '--output', metavar='FILENAME', help='Output file name')

    global options
    options = parser.parse_args()

    if not options.server:
        parser.error("Server is required, use --server to specify")
    if not options.db:
        parser.error("Database is required, use --db to specify")
    if not options.user:
        parser.error("User name is required, use --user to specify")
    if not options.password:
        parser.error("Password is required, use --password to specify")
    if not options.table:
        parser.error("Table is required, use --table to specify")
    if not options.output:
        parser.error("Output file is required, use --output to specify")

def connect():
    global conn
    conn = pymssql.connect(
        server=options.server,
        database=options.db,
        user=options.user,
        password=options.password
        )
    global cursor
    cursor = conn.cursor(as_dict=True)

def execute():
    sql="SELECT * FROM {}".format(options.table)
    if options.where:
        sql += " WHERE {}".format(options.where)
    cursor.execute(sql)

def save(output_file):
    row = cursor.fetchone()
    if not row:
        print("NOTICE: No rows selected", file=stderr)
        return
    count=1
    csv_writer = csv.DictWriter(output_file, sorted(row.keys()))
    csv_writer.writeheader()
    csv_writer.writerow(row)

    row = cursor.fetchone()
    while row:
        count += 1
        csv_writer.writerow(row)
        if count % 1000:
            print("{} rows processed".format(count), file=stderr, end='\r')
        row = cursor.fetchone()

    print("{} rows processed".format(count), file=stderr)

parse_options()
connect()
execute()

with open(options.output, mode='w') as output_file:
    save(output_file)

conn.close()

