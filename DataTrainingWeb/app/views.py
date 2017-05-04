from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Student, Group
from django.templatetags.static import static
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static

import django.contrib.auth  as auth
import json, random, os

#Local debugging
debug = True

#Local ERROR detected string
ERROR='/***/'

#Student
numberOfQueueSet=20

# Location of JSON file
JSONLocation = 'C:/Users/Woramate J/Project/Mike/DTW2/DataTrainingWeb/app/static/content/Content_Set'
# Format should be like this: "loot/to/your/Content_Set"
# Yes, left the content set number empty, the render part can deal with that.

#Views

def loginView( request ):
    return render( request, 'index.html' )

def homeView( request ):
    return render( request, 'home.html' )

def trainingView( request ):
    debug( "In trainingView" )
    arr_word=[]
    arr_pos=[]
    readJson( JSONLocation, '01', '36270191', arr_word, arr_pos )
    sentence=[]
    tmp=''
    for word in arr_word:
        if word!='/***/':
            tmp=tmp+word
        else:
            sentence.append( tmp )
            tmp=''
    sentence.append( tmp )
    return render( request, 'training.html', { 'name':request.session[ 'name' ], 'word':arr_word, 'pos':arr_pos, 'sentence':sentence } )

# Admin views

def adminView( request ):
    return render( request, 'admin/admin.html' )

def manageStudentView( request ):
    return render( request, 'admin/manageStudent.html', { 'stds':getStudentList() } )

def manageGroupView( request ):
    # tmp=getGroupList()
    # groups=[]
    # d=[]
    # for group in tmp:
    #     tmp2=list( group.post.split( ',' ) )
    #     d=[ group.name, tmp2, group.visible ]
    #     groups.append( d )
    #     d=[]

    # post_list=[]
    # for group in groups:
    #     post_list.append( group.post.split( ',' ) )
    # print( post_list )
    return render( request, 'admin/manageGroup.html', { 'groups':getGroupList() } )

#Model

def doLogin( request ):
    login_username = request.POST.get( 'Lusername', ERROR )
    login_password = request.POST.get( 'Lpassword', ERROR )
    row = Student.objects.filter( username=login_username, password=login_password )
    if not row :

        # Debug
        debug( 'login fail' )
        # End debug

        return render( request, 'index.html', { 'msg':"Wrong username or password" } )

    # Debug
    debug( 'login pass' )
    # End debig

    request.session[ 'name' ]=row[0].name
    request.session[ 'username' ]=row[0].username
    if len( row[0].memory )==0:
        return render( request, 'home.html', { 'name':request.session[ 'name' ], 'username':request.session[ 'username' ], 'groups':getGroupList() } )
    else:
        return render( request, 'index.html', {  'msg':"Memory: "+row[0].memory })

def doLogout( request ):
    request.session.clear()
    return render( request, 'index.html' )

def addStudent( request ):
    register_username = request.POST['Ausername']
    register_password = request.POST['Apassword']
    register_name = request.POST['Aname']
    register_queue = generateQueues()
    register_memory = ''
    std = 0

    if register_username=='':
        return render( request, 'admin/manageStudent.html', { 'msg':"You cannot left username empty.", 'stds':getStudentList() } )

    if register_password=='':
        return render( request, 'admin/manageStudent.html', { 'msg':"You cannot left password empty.", 'stds':getStudentList() } )

    if register_name=='':
        return render( request, 'admin/manageStudent.html', { 'msg':"You cannot left name empty.", 'stds':getStudentList() } )

    if register_username==ERROR:
        return render( request, 'admin/manageStudent.html', { 'msg':"Cannot register", 'stds':getStudentList() } )

    row = Student.objects.filter( username=register_username )
    if len( row )>0:
        return render( request, 'admin/manageStudent.html', { 'msg':"Cannot register new student username: " + register_username + "\nAlready exist!", 'stds':getStudentList() } )

    row = Student.objects.filter( name=register_name )
    if len( row )>0:
        return render( request, 'admin/manageStudent.html', { 'msg':"Cannot register new student name: " + register_name + "\nAlready exist!", 'stds':getStudentList() } )

    std = Student( username=register_username, password=register_password, name=register_name, queue=register_queue, memory=register_memory )
    std.save()

    # Debug
    debug( 'username: ' + str( std.username ) )
    debug( 'password: ' + str( std.password ) )
    debug( 'name: ' + str( std.name ) )
    # End debug

    return render( request, 'admin/manageStudent.html', { 'msg':"Succesfully create student name: " + std.name, 'stds':getStudentList() } )

