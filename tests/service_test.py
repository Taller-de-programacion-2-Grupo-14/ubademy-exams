import unittest
from unittest.mock import Mock, patch
from exceptions.ExamException import (
    IsNotTheCourseCreator,
    ExamsLimitReached,
    ExamDoesNotExist,
    InvalidUserAction,
    ResolutionDoesNotExists,
    ExamAlreadyResolvedException,
)
from persistence.mongo import MongoDB
from validator.ExamValidator import ExamValidator
from service.Exam import ExamService


class TestCreateExam(unittest.TestCase):
    def test_create_exam_when_not_creator(self):
        mock_validator = Mock(spec=ExamValidator)
        attrs = {"is_course_creator.return_value": False}
        mock_validator.configure_mock(**attrs)
        service = ExamService(MongoDB, mock_validator)
        with self.assertRaises(IsNotTheCourseCreator):
            service.create_exam({})

    def test_create_exam_when_creator(self):
        mock_validator = Mock(spec=ExamValidator)
        mock_db = Mock(spec=MongoDB)
        attrs_validator = {
            "is_course_creator.return_value": True,
            "exams_limit_reached.return_value": False,
        }
        attrs_db = {"get_exams.return_value": []}
        mock_validator.configure_mock(**attrs_validator)
        mock_db.configure_mock(**attrs_db)
        service = ExamService(mock_db, mock_validator)
        result = service.create_exam({})
        self.assertIsNone(result)


class TestEditExam(unittest.TestCase):
    def test_edit_exam_that_does_not_exist(self):
        mock_db = Mock(spec=MongoDB)
        attrs_db = {"get_course_status.return_value": []}
        mock_db.configure_mock(**attrs_db)
        service = ExamService(mock_db, Mock())
        with self.assertRaises(ExamDoesNotExist):
            service.edit_exam({})

    @patch("service.Exam.ExamService._check_draft_exam_existance")
    def test_edit_exam_when_not_creator(self, mock_check_existance):
        mock_check_existance.return_value = None
        mock_validator = Mock(spec=ExamValidator)
        attrs_validator = {"is_course_creator.return_value": False}
        mock_validator.configure_mock(**attrs_validator)
        service = ExamService(MongoDB, mock_validator)
        with self.assertRaises(IsNotTheCourseCreator):
            service.edit_exam({})

    @patch("service.Exam.ExamService._check_draft_exam_existance")
    def test_edit_exam_being_creator(self, mock_check_existance):
        mock_check_existance.return_value = None
        mock_validator = Mock(spec=ExamValidator)
        attrs_validator = {"is_course_creator.return_value": True}
        mock_validator.configure_mock(**attrs_validator)
        mock_db = Mock(spec=MongoDB)
        attrs_db = {"edit_exam.return_value": None}
        mock_db.configure_mock(**attrs_db)
        service = ExamService(mock_db, mock_validator)
        result = service.edit_exam({})
        self.assertIsNone(result)


class TestPublishExam(unittest.TestCase):
    def test_publish_exam_not_being_creator(self):
        mock_validator = Mock(spec=ExamValidator)
        attrs = {"is_course_creator.return_value": False}
        mock_validator.configure_mock(**attrs)
        service = ExamService(MongoDB, mock_validator)
        with self.assertRaises(IsNotTheCourseCreator):
            service.publish_exam({})

    @patch("service.Exam.ExamService._check_draft_exam_existance")
    def test_publish_exam_when_limit_reached(self, mock_check_existance):
        mock_check_existance.return_value = None
        mock_validator = Mock(spec=ExamValidator)
        attrs = {
            "is_course_creator.return_value": True,
            "exams_limit_reached.return_value": True,
        }
        mock_validator.configure_mock(**attrs)
        mock_db = Mock(spec=MongoDB)
        attrs_db = {"get_exams.return_value": []}
        mock_db.configure_mock(**attrs_db)
        service = ExamService(mock_db, mock_validator)
        with self.assertRaises(ExamsLimitReached):
            service.publish_exam({})

    def test_publish_exam_that_does_not_exist(self):
        mock_db = Mock(spec=MongoDB)
        attrs_db = {"get_course_status.return_value": []}
        mock_db.configure_mock(**attrs_db)
        service = ExamService(mock_db, Mock())
        with self.assertRaises(ExamDoesNotExist):
            service.publish_exam({})

    @patch("service.Exam.ExamService._check_draft_exam_existance")
    def test_publish_exam_successfully(self, check_existance_mock):
        check_existance_mock.return_value = None
        mock_db = Mock(spec=MongoDB)
        attrs_db = {"get_exams.return_value": [], "publish_exam.return_value": None}
        mock_db.configure_mock(**attrs_db)
        mock_validator = Mock(spec=ExamValidator)
        attrs_validator = {
            "is_course_creator.return_value": True,
            "exams_limit_reached.return_value": False,
        }
        mock_validator.configure_mock(**attrs_validator)
        service = ExamService(mock_db, mock_validator)
        result = service.publish_exam({})
        self.assertIsNone(result)


