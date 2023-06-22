from odoo import http, _
from odoo.http import request

class CustomerClass(http.Controller):

    @http.route('/custo',auth='public',type='http',website=True)
    def custo_method(self,**kw):
        custo_data = []
        data = request.env['customers.details'].search([])
        for rec in data:
            custo_data.append({
                'Name': rec.name,
                'Dob': rec.dob,
                'Age': rec.age,
                'Gender': rec.gender,
                'City': rec.city,
            })
        print(custo_data)
        return request.render("bike.custo_details",{'custo_data': custo_data})
