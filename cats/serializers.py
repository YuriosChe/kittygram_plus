from rest_framework import serializers

import datetime as dt
import webcolors

from .models import Cat, Owner, Achievement, AchievementCat, CHOICES

class Hex2NameColor(serializers.Field):
    # При чтении данных ничего не меняем - просто возвращаем как есть
    def to_representation(self, value):
        return value
    # При записи код цвета конвертируется в его название
    def to_internal_value(self, data):
        # Доверяй, но проверяй
        try:
            # Если имя цвета существует, то конвертируем код в название
            data = webcolors.hex_to_name(data)
        except ValueError:
            # Иначе возвращаем ошибку
            raise serializers.ValidationError('Для этого цвета нет имени')
        # Возвращаем данные в новом формате
        return data

class AchievementSerializer(serializers.ModelSerializer):
    # achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name') 
class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True)
    age = serializers.SerializerMethodField()
    color = serializers.ChoiceField(choices=CHOICES)
    '''добавим строку для переопределения чтобы появлялись имена вместо айди'''
    # owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements', 'age')

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year
    
    def create(self, validated_data):
        # Уберем список достижений из словаря validated_data и сохраним его
        achievements = validated_data.pop('achievements')

        # Создадим нового котика пока без достижений, данных нам достаточно
        cat = Cat.objects.create(**validated_data)

        # Для каждого достижения из списка достижений
        for achievement in achievements:
            # Создадим новую запись или получим существующий экземпляр из БД
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement)
            # Поместим ссылку на каждое достижение во вспомогательную таблицу
            # Не забыв указать к какому котику оно относится
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat)
        return cat

class OwnerSerializer(serializers.ModelSerializer):
    '''добавили запись для того чтобы появлялись имена вместо айди котиков'''
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')   


      