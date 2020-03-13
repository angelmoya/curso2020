from odoo import fields, models, api, _


class HelpdeskTicket (models.Model):
    _name = 'helpdesk.ticket'

    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    # _inherit = ['mail.thread.cc', 'mail.thread.blacklist', 'mail.activity.mixin',
    #             'utm.mixin', 'format.address.mixin', 'phone.validation.mixin']

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
    tickets_qty = fields.Integer(
        string='Tickets Qty',
        compute='_compute_tickets_qty')

    @api.depends('responsable_id')
    def _compute_tickets_qty(self):
        ticket_obj = self.env['helpdesk.ticket']
        for ticket in self:
            tickets = ticket_obj.search(
                ['&',
                   '|',
                     ('responsable_id', '=', ticket.responsable_id.id),
                     ('responsable_id', '=', False),
                   ('stage_id', '=', ticket.stage_id.id)])
            ticket.tickets_qty = len(tickets)

    def set_responsable(self):
        self.ensure_one()
        self.responsable_id = self.env.user

    @api.onchange('name', 'date_deadline')
    def _onchange_description(self):
        if self.name and self.date_deadline:
            self.description = '%s - %s'%(self.name, self.date_deadline)

    @api.model
    def create(self, vals):
        date_deadline = vals.get('date_deadline')
        user_id = vals.get('responsable_id')
        user = self.env['res.users'].browse(user_id)
        vals.update({'description': user.name + date_deadline})
        return super(HelpdeskTicket, self).create(vals)

    # """
    # @api.onchange('team_id')
    # def onchange_method(self):
    #     if self.team_id is not None and self.team_id is not False and self.team_id != [] and \
    #             self.team_id.user_ids is not None and self.team_id.user_ids is not False and self.team_id.user_ids != []:
    #         self.user_ids = [user for user in self.team_id.user_ids]
    # """
