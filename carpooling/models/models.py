# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VehicleTrip(models.Model):
    _name = "carpooling.vehicle_trip"
    _description = "carpooling.vehicle_trip.description"

    driver = fields.Many2one("res.users", "Driver", required=True, default=lambda self: self.env.user)
    driver_uid = fields.Integer(compute="_get_driver_uid", store=True)

    # field_lat = fields.Float(string="Latitude")
    # field_lng = fields.Float(string="Longitude")

    @api.depends('driver')
    def _get_driver_uid(self):
        for record in self:
            record.driver_uid = record.driver.id

    is_current_user = fields.Boolean(compute="_is_current_user_driver")

    @api.depends('driver')
    def _is_current_user_driver(self):
        for record in self:
            record.is_current_user = (record.driver == self.env.user)

    vehicle_type = fields.Selection(
        string='Vehicle type',
        selection=[('small_car', 'Small car'), ('medium_car', 'Medium car'), ('big_car', 'Big car'), ('suv', 'SUV'), ('minivan', 'Minivan'), ('minivan', 'Minivan')],
        help="Different possible types of vehicle"
    )

    departure_loc = fields.Char(string="Departure location", required=True)
    destination_loc = fields.Char(string="Destination location", required=True)
    departure_time = fields.Datetime(string="Departure time", required=True)

    available_seats = fields.Integer(required=True, string="Available seats")
    remaining_seats = fields.Integer(compute='_remaining_seats', string="Remaining seats")
    
    description = fields.Text()

    passengers = fields.Many2many(comodel_name="res.users", string="Passengers")

    @api.constrains('passengers')
    def _check_number_of_passengers(self):
        for record in self:
            if len(record.passengers) > record.available_seats:
                raise ValidationError(f"Too many passengers ({len(record.passengers)} > {record.available_seats})")

    # button_txt = fields.Char(compute="_compute_btn_txt")

    # @api.depends("passengers")
    # def _compute_btn_txt(self):
    #     for record in self:
    #         if self.env.user in record.passengers:
    #             record.button_txt = "Cancel booking"
    #         else:
    #             record.button_txt = "Book trip"

    current_user_is_passenger = fields.Boolean(compute="_compute_current_user_is_passenger")
    @api.depends("passengers")
    def _compute_current_user_is_passenger(self):
        for record in self:
            record.current_user_is_passenger = (self.env.user in record.passengers)

    def book_or_cancel(self):
        for record in self:
            if self.env.user in record.passengers:
                record.write({'passengers': [fields.Command.unlink(self.env.uid)] })  
            else:
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
