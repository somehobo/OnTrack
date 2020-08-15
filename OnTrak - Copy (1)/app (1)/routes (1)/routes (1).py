# This code does most of the work for the application.  The @app.route code
# "listens" to the websiite to see what page is being requested. If the pages url
# matches the @app.route the it runs the function defined below it.

from app import app
from flask import render_template, redirect, url_for, session, request
from app.Data import Section, Assignment
from app.Data.User import User
from app.Forms import *
from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
import requests
from flask import Flask, flash, redirect, render_template, request, url_for


google_auth = GoogleClient(
    client_id=("458432068336-tocrspcbepahlmm1ovugke6hq9mqoqdf"
               ".apps.googleusercontent.com"),
    client_secret="HuUgIShcFgfT4P4YJ6IVKVKW",
    redirect_uri="http://localhost:5000/oauth2callback"
    # "http://localhost:5000/oauth2callback"
)
# This tells the app what to do if the use requests the home page --> http://127.0.0.1:5000/
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

# This tells the app what to do if the use requests the classes page --> http://127.0.0.1:5000/classes
# It will request all of the classes from the data object and then send them to the template
# "Section.objects.order_by('+period')" is the critical code.  First it makes a call to the
# Secion class in the Data folder which creates (instantiates) a new object that is sorted by
# field "period" from smallest to largest
@app.route('/classes')
def sections():
    try:
        if session["displayName"]:
            return render_template('classes.html', sections = Section.objects.order_by('+period'))
    except:
        return redirect('/login')

# This is the route and code for a new class. Because this route has a form it needs both the
# get and post methods.
@app.route('/newclass', methods=['GET', 'POST'])
def newSection():
    # This makes a call to the SectionForm class and creates (instantiates) an object that is
    # the form and stores it in the variable 'form'.
    form = SectionForm()

    # This if statement checks to see if the form on the template was submitted and was valid
    # A form is valid if all the data is correctly formatted as entered
    if form.validate_on_submit():
        # This makes a call to the Section class in the data folder (module) and
        # creates (instantiates) a new object with the values that were entered in the form.
        newClass = Section(name=form.name.data, subject=form.subject.data, period=form.per.data, description=form.desc.data, teacher=form.teacher.data)
        # This saves the newClass object to the Sections data collection in MongoDB via the section
        # object in the Data folder (module).
        newClass.save()
        # This redirects the app to the sections function which renders the sections page
        return redirect(url_for('sections'))
    # This return statement will run if this function but the form was not submitted
    # This condition means the user has not yet filled out the form so we render the blank form
    # The form is rendered on the sectionform.html template and the form variable contains the
    # form object that is passed to the template.
    return render_template('sectionform.html', form = form)

# this is very similar to the newclass function except that it adds the ability to
# prepopulate the form with existing values so that the class can be updated or edited
# to do this we have to know what section we are editing so we pass the sectionID in as a variable
@app.route('/editclass/<sectionID>', methods=['GET','POST'])
def editsection(sectionID):
    form = SectionForm()
    # Here we create a data object from the section class.  The object contains all of the
    # data for the specific section we want to edit.  We retrieve that information from the Database
    # with 'Section.objects(pk=sectionID)'. pk = primary key which is how you search for a data
    # object by its unique identifier.  By definition, this will return one and only one object.
    editSection = Section.objects(pk=sectionID)

    # This if statement checks to see if the form where the class is edited has been submitted
    # and all the data is valid.
    if form.validate_on_submit():
        # this for loop puts the section data in to an object variable. Without the for loop
        # the object we need is in a list of one so we need the for loop to select the section we want to edit
        for section in editSection:
            # To update data you have to first 'reload' the data to ensure you have the a right data
            section.reload()
            # After reloading the data, you can update the data.  This code takes the data from the
            # form and insterts it in to the dtaabase via the section class in the Data mosule
            section.update(name=form.name.data,
                           subject=form.subject.data,
                           period=form.per.data,
                           description=form.desc.data,
                           teacher = form.teacher.data)

            # after updating the data this sends the user to the list of sections.
            return redirect(url_for('sections'))
    # This code is run if the form was not yet submitted which means the user is just coming to this
    # page to edit the data in a section. Like above, we first grad the section we want to edit
    # from its list of 1 items.  Then we take each value from the data object that we created and put
    # that value in to the form object so that it shows up in the form and the user knows what the
    # data is that they are editing.
    for section in editSection:
        form.per.data = section.period
        form.teacher.data = section.teacher
        form.name.data = section.name
        form.desc.data = section.description
        form.subject.data = section.subject
        # This renders the pre-populated form with the data from the form object
        return render_template('sectionform.html', form=form)

