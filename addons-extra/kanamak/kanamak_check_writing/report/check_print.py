# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp.report import report_sxw
from amount_to_words import amount_to_words
from openerp.tools.amount_to_text_en import amount_to_text
from openerp.tools.translate import _

class report_print_check_kanamak(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_print_check_kanamak, self).__init__(cr, uid, name, context)
        self.number_lines = 0
        self.number_add = 0
        self.localcontext.update({
            'time': time,
            'get_lines': self.get_lines,
            'get_invoices': self.get_invoices,
            'fill_stars' : self.fill_stars,
            'total_amt' : self.total_amt,
            'amt_word' : self.amt_word,
            'total_credit':self.total_credit,
            'fill_stars_left' : self.fill_stars_left,
            'fill_zeros_left' : self.fill_zeros_left,
            'format_amount_text' : self.format_amount_text,
             
        })
    
    def fill_stars(self, amount):
#        amount = amount.replace('Dollars',' ')
        if len(amount) < 75:
            stars = 75 - len(amount)
            return ' '.join([amount,'*'*stars])

        else: return amount
        
    def fill_stars_left(self, amount, currency = '$', length = 14):
#        amount = amount.replace('Dollars',' ')
        amount_str = currency + '{:,.2f}'.format(amount)
        amount_str = amount_str.rjust(length,'*')
        return amount_str
    
    def format_amount_text(self, amount,  currency = '$', ):
#        amount = amount.replace('Dollars',' ')
        amount = '{:,.2f}'.format(amount)
        amount = amount.split('.')
        amount_str = _('***%s%s Dollars *** %s Cents *')%(currency,amount[0],amount[1])
        
        return amount_str

    def fill_zeros_left(self, value, length = 10):
#        amount = amount.replace('Dollars',' ')
        value_str = str(value)
        
        value_str = value_str.rjust(length, '0')
        return value_str
    
    def total_amt(self, voucher):
        voucher_obj = self.pool.get('account.voucher')
        total = 0.0
        for voucher in voucher_obj.browse(self.cr, self.uid, [voucher.id]):
            if voucher.line_dr_ids:
                for cr in voucher.line_dr_ids:
#                     if cr.move_line_id.invoice.print_check:
                    total += cr.amount
                    if cr.move_line_id.invoice.credit_available:
                        total = total - cr.move_line_id.invoice.credit_available
        return total

    def total_credit(self, voucher_line):
        inv_obj = self.pool.get('account.invoice')
        credit = 0.0
        if voucher_line['name']:
            inv_id = inv_obj.search(self.cr, self.uid, [('number','=',voucher_line['name'])])
            if not inv_id:
                inv_id = inv_obj.search(self.cr, self.uid, [('supplier_invoice_number','=',voucher_line['name'])])
            credit = inv_obj.browse(self.cr, self.uid, inv_id[0]).credit_available
        return credit

    def amt_word(self, amt,crny):
#        if crny and crny.upper() == 'USD':
#            crny = 'Dollars'
        amount = amount_to_text(amt,currency=crny)
        amount = amount.replace('USD','Dollars')
        return amount

    def get_lines(self, voucher_lines):
        result = []
        res = {}
        self.number_lines = len(voucher_lines)
        cnt = 10
        for voucher in voucher_lines:
            cnt -= 1
            if voucher.move_line_id.invoice and voucher.reconcile:  #voucher.move_line_id.invoice.print_check
                res = {
                    'date_due' : voucher.date_due,
                    'name' : voucher.name or voucher.move_line_id and voucher.move_line_id.invoice and voucher.move_line_id.invoice.supplier_invoice_number,
                    'amount_original' : voucher.amount_original and voucher.amount_original or False,
                    'amount_unreconciled' : voucher.amount_unreconciled and voucher.amount_unreconciled or False,
                    'amount' : voucher.amount and voucher.amount or False,
                    'supplier_invoice_number': voucher.move_line_id and voucher.move_line_id.invoice and voucher.move_line_id.invoice.supplier_invoice_number,
                    'date_invoice': voucher.move_line_id.invoice and  voucher.move_line_id.invoice.date_invoice or False,
                    'residual':voucher and voucher.move_line_id and voucher.move_line_id.invoice and voucher.move_line_id.invoice.residual or 0.0,
                    'date_original' :voucher and voucher.date_original or False, 
                }
#                 
#             else :
#                 res = {
#                     'date_due' : False,
#                     'name' : False,
#                     'amount_original' : False,
#                     'amount_due' : False,
#                     'amount' : False,
#                     'date_invoice' : False,
#                     'residual':0.0
#                 }
                result.append(res)
            if cnt == 0:
                break
#         for i in range(0, min(10,self.number_lines)):
#             if i < self.number_lines:
                
        return result
    
    
    def get_invoices(self, invoice_ids):
        result = []
        res = {}
        self.number_lines = len(invoice_ids)
        for inv in invoice_ids:
            res = {
                    'number' : inv.number,
                    'date_invoice' : inv.date_invoice,
                    'amount_total' : inv.amount_untaxed and inv.amount_untaxed or False,
                    'amount_total' : inv.amount_total and inv.amount_total or False,
                }
            result.append(res)
        return result

report_sxw.report_sxw(
    'report.account.print.check.payroll.maddog',
    'account.voucher',
    'kanamak_check_writing/report/check_print_payroll_maddog.rml',
    parser=report_print_check_kanamak,header=False
)

report_sxw.report_sxw(
    'report.account.print.check.top.kanamak',
    'account.voucher',
    'kanamak_check_writing/report/check_print_top.rml',
    parser=report_print_check_kanamak,header=False
)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
