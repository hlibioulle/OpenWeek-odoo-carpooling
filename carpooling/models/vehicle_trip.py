# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VehicleTrip(models.Model):
    _name = "carpooling.vehicle_trip"
    _description = "This model represents a trip that is going from somewhere to somewhere at a given date and time with the corresponding driver and passengers"

    driver = fields.Many2one("res.users", "Driver", required=True, default=lambda self: self.env.user)
    driver_uid = fields.Integer(compute="_get_driver_uid", store=True)

    @api.depends('driver')
    def _get_driver_uid(self):
        for record in self:
            record.driver_uid = record.driver.id

    is_current_user_driver = fields.Boolean(compute="_is_current_user_driver")

    @api.depends('driver')
    def _is_current_user_driver(self):
        for record in self:
            record.is_current_user_driver = (record.driver == self.env.user)

    vehicle_type = fields.Selection(
        string='Vehicle type',
        selection=[('small_car', 'Small car'), ('medium_car', 'Medium car'), ('big_car', 'Big car'), ('suv', 'SUV'), ('minivan', 'Minivan'), ('minivan', 'Minivan')],
        help="Different possible types of vehicle"
    )

    departure_loc = fields.Char(string="Departure location", required=True)
    destination_loc = fields.Char(string="Destination location", required=True)
    departure_time = fields.Datetime(string="Departure time", required=True)
    expired = fields.Boolean(compute="_compute_expired", store=True)

    @api.depends("departure_time")
    def _compute_expired(self):
        for record in self:
            if isinstance(record.departure_time, datetime):
                now = datetime.now()
                record.expired = (record.departure_time < now)
                

    available_seats = fields.Integer(required=True, string="Available seats")
    remaining_seats = fields.Char(compute='_remaining_seats', string="Remaining seats")
    remaining_seats_int = fields.Integer(compute='_remaining_seats_int', string="Remaining seats")
    
    description = fields.Text()

    passengers = fields.Many2many(comodel_name="res.users", string="Passengers")

    @api.constrains('passengers')
    def _check_number_of_passengers(self):
        for record in self:
            if len(record.passengers) > record.available_seats:
                raise ValidationError(f"Too many passengers ({len(record.passengers)} > {record.remaining_seats_int})")

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
                if record.remaining_seats_int <= 0:
                    continue
                record.write({'passengers': [fields.Command.link(self.env.uid)] })  
        return True

    @api.depends("available_seats", "passengers")
    def _remaining_seats(self):
        for record in self:
            record.remaining_seats = str(record.available_seats - len(record.passengers)) + " out of " + str(record.available_seats)

    @api.depends("available_seats", "passengers")
    def _remaining_seats_int(self):
        for record in self:
            record.remaining_seats_int = record.available_seats - len(record.passengers)
