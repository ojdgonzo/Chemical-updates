from django.db import models
import re


class EngineerManager(models.Manager):
    def user_validator(self, post_data):
        errors = {}
        if len(post_data['first_name'])<2:
            errors['first_name'] = "First Name must be at least 1 character"
        if len(post_data['last_name'])<2:
            errors['last_name'] = "Last Name must be at least 1 character"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        user_list = Engineer.objects.filter(email = post_data['email'])
        if len(user_list) >0:
            errors['email_dupe'] = "This Email already exists!"
        if len(post_data['password']) < 9:
            errors['password'] = "Your password must be  at least 8 characters"
        if post_data['password'] != post_data['confirm_password']:
            errors['match_password'] = "Passwords do not match"
        return errors

class Engineer(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=30)
    #engineer_created_recipes
    
    objects = EngineerManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




# Wet Etch Recipe Manager

class WetetchrecipeManager(models.Manager):
    def recipe_validator(self, post_data):
        errors ={}

        if len(post_data['chemical_name']) < 2:
            errors['chemical_name'] = "Chemical must containt at least 2 characters"
        if post_data['liters_to_dispense'] == 0:
            errors['liters_to_dispense'] = "You must dispense something"
        return errors








# Wet Etch Recipe Model
class Wetetchrecipe(models.Model):
    chemical_name = models.CharField(max_length=45)
    liters_to_dispense = models.IntegerField()
    engineer = models.ForeignKey(Engineer, related_name="engineer_created_recipes", on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WetetchrecipeManager()
    

