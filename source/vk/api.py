import vk_api
import requests
from time import sleep
from source.static.methods import webp_to_png
from os import remove
import logging


class VkApi:
    def __init__(self, token: str):
        self.vk = vk_api.VkApi(token=token)
        self.logger = logging.getLogger('vk')

    def get_self_id(self) -> int:
        return self.vk.method('users.get')[0]['id']

    def __create_workspace(self, album):
        upload_server = self.vk.method('photos.getUploadServer', {
            'album_id': album['id']
        })

        return upload_server

    def transfer(self, collection: list, album_name: str):
        album = self.vk.method('photos.createAlbum', {
            'title': album_name,
            'privacy_view': ['nobody'],
            'upload_by_admins_only': 1,
            'description': 'Stickers from telegram imported by TG bot @PicturaBot'
        })

        us = self.__create_workspace(album=album)
        broken = 0
        for i, photo in enumerate(collection):
            try:
                photo = webp_to_png(photo)

                result = requests.post(url=us['upload_url'], files={f'file1': open(photo, 'rb')}).json()
                sleep(0.4)

                remove(photo)

                self.vk.method('photos.save', {
                    'album_id': album['id'],
                    'server': result['server'],
                    'photos_list': result['photos_list'],
                    'hash': result['hash']
                })
                sleep(0.4)
            except Exception as e:
                broken += 1
                remove(photo)
                self.logger.error(e)
                continue
        return broken

    @staticmethod
    def is_token_valid(token: str) -> bool:
        try:
            vk_api.VkApi(token=token).method('users.get')
            return True
        except Exception as e:
            return False