def updateStudent( request ):
    debug( 'In updateStudent' )
    update_username = request.POST.get( 'std_username', ERROR )
    update_password = request.POST.get( 'USpassword', ERROR )
    update_name = request.POST.get( 'USname', ERROR )
    update_memory = request.POST.get( 'USmemory', ERROR )

    if update_username==ERROR:
        return render( request, 'admin/manageStudent.html', { 'stds':getStudentList(), 'msg':"Error - Cannot get student." } )

    std=Student.objects.get( username=update_username )

    msg='Error - Cannot change anything'
    #Nothing change
    if std.password==update_password and std.name==update_name and std.memory==update_memory:
        return render( request, 'admin/manageStudent.html', { 'stds':getStudentList(), 'msg':"You have to change something in Username: \""+update_username+'\"' } )
    #Name change
    elif std.name!=update_name and std.password==update_password:
        msg='Successfully changed name from: \"'+std.name+'\" to: \"'+update_name+'\"'
        std.name=update_name
    #Password change
    elif std.password!=update_password and std.name==update_name:
        msg='Successfully changed password from: \"'+std.password+'\" to: \"'+update_password+'\"'
        std.password=update_password
    #Memory change
    elif std.name==update_name and std.password==update_password and std.memory!=update_memory:
        msg='Successfully changed memory from: \"'+std.memory+'\" to: \"'+update_memory+'\"'
        std.memory=update_memory
    #Name and Password change
    elif std.name!=update_name and std.password!=update_password and std.memory==update_memory:
        msg='Successfully changed name from: \"'+std.name+'\" to: \"'+update_name+'\" and changed password from: \"'+std.password+'\" to: \"'+update_password+'\"'
        std.name=update_name
        std.password=update_password
    #Name and Memory change
    elif std.name!=update_name and std.password==update_password and std.memory!=update_memory:
        msg='Successfully changed name from: \"'+std.name+'\" to: \"'+update_name+'\" and changed memory from: \"'+std.memory+'\" to: \"'+update_memory+'\"'
        std.name=update_name
        std.memory=update_memory
    #Password and Memory change
    elif std.name==update_name and std.password!=update_password and std.memory!=update_memory:
        msg='Successfully changed password from: \"'+std.password+'\" to: \"'+update_password+'\" and changed memory from: \"'+std.memory+'\" to: \"'+update_memory+'\"'
        std.password=update_password
        std.memory=update_memory
    #All change
    else:
        msg='Successfully changed password from: \"'+std.password+'\" to: \"'+update_password+'\" AND changed name from: \"'+std.name+'\" to: \"'+update_name+'\"'
        std.password=update_password
        std.name=update_name

    std.save()

    return render( request, 'admin/manageStudent.html', { 'stds':getStudentList(), 'msg':msg } )

def deleteStudent( request ):
    #Debug
    debug( 'in delete student' )
    #End debug

    _std_username = request.POST.get( 'std_username', ERROR )

    if _std_username==ERROR:
        return render( request, 'admin/manageStudent.html', { 'stds':getStudentList(), 'msg':"Error - Cannot get student." } )
    try:
        std = Student.objects.get( username=_std_username )
        Student.delete( std )
    except():
        return render( request, 'admin/manageStudent.html', { 'stds':getStudentList(), 'msg':"Error - Cannot find group name in database" } )
    # row = Student.objects.filter( name=_std_name )
    # for i in row:
    #     i.delete()
    return render( request, 'admin/manageStudent.html', { 'stds':getStudentList(), 'msg':"Delete student: "+_std_username } )

