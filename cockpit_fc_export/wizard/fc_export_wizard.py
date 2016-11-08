# -*- coding: utf-8 -*-
from openerp import api, fields, models, exceptions
from cStringIO import StringIO
import base64
import xlwt
from datetime import datetime, date
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta


class fc_export_xls(models.TransientModel):
    _name = 'fc.export.xls'


    @api.multi
    def fc_create_xls(self):
        """
        Create an excel export
        """

        self.ensure_one()
        if not self.id:
            return False

        # Chosen dates
        date_start = datetime.strptime(self.data_start_date, DEFAULT_SERVER_DATE_FORMAT).date()
        date_stop = datetime.strptime(self.data_end_date, DEFAULT_SERVER_DATE_FORMAT).date()

        # Check dates
        if date_stop < date_start:
            raise exceptions.Warning('The end date is smaller than the start date.')

        if date_stop.year != date_start.year:
            raise exceptions.Warning('You can export only one year at the time')

        data_year = date_start.year
        company_id_id = self.company_id.id

        # For security
        if not 0 < company_id_id < 1000:
            raise exceptions.Warning('Erreur format company_id')


        query = """    SELECT b.code as account_num,b.name as account_name, c.name as journal_name, extract(year from a.date)::integer as dyear, extract(month from a.date)::integer as dmonth, round(sum(debit),2) as debit, round(sum(credit),2) as credit, round(sum(debit - credit),2) as balance
                          FROM account_move_line a
                          join account_account b on a.account_id = b.id
                          join account_journal c on a.journal_id = c.id
                          where a.date >= '%s'::date and a.date <= '%s'::date and b.company_id = %s
                          group by
                          b.code,b.name, c.name, extract(year from a.date),extract(month from a.date)
                          order by extract(month from a.date), b.code
                    """ % (date_start, date_stop,company_id_id)
        self._cr.execute(query)
        all_data = self._cr.fetchall()



        # Excel Styles :
        # Header Style
        style_header = xlwt.easyxf(
            'font: name Calibri, color-index black, bold on;',
            num_format_str='#,##0.00'
        )
        # Normal style
        style_normal = xlwt.easyxf(
            'font: name Calibri, color-index black;',
            num_format_str='#,##0.00'
        )
        # Date style
        style_date = xlwt.easyxf(
            'font: name Calibri, color-index black;',
            num_format_str='dd-mm-yyyy;@'
        )
        # Integer style
        style_int = xlwt.easyxf(
            'font: name Calibri, color-index black;',
            num_format_str='#'
        )


        company_name = self.company_id.name
        wb = xlwt.Workbook()
        ws = wb.add_sheet(company_name.lower() + '_FC')


        # Write titles
        titles = [
            u'Nom du dossier',
            u'Exercice',
            u'Compte général(Ref)',
            u'Nom(name)',
            u'Journal(jnl)',
            u'Document(docnr)',
            u'Date(date)',
            u'Période',
            u'Débit(debN)',
            u'Crédit(credN)',
            u'Lettrage(match)',
            u'Commentaire(comment)',
            u'Montant(amount)',
            u'Devise(val)',
            u'Report(repN)',
            u'Solde cumulé(cumulN)',
            ]
        x = 0
        for tit in titles:
            ws.write(0,x, tit, style_header)
            x+=1


        # The 2 first columns only need to be filled on first line
        ws.write(1, 0, company_name.upper(), style_normal)
        ws.write(1, 1, data_year, style_int)

        # Write data
        y = 0
        for account_num,account_name, journal_name,dyear,dmonth,debit,credit,balance in all_data:
            y += 1

            period_end_date  = date(dyear, dmonth, 1) + relativedelta(months=1) - relativedelta(days=1)
            period_months = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
            period_txt  = period_months[dmonth - 1] + ' ' + str(dyear)

            ws.write(y, 2, account_num, style_normal)
            ws.write(y, 3, account_name, style_normal)
            ws.write(y, 4, journal_name, style_normal)
            # Empty line : Document(docnr)
            ws.write(y, 6, period_end_date, style_date)
            ws.write(y, 7, period_txt, style_normal)
            ws.write(y, 8, debit, style_normal)
            ws.write(y, 9, credit, style_normal)
            # Empty lines
            ws.write(y, 15, balance, style_normal)


        file_data = StringIO()
        wb.save(file_data)
        out = base64.encodestring(file_data.getvalue())
        filename = 'export_FC.xls'
        self.data_report = out
        self.export_filename = filename

        return {
             'type': 'ir.actions.act_url',
             'url': '/web/binary/download_document?model=fc.export.xls&'
                    'field=data_report&id=%s&filename='
                    'export_FC.xls' % self.id,
             'target': 'self',
        }


    # Wizard fields
    data_report = fields.Binary(string='FC Export Data binary')
    data_start_date = fields.Date( string='Start Date', required=True )
    data_end_date = fields.Date( string='End Date (included)', required=True )
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.user.company_id.id)
