from django.shortcuts import render
from AaoKhaoJao.models import *
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from AaoKhaoJao.serializers import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout
from rest_framework.authentication import SessionAuthentication,BasicAuthentication


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                response = HttpResponse("", status=302)
                response['Location'] = "//aaokhaojaoapp.herokuapp.com/AaoKhaoJao/secondpage"
                return response
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)


@api_view(['GET', 'POST'])
def restaurant_list_owner(request):
            """
            List all snippets, or create a new snippet.
            """
            try:
                lists = Restaurants.objects.filter(owner = request.user.id)
            except lists.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if request.method == 'GET':
                    serializer = RestaurantsSerializer(lists, many=True)
                    return Response(serializer.data)

            elif request.method == 'POST':
                    serializer = RestaurantsSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.

@api_view(['GET', 'POST'])
def restaurant_list(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        lists = Restaurants.objects.all()
        serializer = RestaurantsSerializer(lists, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RestaurantsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def restaurant_detail(request, pk):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        list1 = Restaurants.objects.get(pk=pk)
    except list1.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RestaurantsSerializer(list1)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RestaurantsSerializer(list1,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        list1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def menu_list(request, lid):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        items = Menu.objects.filter(restaurant_id__pk=lid)
        serializer = MenuSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def menu_detail(request, pk):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        item1 = Menu.objects.get(pk=pk)
    except item1.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MenuSerializer(item1)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MenuSerializer(item1, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def menu_all_item(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_items = Menu.objects.all()
        serializer = MenuSerializer(all_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from AaoKhaoJao.forms import UserForm, UserProfileForm

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            #if 'picture' in request.FILES:
                #profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/AaoKhaoJao/login')

def home(request):
    template = get_template("Firstpage.html")
    return HttpResponse(template.render())

def second_home(request):
    template = get_template("Secondpage.html")
    return HttpResponse(template.render())

def manage_restaurants(request,id):
    template = get_template("AaoKhaoJao.html")
    return HttpResponse(template.render())

def order_restaurants(request):
    template = get_template("customeraaokhaojao.html")
    return HttpResponse(template.render())

def confirm_order(request):
    template = get_template("orderconfirmation.html")
    return HttpResponse(template.render())

def restaurant_owners(request):
    template = get_template("page.html")
    return HttpResponse(template.render())