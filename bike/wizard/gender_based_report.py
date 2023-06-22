from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError

GENDER = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]


class CustomerGenderWizard(models.TransientModel):

    _name = "customer.wizard"
    _description = "Customer wizard report"

    gender = fields.Selection(GENDER, string="Select Gender")

    def customer_gender_wizard_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['active_model'] = self.env.context.get('active_model','ir.ui.menu')
        data['form'] = self.read(['gender'])[0]
        return self.env.ref('bike.customer_gender_report_action').report_action(self, data=data)













