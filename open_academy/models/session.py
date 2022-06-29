# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta

class session(models.Model):
    _name = 'open_academy.session'
    _description = 'open_academy.session.description'

    name = fields.Char(required=True)

    start_date = fields.Datetime(required=True)#.to_datetime()
    duration = fields.Float(required=True)
    #end_date = fields.Datetime(compute='_compute_end_date')#.to_datetime()

    number_of_seats = fields.Integer(required=True)

    instructor = fields.Many2one("res.partner", "Instructor", required=True)
    course = fields.Many2one("open_academy.course", "Course", required=True)

    # @api.depends('start_date', 'duration')
    # def _compute_end_date(self):
    #     for record in self:
    #         record.end_date = record.start_date + timedelta(hours=record.duration)