def addGroup( request ):
    _name = request.POST.get( 'groupName', ERROR )
    _post = request.POST.get( 'ids', ERROR )
    _visible = request.POST.get( 'visible', False )

    if _name==ERROR:
        return render( request, 'admin/manageGroup.html', { 'msg':"You cannot left group name empty.", 'groups':getGroupList() } )

    if _post==ERROR:
        return render( request, 'admin/manageGroup.html', { 'msg':"You cannot left post ids empty.", 'groups':getGroupList() } )

    row = Group.objects.filter( name=_name )

    if len( row )>0:
        return render( request, 'admin/manageGroup.html', { 'msg':"Group name already exist.", 'groups':getGroupList() } )

    group = Group( name=_name, post=_post, visible=_visible )
    group.save()

    # Debug
    debug( 'name: ' + str( group.name ) )
    debug( 'post: ' + str( group.post ) )
    debug( 'visible: ' + str( group.visible ) )
    # End debug

    return render( request, 'admin/manageGroup.html', {'groups':getGroupList() } )

def deleteGroup( request ):
    #Debug
    debug( 'In delete group' )
    #End debug

    _group=request.POST[ 'group' ]

    try:
        group = Group.objects.get( name=_group )
        Group.delete( group )
    except():
        return render( request, 'admin/manageGroup.html', { 'groups':getGroupList(), 'msg':"Error - Cannot find group name in database" } )
    return render( request, 'admin/manageGroup.html', { 'groups':getGroupList(), 'msg':"Delete group: "+_group } )

def selectGroup( request ):

    selectedGroup=request.POST[ 'selectedGroup' ]

    #Debug
    debug( "In selectedGroup")
    debug( selectedGroup )
    #End debug
    #
    # request.session[ 'name' ]=row[0].name
    # request.session[ 'username' ]=row[0].username
    msg="You selected "+selectedGroup
    return render( request, 'home.html', { 'name':request.session[ 'name' ], 'username':request.session[ 'username' ], 'msg':msg, 'groups':getGroupList() } )

#Misc

def getStudentList():
    return Student.objects.all()

def getGroupList():
    return Group.objects.all()

def readJson( JSONLocation, set, id_num, arr_word, arr_pos ):
    with open( JSONLocation+set+'/'+'id_'+id_num+'.json', encoding='utf-8' ) as json_data:
        decoded=json.loads( json_data.read() )
    for i in range( len( decoded[ 'id_'+id_num ] ) ):
        if decoded[ 'id_'+id_num ][ i ][ 'word' ]=='':
            arr_word.append( '/***/' )
            arr_pos.append( '/***/' )
        else:
            arr_word.append( decoded[ 'id_'+id_num ][ i ] [ 'word' ] )
            arr_pos.append( decoded[ 'id_'+id_num ][ i ][ 'pos' ] )

def writeJson( JSONLocation, set, id_num, arr_word, arr_pos, username ):
    data = {}
    data['id_'+str(id_num)+'_'+username] = []
    for i in range(len(arr_word)):
        data['id_'+id_num].append({'word':arr_word[i],'pos':arr_pos[i]})
    with open(JSONLocation+set+'/'+'id_'+id_num+'.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def generateQueue():
    l = [[0,True],[1,True],[2,True],[3,True],[4,True],[5,True],[6,True],[7,True],[8,True],[9,True],[10,True],[11,True],[12,True],[13,True],[14,True],[15,True],[16,True],[17,True],[18,True],[19,True]]
    tmp = ''
    count = 0
    while( True ):
        r = random.randint( 0, 19 )
        if l[r-1][1]:
            l[r-1][1] = False
            if r<10:
                tmp = tmp+'0'+str( r )
            else:
                tmp = tmp+str( r )
            count = count+1
        if count == 20:
            break
    return tmp

def generateQueues():
    n = numberOfQueueSet
    tmp = ''
    i = 0
    while( i<n ):
        tmp = tmp+generateQueue()
        i=i+1
        if n-i!=0:
            tmp=tmp+','
    return tmp

def debug( msg ):
    if debug:
        print( "Debug: " + msg )
