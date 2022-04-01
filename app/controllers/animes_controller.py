from http import HTTPStatus
from flask import jsonify, request
from app.models.anime_model import Anime
from psycopg2.errors import UniqueViolation


def get_animes():
    animes = Anime.read_animes()

    serialized_animes = [Anime.serialize(anime) for anime in animes]

    return jsonify({"data": serialized_animes})


def get_anime_by_id(anime_id):
    anime = Anime.read_anime(int(anime_id))

    try:
        anime = Anime.serialize(anime)
    except TypeError:
        return {"Error": f"Id {anime_id} not found"}, HTTPStatus.NOT_FOUND

    return jsonify({"data": [anime]})


def add_anime():
    data = request.get_json()

    data_check = Anime.check_data(data)
    if data_check:
        return data_check, HTTPStatus.UNPROCESSABLE_ENTITY

    anime = Anime(**data)

    try:
        inserted_anime = anime.create_anime()

    except UniqueViolation:
        return {"error": "Anime name already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY

    except KeyError:
        return {"error": "Key(s) missing"}, HTTPStatus.BAD_REQUEST

    serialized_anime = Anime.serialize(inserted_anime)

    return serialized_anime, HTTPStatus.CREATED


def update_anime(anime_id):
    data = request.get_json()

    data_check = Anime.check_data(data)
    if data_check:
        return data_check, HTTPStatus.UNPROCESSABLE_ENTITY

    updated_anime = Anime.patch_anime(anime_id, data)

    try:
        serialized_anime = Anime.serialize(updated_anime)

    except TypeError:
        return {"Error": f"Id {anime_id} not found"}, HTTPStatus.NOT_FOUND

    return serialized_anime


def remove_anime(anime_id):
    deleted_anime = Anime.delete_anime(anime_id)

    try:
        Anime.serialize(deleted_anime)

        return "", HTTPStatus.NO_CONTENT

    except:
        return {"error": f"Id {anime_id} not found"}, HTTPStatus.NOT_FOUND
