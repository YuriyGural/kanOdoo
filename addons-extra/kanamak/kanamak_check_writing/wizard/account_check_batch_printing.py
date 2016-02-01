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

from openerp.tools.translate import _

from openerp.osv import fields, osv

class account_check_write(osv.TransientModel):
    _inherit = 'account.check.write'
    _description = 'Print Check in Batch'
    
    def reprint_check_write(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_check_writing', 'sequence_check_number')
        voucher_ids = context.get('active_ids', [])
        new_value = self.browse(cr, uid, ids[0], context=context).new_no
        
        check_status = self.browse(cr, uid, ids[0],context=None).check_print_choice
        if check_status == 're_print':
            if new_value:
                ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': (new_value + 1)})
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            if check_status == 're_print':
                voucher_obj.write(cr, uid, check.id,{'chk_seq':new_value, 'check_status': 're_print'}, context=context)
            elif check_status == 'void':
                voucher_obj.write(cr, uid, check.id,{'check_status': 'void'}, context=context)
            elif check_status == 'clear':
                voucher_obj.write(cr, uid, check.id,{'check_status': 'clear'}, context=context)
        check_layout_report = {
            'top' : 'account.print.check.top.multi',
            'middle' : 'account.print.check.middle.ags',
            'bottom' : 'account.print.check.bottom.multi',
        }
        check_layout = voucher_obj.browse(cr, uid, voucher_ids[0], context=context).company_id.check_layout
        if not check_layout:
            check_layout = 'top'
        report_name=check_layout_report[check_layout]            
                
                
                
        return {
            'type': 'ir.actions.report.xml', 
            'report_name':report_name,
            'datas': {
                'model':'account.voucher',
                'ids': voucher_ids,
                'report_type': 'pdf'
                },
            'nodestroy': True
            }

    def print_check_write(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')
        #update the sequence to number the checks from the value encoded in the wizard
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_check_writing', 'sequence_check_number')
        increment = ir_sequence_obj.read(cr, uid, sequence_id, ['number_increment'])['number_increment']
        new_value = self.browse(cr, uid, ids[0], context=context).check_number
        wizard = self.browse(cr, uid, ids[0], context=context)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})
        #validate the checks so that they get a number
        voucher_ids = context.get('active_ids', [])
        cr.execute("SELECT id FROM account_voucher s  \
                                WHERE s.id in %s \
                                order by partner_id\
                                    ",(tuple(voucher_ids),))
        voucher_ids =  map(lambda x: x[0], cr.fetchall())
        partner_ids = []
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            if not check.partner_id.id in partner_ids:
                check_mumber = new_value
                new_value += increment
            partner_ids.append(check.partner_id.id)
            if check.number and wizard.check_state == 're_print':
                voucher_obj.write(cr, uid, check.id,{'chk_seq':check_mumber, 'check_status': 're_print'}, context=context)
            elif check.number and wizard.check_state == 'void':
                voucher_obj.write(cr, uid, check.id,{'chk_seq':check_mumber, 'check_status': 'void'}, context=context)
#                raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
            elif check.number and wizard.check_state == 'clear':
                voucher_obj.write(cr, uid, check.id,{'chk_seq':check_mumber, 'check_status': 'clear' }, context=context)
#            elif check.number and not wizard.check_state:
#                raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
            elif check.number and not wizard.check_state:
                voucher_obj.write(cr, uid, check.id,{'chk_seq':check_mumber, 'check_status': 'print'}, context=context)
            elif not check.number and not wizard.check_state:
                voucher_obj.write(cr, uid, check.id,{'chk_seq':check_mumber, 'check_status': 'print'}, context=context)
#            voucher_obj.button_proforma_voucher(cr, uid, voucher_ids, context=context)
        #update the sequence again (because the assignation using next_val was made during the same transaction of
        #the first update of sequence)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})
        #print the checks
        check_layout_report = {
            'top' : 'account.print.check.top.multi',
            'middle' : 'account.print.check.middle.ags',
            'bottom' : 'account.print.check.bottom.multi',
        }
        check_layout = voucher_obj.browse(cr, uid, voucher_ids[0], context=context).company_id.check_layout
        if not check_layout:
            check_layout = 'top'
        report_name=check_layout_report[check_layout]    
        return {
            'type': 'ir.actions.report.xml', 
            'report_name':report_name,
            'datas': {
                'model':'account.voucher',
                'ids': voucher_ids,
                'report_type': 'pdf'
                },
            'nodestroy': True
            }

