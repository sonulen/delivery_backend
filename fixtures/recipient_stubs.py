from fixtures import request_dataset


class Recipients:
    __url = 'https://stepik.org/media/attachments/course/73594/recipients.json'

    def request(self):
        return request_dataset.request(self.__url)
