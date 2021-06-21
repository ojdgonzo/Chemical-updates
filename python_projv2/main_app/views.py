from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Engineer, Wetetchrecipe
import bcrypt

# THIS FUNCTION RENDERS THE LOGIN PAGE
def index(request):
    return render(request, 'index.html')

# THIS FUNCTION RENDERS THE REGISTRATION PAGE
def registration(request):
    return render(request, 'register.html')

# THIS FUNCTION VALIDATES REGISTRATION DATA
# IF NOT VALID THEN REDIRECT USER TO USER BACK TO REGISTRATION PAGE
# IF VALID THEN SAVE USER TO DATABASE, THEN REDIRECT TO DASHBOARD 
def register(request):
    errors = Engineer.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/registration')
    else:
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        registered = Engineer.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw
        )
        request.session['user_id'] = registered.id
        return redirect("/dashboard")

# THIS FUNCTION ENSURES THE USER EXIST
# IF NOT THEN USER IS REDIRECTED TO LOGIN PAGE WITH 
# ERROR OF INVALID CREDENTIALS
# ELSE USERS GETS REDIRECTED TO DASHBOARD
def login(request):
    user_list = Engineer.objects.filter(email = request.POST['email'])
    if len(user_list) ==0:
        messages.error(request, "User does not exist")
        return redirect('/')
    logged_user = user_list[0]
    if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
        request.session['user_id'] = logged_user.id
        return redirect('/dashboard')
    else:
        messages.error(request, 'INVALID CREDENTIALS')
        return redirect('/')

# THIS FUNCTION RENDERS THE DASHBOARD 
# AND HAS THE DATA PASSED THROUGH CONTEXT
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect(f"/")
    
    # Grab reverse relationship for chemicals used by Engineer
    # current_engineer = Engineer.objects.get(id = request.session['user_id'])
    # chemical_recipe_created = current_engineer.engineer_created_recipes.all()
    # Grab all recipes to display
    context = {
        'welcome_user' : Engineer.objects.get(id=request.session['user_id']),
        'all_recipes' : Wetetchrecipe.objects.all(),

    }

    # TO-DO: PASS THE DATA TO CHART.JS
    return render(request, 'dashboard.html', context)

def new_recipe(request):
    return render(request, "create.html")

def process_new(request):
        if 'user_id' not in request.session:
            return redirect(f"/")
        else:
            Wetetchrecipe.objects.create(
                chemical_name = request.POST['chemical_name'],
                liters_to_dispense = request.POST['liters_to_dispense'],
                engineer = Engineer.objects.get(id=request.session['user_id'])
            )
            return redirect('/dashboard')

# THIS FUNCTION IS RENDERING THE EDIT PAGE AND HAS DATA PASSED
# THROUGH CONTEXT
def edit_recipe(request, recipe_id):
    context = {
        "this_recipe" : Wetetchrecipe.objects.get(id=recipe_id)
    }
    #Check for user not in session, show not authorized message
    if 'user_id' not in request.session:
        return redirect(f"/")
    else:
        return render(request, 'update.html', context)


# THIS FUNCTION IS VALIDATING AND POSTING THE EDIT PAGE NEW DATA
# IF USER IS NOT AUTHORIZED, THEY ARE REDIRECTED TO LOGIN PAGE
# IF VALIDATION IS UNSUCCESFULL IT WILL REDIRECT BACK TO EDIT PAGE
# IF VALIDATION PASSES, RECIPE DATE IS UPDATED AND THEN REDIRECTED TO DASHBOARD
def process_update(request, recipe_id):
    #Check for user not in session, show not authorized message
    if 'user_id' not in request.session:
        return redirect(f"/")

    # Save current recipe
    current_recipe = Wetetchrecipe.objects.get(id= recipe_id)

    # recipe_errors
    recipe_errors = Wetetchrecipe.objects.recipe_validator(request.POST)

    # check for recipe validation from manager
    # Case 1: Validation doesnt pass

    if len(recipe_errors) > 0:
        for key, val in recipe_errors.items():
            messages.error(request, val)
        return redirect(f'/wet_etch_recipes/{recipe_id}/edit')
    else:
    # Case 2: Validation passes
        current_recipe.chemical_name = request.POST['chemical_name']
        current_recipe.liters_to_dispense = request.POST['liters_to_dispense']
        current_recipe.engineer = Engineer.objects.get(id=request.session['user_id'])
        current_recipe.save()

    # Once created redirect to dashboard
    return redirect('/dashboard')

# THIS FUNCTION LOGS USERS OUT BY CLEARING CURRENT SESSION
# THEN REDIRECTS TO LOGIN PAGE
def logout(request):
    # Clear session
    # redirect to login page
    request.session.clear()
    return redirect("/")
    


# THIS FUNCTION DELETES THE CURRENTLY SELECTED RECIPE
def delete(request, recipe_id):
    recipe_deleted = Wetetchrecipe.objects.get(id=recipe_id)
    recipe_deleted.delete()
    return redirect("/dashboard")
