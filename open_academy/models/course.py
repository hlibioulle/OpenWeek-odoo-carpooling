# -*- coding: utf-8 -*-

from odoo import models, fields

class course(models.Model):
    _name = 'open_academy.course'
    _description = 'open_academy.course.description'

    title = fields.Char(required=True)
    description = fields.Text()
    responsible_user = fields.Many2one("res.users", "Responsible user", required=True)

    sessions = fields.One2many("open_academy.session", "course", "Sessions", required=True)
