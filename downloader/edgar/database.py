from google.cloud import bigquery
import google.api_core.exceptions
import datetime

# probably need a function to de-dup the table
# that would be called at the end of the day

class database():
    client = None
    dataset = None
    table = None

    def __init__(self):
        self.client = bigquery.Client()
        self.dataset = self.client.dataset('downloader')

        schema = [
            bigquery.SchemaField('SecDocument', 'STRING'),
            bigquery.SchemaField('AcceptanceDatetime', 'DATETIME'),
            bigquery.SchemaField('IssuerTradingSymbol', 'STRING'),
            bigquery.SchemaField('RptOwnerCik', 'STRING'),
            bigquery.SchemaField('RptOwnerName', 'STRING'),
            bigquery.SchemaField('IsDirector', 'BOOLEAN'),
            bigquery.SchemaField('IsOfficer', 'BOOLEAN'),
            bigquery.SchemaField('IsTenPercentOwner', 'BOOLEAN'),
            bigquery.SchemaField('IsOther', 'BOOLEAN'),
            bigquery.SchemaField('TransactionDate', 'DATE'),
            bigquery.SchemaField('TransactionShares', 'FLOAT'),
            bigquery.SchemaField('TransactionPricePerShare', 'FLOAT'),
            bigquery.SchemaField('TransactionAcquired', 'BOOLEAN'),
            bigquery.SchemaField('SharesOwned', 'FLOAT')
        ]

        table_ref = self.dataset.table('form4')
        self.table = bigquery.Table(table_ref, schema=schema)

        # Create the table or pass if it already exists
        try:
            self.table = self.client.create_table(self.table)
        except google.api_core.exceptions.Conflict:
            pass

        assert self.table.table_id == 'form4'


    def insert(self, form4Information):
        year = form4Information['acceptanceDatetime'][0:4]
        month = form4Information['acceptanceDatetime'][4:6]
        day = form4Information['acceptanceDatetime'][6:8]
        hour = form4Information['acceptanceDatetime'][8:10]
        minute = form4Information['acceptanceDatetime'][10:12]
        second = form4Information['acceptanceDatetime'][12:14]
        acceptanceDatetime = year + '-' + month + '-' + day + 'T' + hour + ':' + minute + ':' + second

        year = form4Information['transactionDate'][0:4]
        month = form4Information['transactionDate'][5:7]
        day = form4Information['transactionDate'][8:10]
        transactionDate = year + '-' + month + '-' + day

        if(form4Information['transactionAcquiredDisposedCode']=='A'):
            transactionAcquired = True
        else:
            transactionAcquired = False

        row = (
            form4Information['secDocument'],
            acceptanceDatetime,
            form4Information['issuerTradingSymbol'],
            form4Information['rptOwnerCik'],
            form4Information['rptOwnerName'],
            form4Information['isDirector'],
            form4Information['isOfficer'],
            form4Information['isTenPercentOwner'],
            form4Information['isOther'],
            transactionDate,
            form4Information['transactionShares'],
            form4Information['transactionPricePerShare'],
            transactionAcquired,
            form4Information['sharesOwned'],
        )
        rows=[row]
        result = self.table.insert_data(rows)

        if result != []:
            print(rows)
            print(result)
