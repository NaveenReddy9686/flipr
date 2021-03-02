from django.contrib.auth.models import User
from rest_framework import serializers

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user.id

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('id','username',
                  'email',
                  'first_name',
                  'last_name',
                   'password', )
        read_only_fields = ('date_created', 'date_modified', 'username')

    def update(self, instance, validated_data):
        print('IN UPDATE')
        print(instance)
        # instance = User.objects.get(username=validated_data['username'])
        print(validated_data)
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            print(key,value)
            setattr(instance, key, value)
        # if password is not None:
            # instance.set_password(password)
        instance.save()
        return instance    


