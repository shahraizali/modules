from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.forms import ResetPasswordForm
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists, generate_unique_username
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers

from home.models import OfferigsPage, Activities, UserConnectRequest, ConnectProfile, AboutTeamAndBoardMember, Session, \
    UserSession, SessionAttachment, ActivitiesAttachment, UserActivities

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            }
        }

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            username=generate_unique_username([
                validated_data.get('name'),
                validated_data.get('email'),
                'user'
            ])
        )
        user.set_password(validated_data.get('password'))
        user.save()
        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class PasswordSerializer(PasswordResetSerializer):
    """Custom serializer for rest_auth to solve reset password error"""
    password_reset_form_class = ResetPasswordForm

class ActivitiesAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitiesAttachment
        fields = '__all__'

class SessionAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionAttachment
        fields = '__all__'


class UserSessionSerializer(serializers.ModelSerializer):
    attachments = serializers.SerializerMethodField()

    def get_attachments(self, obj):
        return SessionAttachmentSerializer(obj.session_attachment.all(), many=True, context=self.context).data

    class Meta:
        model = Session
        fields = [
            'id', 'title', 'date', 'start_time', 'session_number', 'image', 'sort', 'description', 'attachments'
        ]
        extra_kwargs = {
            "user": {"required": False}
        }


class EventsActivitySerializer(serializers.ModelSerializer):
    attachments = serializers.SerializerMethodField()

    def get_attachments(self, obj):
        return ActivitiesAttachmentSerializer(obj.activity_attachment.all(), many=True, context=self.context).data

    class Meta:
        model = Activities
        fields = '__all__'


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConnectRequest
        fields = '__all__'
        extra_kwargs = {
            "requester": {"required": False}
        }


class ConnectProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ConnectProfile
        fields = '__all__'


class AboutTeamAndBoardSerializer(serializers.ModelSerializer):
    connect_user = ConnectProfileSerializer(read_only=True)

    class Meta:
        model = AboutTeamAndBoardMember
        fields = ['select', 'connect_user']
        ordering = ['connect_user__user__last_name']


class OfferigsPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferigsPage
        fields = '__all__'


class HomeSessionSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format="%I:%M %p", required=False, source='session.start_time')
    title = serializers.CharField(required=False, source='session.title')
    description = serializers.CharField(required=False, source='session.description')
    image = serializers.ImageField(required=False, source='session.image')
    type = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    start_time_stamp = serializers.SerializerMethodField()

    def get_start_time_stamp(self, obj):
        return obj.session.start_time

    def get_type(self, obj):
        return "session"

    def get_attachments(self, obj):
        all_session_attachments = self.context.get('all_session_attachments')
        session_id = obj.session.id
        if not all_session_attachments:
            all_session_attachments = obj.session.session_attachment.all()
        return SessionAttachmentSerializer(
            all_session_attachments.filter(session_id=session_id), many=True,
            context=self.context
        ).data

    class Meta:
        model = UserSession
        fields = '__all__'




class HomeActivitiesSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format="%I:%M %p", required=False, source='activity.start_time')
    title = serializers.CharField(required=False, source='activity.title')
    description = serializers.CharField(required=False, source='activity.description')
    image = serializers.ImageField(required=False, source='activity.image')
    type = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    start_time_stamp = serializers.SerializerMethodField()

    def get_type(self, obj):
        return "activity"

    def get_start_time_stamp(self, obj):
        return obj.activity.start_time

    def get_attachments(self, obj):
        all_activity_attachments = self.context.get('all_activity_attachments')
        activity_id = obj.activity.id
        if not all_activity_attachments:
            all_activity_attachments = obj.activity.activity_attachment.all()
        return ActivitiesAttachmentSerializer(
            all_activity_attachments.filter(activity_id=activity_id), many=True,
            context=self.context
        ).data

    class Meta:
        model = UserActivities
        fields = '__all__'

