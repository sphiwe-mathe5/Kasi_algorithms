from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from .forms import PostForm
from django.urls import reverse
import random



from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'core/index.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'core/index.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 8


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'core/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 8

    def dispatch(self, request, *args, **kwargs):

        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)

        
        if request.user != user:
            return redirect('subscribe')  

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['profile'] = user.profile

        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object

        all_other_videos = Post.objects.filter(image__isnull=False).exclude(
            pk=post.pk)

        random_suggested_videos = random.sample(list(all_other_videos),
                                                min(6, len(all_other_videos)))

        context['random_suggested_videos'] = random_suggested_videos

        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'core/post_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        post_form = self.get_form()
        return self.handle_post_form(post_form)

    def handle_post_form(self, form):
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user

        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image' ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def subscribe(request):
    if request.method == 'POST':

        profile = request.user.profile
        profile.is_paid = True
        profile.save()
        messages.success(request, 'You have successfully subscribed to the paid plan!')
        return redirect('profile')
    return render(request, 'core/subscribe.html')


def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')

def terms(request):
    return render(request, 'core/terms.html')


def prompt(request):
    return render(request, 'core/prompt.html')

def enquire(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        email_message = EmailMessage(
            subject='New Subscription from',
            body=f'Email: {email}',
            from_email=settings.ADMIN_EMAIL,  
            to=[settings.ADMIN_EMAIL],
            reply_to=[email],  
        )
        email_message.send(fail_silently=False)

        html_content = render_to_string('emails/subscribe.html', {'email': email})

        confirmation_email = EmailMultiAlternatives(
            subject="Subscription Confirmation", 
            body='', 
            from_email=settings.ADMIN_EMAIL,  
            to=[email],  
        )
        confirmation_email.attach_alternative(html_content, "text/html") 


        confirmation_email.send(fail_silently=False)

        messages.success(request, 'Thank you for Subscribing, a confirmation email has been sent!')
        return redirect('index')

    return redirect('index')



def optout(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        # Construct the email content
        email_subject = 'New Inquiry from {}'.format(first_name + ' ' + last_name)
        email_message = f'''
        You have received a new message from {first_name} {last_name}.
        
        Email: {email}
        Phone: {phone_number}
        
        Message:
        {message}
        '''

        # Send the email
        send_mail(
            subject=email_subject,
            message=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        # Notify the user
        messages.success(request, 'Your enquiry has been received. We will send you an email soon.')
        
        # Redirect to a success page or another page
        return redirect('prompt')  # or wherever you want to redirect after form submission

    return redirect('index')  # If not a POST request, redirect to index or another appropriate page
#ymws rmpb vhre njwh