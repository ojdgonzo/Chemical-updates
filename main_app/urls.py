from django.urls import path
from . import views

urlpatterns = [
    # Shows my main Login index.html
    path("", views.index),
    # Shows Registration page
    path("registration", views.registration),
    # Route coming from Register form in index.html
    path("register", views.register),
    # Route coming from Login form in index.html
    path("login", views.login),
    # Route displaying Engineering Dashboard
    path("dashboard", views.dashboard),
    #render new recipe form on html page
    path("wet_etch_recipes/new", views.new_recipe),#get
    # Route to create new recipe from submit button on Dashboard form
    path("wet_etch_recipes/create", views.process_new),#POST
    #render update recipe html for the selected recipe
    path('wet_etch_recipes/<int:recipe_id>/edit', views.edit_recipe),#get
    #route to update existing recipe from rendered html
    path("wet_etch_recipes/<int:recipe_id>/update", views.process_update),#post
    #delete selected recipe from dropdown
    path('wet_etch_recipes/<int:recipe_id>/delete', views.delete),#render on post
    # Route to logout user
    path("logout", views.logout),


]




# RECIPE ROUTE PROGRESSION

# CREATE
# wet_etch_recipes/new (post)
#wet _etch_recipes/update(post)
# trip_to_update.destination = request.POST['destination']
#         trip_to_update.start_date = request.POST['start_date']
#         trip_to_update.end_date = request.POST['end_date']
#         trip_to_update.plan = request.POST['plan']
#         trip_to_update.save()
# CREATE

# READ
# wet_etch_recipes/<int:recipe_id>
# READ

# UPDATE
# wet_etch_recipes/<int:recipe_id>/edit
# wet_etch_recipes/<int:recipe_id>/update
# UPDATE

# DELETE
# wet_etch_recipes/new
# DELETE


# MAPPING THINGS OUT
# Login -> redirect to Dashboard
#  Form on dashboard button -> wetetch/new (Validates then redirects back to dashboard)


#update button for html
# <select>
# {%for recipe in all_recipes%}
# <option>recipe.chemical_name
# {%endfor%}
# input:submit