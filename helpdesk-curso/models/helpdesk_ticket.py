from odoo import fields, models, api, _


class HelpdeskTicket (models.Model):
    _name = 'helpdesk.ticket'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    date_deadline = fields.Datetime(string='Date limit')

    stage_id = fields.Many2one(
        comodel_name='helpdesk.ticket.stage',
        string='Stage',
        required=False)
    team_id = fields.Many2one(
        comodel_name='helpdesk.team',
        string='Team',
        required=False)
    user_ids = fields.Many2many(
        comodel_name='res.users',
        relation="helpdesk_ticket_users_rel",
        column1="ticket_id", column2="user_id",
        string='Users',
    )
    responsable_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsable')


    def set_responsable(self):
        self.ensure_one()
        self.responsable_id = self.env.user


    # """
    # @api.onchange('team_id')
    # def onchange_method(self):
    #     if self.team_id is not None and self.team_id is not False and self.team_id != [] and \
    #             self.team_id.user_ids is not None and self.team_id.user_ids is not False and self.team_id.user_ids != []:
    #         self.user_ids = [user for user in self.team_id.user_ids]
    # """
