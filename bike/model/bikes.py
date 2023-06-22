from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError, Warning
from odoo.osv import expression
from lxml import etree
import json

class Bike(models.Model):
    _name = "bike.details"
    _description = "its to maintain information about bike details"


    name = fields.Char(string="Name", required=True)
    bike_model = fields.Char(string="Bike Model")
    engine = fields.Char(string="Engine")
    colours = fields.Char(string="Colour")
    year = fields.Integer(string="Year")
    damage = fields.Selection([("yes", "Yes"), ("no", "No")],string="Damage", default='no')
    bike_con = fields.Boolean(string="good condition", default=True)
    delivery_date = fields.Date(string="delivery_date")
    picture = fields.Image("Picture")
    bike_file = fields.Binary("Bike_file")
    cc = fields.Integer("CC")
    details = fields.Text(string="Details")
    customer_id = fields.Many2one("customers.details", string="Customer")
    records = fields.Char(string="Records", compute="_check_record")
    # records = fields.Char(string="Records")
    currency_id = fields.Many2one('res.currency', string="Currency")
    amount = fields.Monetary(string="Amount", required=True)
    count = fields.Char(string="Count", compute='_compute_count')
    status = fields.Selection([("order","Order"),("progress","Progress"),("payment","payment")])

    def action_order(self):
        self.status = 'order'
    def action_progress(self):
        self.status = 'progress'
    def action_payment(self):
        self.status = 'payment'

    #-------------------- default get ORM----------------------------

    # @api.model
    # def default_get(self, fields):
    #     res = super(Bike, self).default_get(fields)
    #     res['details'] = 'bike has good looking'
    #     return res

# -----------------Default get ORM--------------------------------------
    @api.model
    def default_get(self, fields):
        res = super(Bike, self).default_get(fields)
        res['currency_id'] = self.env['res.currency'].search([('name', 'like', 'INR')], limit=1).id
        return res

    #----------------- Name get ORM-------------------------------------
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.bike_model:
                name = rec.name + ' (' + rec.bike_model + ')'
                result.append((rec.id, name))
        return result

# ----------------------Name Create ORM ________________________________
    @api.model
    def name_create(self, bike):
        result = super(Bike, self).name_create(bike)
        return result

#---------------------------- NAME_SEARCH ORM-----------------------------------------------------------------------------------------
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []

        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', operator, name), ('bike_model', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))

# #------------------     UNLINK ORM --------------------------------------------
    def unlink(self):
        for rec in self:
            if rec.bike_con == 1:
                raise ValidationError(_("You cannot delete Good Condition bikes"))
            return super(Bike, self).unlink()

#--------------------------- Search Count ORM / COMPUTE COUNT ORM-------------------
    def _compute_count(self):
        self.count = self.env['customers.details'].search_count([('bike_id', '=', self.id)])

#-----------------------------Url Action-----------------------------------------------------
    def sample_bike(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.bikewale.com/',
            'target': 'new'
        }

#----------------------ONCHANGE decorator--------------
    @api.onchange("delivery_date")
    def _check_delivery_date(self):
        if self.delivery_date and self.delivery_date < fields.date.today():
            raise UserError("Delievry date is not valid please enter the valid date")

    # @api.depends('student_mark_ids')
    # def _compute_percentage(self):
    #     total = 0.0
    #     self.overall_percentage = False
    #     for rec in self:
    #         if rec.student_mark_ids:
    #             stud_mark = rec.student_mark_ids.search([('status','=','pass')])
    #             if stud_mark:
    #                 for mark in stud_mark:
    #                     total = total + mark.total





    #                 rec.overall_percentage = total/len(stud_mark)


        #-------------------Create ORM-------------------------------------
    @api.model
    def create(self, vals):
        print(vals)
        print(self)
        vals['engine'] = 'Petrol'
        return super(Bike, self).create(vals)

    def _check_record(self):
        print(self)
        self.records = self.env['bike.details'].search_count([('year', '>=', '2016')])
        bike_records = self.env['bike.details'].search([])
        print("bike records ", bike_records)
        color_records = self.env['bike.details'].search([('colours', '=', 'blue')])
        print("bike colors", color_records)
        self.write({'colours': 'Fire red'})
        # self.copy({'name': 'MT-15'})

    #     # self.unlink({'colours': 'blue'})
    #
    #     def write(self, vals):
    #         #print(vals)
    #         return super(Bike, self).write(vals)
    #
    #     def copy(self,vals):
    #         #print(vals)
    #         return super(Bike,self).copy(vals)
    #
    #     def unlink(self):
    #         #print(self)
    #         return super(Bike, self).unlink()
    #



