from src.utils.image_utils import upload_img, download_img, super
from src.save import save


class UpScale:
    def __init__(self, img_path, key, scale, face_enhance, output_folder):
        self.img_path = img_path
        self.key = key
        self.scale = scale
        self.face_enhance = face_enhance
        self.output_folder = output_folder

    def upload(self):
        self.img_url = upload_img(self.img_path)

    def super_resolution(self):
        response, self.image_urls = super(self.key, str(self.img_url), self.scale, self.face_enhance)
        
    def download(self):
        download_img(self.image_urls, self.output_folder)
