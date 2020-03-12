from odoo import models, api, fields, _


class HelpdeskSetResponsable(models.TransientModel):
    _name = 'helpdesk.set.responsable'



    def set_responsable(self):
        self.ensure_one()
        ticket = False
        # ticket.responsable_id = self.env.user