class Customer(models.Model):
    _name = "customers.details"
    _description = "this record maintain to customer record"
    _rec_name = "name"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True, tracking=True)
    dob = fields.Date(string="Dob", tracking=True)
    age = fields.Integer(string="Age",tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others','Others')])
    bike_id = fields.Many2one('bike.details', string="Enter the bike info", domain=[('year','=','2018')])
    bike_model = fields.Char(related="bike_id.bike_model")
    engine = fields.Char(related="bike_id.engine")
    colour = fields.Char(related="bike_id.colours")
    staff_id = fields.Many2one('staff.details', string="Salesman")
    street1 = fields.Char(string="Street 1", required=True)
    street2 = fields.Char(string="Street 2")
    city = fields.Char(string="City")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    zip = fields.Char(string="ZIP")
    mail = fields.Char(string="Email")

    #Client_action Function
    @api.model
    def get_customer_details(self):
        print("Python Call")
        val = []
        data = self.env['customers.details'].search([])
        for dt in data:
            val.append((dt.name, dt.dob, dt.age, dt.city))
            print(dt)
            print(val)
        return val


    #ORM concepts try button for name is customer

    def get_cus_details(self):
        print("button is active")

    # -------------------Server Action---------------------
    def customer_server_action(self):
        print("server action function called")
        for record in self:
            record.city = "chennai"

#------------------ constains decorator-----------------
    @api.constrains("age")
    def _check_age(self):
        print("constraints")
        if self.age and self.age <= 18:
            raise UserError("your age age is under 18 so u didn't buy vechile")
#-----------------Default get ORM--------------------------------------
    @api.model
    def default_get(self, fields):
        res = super(Customer, self).default_get(fields)
        res['country_id'] = self.env['res.country'].search([('code', 'like', 'IN')], limit=1).id
        res['state_id'] = self.env['res.country.state'].search([('name', '=', 'Tamil Nadu')], limit=1).id
        return res


    def send_mail(self):
        print("cron called")
        template = self.env.ref('bike.send_mail_template')
        if template:
            template.with_context(name="I am context's value").send_mail(self.id, force_send = True)
        else:
            print("Mail Could not be sent....!")





class Employee(models.Model):
    _name = "staff.details"
    _description = "its has maintain staff all details"
    _rec_name = "staff_name"
    _inherit = ['mail.activity.mixin','mail.thread']

    staff_no = fields.Char(string="Employee ID")
    staff_name = fields.Char(string="Name")
    staff_phone = fields.Char(string="Phone")
    staff_add = fields.Char(string="Address")
    dob = fields.Char(string="DOB")
    staff_cus_ids = fields.One2many('customers.details', 'staff_id', string=" Employee access" )
    age = fields.Char(string="Age")
    # bike_id = fields.Many2one("bike.details",string="Bike_id")

    @api.constrains("staff_phone")
    def _check_phone(self):
        for rec in self:
            if rec.staff_phone.isdigit():
                if len(rec.staff_phone) != 10:
                  raise UserError("Enter the 10 digit valid number")
            else:
                raise UserError("Enter the numeric valid number")

        # -----------------Create ORM------------------------------

    # @api.model
    # def create(self, vals):
    #     for rec in self:
    #         if rec.age and rec.age < 19:
    #              raise ValidationError(_("Your age is under 19 is to work here"))
    #         else:
    #             return super(Employee, self).create(vals)
    def open_customer(self):
        print("customer button called")
        action = self.env.ref("bike.action_customer_details").read()[0]
        print(action)
        return action

    @api.model
    def create(self,vals):
        print(vals)
        vals['staff_no'] = self.env['ir.sequence'].next_by_code('employee.seq')
        return super(Employee,self).create(vals)









