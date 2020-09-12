from fixtures import request_dataset


class FoodBoxes:
    __url = 'https://stepik.org/media/attachments/course/73594/foodboxes.json'

    def request(self):
        return request_dataset.request(self.__url)
