#!/usr/bin/env python3
# License: CC0 https://creativecommons.org/publicdomain/zero/1.0/

import csv
import datetime


def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source..
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


def main():
    with open("grants2.csv", "r") as f:
        reader = csv.DictReader(f)

        first = True

        print("""insert into donations (donor, donee, amount, donation_date,
        donation_date_precision, donation_date_basis, cause_area, url,
        donor_cause_area_url, notes, affected_countries,
        affected_regions) values""")

        for row in reader:
            donee = row[' Grantee']

            # FIXME which location do we want?
            location = (row[' Benefiting Locations'] + "; " +
                        row[' Benefiting Populations'] + "; " +
                        row[' Regions'])

            amount = row[' Amount'].replace("$", "").replace(",", "")

            # there's also "Fiscal Year" and "End Date"
            donation_date = convert_date(row[' Start Date'])

            notes = row[' Description']

            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("Ford Foundation"),  # donor
                mysql_quote(donee),  # donee
                amount,  # amount
                mysql_quote(donation_date),  # donation_date
                mysql_quote("day"),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote("FIXME"),  # cause_area
                mysql_quote("http://www.fordfoundation.org/work/our-grants/grants-database/grants-all"),  # url
                mysql_quote("FIXME"),  # donor_cause_area_url
                mysql_quote(notes),  # notes
                mysql_quote("FIXME"),  # affected_countries
                mysql_quote(location),  # affected_regions
            ]) + ")")
            first = False
        print(";")


def convert_date(x):
    """Convert date string from D/M/YYYY to YYYY-MM-DD format."""
    return datetime.datetime.strptime(x, "%m/%d/%Y").strftime("%Y-%m-%d")

if __name__ == "__main__":
    main()
