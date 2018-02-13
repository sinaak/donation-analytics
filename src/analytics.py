import os
import sys
import json

from models import Donation, Result


def add_related_donations(donation):
    global donations, repeats, results

    def check(index):
        if not repeats[index]:
            return False

        other = donations[index]
        return donation.cmte_id == other.cmte_id and \
            donation.zip_code == other.zip_code and \
            donation.transaction_date.year == other.transaction_date.year

    new_result = Result(cmte_id=donation.cmte_id,
                        zip_code=donation.zip_code,
                        year=donation.transaction_date.year)
    for index in range(len(donations)):
        if check(index):
            new_result.add(donations[index].transaction_amount)

    new_result.done(percentile)

    results.append(new_result)


def is_repeat_donor(donation):
    global donations

    def check(other):
        return donation == other and \
            donation.transaction_date.year > other.transaction_date.year

    count = 0
    for d in donations:
        if check(d):
            count += 1

    return count > 0


def read_and_process_donations():
    global donations, repeats

    with open(FIELD_POSITIONS_FILE, 'r') as p_file:
        positions = json.load(p_file)
    with open(DONATIONS_FILE, 'r') as d_file:
        lines = d_file.readlines()

    for line in lines:
        line = line.split('|')
        new_donation = Donation(
            cmte_id=line[positions['CMTE_ID']],
            name=line[positions['NAME']],
            zip_code=line[positions['ZIP_CODE']],
            transaction_date=line[positions['TRANSACTION_DT']],
            transaction_amount=line[positions['TRANSACTION_AMT']],
            other_id=line[positions['OTHER_ID']]
        )
        if new_donation.is_clean():
            donations.append(new_donation)

            is_repeat = is_repeat_donor(new_donation)
            repeats.append(is_repeat)
            if is_repeat:
                add_related_donations(new_donation)


def read_percentile():
    global percentile

    with open(PERCENTILE_FILE, 'r') as p_file:
        percentile = int(p_file.read())


if __name__ == '__main__':
    FIELD_POSITIONS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'field_positions.json')

    DONATIONS_FILE = sys.argv[1]
    PERCENTILE_FILE = sys.argv[2]
    OUTPUT_NAME = sys.argv[3]

    global donations, repeats, results
    donations = []
    repeats = []
    results = []

    read_percentile()
    read_and_process_donations()

    with open(OUTPUT_NAME, 'w') as r_file:
        for result in results:
            r_file.write('{}\n'.format(result))
