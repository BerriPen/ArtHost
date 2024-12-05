from django.db import models

class Usertype(models.Model):
    name                = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class User(models.Model):
    username            = models.CharField(max_length=255, unique=True)
    email               = models.EmailField(max_length=255, unique=True)
    password            = models.CharField(max_length=255)
    usertype            = models.ForeignKey(Usertype, on_delete=models.CASCADE, null=True)
    dateJoined          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user                = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)
    followers           = models.ManyToManyField(User, related_name='following', blank=True)
    fname               = models.CharField(max_length=255)
    mname               = models.CharField(max_length=255, blank=True)
    lname               = models.CharField(max_length=255)
    suffix              = models.CharField(max_length=255, blank=True)
    contact_num         = models.CharField(max_length=15, blank=True)
    birthdate           = models.DateField()
    profile_img         = models.ImageField(upload_to='profile_imgs/', blank=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"

class Post(models.Model):
    user                = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, null=True)
    photo               = models.FileField(upload_to='general-post/')
    caption             = models.TextField(max_length=255)
    likes               = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    createdAt           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption
    
class Comment(models.Model):
    user                = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, null=True)
    post                = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True)
    content             = models.TextField(max_length=255)
    likes               = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    createdAt           = models.DateTimeField(auto_now_add=True)
    reply               = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"

class Submission(models.Model):
    user                = models.ForeignKey(User, related_name='submissions', on_delete=models.CASCADE, null=True)
    submission          = models.ImageField(upload_to='submissions/')
    caption             = models.CharField(max_length=255)
    likes               = models.ManyToManyField(User, related_name='liked_submissions', blank=True)
    createdAt           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.caption[:20]} by {self.user.username}"

class Evaluation(models.Model):
    submission          = models.ForeignKey(Submission, related_name='evaluations', on_delete=models.CASCADE)
    score               = models.IntegerField()

    def __str__(self):
        return f"Score: {self.score}"

class EventType(models.Model):
    name                = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class EventCategory(models.Model):
    name                = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Event(models.Model):
    host                = models.ForeignKey(User, related_name='hosted_events', on_delete=models.CASCADE)
    judges              = models.ManyToManyField(User, related_name='judged_events', blank=True)
    competitors         = models.ManyToManyField(User, related_name='competitor_events', blank=True)
    submissions         = models.ManyToManyField(Submission, related_name='event_submissions', blank=True)
    eventType           = models.ForeignKey(EventType, on_delete=models.CASCADE)
    eventCategory       = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    name                = models.CharField(max_length=255)
    startDate           = models.DateTimeField()
    endDate             = models.DateTimeField()
    theme               = models.CharField(max_length=255)
    description         = models.TextField(max_length=255)
    submission_rules    = models.TextField(max_length=255)
    voting_criteria     = models.TextField(max_length=255)
    prizes              = models.TextField(max_length=255)
    event_banner        = models.ImageField(upload_to='banners/', blank=True)
    createdAt           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.theme}"
