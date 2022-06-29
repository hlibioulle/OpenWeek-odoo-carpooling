# -*- coding: utf-8 -*-

from odoo import models, fields, api

class VehicleTrip(models.Model):
    _name = "carpooling.vehicle_trip"
    _description = "carpooling.vehicle_trip.description"

    driver = fields.Many2one("res.users", "Driver", required=True, default=lambda self: self.env.user)
    vehicle_type = fields.Char()

    departure_loc = fields.Char(required=True)
    destination_loc = fields.Char(required=True)
    departure_time = fields.Datetime(required=True)

    available_seats = fields.Integer(required=True, string="Available seats")
    remaining_seats = fields.Integer(compute='_remaining_seats', string="Remaining seats")
    
    description = fields.Text()

    passengers = fields.Many2many(comodel_name="res.users", string="Passenger")

    def do_something(self):
        for record in self:
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
