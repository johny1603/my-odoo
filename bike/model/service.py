from odoo import models,fields, api
from odoo.exceptions import UserError
from odoo.osv import expression
from lxml import etree
import json




class Service(models.Model):
    _name = "service.details"
    _description = "its has maintain to bike service details"
    _rec_name = "service_bike_name"

    def name_get(self):
        result = []
        for rec in self:
            if rec.service_bike_name and rec.service_bike_number:
                name = rec.service_bike_name + ' (' + rec.service_bike_number + ')'
                result.append((rec.id, name))
        return result


    service_bike_no = fields.Char(string="Service bike No")
    service_bike_number = fields.Char(string="Bike number")
    service_bike_type = fields.Char(string="Type")
    service_bike_name = fields.Char(string="Bike name")
    service_bike_bill = fields.Image(string="Bikebill")
    service_bike_desc = fields.Html(String="Description")
    service_price = fields.Float(string="Price")
    service_charge = fields.Float(string="Service charge")
    custo_id = fields.Many2one('customers.details',string="Customer Name")
    total_amount = fields.Float(string="Total",compute="_check_total")

    def send_pay_mail(self):
            print("Service template called")
            template = self.env.ref('bike.service_mail_template')
            if template:
                template.with_context(name="I am context's value").send_mail(self.id, force_send=True)
            else:
                print("Mail Could not be sent....!")

    @api.depends("service_price","service_charge","total_amount")
    def _check_total(self):
        self.total_amount = self.service_price + self.service_charge

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(Service, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                   submenu=submenu)
        if view_type == 'form':
            print("Form")
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='service_bike_no']"):
                modifiers = json.loads(node.get('modifiers'))
                modifiers['readonly'] = True
                node.set('modifiers', json.dumps(modifiers))
            # for node in doc.xpath("//field[@name='date_time']"):
            #     modifiers = json.loads(node.get('modifiers'))
            #     modifiers['invisible'] = True
            #     node.set('modifiers', json.dumps(modifiers))
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res



class Spares(models.Model):
    _name = "spare.details"
    _description = "its maintain to bike spare parts details"

    name = fields.Char(string="Spares",required=True)

class User(models.Model):
    _inherit = "res.users"

    emp_id = fields.Many2one("staff.details",string="Staff")
    cus_id = fields.Many2one("customers.details",string="Customer")








