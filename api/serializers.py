from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        extra_kwargs = {'email': {'required': True}, }

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Недопустимое имя "me".')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return value


class MeSerializer(UserSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        extra_kwargs = {'email': {'required': True}, }
        read_only_fields = ['role']

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Недопустимое имя "me".')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('text', 'score')
        model = Review


class ReviewDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        read_only_fields = ('title', )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review', )
        model = Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        ]
        model = Title

    def get_rating(self, obj):
        scores = obj.reviews.values_list('score', flat=True)
        if len(scores) > 0:
            return sum(scores) // len(scores)
        return None


class TitleAdminSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = [
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        ]
        model = Title
