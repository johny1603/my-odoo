from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError, Warning
from odoo.osv import expression
from lxml import etree
import json

class Payment(models.Model):
    _name = "payment.details"
    _description = "its maintain payment details"

    payment_custo_id = fields.Many2one("customers.details",string="Customer Name")
    payment_date = fields.Date(string="Payment Date")
    payment_amount = fields.Integer(string="Payment Amount")
    payment_desc = fields.Char(string="Description")


