import pytest

from apps.academics.models import Department
from apps.accounts.models import User
from apps.core.models import ApprovalAction
from apps.core.services.workflow import transition
from apps.students.models import Student
from apps.theses.models import Thesis


def create_user(username, role):
    user = User.objects.create(username=username, role=role)
    user.set_unusable_password()
    user.save(update_fields=["password"])
    return user


@pytest.fixture
def thesis(db):
    department = Department.objects.create(
        code="WFLOW",
        name_ar="قسم اختبار سير العمل",
        name_en="Workflow Test Department",
    )
    student = Student.objects.create(
        university_id="WFLOW001",
        name_ar="طالب اختبار سير العمل",
        department=department,
    )
    return Thesis.objects.create(
        student=student,
        title_ar="رسالة اختبار محرك سير العمل",
        status="REGISTERED",
    )


@pytest.mark.django_db
def test_transition_updates_status_and_creates_audit(thesis):
    user = create_user("workflow_staff", User.Role.STAFF)

    result = transition(
        thesis,
        "SUBMIT",
        user,
        notes="اختبار الانتقال",
    )

    thesis.refresh_from_db()

    assert result.status == "SUBMITTED"
    assert thesis.status == "SUBMITTED"

    audit = ApprovalAction.objects.get(
        request_type="Thesis",
        object_id=thesis.id,
    )

    assert audit.action == "SUBMIT"
    assert audit.from_status == "REGISTERED"
    assert audit.to_status == "SUBMITTED"
    assert audit.performed_by == user
    assert audit.notes == "اختبار الانتقال"


@pytest.mark.django_db
def test_transition_rejects_unauthorized_role(thesis):
    user = create_user("workflow_student", User.Role.STUDENT)

    with pytest.raises(PermissionError):
        transition(thesis, "SUBMIT", user)

    thesis.refresh_from_db()

    assert thesis.status == "REGISTERED"
    assert not ApprovalAction.objects.filter(
        request_type="Thesis",
        object_id=thesis.id,
    ).exists()


@pytest.mark.django_db
def test_transition_rejects_invalid_state_transition(thesis):
    user = create_user("workflow_staff_invalid_state", User.Role.STAFF)

    thesis.status = "COMPLETED"
    thesis.save(update_fields=["status"])

    with pytest.raises(ValueError):
        transition(thesis, "SUBMIT", user)

    thesis.refresh_from_db()

    assert thesis.status == "COMPLETED"
    assert not ApprovalAction.objects.filter(
        request_type="Thesis",
        object_id=thesis.id,
    ).exists()