class TestGetExams(unittest.TestCase):
    def test_get_exams_not_being_on_the_course(self):
        mock_validator = Mock(spec=ExamValidator)
        attrs = {
            "is_course_creator.return_value": False,
            "is_student.return_value": False,
            "is_course_collaborator.return_value": False,
        }
        mock_validator.configure_mock(**attrs)
        service = ExamService(Mock(), mock_validator)
        with self.assertRaises(InvalidUserAction):
            service.get_exams(0, 0, {})

    @patch("service.Exam.ExamService._check_published_exam_existance")
    def test_get_resolutions_not_being_on_the_course(self, check_existance_mock):
        check_existance_mock.return_value = None
        mock_validator = Mock(spec=ExamValidator)
        attrs = {"is_grader.return_value": False, "is_student.return_value": False}
        mock_validator.configure_mock(**attrs)
        service = ExamService(Mock(), mock_validator)
        with self.assertRaises(InvalidUserAction):
            service.get_resolutions(0, 0, None)


class TestGetResolutions(unittest.TestCase):
    @patch("service.Exam.ExamService._check_published_exam_existance")
    def test_get_resolution_of_nonexistent_exam(self, check_existance_mock):
        check_existance_mock.side_effect = ExamDoesNotExist
        mock_validator = Mock(spec=ExamValidator)
        attrs = {"is_grader.return_value": False, "is_student.return_value": False}
        mock_validator.configure_mock(**attrs)
        service = ExamService(Mock(), mock_validator)
        with self.assertRaises(ExamDoesNotExist):
            service.get_resolution(0, "", 0, 0)

    @patch("service.Exam.ExamService._check_published_exam_existance")
    def test_get_resolution_of_classmate(self, check_existance_mock):
        check_existance_mock.return_value = None
        mock_validator = Mock(spec=ExamValidator)
        attrs = {"is_grader.return_value": False, "is_student.return_value": True}
        mock_validator.configure_mock(**attrs)
        service = ExamService(Mock(), mock_validator)
        with self.assertRaises(InvalidUserAction):
            service.get_resolution(0, "", 0, 2)

    @patch("service.Exam.ExamService._check_published_exam_existance")
    def test_get_resolution_not_being_on_the_course(self, check_existance_mock):
        check_existance_mock.return_value = None
        mock_validator = Mock(spec=ExamValidator)
        attrs = {"is_grader.return_value": False, "is_student.return_value": False}
        mock_validator.configure_mock(**attrs)
        service = ExamService(Mock(), mock_validator)
        with self.assertRaises(InvalidUserAction):
            service.get_resolution(0, "0", 0, 0)


