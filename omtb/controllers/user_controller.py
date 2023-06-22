import re
from odoo import api, models, tools, fields, _
from odoo.exceptions import ValidationError, Warning
from odoo import http
from odoo.http import request


class ControllerClass(http.Controller):

    # @http.route('/list_users', auth='user', type='http', website=True)
    # def books_method(self, **kw):
    #     student_data = []
    #     data = request.env['student.details'].search([])
    #     for rec in data:
    #         student_data.append({
    #             'name_seq': rec.name_seq,
    #             'name': rec.name,
    #             'dob': rec.dob,
    #             'age': rec.age,
    #             'gender': rec.gender
    #         })
    #     print(student_data)
    #     return request.render("college.student_details", {'student_data': student_data})

    @http.route('/movie_booking', auth='user', type='http', website=True)
    def movie_booking_form(self):
        country = request.env['res.country'].search([])
        state = request.env['res.country.state'].search([])
        print(state)
        print(country)
        return request.render("omtb.user_movie_form",
                              {'state': state, 'country': country})

    # @api.onchange('age')
    # def age_constrains(self):
    #     for rec in self:
    #         if self.age <= 18:
    #             raise ValidationError(_("Your age must above 18 to book tickets.."))
    #
    # @api.constrains('email')
    # def validate_mail(self):
    #     if self.email and not tools.single_email_re.match(self.email):
    #         raise ValidationError("Email is not valid")
    #
    # @api.onchange('phone_no')
    # def validate_mobile(self):
    #     mo = re.compile("^[6-9]")
    #     for rec in self:
    #         if not mo.match(rec.phone_no) and len(str(rec.phone_no)) != 10:
    #             raise ValidationError(_("Invalid Mobile Number"))
    #         # elif :
    #         #     raise ValidationError(("Invalid Mobile Number"))
    #         return True

    @http.route('/user_form', auth='user', type='http', website=True)
    def user_booking_form(self, **k):
        print(k)
        name = k['name']
        gender = k['gender']
        age = k['age']
        phone_no = k['phone_no']
        email = k['email']
        state_id = k['state']
        country_id = k['country']
        request.env['user.details'].create({
            'user_name': name,
            'user_gender': gender,
            'user_age': age,
            'user_mobile_no': phone_no,
            'user_email_id': email,
            'user_state_id': state_id,
            'user_country_id': country_id,
        })
        return request.render("omtb.booking_success", {})
