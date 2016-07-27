var Restaurants = Backbone.Model.extend({
    defaults: {
        name: 'Empty',
        location: 'Kachiguda',
        id: null,
        owner: null
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
    url: 'https://aaokhaojaoapp.herokuapp.com/AaoKhaoJao/api/restaurantlist/'
});

var MenuCollection = Backbone.Collection.extend({
    model: Menu,
    url: 'https://aaokhaojaoapp.herokuapp.com/AaoKhaoJao/api/menu/'

});
 
var RestaurantcollView = Backbone.View.extend({
    tagName: 'ol',

    initialize: function() {
        //this.collection.on('add', this.addOne, this); 
        // this.list = $('#listid') // listeners/anouncers for the collection on add..
        console.log(this.collection);
        var self = this
        this.collection.fetch({
            success: function(collection, response, options) {
                console.log(collection)
                self.render();
            },
            error: function(model, response, options) {
                console.log(options.xhr);
            }    
        });

    },
    render: function(){
        this.collection.each(this.addOne, this);
		return this;
	},
// called from render method of collection view..
	addOne: function(restaurants){
		console.log("Added Restaurant");
		var courseView = new RestaurantView({ model: restaurants });
		this.$el.append(courseView.render().el);
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
            error: function(model, response, options) {
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
        this.model.on('destroy', this.remove, this);
    },

    render: function() {
        console.log(this.model)
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },

    events: {
        'click #view': 'showAlert',
        'click #edit': 'editList',
        'click #delete': 'DestroyList',
        "click #save": "saveList",

    },

    showAlert: function() {
        $("#maindiv").hide();
        $("#listid").hide();
        //alert("You clicked me");
        router.navigate("show/" + this.model.get('id'), trigger = true)
    },
    editList: function() {
       // console.log('editing');
        // this.$el.html(this.editTemplate(this.model.toJSON()));
        this.$el.html(this.editingTemplate(this.model.toJSON()));
    },

    saveList:function(){
        editname = $('input.name').val();
        editlocation = $('input.location').val();
        this.model.set({
            name:editname,
        });
        this.model.set({
        location: editlocation
        });
        this.model.save()
    },

    DestroyList: function() {
        var id = this.model.get("id");
        var del_items = RestaurantsColl.where({
            'id': id
        });
        for (var i = 0; i < del_items.length; i++) {
            del_items[i].destroy(); //  calling backbone js destroy function to destroy that model object
            //del_items[i].remove();
        };
        //this.model.destroy();
        this.$el.remove();
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

    events: {
        'click #edit': 'editItem',
        'click #delete': 'DestroyItem',
        "click #savecomp": "saveCompleted",

    },

    editItem: function() {
       // console.log('editing');
        this.$el.html(this.editTemplate(this.model.toJSON()));
    },

    saveCompleted: function() {
        edititem = $('input.item').val();
        editprice = $('input.price').val();
        this.model.save({
            item:edititem,
            price: editprice
        });
        //this.$el.html(this.template(this.model.toJSON()));
        //console.log('saved');
    },

    DestroyItem: function() {
        this.model.destroy(); //  calling backbone js destroy function to destroy that model object
    },

    remove: function() {
        this.$el.remove();
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
    events: {

        'click #additem': 'itemadd' // binding submit click to submit function..
    },
    render: function() {
        $("#maindiv").hide();
        $("#listid").hide();
        this.$el.html("Item<input id=\"desc\" type=\"text\" placeholder=\"Item Name\"><br>\
        Price<input id=\"comp\" type=\"text\" placeholder=\"Price\"><br><br>\
        <button class=\"btn btn btn-success\" id=\"additem\">AddItem</button>");

        var itemView = new MenucollView({
            collection: Menus
        });
        //itemView.initialize()

    },
    itemadd: function(e) {
        $("#maindiv").hide();
        $("#listid").hide();
        //console.log("Inside submit")
        e.preventDefault(); // preventing default submission..
        var newItemDesc = $("#desc").val();
        var newItemComp = $("#comp").val();
        var itemView = new MenucollView({
            collection: Menus
        });
        //var newItemId = ToDoItems.length + 1;
        //console.log(newItemId);
        var url = Backbone.history.getFragment();
        var index = url.indexOf("/");
        var newid = url.slice(index + 1);
        var item = new Menu
        ({
            'item': newItemDesc,
            'price': newItemComp,
            //'id': newItemId,
            'restaurant_id': newid
        }); // creating a new To Do list object..
        Menus.create(item); // adding this to current collection..  
        this.$el.html("Item<input id=\"desc\" type=\"text\" placeholder=\"Item Name\"><br>\
        Price<input id=\"comp\" type=\"text\" placeholder=\"Price\"><br><br>\
        <button class=\"btn btn btn-success\" id=\"additem\">AddItem</button>");
        //console.log(itemView);
        var xyz = Menus.where({
            'restaurant_id': newid
        })
        for (var i = 0; i < xyz.length; i++) {
           // console.log(xyz[i])
            var printView = new MenuView({
                model: xyz[i]
            });
            //console.log(printView)
            this.$el.append(printView.render().el);
        };
        function updateDiv(){
            //Get new content through Ajax
        location.reload();
        }
        setInterval(updateDiv, 100);
        //location.reload(true);
    }
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
    events: {
        'click #addbutton': 'clickedadd' // binding submit click to submit function..
    },
    initialize: function() {

    },
    clickedadd: function(e) 
    {
        //$("#listid").hide();
        //this.$el.empty();
        //console.log("Inside submit")
        e.preventDefault(); // preventing default submission..
        var newListName = $("#nm").val();
        var newListLocation = $("#loc").val();
        //console.log(newListName)
        var listView = new RestaurantcollView({
            collection: RestaurantsColl
        });
        var list = new Restaurants
        ({
            'name': newListName,
            'location':newListLocation
        });
        RestaurantsColl.create(list);
        this.$el.html("<table class=\"table\">\
            <thead>\
                <tr>\
                    <th>Restaurants</th>\
                </tr>\
                <tr>\
                <td><input id=\"nm\" type=\"text\" class=\"form-control todotask-input\" placeholder=\"Name of the Restaurant\" name=\"name\"></td>\
                <td><input id=\"loc\" type=\"text\" class=\"form-control todotask-input\" placeholder=\"location of the Restaurant\" name=\"name\"></td>\
                <td><button class=\"btn btn btn-success\" id=\"addbutton\">Add</button></td>\
                </tr>\
            </thead>");
        //this.$el.append(listView.render().el);
        //console.log(Todos);
        var xyz=RestaurantsColl.where({
        })
        for (var i = 0; i < xyz.length; i++) {
           // console.log(xyz[i])
            var printView = new RestaurantView({
                model: xyz[i]
            });
           // console.log(printView)
            this.$el.append(printView.render().el);
        };
       // console.log(xyz);
        function updateDiv(){
            //Get new content through Ajax
            location.reload();
        }
        setInterval(updateDiv, 100);
   },
     render: function() {
        //this.$el.empty();
        this.$el.html("<table class=\"table\">\
            <thead>\
                <tr>\
                    <th>Restaurants</th>\
                </tr>\
                <tr>\
                <td><input id=\"nm\" type=\"text\" class=\"form-control todotask-input\" placeholder=\"Name of the Restaurant\" name=\"name\"></td>\
                <td><input id=\"loc\" type=\"text\" class=\"form-control todotask-input\" placeholder=\"location of the Restaurant\" name=\"name\"></td>\
                <td><button class=\"btn btn btn-success\" id=\"addbutton\">Add</button></td>\
                </tr>\
            </thead>");
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