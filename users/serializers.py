from rest_framework import serializers

from users.models import User, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=True)

    class Meta:
        model = Location
        fields = ['username', 'location']


class UserSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=True)

    class Meta:
        model = User
        exclude = ['password', ]


class UserListSerializer(serializers.ModelSerializer):
    total_ads = serializers.IntegerField()

    class Meta:
        model = User
        exclude = ['password', 'location', ]


class UserCreateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False, many=True, slug_field="name",
                                            queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop("location", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        new_user = User.objects.create(**validated_data)
        new_user.set_password(validated_data['password'])  # второй метод хеширования пароля при создании пользователя
        new_user.save()
        for loc in self._locations:
            loc, created = Location.objects.get_or_create(name=loc)
            new_user.location.add(loc)
        return new_user

    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False, many=True, slug_field="name",
                                            queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop("location", [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.location.all().delete()

        for loc in self._locations:
            loc, created = Location.objects.get_or_create(name=loc)
            user.location.add(loc)
        return user

    class Meta:
        model = User
        fields = '__all__'
