import telebot
import datetime

from django.conf import settings
from django.utils import timezone, dateformat

from information_manager import models as information_manager_models
from tg_bot import models
from tg_bot.utils import keyboards
from threading import Thread


class Bot(telebot.TeleBot):
    @staticmethod
    def get_start_message() -> str:
        message = 'Добрейшего времени суток!🤗\n\n' \
                  '✋Тебя приветствует хоккейный помощник Иркутского политеха.🤚\n' \
                  'Я расскажу тебе все о команде Иркутского политеха по хоккею с мячом, ' \
                  'подскажу раписание ближайших игр, а время игры буду вести текстовую трансляцию,' \
                  'еще с моей помощью можно приобрести билеты на матч и многое другое.\n\n' \
                  'Добро пожаловать!✨'

        return message

    @staticmethod
    def get_list_of_commands() -> str:
        message = '/start - запустить бота'

        return message

    def send_invalid_message_answer(self, chat_id):
        text = 'Я Вас не понимаю. Воспользуйтесь клавиатурой'
        self.send_message(chat_id=chat_id, text=text, reply_markup=keyboards.get_main_menu_keyboard())

    @staticmethod
    def get_authors() -> str:
        text = 'Авторы проекта ВасГен бот:\n' \
               'Сидоренко Анжелика - @alikastory\n' \
               'Лесков Алексей - @bolanebyla\n' \
               'Ашимов Султан - @ace_sultan\n'

        return text

    def send_message_to_all_users(self, text):
        pass

    def send_message_text_translation(self, match: information_manager_models.Event, text):
        """
        Отправка сообщения текстовой трансляции
        :param match:
        :param text:
        :return:
        """
        users = match.users_for_text_translation.all()
        title = 'Текстовая трансляция\n' \
                f'{match.title}\n' \
                f'----------------------------------\n'
        for user in users:
            try:
                self.send_message(chat_id=user.chat_id, text=title + text)
            except Exception as e:
                continue

    def send_news(self, news: information_manager_models.News, photo: bytes = None):
        """
        Отправка новости пользователям, у которых включено получение новостей.
        :param photo:
        :param news:
        :return:
        """
        users = models.TgUser.objects.filter(news_subscription=True)

        title = 'Новости🛎\n'
        title += f'{news.title}\n' if news.title else ''
        title += '----------------------------------\n'

        text = news.news

        for user in users:
            try:
                if photo:
                    msg = self.send_photo(chat_id=user.chat_id, photo=photo, caption=title + text)
                else:
                    msg = self.send_message(chat_id=user.chat_id, text=title + text)

                information_manager_models.SentNews.objects.create(news=news, user=user, message_id=msg.message_id)
            except Exception as e:
                print(e)
                continue

    def delete_sent_news(self, news_id):
        """
        Удаление отправленных новостей
        :param news_id:
        :return:
        """
        sent_news_info = information_manager_models.SentNews.objects.filter(news__id=news_id)
        for news in sent_news_info:
            try:
                self.delete_message(chat_id=news.user.chat_id, message_id=news.message_id)
            except Exception as e:
                continue
        try:
            information_manager_models.News.objects.get(id=news_id).delete()
        except information_manager_models.News.DoesNotExist:
            pass

    def start_reminders(self):
        """
        Запуск сервиса напоминаний
        !Запускать в отдельном потоке!
        :return:
        """
        print('Напоминания запущены...')
        minutes_old = None
        while True:
            now = datetime.datetime.now()

            # действие выполняется кадую минуту
            if minutes_old != now.minute:
                minutes_old = now.minute

                # определяем время матча через день
                time_very_other_day = now + datetime.timedelta(days=1)
                date_matches_very_other_day = time_very_other_day.date()
                hours_matches_very_other_day = time_very_other_day.hour
                minutes_matches_very_other_day = time_very_other_day.minute

                # получаем матчи которые будут через день
                matches_every_other_day = information_manager_models.Event.objects.filter(
                    type_of_event='match',
                    date_of_the_event__date=date_matches_very_other_day,
                    date_of_the_event__hour=hours_matches_very_other_day,
                    date_of_the_event__minute=minutes_matches_very_other_day)

                # определяем время матча через час
                time_matches_in_an_hour = now + datetime.timedelta(hours=1)
                date_matches_in_an_hour = time_matches_in_an_hour.date()
                hours_matches_in_an_hour = time_matches_in_an_hour.hour
                minutes_matches_in_an_hour = time_matches_in_an_hour.minute

                # получаем матчи которые будут через час
                matches_in_an_hour = information_manager_models.Event.objects.filter(
                    type_of_event='match',
                    date_of_the_event__date=date_matches_in_an_hour,
                    date_of_the_event__hour=hours_matches_in_an_hour,
                    date_of_the_event__minute=minutes_matches_in_an_hour)

                # запускаем потоки с отправкой уведомлений
                if matches_every_other_day:
                    send_reminders_every_other_day = Thread(target=self._send_reminders,
                                                            args=(matches_every_other_day, 'Уже завтра!\n',))
                    send_reminders_every_other_day.start()

                if matches_in_an_hour:
                    send_reminders_an_hour = Thread(target=self._send_reminders,
                                                    args=(matches_in_an_hour, 'Уже через час!\n'))
                    send_reminders_an_hour.start()

    def _send_reminders(self, matches_queryset, title):
        """
        Отправка уведомлений о матче пользователям
        :param matches_queryset:
        :return:
        """
        users = models.TgUser.objects.filter(event_notifications=True)
        for match in matches_queryset:
            for user in users:
                try:
                    match.users_for_text_translation.get(chat_id=user.chat_id)
                    is_text_translation_active = True
                except models.TgUser.DoesNotExist:
                    is_text_translation_active = False

                try:
                    self.send_message(
                        chat_id=user.chat_id, text=f'{title}' + Match.get_match_info(match),
                        reply_markup=keyboards.get_inline_match_keyboard(
                            event_id=match.id,
                            is_text_translation_active=is_text_translation_active))
                except Exception as e:
                    continue


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.object = self._registration()

    def _registration(self):
        try:
            return models.TgUser.objects.get(chat_id=self.chat_id)
        except models.TgUser.DoesNotExist:
            return models.TgUser.objects.create(chat_id=self.chat_id)

    def enable_match_notifications(self):
        pass

    def disable_match_notifications(self):
        pass

    def enable_newsletter(self):
        pass

    def disable_newsletter(self):
        pass


