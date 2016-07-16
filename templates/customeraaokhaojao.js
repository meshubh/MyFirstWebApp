var Restaurants = Backbone.Model.extend({
    defaults: {
        name: 'Empty',
        location: 'Kachiguda',
        id: null
    }
});

var Menu = Backbone.Model.extend({
    defaults: {
        item: 'No Item',
        price: 0,
        restaurant_id: '-1'
    }
});


var RestaurantCollection = Backbone.Collection.extend({
    model: Restaurants,
    url: 'http://127.0.0.1:8000/AaoKhaoJao/api/restaurantlist/'
});

var MenuCollection = Backbone.Collection.extend({
    model: Menu,
    url: 'http://127.0.0.1:8000/AaoKhaoJao/api/menu/'

});
 
var RestaurantcollView = Backbone.View.extend({
    tagName: 'ol',

    initialize: function() {
        //this.collection.on('add', this.addOne, this); 
        // this.list = $('#listid') // listeners/anouncers for the collection on add..
        // console.log(this.collection);
        var self = this
        this.collection.fetch({
            success: function(collection, response, options) {
                self.render();
            },
            error: function(model, responce, options) {
                console.log(options.xhr);
            }    
        });

    },
    render: function() {
        this.collection.each(function(restaurants) {
            var personView = new RestaurantView({
                model: restaurants
            });
            this.$el.append(personView.render().el);
        }, this);
        //console.log(this)
        return this;
    }
});

var RestaurantsColl = new RestaurantCollection;
var Menus = new MenuCollection;

var InFetchView = Backbone.View.extend
({
    el: ('#itemdiv'),
    initialize: function() {
        var url = Backbone.history.getFragment();
        var index = url.indexOf("/");
        var id = url.slice(index + 1);
        var xyz = Menus.where({
            'restaurant_id': parseInt(id)
        });
        for (var i = 0; i < xyz.length; i++) {
            var printView = new MenuView({
                model: xyz[i]
            });
            this.$el.append(printView.render().el);
        };
        return this
    }
})

var MenucollView = Backbone.View.extend({
    tagName: 'ol',
    
    initialize: function() 
    {
        var self = this
        this.collection.fetch({
            success: function(collection, response, options) {
                //console.log("hello")
                self.render();
                var IFV = new InFetchView();
                return this

            },
            error: function(model, responce, options) {
               // console.log(options.xhr);
            }
        });

    },

    render: function() {
        this.collection.each(function(menu) {
            var menView = new MenuView({
                model: menu
            });
            this.$el.append(menView.render().el);
        }, this);
        return this;
    }
});

var RestaurantView = Backbone.View.extend({
    tagName: 'ol',


    template: _.template($('#restaurantTemplate').html()),
    editingTemplate: _.template('<input class="name" value="<%= name %>" />\
        <input class="location" value="<%= location %>"<br><button id="save">Save</button><br>'),


    initialize: function() {
        this.model.on('change', this.render, this);
        //this.render();
        this.model.on('destroy', this.remove, this);
    },

    render: function() {
        //console.log(this.model)
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },

    events: {
        'click #view': 'showAlert',
    },

    showAlert: function() {
        $("#maindiv").hide();
        $("#listid").hide();
        //alert("You clicked me");
        router.navigate("show/" + this.model.get('id'), trigger = true)
    },
    
})

var MenuView = Backbone.View.extend({
    tagName: 'ol',


    template: _.template($('#menuTemplate').html()),
    editTemplate: _.template('<input class="item" value="<%= item %>" />\
        <input class="price" value="<%= price %>"<br><button id="savecomp">Save</button><br>'),

    initialize: function(options) {
        //this.render();
        //console.log("id of contact selected ", options.model.id);
        this.model.on('change', this.render, this);
        this.model.on('destroy', this.remove, this);
    },

    render: function() {
       // console.log(this.model)
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },
})



var AppItemView = Backbone.View.extend({
    el: ('#itemdiv'),
    initialize: function() {

    },
    render: function() {
        $("#maindiv").hide();
        $("#listid").hide();

        var itemView = new MenucollView({
            collection: Menus
        });
        //itemView.initialize()

    },
});

var Router = Backbone.Router.extend({
    // el:('#maindiv'),
    routes: {
        '': 'index',
        'show/:id': 'show'
    },
    show: function(id) {
        var AIV = new AppItemView({
            collection: Menus
        })
        AIV.render();
        //location.reload(true);
    }
});
var AppView = Backbone.View.extend({

    el: ('#listid'),

    initialize: function() {

    },

     render: function() {
        //this.$el.empty();
        var listView = new RestaurantcollView({
            collection: RestaurantsColl
        });
        //console.log("in render");
        this.$el.append(listView.render().el);
     },
});

 

var App = new AppView;
App.render();
var router = new Router();
Backbone.history.start();