# This is a very simple route and function that deletes the class the user selects. The value
# for the sectionID is passed via the url and then used to find and delete the right section.
@app.route('/deleteclass/<sectionID>')
def deletesection(sectionID):
    deletesection = Section.objects(pk=sectionID)
    deletesection.delete()
    # the user is redirected to the list of classes (sections)
    return redirect(url_for('sections'))

# The following routes and functions are very similar the ones above with one exception
# because assignments are necessarily related to Classes (sections) you also need the sectionID
# create and edit assignments. You also need the sectionID to list assignments by section. In
# this case the code is creating a list of assignments for a secific class (section). The sectionID
# is passed from the classes template to this route.
@app.route('/assignments/<sectionID>')
def assignments(sectionID):
    # This gets the list of sections with a specific sectionID. This will always be a be a list of
    # one but we need the for loop to get to the section we want to work on.
    sections = Section.objects(pk=sectionID)
    for section in sections:
        # We want to get the section name as a variable so we can pass it to the template to be displayed
        # we could also retrielve it from the object by passing the whole object.
        sectionName = section.name
        # This creates the list of assignment objects that are associated to a specific class (section)
        # by calling to the assignment class in the Data folder (module) and passing the sectionID
        # as a search term.
        assignments = Assignment.objects(section = sectionID)
        # This then renders the assignments.html template and passes several variables to that template
        # that will be used on the template.
        return render_template('assignments.html', assignments = assignments, sectionName = sectionName, sectionID = sectionID)

# this is the route and function for creatin a new assignment that is associated with a specific class
@app.route('/newassignment/<sectionID>', methods=['GET','POST'])
def newAssignment(sectionID):
    # create a form object from the assignmentform class.
    form = AssignmentForm(request.form)

    # if the function was called by submitting the form and the form data is valid
    # then this if statement will be true
    if form.is_submitted():
        print("is submitted")
        print(form.validate())
        if form.validate():
            print("validated")
            # take the data from the form and put in in a newAssignment data object from the assignment class
            newAssignment = Assignment(section=sectionID,
                                       name = form.name.data,
                                       duedate = form.duedate.data,
                                       assigndate = form.assigndate.data,
                                       description = form.desc.data)
            # save the newAssignment data object to the database via the assignment class in the Data folder (module)
            newAssignment.save()
            # Send the user to the list of assignments for a specific sclass (section) which should include the new assignment
            return redirect(url_for("assignments", sectionID=sectionID))
    else:
        print("something is wrong")
    # if this function was not run as a result of the a valid form submission then the user
    # is expecting a blank new assignment form. We need to retreive the Class (section) Name
    # so the user understands that the assignment they are creating is for this class (section).
    sections = Section.objects(pk=sectionID)
    # because we are searching by sectionID which is unique we can assume that the list of Sections
    # that is returned will be a list of exactly one section so we only need one iteration of a for loop
    for sectionObj in sections:
        return render_template('assignmentform.html', form=form, sectionName=sectionObj.name)


# as with the editclass route and function above, this edits an assignment. We also need the
# sectionID but mostly to show to the user so the user is clear that they are editing a speciufic
# assignment for a specific class.  We can retrieve and edit the assignment with only the assignmentID.
@app.route('/editassignment/<sectionID>/<assignmentID>', methods=['GET','POST'])
def editassignments(sectionID,assignmentID):
    # Create the assignmentform object
    form = AssignmentForm()
    # Get the list of exactly one assignment wiht a specific assignmentID
    editAssignments = Assignment.objects(pk=assignmentID)

    # if the this function was called by the form being submitted and the data is validators
    # then this will evaluate as true
    if form.validate_on_submit():
        for assignment in editAssignments:
            # via the reload method in the assignment class from the data folder (module)
            # reload the assignment object so it is ready to edit
            assignment.reload()
            # take the data from the form that the user submits and put it in to the data object
            # that is being updated and via the update method in the assignment class in data module,
            # update the database
            assignment.update(name=form.name.data,
                           duedate=form.duedate.data,
                           assigndate=form.assigndate.data,
                           description=form.desc.data,
                           section=assignment.section.to_dbref())
            # send the user to the list of assignments for the specific class (section)
            return redirect(url_for('assignments', sectionID=sectionID))

    # if this function is not run by the valid submission of the form then the user expects the
    # form to be rendered and to filled in with the data to be entered.  This is done by copying
    # the data from the assignment object that was created with the assignment class in the Data module
    # and putting that data in to the form object to be displayed to and edited by the user.
    for assignment in editAssignments:
        form.name.data = assignment.name
        form.duedate.data = assignment.duedate
        form.assigndate.data = assignment.assigndate
        form.desc.data = assignment.description
        # render the assignment form with the necessary variables
        return render_template('assignmentform.html', form=form, sectionID=sectionID, assignmentID=assignmentID)

