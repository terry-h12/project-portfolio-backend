from rest_framework import serializers
from Project.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_account')
    profile_pic = serializers.SerializerMethodField('get_profile_pic_from_account')

    def get_username_from_account(self, project):
        username = project.account_id.username
        return username

    def get_profile_pic_from_account(self, project):
        pfp = project.account_id.profile_pic
        return pfp

    class Meta:
        model = Project
        fields = ['pk', 'image_url', 'username', 'profile_pic', 'account_id', 'title', 'description', 'is_public', 'time_created']

class ProjectUpdateSerializer(serializers.ModelSerializer):
     class Meta:
        model = Project
        fields = ['title', 'image_url', 'description', 'backend_repo', 'frontend_repo', 'website']   

     def validate(self, project):
        try:
            title          = project['title']
            image_url      = project['image_url']
            description    = project['description']
            backend_repo   = project['backend_repo']
            frontend_repo  = project['frontend_repo']
            website        = project['website']
        except KeyError:
            pass
        return project 

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['image_url', 'account_id', 'title', 'description', 'is_public', 'time_created', 'backend_repo', 'frontend_repo', 'website']

    def save(self):
        try:
            image_url = self.validated_data['image_url']
            account_id = self.validated_data['account_id']
            title = self.validated_data['title']
            description = self.validated_data['description']
            is_public = self.validated_data['is_public']
            backend_repo = self.validated_data['backend_repo']
            frontend_repo = self.validated_data['frontend_repo']
            website = self.validated_data['website']
            # if ('backend_repo' in self.validated_data):
            #     backend_repo = self.validated_data['backend_repo']
            # else:
            #     backend_repo = None
            # if ('frontend_repo' in self.validated_data):
            #     frontend_repo = self.validated_data['frontend_repo']
            # else:
            #     backend_repo = None
            # if ('website' in self.validated_data):
            #     website = self.validated_data['website']
            # else:
            #     website = None
            #current_dollar = self.validated_data['current_dollar']
            #time_created = self.validated_data['time_created']
            project = Project(
                image_url      = image_url,
                account_id     = account_id,
                title          = title,
                description    = description,
                is_public      = is_public,
                website        = website,
                backend_repo   = backend_repo,
                frontend_repo  = frontend_repo
            )
            project.save()
            return project
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a title, description, title and a backend/frontend repo"}) 
