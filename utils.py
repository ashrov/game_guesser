from aiogram.utils.helper import Helper, HelperMode, ListItem


class UserStates(Helper):
    mode = HelperMode.snake_case

    IDLING = ListItem()
    GUESSING = ListItem()
