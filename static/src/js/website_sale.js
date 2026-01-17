odoo.define('kw_partner_localization.website_sale', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var publicWidget = require('web.public.widget');
require('website_sale.website_sale');

var _t = core._t;

publicWidget.registry.WebsiteSale.include({

 events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events || {}, {
        'change select[name="state_id"]': '_onChangeStates',
         'click .a-visible': '_onClickVisible',
         'click .a-invisible': '_onClickInvisible',
    }),

    init: function () {
        this._super.apply(this, arguments);
        // this._changeState = _.debounce(this._changeState.bind(this), 500);
    },


_changeCountry: function () {
        if (!$("#country_id").val()) {
            return;
        }
        this._rpc({
            route: "/shop/country_infos/" + $("#country_id").val(),
            params: {
                mode: $("#country_id").attr('mode'),
            },
        }).then(function (data) {
            // placeholder phone_code
            $("input[name='phone']").attr('placeholder', data.phone_code !== 0 ? '+'+ data.phone_code : '');
            console.log("data ===",data)

            // populate states and display
            var selectStates = $("select[name='state_id']");
            // dont reload state at first loading (done in qweb)
                console.log("condition 1")

                if (data.states.length || data.state_required) {
                console.log("condition 2")

                    selectStates.html('');
                    selectStates.append('<option value="' + '' + '">' + 'Select...' + '</option>')
                    _.each(data.states, function (x) {
                        var opt = $('<option>').text(x[1])
                            .attr('value', x[0])
                            .attr('data-code', x[2]);
                        selectStates.append(opt);

                    });

                    selectStates.parent('div').show();
                } else {
                    selectStates.val('').parent('div').hide();
                }
                selectStates.data('init', 0);            

            console.log("selectCountry ===",selectStates)

            // manage fields order / visibility
    
        });
    },

_changeState: function (eventValue) {
    console.log("in change state")
    console.log(eventValue)
    console.log("before if")

        if (!eventValue) {
            console.log("in if")
            return;
        }
    console.log("after if")

        this._rpc({
            route: "/shop/state_infos/" +eventValue,
        }).then(function (data) {
            var selectAreas = $("select[name='area_id']");
            // dont reload state at first loading (done in qweb)
            console.log("selectAreas.data('init')===0 ===",selectAreas.find('option').length===1)
              selectAreas.data('init', 0);
            if (selectAreas.data('init')===0 || selectAreas.find('option').length===1) {
                console.log("STATE ID ==",eventValue)
                if (data.area.length) {
                    selectAreas.html('');
                    var data_area=data.area
                    var fiter_area=[]
                     for (var x in data_area) {
                     for ( var i = 0; i < data_area.length; i++ ) {

                        if (data_area[x][2]==eventValue)
                            {
                                  console.log("FOR AREA ==",data_area[x])
                                fiter_area.push(data_area[x])
                            }

                     }
                     }
                    const uniqueIds = [];
                    const unique = fiter_area.filter(element => {
                      const isDuplicate = uniqueIds.includes(element[0]);
                      if (!isDuplicate) {
                        uniqueIds.push(element[0]);

                        return true;
                      }

                      return false;
                    });
                     selectAreas.append('<option value="' + '' + '">' + 'Select...' + '</option>')
                    _.each(unique, function (x) {
                        var opt = $('<option>').text(x[1])
                            .attr('value', x[0])
                            .attr('data-code', x[2]);
                        selectAreas.append(opt);
                    });
                    selectAreas.parent('div').show();
                } else {
                    selectAreas.val('').parent('div').hide();
                }
                selectAreas.data('init', 0);
            } else {
                selectAreas.data('init', 0);
            }


        });
    },
    _onChangeStates: function (ev) {
        console.log(ev.currentTarget.value);

        // console.log(ev.val())
        // if (!this.$('.checkout_autoformat').length) {

        //     return;
        // }
        this._changeState(ev.currentTarget.value);
    },

    _onClickVisible: function () {
       $("#div_paci_number").css('display', 'flex');
       $("#div_google_map_link").css('display', 'flex');
       $("#div_kuwait_finder_link").css('display', 'flex');
       $("#visible_button").css('display', 'none');
       $("#invisible_button").css('display', 'flex');

     },

    _onClickInvisible: function () {
       $("#div_paci_number").css('display', 'none');
       $("#div_google_map_link").css('display', 'none');
       $("#div_kuwait_finder_link").css('display', 'none');
       $("#invisible_button").css('display', 'none');
        $("#visible_button").css('display', 'flex');


     },

});

return {
    WebsiteSale: publicWidget.registry.WebsiteSale,
    }

});
