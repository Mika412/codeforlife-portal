import pytest
from aimmo.worksheets import WORKSHEETS, Worksheet
from aimmo.models import Game
from common.models import Class
from common.tests.utils.classes import create_class_directly
from common.tests.utils.teacher import signup_teacher_directly

from portal.forms.add_game import AddGameForm


@pytest.fixture
def teacher1_email(db) -> str:
    email, _ = signup_teacher_directly()
    return email


@pytest.fixture
def class1(db, teacher1_email) -> Class:
    klass, _, _ = create_class_directly(teacher1_email)
    return klass


@pytest.fixture
def worksheet() -> Worksheet:
    return WORKSHEETS.get(1)


def test_create_game(class1: Class):
    form = AddGameForm(
        Class.objects.all(),
        data={"game_class": class1.id},
    )
    assert form.is_valid()

    game = form.save()
    assert game.game_class == class1
    assert game.worksheet.id == 1


@pytest.mark.django_db
def test_form_with_non_existing_class():
    form = AddGameForm(
        Class.objects.all(),
        data={"game_class": 12345},
    )

    assert not form.is_valid()


@pytest.mark.django_db
def test_cannot_create_duplicate_game(class1: Class):
    # Create first game
    form = AddGameForm(
        Class.objects.all(),
        data={"game_class": class1.id},
    )
    _ = form.save()

    # Create second game with the same class
    form = AddGameForm(
        Class.objects.all(),
        data={"game_class": class1.id},
    )

    assert not form.is_valid()

    # test only one active game at a time
    assert Game.objects.filter(game_class=class1, is_archived=False).count() == 1

    assert class1.active_game != None


@pytest.mark.django_db
def test_cannot_add_game_for_classes_not_given_to_form(
    class1: Class, worksheet: Worksheet, teacher1_email: str
):
    # Make query set for form
    class_query_set = Class.objects.filter(id=class1.id)

    # Create class not in the query set
    klass, _, _ = create_class_directly(teacher1_email)

    form = AddGameForm(
        class_query_set,
        data={"game_class": klass.id, "worksheet": worksheet.id},
    )

    assert not form.is_valid()
