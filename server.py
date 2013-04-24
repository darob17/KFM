'''
Created on Apr 22, 2013

@author: David
'''
"""
*******************************************************
This file is the only file that needs to be run it is the
server of the web app using flask. First run the code in whatever
terminal or IDE you want. Type the address http://127.0.0.1:5000 in the
address bar to get the First Index page. You will see a title page with a facebook
button. Click it this should bring you to the facebook page and ask for perminsion
to see friends relationship statuses. Press ok and you will see a blank screen with text
saying to exit the tab. This should bring you back to the orignial tab and the sumbition screen
should be up here you have 4 things to choos from. You can play the game with males, females, people who are single,
and people in relationships. After you pick what you want press submit. You should be at the facebook game page
With 3 facebook profile picture of your friends and there name under them. There are three rows
each corrisponding to kill, flirt, marry. If you mess up and give on person more than one catagory an error message
will come up telling you to redo the game. Finnally if you succesfully do one catagory per
a person you will the same page but with three different people. Finnally if you want to choose different parameters
or just reshuffle your friends hit the reset button.

IMPORTANT make sure that server is a level above templates and static folder

"""













import fbconsole
'''Controls Facebook Authetication and Date Retrieval'''
import random
''' Used To shuffle friends List'''
import easygui
'''Used for alerts'''

from flask import Flask, request, render_template, redirect, url_for
'''used To make server'''
app = Flask(__name__)
SUBMIT_TITLE=False
FACEBOOK_VAL=False
PARAMS={ }
FRIENDS={}

fbconsole.logout()
'''Initialize variables and logout fbconsole so that it does not get confused
with a past login token'''

@app.route("/")
def index_page():
    """This takes care fo the index page before and after facebook authentication
    Also, takes care of facebook authentication using fbconsole"""
    
    global SUBMIT_TITLE
    global FACEBOOK_VAL
    global PARAMS
    global FRIENDS
    if SUBMIT_TITLE:
        """IF at the submition page clear the filter parmeters and clear list of Friends"""  
        
        
        PARAMS={'male':False,'female':False,'relationship':False,'single':False}
        FRIENDS={}
        
        if not FACEBOOK_VAL:
            """If not facebook Validated initalize facebook authentication"""
            fbconsole.APP_ID="316500388373772"
            fbconsole.AUTH_SCOPE= ['friends_relationships']
            fbconsole.authenticate()
            
            FACEBOOK_VAL=True
        """render  submition page to see"""
        return render_template('submit.html')  
    else:
        """if neither facebook authticated or at the submition
        page render the initial facebook initilaztion page"""
        fbconsole.logout()
        SUBMIT_TITLE=True

        return render_template('index.html')
        
    




   
    
@app.route("/Facebook/")
def Facebook():
    """Used to Control KFM game page"""
    global PARAMS
    global FRIENDS
    if PARAMS['male']==False:
        """If params have not been set the (equal to false) set params"""
        PARAMS = {k:(request.args[k] if k in request.args else'off') for k in PARAMS.keys()}
    if FRIENDS == {}:
        """If Friends are empty Populate Friends"""
        SqL_Filter=""
        if PARAMS['male']=='on' and PARAMS['female']!='on':
            SqL_Filter+=(" and sex='male'")
        if PARAMS['female']=='on' and PARAMS['male']!='on':
            SqL_Filter+=(" and sex='female'")
        if PARAMS['relationship']!='on' and PARAMS['single']=='on':
            SqL_Filter+=(" and relationship_status='single'")
        if PARAMS['relationship']=='on' and PARAMS['single']!='on':
            SqL_Filter+=(" and relationship_status<>'single'")
        """Uses fbconsole to make fql query to facebook graph to get name and Profile Pic
        of people who fit within the query"""    
        FRIENDS = fbconsole.fql("SELECT name, pic_big FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())"
               +SqL_Filter)
        random.shuffle(FRIENDS)
        """Shuffle Friends list to make them random every time"""
        """render Facebook.html with three friends's name and profile pics being displayed"""
        return render_template('Facebook.html',friend_one=FRIENDS[0], friend_two=FRIENDS[1], friend_three=FRIENDS[2])
    if 'Kill' in request.args:
        
        if 3 == len(set(request.args.values())):
            """IF Kill Flirt Marry has been submitted check if all values are different"""
            FRIENDS=FRIENDS[3:]
            """remove first three firends if submition follows the rules"""
            if len(FRIENDS)<3:
                """If Friends list is less than three the game is over and takes you back
                to the submition page"""
                easygui.msgbox("Try another filter or log onto a friends facebook",title="Congradulations", ok_button="Finish")
                return redirect(url_for('index_page'))
            """update pictures and names with next three friends"""    
            return render_template('Facebook.html',friend_one=FRIENDS[0], friend_two=FRIENDS[1], friend_three=FRIENDS[2])
        else:
            """If mutliple catagories given to one person"""
            easygui.msgbox("One Catagory for each Person",title="Try Agian", ok_button="Redo")
            return render_template('Facebook.html',friend_one=FRIENDS[0], friend_two=FRIENDS[1], friend_three=FRIENDS[2])
   
            
    
    

if __name__ == "__main__":
   # Debug mode should be turned off when you are finished
   #
   app.run(debug=False)