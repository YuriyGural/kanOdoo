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
        result = super(account_check_write,self).reprint_check_write(cr, uid, ids, context)
        result['report_name']= 'account.print.check.top.kanamak'                    
        return result

    def print_check_write(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        result = super(account_check_write,self).reprint_check_write(cr, uid, ids, context)   
        result['report_name']= 'account.print.check.top.kanamak'
        return result
