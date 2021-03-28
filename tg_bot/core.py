import telebot
import datetime

from django.utils import timezone

from information_manager import models as information_manager_models
from tg_bot import models
from tg_bot.utils import keyboards
from threading import Thread


class Bot(telebot.TeleBot):
    @staticmethod
    def get_start_message() -> str:
        message = 'Добрейшего времени суток!\n\n' \
                  'Тебя приветствует хоккейный помощник Иркутского политеха.\n' \
                  'Я расскажу тебе все о команде Иркутского политеха по хоккею с мячом, ' \
                  'подскажу раписание ближайших игр, а время игры буду вести текстовую трансляцию,' \
                  'еще с моей помощью можно приобрести билеты на матч и многое другое.\n\n' \
                  'Добро пожаловать!'

        return message

    @staticmethod
    def get_list_of_commands() -> str:
        message = '/start - запустить бота'

        return message

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

    def send_news(self, news: information_manager_models.News):
        """
        Отправка новости пользователям, у которых включено получение новостей.
        :param news:
        :return:
        """
        users = models.TgUser.objects.filter(news_subscription=True)

        title = 'Новости\n'
        title += f'{news.title}\n' if news.title else ''
        title += '----------------------------------\n'

        text = news.news

        for user in users:
            try:
                msg = self.send_message(chat_id=user.chat_id, text=title + text)
                information_manager_models.SentNews.objects.create(news=news, user=user, message_id=msg.message_id)
            except Exception as e:
                print(e)
                continue

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
               f'{timezone.localtime(match_query.date_of_the_event).date().strftime("%d.%m.%Y")}\n' \
               f'Время: {timezone.localtime(match_query.date_of_the_event).time().strftime("%H:%M")}\n' \
               f'{match_query.description}'

        return text

    @staticmethod
    def get_matches_this_month() -> (str, list):
        month_list = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                      'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

        month_index = datetime.datetime.now().month
        month = month_list[month_index - 1]

        matches = information_manager_models.Event.objects.filter(type_of_event='match',
                                                                  date_of_the_event__month=month_index)
        return month, matches

    def get_queryset(self) -> information_manager_models.Event:
        try:
            return information_manager_models.Event.objects.get(id=self.match_id)
        except information_manager_models.Event.DoesNotExist:
            return None
