# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers import main
from werkzeug.exceptions import Forbidden, NotFound
from odoo.tools.json import scriptsafe as json_scriptsafe
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import request
from odoo import fields, http, SUPERUSER_ID, tools, _
import re


_logger = logging.getLogger(__name__)


class WebsiteSale(main.WebsiteSale):

    def values_postprocess(self, order, mode, values, errors, error_msg):
        new_values = {}
        authorized_fields = request.env['ir.model']._get('res.partner')._get_form_writable_fields()

        additional_fields = {
            'area_id': {'type': 'many2one', 'change_default': False, 'company_dependent': False, 'context': {},
                        'depends': (), 'manual': False, 'readonly': False, 'relation': 'area',
                        'required': True, 'searchable': True, 'sortable': True, 'store': True, 'string': 'Area',
                        'name': 'area_id'},
            'block': {'type': 'char', 'string': 'Block', 'name': 'block', 'required': False,
                      'searchable': True, 'sortable': True, 'store': True},
            'avenue': {'type': 'char', 'string': 'Avenue', 'name': 'avenue', 'required': False,
                       'searchable': True, 'sortable': True, 'store': True},
            'building_number': {'type': 'char', 'string': 'Building Number', 'name': 'building_number',
                                'required': False, 'searchable': True, 'sortable': True, 'store': True},
            'additional_info': {'type': 'char', 'string': 'Additional Info', 'name': 'additional_info',
                                'required': False, 'searchable': True, 'sortable': True, 'store': True},
            'floor': {'type': 'char', 'string': 'Floor', 'name': 'floor', 'required': False,
                      'searchable': True, 'sortable': True, 'store': True},
            'flat': {'type': 'char', 'string': 'Flat', 'name': 'flat', 'required': False,
                     'searchable': True, 'sortable': True, 'store': True},
            'paci_number': {'type': 'char', 'string': 'Paci Number', 'name': 'paci_number',
                            'required': False, 'searchable': True, 'sortable': True, 'store': True},
            'google_map_link': {'type': 'char', 'string': 'Google Map Link', 'name': 'google_map_link',
                                'required': False, 'searchable': True, 'sortable': True, 'store': True},
            'kuwait_finder_link': {'type': 'char', 'string': 'Kuwait Finder Link', 'name': 'kuwait_finder_link',
                                   'required': False, 'searchable': True, 'sortable': True, 'store': True},
        }

        for k, v in values.items():
            # don't drop empty value, it could be a field to reset
            if k in authorized_fields and v is not None:
                new_values[k] = v
            elif k in additional_fields and v is not None:
                new_values[k] = v
            else:  # DEBUG ONLY
                if k not in ('field_required', 'partner_id', 'callback', 'submitted'):  # classic case
                    _logger.debug("website_sale postprocess: %s value has been dropped (empty or not writable)" % k)

        if request.website.specific_user_account:
            new_values['website_id'] = request.website.id

        if mode[0] == 'new':
            new_values['company_id'] = request.website.company_id.id
            new_values['team_id'] = request.website.salesteam_id and request.website.salesteam_id.id
            new_values['user_id'] = request.website.salesperson_id.id

        lang = request.lang.code if request.lang.code in request.website.mapped('language_ids.code') else None
        if lang:
            new_values['lang'] = lang
        if mode == ('edit', 'billing') and order.partner_id.type == 'contact':
            new_values['type'] = 'other'
        if mode[1] == 'shipping':
            new_values['parent_id'] = order.partner_id.commercial_partner_id.id
            new_values['type'] = 'delivery'

        return new_values, errors, error_msg


    @http.route(['/shop/state_infos/<model("res.country.state"):state>'], type='json', auth="public", methods=['POST'],
                website=True)
    def state_infos(self, state, **kw):
        return dict(
            fields=state.country_id.sudo().get_address_fields(),
            area=[(ar.id, ar.name, ar.state_id.id) for ar in state.get_website_sale_areas()],
        )

    def _get_mandatory_fields_billing(self, country_id=False):
        res = super()._get_mandatory_fields_billing(country_id)
        res +=['state_id','building_number','additional_info','area_id']
        if 'zip' in res:
            res.remove('zip')
        if 'city' in res:
            res.remove('city')
        if 'email' in res:
            res.remove('email')

        return res

    def _get_mandatory_fields_shipping(self, country_id=False):
        res = super()._get_mandatory_fields_shipping(country_id)
        if 'zip' in res:
            res.remove('zip')
        if 'email' in res:
            res.remove('email')
        if 'city' in res:
            res.remove('city')

        return res

    def _get_country_related_render_values(self, kw, render_values):
        res = super()._get_country_related_render_values(kw, render_values)
        res.update({
            'state_areas': res['country'].get_website_sale_areas(),
        })
        return res
