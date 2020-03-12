from odoo import models, api, fields, _


class HelpdeskSetResponsable(models.TransientModel):
    _name = 'helpdesk.set.responsable'

    tickets_qty = fields.Integer(
        string='Tickets Qty')

    @api.model
    def default_get(self, fields):
        res = super(HelpdeskSetResponsable, self).default_get(fields)
        user_id = self.env.user.id
        tickets = self.env['helpdesk.ticket'].search(
            [('responsable_id', '=', user_id)])
        res['tickets_qty'] = len(tickets)
        return res


    def set_responsable(self):
        self.ensure_one()
        # context = {
        #     'active_id': 3,
        #     'active_model': 'helpdesk.ticket'
        # }
        # context.get('active_ids') = False
        active_id = self.env.context.get('active_id')
        active_model = self.env.context.get('active_model')
        if active_id and active_model and active_model == 'helpdesk.ticket':
            ticket = self.env['helpdesk.ticket'].browse(active_id)
            ticket.responsable_id = self.env.user