# Delete an assignment.  The sectionID is passed just to notify the user of the section that the assignement
# belongs to.  The section could also be retreived from the assignment because it is a field in the assignment
# data class.


@app.route('/deleteassignment/<sectionID>/<assignmentID>')
def deleteAssignment(sectionID, assignmentID):
    # retrieve the specific assignment object
    deleteAssignment = Assignment.objects(pk=assignmentID)
    # delete that object
    deleteAssignment.delete()
    # send the user to the assignments list for a specific section
    return redirect(url_for('assignments', sectionID=sectionID, assignmentID=assignmentID))

@app.route('/rlogin') #student
def rlogin():
    session['Teacher'] = 2
    print(session['Teacher'])
    if not session.get("access_token"):
        return redirect("/oauth2callback")
    with requests.Session() as s:
        s.auth = OAuth2BearerToken(session["access_token"])
        r = s.get("https://www.googleapis.com/plus/v1/people/me?access_token={}".format(session.get("access_token")))
    r.raise_for_status()
    data = r.json()
    session["displayName"] = data["displayName"]
    session["routeName"] = data["displayName"].replace(" ", "_")
    return render_template("profile.html", data=data)




# Once you log in create a new project
# then click the three lines in the top left to get a menu
# Then MouseOver APIs and Services and choose Credentials.
# There's more.  I will write it up.

google_auth = GoogleClient(
    client_id="463567652450-1nvs7u2n0tqeiesku1g44v7id115aa8r.apps.googleusercontent.com",
    client_secret="DrnlWFeQ5RORtxplDmKIW2sC",
    # Do not change this value
    redirect_uri="http://localhost:5000/oauth2callback"
)




@app.route('/login') #Teacher
def login():
    if not session.get("access_token"):
        return redirect("/oauth2callback")
    with requests.Session() as s:
        s.auth = OAuth2BearerToken(session["access_token"])
        r = s.get("https://www.googleapis.com/plus/v1/people/me?access_token={}".format(session.get("access_token")))
    r.raise_for_status()
    data = r.json()
    session["displayName"] = data["displayName"]
    session["routeName"] = data["displayName"].replace(" ", "_")
    session['emails'] = data['emails'][0]['value']
    user = User()
    for i in User.objects:
        if i.name == session["displayName"]:
            # session["wallet"] = i.wallet
            # session["reputation"] = i.reputation
            return redirect("/")
    user.name = session["displayName"]
    user.save()
    return render_template("profile.html", data=data)

@app.route("/student/<user>")
def profile(user):
    if not session.get("access_token"):
        return redirect("/oauth2callback")
    with requests.Session() as s:
        s.auth = OAuth2BearerToken(session["access_token"])
        r = s.get("https://www.googleapis.com/plus/v1/people/me?access_token={}".format(session.get("access_token")))
    r.raise_for_status()
    data = r.json()
    session["displayName"] = data["displayName"]
    session["routeName"] = data["displayName"].replace(" ", "_")
    return render_template("profile.html", data=data)
    # if usercheck(data["emails"][0]['value']):
    #     session["displayName"] = data["displayName"]
    #     session["routeName"] = data["displayName"].replace(" ", "_")
    #     # Creates new user if display is not in a User object:
    #     if data["displayName"] in displayname():
    #         return redirect("/")
    #     createuser(data["displayName"], data["emails"][0]['value'])
    #     return redirect("/")
    # session.pop("access_token")
    # flash("Must be a Oakland Tech teacher to login")
    # return redirect("/error")


@app.route('/help')
def help():
    return render_template('help.html')

    
@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/oauth2callback")
def google_oauth2callback():
    code = request.args.get("code")
    error = request.args.get("error")
    if error:
        return "error :( {!r}".format(error)
    if not code:
        return redirect(google_auth.authorize_url(
            scope=["profile", "email"],
            response_type="code",
        ))
    data = google_auth.get_token(
        code=code,
        grant_type="authorization_code",
    )
    session["access_token"] = data.get("access_token")
    return redirect("/login")


@app.route("/logout")
def logout():
    session.pop("access_token")
    session.pop("displayName")

    return redirect("/")
