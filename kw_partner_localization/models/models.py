from odoo import fields, models, api, _



class ResCountry(models.Model):
    _inherit = 'res.country'

    def get_website_sale_countries(self, mode='billing'):
        res = super().get_website_sale_countries(mode)
        return res.sudo().search([('code','=','KW')])

    def get_website_sale_areas(self, mode='billing'):
        areas = self.env['area'].search([])
        return areas


class CountryStates(models.Model):
    _inherit="res.country.state"
    area_ids = fields.One2many("area",'state_id')

    def get_website_sale_areas(self, mode='billing'):
        areas = self.env['area'].sudo().search([])
        return areas

class Area(models.Model):
    _name = 'area'

    state_id = fields.Many2one('res.country.state')
    name = fields.Char()


class Partner(models.Model):
    _inherit = 'res.partner'

    area_id = fields.Many2one(comodel_name='area', string='Area', required='True')
    block = fields.Char(string='Block')
    avenue = fields.Char(string='Avenue')
    building_number = fields.Char(string='Building')
    additional_info = fields.Char(string='Additional Info')
    floor = fields.Char(string='Floor')
    flat = fields.Char(string='Flat')
    paci_number = fields.Char(string='PACI No.')
    google_map_link = fields.Char(string='Google Map Link')
    kuwait_finder_link = fields.Char(string='Kuwait Finder Link')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    phone = fields.Char(string='phone',related="partner_id.phone")
    area_id = fields.Many2one(comodel_name='area', related="partner_id.area_id")
    block = fields.Char(string='Block',related="partner_id.block")
    street = fields.Char(string='Street', related="partner_id.street")
    street2 = fields.Char(string='Street 2', related="partner_id.street2")
    avenue = fields.Char(string='Avenue',related="partner_id.avenue")
    building_number = fields.Char(string='Building',related="partner_id.building_number")
    additional_info = fields.Char(string='Additional Info', related="partner_id.additional_info")
    floor = fields.Char(string='Floor',related="partner_id.floor")
    flat = fields.Char(string='Flat',related="partner_id.flat")
    paci_number = fields.Char(string='PACI No.',related="partner_id.paci_number")
    google_map_link = fields.Char(string='Google Map Link',related="partner_id.google_map_link")
    kuwait_finder_link = fields.Char(string='Kuwait Finder Link',related="partner_id.kuwait_finder_link")
