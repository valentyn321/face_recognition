from unittest import result
import pytest
import sys

from recognition.logic import Recognizer
from django.core.files.uploadedfile import InMemoryUploadedFile


@pytest.fixture(scope="module")
def recognizer():
    return Recognizer()


@pytest.fixture(scope="module")
def in_memory_image_without_face_on_it():
    with open("recognition/assets/image_without_faces_on_it.jpg", "rb") as picture:
        in_memory_image = InMemoryUploadedFile(
            picture,
            "ImageField",
            picture.name,
            "JPEG",
            sys.getsizeof(picture),
            None,
        )
        yield in_memory_image


@pytest.fixture(scope="module")
def in_memory_image_with_face_on_it1():
    with open(
        "recognition/assets/image_with_valentyn_face_on_it1.png", "rb"
    ) as picture:
        in_memory_image = InMemoryUploadedFile(
            picture,
            "ImageField",
            picture.name,
            "PNG",
            sys.getsizeof(picture),
            None,
        )
        yield in_memory_image


@pytest.fixture(scope="module")
def in_memory_image_with_face_on_it2():
    with open(
        "recognition/assets/image_with_valentyn_face_on_it2.jpg", "rb"
    ) as picture:
        in_memory_image = InMemoryUploadedFile(
            picture,
            "ImageField",
            picture.name,
            "JPG",
            sys.getsizeof(picture),
            None,
        )
        yield in_memory_image


@pytest.fixture(scope="module")
def in_memory_image_with_another_face_on_it():
    with open("recognition/assets/another_image_with_face_on_it.png", "rb") as picture:
        in_memory_image = InMemoryUploadedFile(
            picture,
            "ImageField",
            picture.name,
            "PNG",
            sys.getsizeof(picture),
            None,
        )
        yield in_memory_image


def test_picture_face_recognition_fails_bad_format(recognizer):
    result = recognizer.picture_face_recognition("")
    assert result == "You have not inserted an InMemoryUploadedFile!"


def test_picture_face_recognition_no_faces(
    recognizer, in_memory_image_without_face_on_it
):
    result = recognizer.picture_face_recognition(in_memory_image_without_face_on_it)
    assert result == "There is no faces on this image!"


def test_face_detection_passes(recognizer, in_memory_image_with_face_on_it1):
    result = recognizer.picture_face_recognition(in_memory_image_with_face_on_it1)
    assert type(result) == tuple
    assert type(result[1]) == list
    assert len(result[1][0]) == 4


def test_faces_comparison_failes_because_of_bad_inputs(recognizer):
    result = recognizer.compare_two_faces([], [])
    assert result == "Not empty ndarrays should be inputs of this function!"


def test_faces_comparison_failes(
    recognizer,
    in_memory_image_with_face_on_it1,
    in_memory_image_with_another_face_on_it,
):
    image1, _ = recognizer.picture_face_recognition(in_memory_image_with_face_on_it1)
    image2, _ = recognizer.picture_face_recognition(
        in_memory_image_with_another_face_on_it
    )
    result = recognizer.compare_two_faces(image1, image2)
    assert result[0] == False


def test_faces_comparison_passes(
    recognizer, in_memory_image_with_face_on_it1, in_memory_image_with_face_on_it2
):
    image1, _ = recognizer.picture_face_recognition(in_memory_image_with_face_on_it1)
    image2, _ = recognizer.picture_face_recognition(in_memory_image_with_face_on_it2)
    result = recognizer.compare_two_faces(image1, image2)
    assert result[0] == True


# TODO
def test_faces_comparison_failes_with_many_faces():
    pass


def test_faces_comparison_failes_with_many_passes():
    pass


def test_faces_comparison_failes_one_face_vs_many():
    pass
