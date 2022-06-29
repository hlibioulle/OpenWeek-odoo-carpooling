# -*- coding: utf-8 -*-

from odoo import models, fields

class SharedVehicle(models.Model):
    _name = 'carpooling.shared_car'
    _description = 'carpooling.shared_car.description'

    driver = fields.Many2one("res.users", "Driver", required=True)
    vehicle_type = fields.Char()

    departure_loc = fields.Char(required=True)
    destination_loc = fields.Char(required=True)
    departure_time = fields.Datetime(required=True)

    avalaible_seats = fields.Integer(required=True)
    
    description = fields.Text()

    passengers = fields.Many2many(comodel_name="carpooling.passenger", string="Passenger")

class Passenger(models.Model):
    _name = "carpooling.passenger"
    _description = "carpooling.passenger.description"
    _inherit = "res.users"

    shared_car = fields.Many2many("res.users", "Passenger")
