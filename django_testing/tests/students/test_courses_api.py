import pytest
from rest_framework.test import APIClient
from students.models import Course, Student
from django.contrib.auth.models import User
from model_bakery import baker


URL = '/api/v1/courses/'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_course_retrieve(client, student_factory, course_factory):
    students = student_factory(_quantity=3)
    courses = course_factory(_quantity=3, students=students)

    response = client.get(f'{URL}{courses[0].id}/')

    data = response.json()
    assert response.status_code == 200
    assert data['id'] == courses[0].id


@pytest.mark.django_db
def test_course_list(client, student_factory, course_factory):
    students = student_factory(_quantity=4)
    courses = course_factory(_quantity=5, students=students)

    response = client.get(URL)

    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name


@pytest.mark.django_db
def test_course_filter_id(client, student_factory, course_factory):
    students = student_factory(_quantity=10)
    courses = course_factory(_quantity=10, students=students)

    response = client.get(f'{URL}?id={courses[1].id}')

    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == courses[1].id


@pytest.mark.django_db
def test_course_filter_name(client, student_factory, course_factory):
    students = student_factory(_quantity=7)
    courses = course_factory(_quantity=3, students=students)

    response = client.get(f'{URL}?name={courses[2].name}')

    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == courses[2].name


@pytest.mark.django_db
def test_course_post(client,):
    courses = Course.objects.all().count()

    response = client.post(URL, data={'name': 'math'})
    
    assert Course.objects.all().count() == courses + 1
    assert response.status_code == 201


@pytest.mark.django_db
def test_course_patch(client, student_factory, course_factory):
    students = student_factory(_quantity=2)
    courses = course_factory(_quantity=4, students=students)

    response = client.patch(f'{URL}{courses[2].id}/',
                            data={'name': 'math'})

    data = response.json()
    assert response.status_code == 200
    assert data['name'] == 'math'


@pytest.mark.django_db
def test_course_delete(client, student_factory, course_factory):
    students = student_factory(_quantity=3)
    courses = course_factory(_quantity=3, students=students)
    courses_number = Course.objects.all().count()

    response = client.delete(f'{URL}{courses[1].id}/')

    assert response.status_code == 204
    assert Course.objects.all().count() == courses_number - 1