class TestGradeResolution(unittest.TestCase):
    def test_grade_resolution_not_being_grader(self):
        mock_validator = Mock(spec=ExamValidator)
        attrs = {"is_grader.return_value": False}
        mock_validator.configure_mock(**attrs)
        service = ExamService(Mock(), mock_validator)
        with self.assertRaises(InvalidUserAction):
            service.grade_resolution(0, {})

    @patch("service.Exam.ExamService._check_resolution_exam")
    def test_grade_nonexistent_resolution(self, check_existance_mock):
        check_existance_mock.side_effect = ResolutionDoesNotExists
        mock_validator = Mock(spec=ExamValidator)
        attrs = {"is_grader.return_value": True}
        mock_validator.configure_mock(**attrs)
        service = ExamService(Mock(), mock_validator)
        with self.assertRaises(ResolutionDoesNotExists):
            service.grade_resolution(0, {})

    @patch("service.Exam.ExamService.get_resolutions")
    @patch("service.Exam.ExamService._check_resolution_exam")
    def test_grade_resolution_successfully(
        self, check_existance_mock, get_resolutions_mock
    ):
        check_existance_mock.return_value = None
        get_resolutions_mock.return_value = None
        mock_validator = Mock(spec=ExamValidator)
        attrs_validator = {
            "is_grader.return_value": True,
            "notify_course.return_value": None,
        }
        mock_validator.configure_mock(**attrs_validator)
        mock_db = Mock(spec=MongoDB)
        attrs_db = {"grade_exam.return_value": None}
        mock_db.configure_mock(**attrs_db)
        service = ExamService(Mock(), mock_validator)
        result = service.grade_resolution(0, {})
        self.assertIsNone(result)


class TestGetExam(unittest.TestCase):
    def test_get_nonexistent_exam(self):
        mock_validator = Mock(spec=ExamValidator)
        attrs_validator = {
            "is_student.return_value": True,
            "is_course_creator.return_value": True,
        }
        mock_validator.configure_mock(**attrs_validator)
        mock_db = Mock(spec=MongoDB)
        attrs_db = {"get_exam.return_value": None}
        mock_db.configure_mock(**attrs_db)
        service = ExamService(mock_db, mock_validator)
        with self.assertRaises(ExamDoesNotExist):
            service.get_exam(0, "", 8)

    def test_get_exam_not_being_on_the_course(self):
        mock_validator = Mock(spec=ExamValidator)
        attrs = {
            "is_student.return_value": False,
            "is_course_creator.return_value": False,
        }
        mock_validator.configure_mock(**attrs)
        service = ExamService(Mock(), mock_validator)
        with self.assertRaises(InvalidUserAction):
            service.get_exam(0, "", 8)


class TestCompleteExam(unittest.TestCase):
    @patch("service.Exam.ExamService._check_published_exam_existance")
    def test_complete_nonexistent_exam(self, check_existance_mock):
        check_existance_mock.side_effect = ExamDoesNotExist
        service = ExamService(Mock(), Mock())
        with self.assertRaises(ExamDoesNotExist):
            service.complete_exam(0, {})

    @patch("service.Exam.ExamService._check_published_exam_existance")
    def test_complete_exam_not_being_student(self, check_existance_mock):
        check_existance_mock.return_value = None
        mock_validator = Mock(spec=ExamValidator)
        attrs = {"is_student.return_value": False}
        mock_validator.configure_mock(**attrs)
        service = ExamService(Mock(), mock_validator)
        with self.assertRaises(InvalidUserAction):
            service.complete_exam(0, {})

    @patch("service.Exam.ExamService._check_published_exam_existance")
    def test_complete_exam_already_done(self, check_existance_mock):
        check_existance_mock.return_value = None
        mock_validator = Mock(spec=ExamValidator)
        attrs_validator = {"is_student.return_value": True}
        mock_validator.configure_mock(**attrs_validator)
        mock_validator.configure_mock(**attrs_validator)
        mock_db = Mock(spec=MongoDB)
        attrs_db = {"get_resolution.return_value": ["hola"]}
        mock_db.configure_mock(**attrs_db)
        service = ExamService(mock_db, mock_validator)
        with self.assertRaises(ExamAlreadyResolvedException):
            service.complete_exam(0, {})

    @patch("service.Exam.ExamService._check_published_exam_existance")
    def test_complete_exam_successfully(self, check_existance_mock):
        check_existance_mock.return_value = None
        mock_validator = Mock(spec=ExamValidator)
        attrs_validator = {"is_student.return_value": True}
        mock_validator.configure_mock(**attrs_validator)
        mock_validator.configure_mock(**attrs_validator)
        mock_db = Mock(spec=MongoDB)
        attrs_db = {
            "get_resolution.return_value": None,
            "add_resolution.return_value": None,
        }
        mock_db.configure_mock(**attrs_db)
        service = ExamService(mock_db, mock_validator)
        result = service.complete_exam(5, {})
        self.assertIsNone(result)
