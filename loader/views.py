import os.path
from flask import Blueprint, render_template, request, current_app
from classes.database import DataBase
from .exceptions import PictureFormatNotSupportedError
from .exceptions import PictureNotUploadedError
import logging


logger = logging.getLogger("basic")

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')


def is_file_type_valid(file_type):
    if file_type.lower() in ["jpg", "jpeg", "gif", "pnd", ""]:
        return True
    return False


@loader_blueprint.route('/post', methods=['GET', 'POST'])
def page_create_posts():
    if request.method == "POST":
        picture = request.files.get('picture', None)
        content = request.values.get('content', '')
        filename = picture.filename

        file_type = filename.split('.')[-1].lower()
        logger.info(f"Формат файла {file_type} ")
        if not is_file_type_valid(file_type):
            raise PictureFormatNotSupportedError("Формат  не поддерживается")

        os_path = os.path.join(".", "uploads", "images", filename)

        if not filename:
            raise PictureNotUploadedError(f"{os_path, filename}")
        logger.info(f"Картинка загружена")
        picture.save(os_path)

        web_path = os.path.join("/", "uploads", "images", filename)
        pic = web_path
        path = current_app.config.get("POST_PATH")
        db = DataBase(path)

        post = {"pic": pic, "content": content}

        db.add(post)

        return render_template('post_uploaded.html', pic=pic, content=content)
    return render_template('post_form.html')


@loader_blueprint.errorhandler(PictureFormatNotSupportedError)
def error_format_not_supported(e):
    logger.error(f"Недопустимый формат файла")
    return "Формат картинки не поддерживается выберите другой"


@loader_blueprint.errorhandler(PictureNotUploadedError)
def error_picture_not_uploaded(e):
    logger.error(f"Картинка не загружена")
    return "Картинки не загружена"
