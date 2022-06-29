# -*- coding: utf-8 -*-

from odoo import models, fields

#####################################################
#                      COURSE                       #
#####################################################

class course(models.Model):
    _name = 'open_academy.course'
    _description = 'open_academy.course.description'

    title = fields.Char(required=True)
    description = fields.Text()
    responsible_user = fields.Many2one("res.users", "Responsible user", required=True)

    sessions = fields.One2many("open_academy.session", "course", "Sessions", required=True)

#####################################################
#                      SESSION                      #
#####################################################

class session(models.Model):
    _name = 'open_academy.session'
    _description = 'open_academy.session.description'

    name = fields.Char(required=True)

    start_date = fields.Datetime(required=True)#.to_datetime()
    duration = fields.Float(required=True)
    #end_date = fields.Datetime(compute='_compute_end_date')#.to_datetime()

    number_of_seats = fields.Integer(required=True)

    instructor = fields.Many2one("res.partner", "Instructor", required=True, domain=[('is_instructor', '=', True)])
    course = fields.Many2one("open_academy.course", "Course", required=True)

    attendees = fields.Many2many(comodel_name="res.partner", string="Attendees")

    # @api.depends('start_date', 'duration')
    # def _compute_end_date(self):
    #     for record in self:
    #         record.end_date = record.start_date + timedelta(hours=record.duration)

#####################################################
#                EXTENDED PARTNER                   #
#####################################################

class InstructorPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    is_instructor = fields.Boolean(string="Instructor")
    sessions = fields.Many2many(comodel_name="open_academy.session", string="Attended/ing sessions")