import os

class Settings:
    def __init__(self):
        self.app_port=int(os.environ["APP_PORT"])
        self.app_host=os.environ["APP_HOST"]
        
        self.db_api_url=os.environ["DB_API_URL"]
        self.picture_api_url=os.environ["PICTURE_API_URL"]

        try:
            self.default_pictures_urls = self._get_all_paths_in_folder("static/images/default_hobbies")
        except:
            self.default_pictures_urls = self._get_all_paths_in_folder("microservices\\web-ui\\src\\static\\images\\default_hobbies")

    def _get_all_paths_in_folder(self, directory):
        file_urls = []
        for filename in os.listdir(directory):
            # Get the full path
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                # Convert file path to a URL-like path (if needed)
                file_urls.append(file_path.replace('\\', "/").replace('microservices/web-ui/src/static/', ""))
        return file_urls