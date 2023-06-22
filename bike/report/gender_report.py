from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError


class WizardReport(models.AbstractModel):
    _name = "report.bike.gender_report_template"

    def get_data(self,values):
        data, recordsets = [],self.env['customers.details']
        if values['gender']:
            recordsets = recordsets.search([('gender','=',values['gender'])])

        for record in recordsets:
            data.append({
                'name': record.name,
                'dob': record.dob,
                'age': record.age,
                'city': record.city,
            })
        return data
    @api.model
    def _get_report_values(self, docids, data=None):
        print("hello")
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        member = self.env['customers.details'].search([('gender','=',data['form']['gender'])])
        print(data)
        print(member)
        return {
            'doc_ids': docids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'get_data': member,
        }



