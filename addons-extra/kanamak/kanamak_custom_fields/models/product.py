# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp

class product_product(models.Model):
    
    _inherit = 'product.template'

    list_price = fields.Float('List Price', digits_compute=dp.get_precision('Product Price'), help="Base price to compute the customer price. Sometimes called the catalog price.")
    wholesale_price = fields.Float("Wholesale Price", digits_compute=dp.get_precision('Product Price'))
    fleet_price = fields.Float("Fleet Price", digits_compute=dp.get_precision('Product Price'))
    retail_price = fields.Float("Retail Price", digits_compute=dp.get_precision('Product Price'))

    wholesale_margin = fields.Float("Wholesale Margin")
    fleet_margin = fields.Float("Fleet Margin")
    retail_margin = fields.Float("Retail Margin")
    list_margin = fields.Float("List Margin")
    
    interchange_product = fields.Many2one("product.procut", string="Interchange Product", )