from re import U
from traceback import print_list, print_tb
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from pip import List
from .models import FollowersCount, Profile,Post,LikePost,Comment
from itertools import chain
import random
# Create your views here.
@login_required(login_url='signin')
def index(request, *args,**kwargs):
    user_profile = Profile.objects.get(user=request.user)
    user_following_list = []
    feed = []
    user_following=FollowersCount.objects.filter(follower=request.user.username)
    for x in user_following:
        user_following_list.append(x.user)
    user_following_list.append(request.user)
    for user in user_following_list:
        feed_lists = Post.objects.filter(user=user)
        feed.append(feed_lists)
    feed_list=list(chain(*feed))
    #comment start here
    comment = Comment.objects.all()
    comments=comment.count()

    #suggestion starts   
    all_users= User.objects.all()
    user_follwing_all=[]
    for user in user_following:
        try:
            user_list = User.objects.get(username=user.user)
            user_follwing_all.append(user_list)
        except User.DoesNotExist:
            pass
    current_user = User.objects.filter(username=request.user.username)
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_follwing_all))]
    final_suggestions_list = [x for x in (new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)
    username_profile_list=[]
    for users in final_suggestions_list:
        user = Profile.objects.filter(user=users)
        username_profile_list.append(user)
    suggestions = list(chain(*username_profile_list))
    return render(request, 'index.html',{'user_profile':user_profile,'posts':feed_list,'comments':comments,'suggestions':suggestions[:3]})#,'suggetions':suggetions[:4]})
@login_required(login_url='signin')
def setting(request, *args, **kwargs):
    user_profile= Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('profile') == None:
            image= user_profile.profileimg
            bio =request.POST['bio']
            location=request.POST['location']
            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        if request.FILES.get('profile') != None:
            image= request.FILES.get('profile')
            bio= request.POST['bio']
            location= request.POST['location']
            
            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
    return render(request, 'setting.html',{'user_profile':user_profile})
# POST_UPLOAD START
@login_required(login_url='signin')
def upload(request, *args,**kwargs):
    if request.method == 'POST':
        user = request.user.username
        image= request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post=Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
# LIKE_POSTS START
@login_required(login_url='signin')
def like_post(request,*args,**kwargs):
        username=request.user.username
        post_id = request.GET.get('post_id') 
        post = Post.objects.get(id=post_id)
        like_filter=LikePost.objects.filter(post_id=post_id,username=username).first()
        if like_filter==None:
            new_like=LikePost.objects.create(post_id=post_id,username=username)
            new_like.save()
            try:
                post.no_of_likes=post.no_of_likes+1
                post.save()
                return redirect('/')
            except Exception as e:
                return redirect('/',e)
        else:
            like_filter.delete()
            try:
                post.no_of_likes=post.no_of_likes-1
                post.save()
                return redirect('/')
            except Exception as e:
                return redirect('/',e)
# PROFILE STARTS
@login_required(login_url='signin')
def profile(request, pk,*args,**kwargs):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts= Post.objects.filter(user=pk)
    user_post_length=len(user_posts)
    follower = request.user.username 
    user =pk
    if FollowersCount.objects.filter(follower=follower,user=user).exists():
        button_text='unfollow'
    else:
        button_text = 'follow'
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))
    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_length':user_post_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following,
    }
    return render(request,'pro2.html',context)
# FOLLOW_USER STARTS
@login_required(login_url='signin')
def follow(request, *args,**kwargs):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        if FollowersCount.objects.filter(follower=follower,user=user).first():
            delete_follower= FollowersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_followers= FollowersCount.objects.create(user=user,follower=follower)
            new_followers.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')
# FOLLOWERS_LIST STARTS
@login_required(login_url='signin')
def followers_list(request, *args,**kwargs):
    user_followers_list=[]
    user_followers=FollowersCount.objects.filter(user=request.user.username)
    for x in user_followers:
        user=User.objects.filter(username=x.follower)
        user_followers_list.append(user)
    profile=[]
    profile_list=[]
    for x in user_followers_list:
        user_profile=Profile.objects.filter(user=x)
        profile.append(user_profile)
    return render(request, 'followers_list.html') 
# SEARCH_USERS STARTS
@login_required(login_url='signin')
def search(request, *args,**kwargs):
    if request.method == 'POST':
        username =request.POST['username']
        username_profile =User.objects.filter(username__icontains=username)

        username_profile_list=[]
        for user in username_profile:
            profile_lists=Profile.objects.filter(user=user)
            username_profile_list.append(profile_lists)
    
        username_profile_list=list(chain(*username_profile_list))
    return render(request, 'search.html',{'users':username_profile_list})
# DELETE_POST STARTS
def delete_post(request, pk,*args,**kwargs):
    post =  Post.objects.get(id=pk)
    user = request.user
    if user.username == post.user:
        Post.objects.get(id=post.id).delete()
        return redirect('/')
    else:
         messages.info(request,"not allowed")
    return redirect('/')
# ADD_COMMENT STARTS
def addcomment(request, *args,**kwargs):
    user=User.objects.get(username=request.user.username)
    if request.method =='POST':
                comment=request.POST['comment']  
                post= request.POST['post']
                commented_post =Post.objects.get(id=post)
                create= Comment.objects.create(user=user,comment=comment,post=commented_post)
                create.save()
                return redirect('/')
# LIST_COMMENTS STARTS
def list_comment(request,pk = None, *args,**kwargs):
    post = Post.objects.get(id=pk)
    comment = Comment.objects.filter(post=post)
    return render (request,'comment_list.html',{'comment':comment})
# SIGN_UP
def signup(request, *args,**kwargs):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email Taken")
                return redirect('signup')

            elif User.objects.filter(username=username).exists():
                messages.info(request,"username Taken")
                return redirect('signup')
            else:
                user =User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                user_login=auth.authenticate(username=username, password=password1)
                auth.login(request,user_login)
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()  
                return redirect('setting')
    return render(request, 'signup.html')
# SIGN IN
def signin(request, *args,**kwargs):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user= auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid username or password')
            return render(request, 'signin.html')

    else:   
        return render(request, 'signin.html')
# LOGOUT
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')