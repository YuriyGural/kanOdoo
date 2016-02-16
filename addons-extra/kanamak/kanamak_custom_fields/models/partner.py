# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions, _

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    tax_id = fields.Char("Tax ID",size=12)
    tax_labor = fields.Char("Tax Labor",size=10)
    tax_area = fields.Char("Tax Area", size=10)
    price_level = fields.Char("Price Level", size=1)