class BettingOnGames:
    def get_score(self, user: User) -> str:
        pass

    def get_matches_list(self) -> list:
        pass


class Coaches:
    def __init__(self, post):
        self.post = post
        self.object = self.get_queryset()

    @staticmethod
    def get_coach(post):
        try:
            return information_manager_models.CoachingStaff.objects.get(post=post)
        except information_manager_models.CoachingStaff.DoesNotExist:
            return information_manager_models.CoachingStaff.objects.none()

    @staticmethod
    def get_coach_info(coach_query) -> str:
        text = f'👉{coach_query.lastname} {coach_query.firstname} {coach_query.patronymic}\n' \
               f'Родился {coach_query.birthdate.strftime("%d.%m.%Y")}\n' \
               f'--------------------------------------\n' \
               f'📃Краткая информация:\n{coach_query.brief_information}\n' \
               f'--------------------------------------\n' \
               f'🏆Карьера:\n{coach_query.progress}\n'
        return text

    def get_queryset(self) -> information_manager_models.CoachingStaff:
        try:
            return information_manager_models.CoachingStaff.objects.get(post=self.post)
        except Exception as e:
            return information_manager_models.CoachingStaff.objects.none()


class Players:
    def __init__(self, playing_position):
        self.playing_position = playing_position
        self.object = self.get_queryset()

    @staticmethod
    def get_players(playing_position):
        try:
            player_query = information_manager_models.Player.objects.filter(playing_position=playing_position)
            return player_query
        except information_manager_models.Player.DoesNotExist:
            return information_manager_models.Player.objects.none()

    @staticmethod
    def get_player(full_name):
        try:
            return information_manager_models.Player.objects.get(lastname=full_name.split()[0],
                                                                 firstname=full_name.split()[1])
        except information_manager_models.Player.DoesNotExist:
            return information_manager_models.Player.objects.none()

    @staticmethod
    def get_player_info(player_query) -> str:
        cap = "Является капитаном команды!\n"
        text = f'👉{player_query.lastname} {player_query.firstname} {player_query.patronymic}\n' \
               f'Родился {player_query.birthdate.strftime("%d.%m.%Y")}\n' \
               f'Игровая позиция: {player_query.playing_position}\n' \
               f'{cap if player_query.is_captain else ""}' \
               f'--------------------------------------\n' \
               f'📃Краткая информация:\n{player_query.brief_information}\n' \
               f'--------------------------------------\n' \
               f'🏆Карьера:\n{player_query.progress}\n'
        return text

    def get_queryset(self) -> information_manager_models.CoachingStaff:
        try:
            return information_manager_models.CoachingStaff.objects.get(post=self.post)
        except information_manager_models.CoachingStaff.DoesNotExist:
            return information_manager_models.CoachingStaff.objects.none()


class Match:
    def __init__(self, match_id):
        self.match_id = match_id
        self.object = self.get_queryset()

    def enable_match_notifications(self, chat_id):
        pass

    def disable_match_notifications(self, chat_id):
        pass

    def enable_text_translation(self, user: User):
        self.object.users_for_text_translation.add(user.object.id)

    def disable_text_translation(self, user: User):
        self.object.users_for_text_translation.remove(user.object.id)

    @staticmethod
    def get_match_info(match_query) -> str:
        text = f'{match_query.title}\n' \
               f'{dateformat.format(timezone.localtime(match_query.date_of_the_event).date(), settings.DATE_FORMAT)}\n' \
               f'Время: {timezone.localtime(match_query.date_of_the_event).time().strftime("%H:%M")}\n' \
               f'{match_query.description}'

        return text

    @staticmethod
    def get_matches_this_month() -> (str, list):
        month_list = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                      'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

        now = datetime.datetime.now()

        month_index = now.month
        month = month_list[month_index - 1]

        matches = information_manager_models.Event.objects.filter(
            type_of_event='match',
            date_of_the_event__month=month_index,
            date_of_the_event__gte=now - datetime.timedelta(hours=2))
        return month, matches

    def get_queryset(self) -> information_manager_models.Event:
        try:
            return information_manager_models.Event.objects.get(id=self.match_id)
        except information_manager_models.Event.DoesNotExist:
            return information_manager_models.Event.objects.none()

    @staticmethod
    def get_nearest_match() -> information_manager_models.Event:
        now = datetime.datetime.now()
        matches = information_manager_models.Event.objects.filter(date_of_the_event__gte=now, type_of_event='match')
        if matches:
            return matches[0]
        else:
            return information_manager_models.Event.objects.none()
