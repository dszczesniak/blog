from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserLoginForm, UserRegisterForm, NewProfForm, PostForm, CommentForm, SendMessageForm
from .models import Profile, Post
from datetime import datetime



# Create your views here.
def home(request):
	all_profiles = Profile.objects.order_by('?')[:5]

	if request.user.is_authenticated():
		profile = Profile.objects.filter(author = request.user)

		context = {
		'profile':profile,
		'all_profiles':all_profiles,
		}

		return render(request, "home.html", context)
	else:

		form = SendMessageForm(request.POST or None)
		if form.is_valid():
			
			form_message = form.cleaned_data.get("message")

			subject = form.cleaned_data.get("subject")
			from_emial = settings.EMAIL_HOST_USER
			
			to_email = ['testowymailemail@gmail.com']

			contact_message = "\n\n%s \n\ngreetings" %(form_message)

			send_mail(subject, contact_message, from_emial, to_email, fail_silently=False)

			return redirect("/")

		con = {
			"form": form,
			"all_profiles":all_profiles,

		}

		return render(request, "home.html", con)



def login_view(request):
	#print(request.user.is_authenticated())
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")

		user = authenticate(username=username, password=password)
		login(request, user)
		#print(request.user.is_authenticated())
		return HttpResponseRedirect('/')

	context = {
		"form":form,
		"title":title
	}


	return render(request, "login.html", context)


def register_view(request):
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()

		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)

		return HttpResponseRedirect('/new_prof')

	context = {
		"form":form,
		"title": title
	}

	return render(request, "login.html", context)


def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')


@login_required
def new_prof_view(request):

	if request.user.is_authenticated():
		profile = Profile.objects.filter(author = request.user)

		if profile:
			print ('good')
			return HttpResponseRedirect('/my_blog')


		else:
			if request.method == "POST":
				form = NewProfForm(request.POST or None)
				if form.is_valid():
					profile = form.save(commit=False)
					profile.author = request.user
					#if profile.age > 100:
						#profile.birth_date = datetime.now()
					profile.save()
					return redirect('/my_blog')
			else:
					form = NewProfForm()
			
			return render(request, "new_prof.html", {'form': form})



def blog_detail_view(request, pk):
	user = request.user
	profile = get_object_or_404(Profile, pk=pk)
	posts_list = Post.objects.filter(author = profile.author).order_by('-updated')
	


	context = {
		'profile':profile,
		'posts_list':posts_list,
	}

	return render(request,"blog_detail.html", context)


@login_required
def my_blog_view(request):

	if request.user.is_authenticated():
		profile = Profile.objects.filter(author = request.user)

		if not profile:
			return HttpResponseRedirect('/new_prof')

		else:

			user = request.user
			profile = Profile.objects.filter(author = request.user)
			posts_list = Post.objects.filter(author = request.user).order_by('-updated')
			paginator = Paginator(posts_list, 6)

			#pagination
			page = request.GET.get('page')
			try:
				posts = paginator.page(page)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)

			#creating_form
			form = PostForm(request.POST or None, request.FILES or None)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.author = request.user
				instance.save()
				return redirect('/my_blog')
			else:
			#list_of_posts
				form = PostForm()

			context = {
				'profile':profile,
				'form': form,
				'posts':posts,
				'object_list':posts,
			}

			return render(request, "my_blog.html", context)




def post_view(request, pk):

	post = get_object_or_404(Post, pk=pk)

	if request.method == "POST" and "delete" in request.POST:
		post = get_object_or_404(Post, pk=pk).delete()
		return redirect('/my_blog')


	elif request.method == "POST" and "comment" in request.POST:
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author = request.user
			comment.post = post
			comment.save()
			return redirect('post_view', pk=post.pk)
	else:
		post = get_object_or_404(Post, pk=pk)
		if request.user.is_authenticated():
			profile = Profile.objects.filter(author = request.user)
		form = CommentForm()



	if request.user.is_authenticated():
		context = {
			'post':post,
			'profile':profile,
			'form':form,
		}
		return render(request, "post_view.html", context)

	else:
		context = {
			'post':post,
		}
		return render(request, "post_view.html", context)
