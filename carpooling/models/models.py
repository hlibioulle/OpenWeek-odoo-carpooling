# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VehicleTrip(models.Model):
    _name = "carpooling.vehicle_trip"
    _description = "carpooling.vehicle_trip.description"

    driver = fields.Many2one("res.users", "Driver", required=True, default=lambda self: self.env.user)
    driver_uid = fields.Integer(compute="_get_driver_uid", store=True)

    @api.depends('driver')
    def _get_driver_uid(self):
        for record in self:
            record.driver_uid = record.driver.id

    is_current_user = fields.Boolean(compute="_is_current_user_driver")

    @api.depends('driver')
    def _is_current_user_driver(self):
        for record in self:
            record.is_current_user = (record.driver == self.env.user)

    vehicle_type = fields.Char()

    departure_loc = fields.Char(required=True)
    destination_loc = fields.Char(required=True)
    departure_time = fields.Datetime(required=True)

    available_seats = fields.Integer(required=True, string="Available seats")
    remaining_seats = fields.Integer(compute='_remaining_seats', string="Remaining seats")
    
    description = fields.Text()

    passengers = fields.Many2many(comodel_name="res.users", string="Passenger")

    @api.constrains('passengers')
    def _check_number_of_passengers(self):
        for record in self:
            if len(record.passengers) > record.available_seats:
                raise ValidationError(f"Too many passengers ({len(record.passengers)} > {record.available_seats})")

    def do_something(self):
        for record in self:
            if record.remaining_seats <= 0:
                continue
            record.write({'passengers': [fields.Command.link(self.env.uid)] })  
        return True
    
    # @api.onchange('passengers')
    # def _on_passengers_change(self):
    #     return {
    #         'warning': {
    #             'title': "You should NOT do that",
    #             'message': "The passengers list is NOT editable",
    #         }
    #     }

    @api.depends("available_seats", "passengers")
    def _remaining_seats(self):
        for record in self:
            record.remaining_seats = record.available_seats - len(record.passengers)

class Passenger(models.Model):
    _name = "res.users"
    #_description = "carpooling.passenger.description"
    _inherit = "res.users"

    #is_driver = fields.Boolean(string="Is a driver?")
    booked_trips = fields.Many2many(comodel_name="carpooling.vehicle_trip", string="Booked trips")
