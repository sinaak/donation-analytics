from datetime import datetime


class Donation:

    def __init__(self, cmte_id, name, zip_code, transaction_date, transaction_amount, other_id):
        self.cmte_id = cmte_id
        self.name = name
        self.zip_code = zip_code[:5]
        self.transaction_date = transaction_date
        self.transaction_amount = transaction_amount
        self.other_id = other_id
        self.clean()

    def is_clean(self):
        return self.cleaned

    def clean(self):
        self.errors = ''

        self.cleaned = self.clean_other_id() and \
            self.clean_tr_date() and \
            self.clean_zip_code() and \
            self.clean_name() and \
            self.clean_cmte_id() and \
            self.clean_tr_amount()

    def clean_other_id(self):
        if self.other_id == '':
            return True
        else:
            self.errors += 'Other ID\n'
            return False

    def clean_tr_date(self):
        try:
            self.transaction_date = datetime.strptime(
                self.transaction_date, '%m%d%Y')
            return True
        except:
            self.errors += 'Transaction Date\n'
            return False

    def clean_zip_code(self):
        if len(self.zip_code) == 5:
            return True
        else:
            self.errors += 'Zip Code Length\n'
            return False

    def clean_name(self):
        self.name = self.name.strip()
        if self.name != '':
            return True
        else:
            self.errors += 'Name is empty\n'
            return False

    def clean_cmte_id(self):
        if self.cmte_id != '':
            return True
        else:
            self.errors += 'CMTE ID is empty\n'
            return False

    def clean_tr_amount(self):
        if self.transaction_amount != '':
            self.transaction_amount = int(self.transaction_amount)
            return True
        else:
            self.errors += 'Transaction Amount is empty\n'
            return False

    def __str__(self):
        return 'Donation(cmte_id={}, name={}, zip_code={}, t_date={}, t_amount={}, other_id={})'.format(self.cmte_id, self.name, self.zip_code, self.transaction_date, self.transaction_amount, self.other_id)

    def __eq__(self, other):
        return self.name == other.name and self.zip_code == other.zip_code

    def __hash__(self):
        return hash((self.cmte_id, self.name, self.zip_code, self.transaction_date, self.transaction_amount, self.other_id))


class Result:

    def __init__(self, cmte_id, zip_code, year):
        self.cmte_id = cmte_id
        self.zip_code = zip_code
        self.year = year
        self.total = 0
        self.num = 0
        self.amounts = []

    def add(self, amount):
        self.total += amount
        self.num += 1
        self.amounts.append(amount)

    def done(self, percentile):
        index = int(percentile / 100 * len(self.amounts) + 0.5) - 1
        self.percentile = self.amounts[index]

        return

    def __str__(self):
        return '{}|{}|{}|{}|{}|{}'.format(self.cmte_id, self.zip_code, self.year, self.percentile, self.total, self.num)
