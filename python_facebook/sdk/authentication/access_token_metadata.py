from datetime import datetime

from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException


class AccessTokenMetadata(object):

    date_properties = ['expires_at', 'issued_at']

    def __init__(self, metadata):
        if not metadata.get('data'):
            raise FacebookSDKException('Unexpected debug token response data.', 401)

        self.metadata = metadata['data']
        self.cast_timestamps_to_datetime()

    def get_field(self, name, default=None):
        return self.metadata.get(name, default)

    def get_child_property(self, parent_field, name, default=None):
        if parent_field not in self.metadata:
            return default

        if name not in self.metadata[parent_field]:
            return default

        return self.metadata[parent_field][name]

    def get_error_property(self, name, default=None):
        return self.get_child_property('error', name, default)

    def get_metadata_property(self, name, default=None):
        return self.get_child_property('metadata', name, default)

    def get_app_id(self):
        return self.get_field('app_id')

    def get_application(self):
        return self.get_field('application')

    def is_error(self):
        return self.get_field('error') is not None

    def get_error_code(self):
        return self.get_error_property('code')

    def get_error_message(self):
        return self.get_error_property('message')

    def get_error_subcode(self):
        return self.get_error_property('subcode')

    def get_expires_at(self):
        return self.get_field('expires_at')

    def get_is_valid(self):
        return self.get_field('is_valid')

    def get_issued_at(self):
        return self.get_field('issued_at')

    def get_metadata(self):
        return self.get_field('metadata')

    def get_sso(self):
        return self.get_metadata_property('sso')

    def get_auth_type(self):
        return self.get_metadata_property('auth_type')

    def get_auth_nonce(self):
        return self.get_metadata_property('auth_nonce')

    def get_profile_id(self):
        return self.get_field('profile_id')

    def get_scopes(self):
        return self.get_field('scopes')

    def get_user_id(self):
        return self.get_field('user_id')

    def validate_app_id(self, app_id):
        if self.get_app_id() != app_id:
            raise FacebookSDKException('Access token metadata contains unexpected app ID.', 401)

    def validate_user_id(self, user_id):
        if self.get_user_id() != user_id:
            raise FacebookSDKException('Access token metadata contains unexpected user ID.', 401)

    def validate_expiration(self):
        if not isinstance(self.get_expires_at(), datetime):
            return

        if self.get_expires_at() < datetime.now():
            raise FacebookSDKException('Inspection of access token metadata shows that the access token has expired.', 401)

    def convert_timestamp_to_datetime(self, timestamp):
        return datetime.fromtimestamp(timestamp)

    def cast_timestamps_to_datetime(self):
        for key in self.date_properties:
            if self.metadata.get(key) and self.metadata.get(key) != 0:
                self.metadata[key] = self.convert_timestamp_to_datetime(self.metadata[key])
