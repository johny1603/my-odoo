odoo.define('bike.dash', function (require) {
	"use strict";
	console.log("Client action called");

	var AbstractAction = require('web.AbstractAction');
	var core = require('web.core');
	var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    var framework = require('web.framework');
    var session = require('web.session');
    var web_client = require('web.web_client');
    var _t = core._t;
    var QWeb = core.qweb;

	var bikeDash = AbstractAction.extend({
			    template: 'bikeClient',
			    init: function(parent, context){
			        console.log("INIT");
			        this._super(parent, context);
			        this.dashboards_templates = ['customerDash'];
			    },
//			    willStart: function(){
//			        var self = this;
//			        return self.fetch_data();
//			    },
//
//			    fetch_data: function(){
//			        console.log("Fetch")
//			        var self = this;
//			        var def1 = this._rpc({
////			            model: 'products.details',
////			            method : 'get_products_info',
//			        }).then(function(result){
//			               console.log(result)
//			               self.data = result;
//			        });
//			        return $.when(def1);
//			    },

    willStart: function() {
        console.log("WILLSTART FUNCTION")
        var self = this;
        return self.fetch_data();
    },

    start: function() {
        console.log("START FUNCTION")
        var self = this;
        this.set("title", 'customer Dashboard');
        return this._super().then(function() {
            self.render_dashboards();
            });
        },

    fetch_data: function() {
           var self = this;
           var def1 = this._rpc({
                model: 'customers.details',
                method: 'get_customer_details'
            }).then(function(result){
                console.log(result);
                self.data =  result;
                console.log("data defined")
                console.log(self.data)
            });
            return $.when(def1);
        },
    render_dashboards: function() {
        	console.log("RENDER_DASHBOARD")
            var self = this;
            _.each(this.dashboards_templates, function(template) {
                self.$('.o_dashboard').append(QWeb.render(template, {widget:self}));
            });
        },

	});
	core.action_registry.add('bike_dash', bikeDash);
	return bikeDash;
});