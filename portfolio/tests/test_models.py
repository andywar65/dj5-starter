from datetime import datetime

from django.test import TestCase, override_settings

from portfolio.models import Project


@override_settings(USE_I18N=False)
class ProjectModelTest(TestCase):
    """Testing all methods that don't need SimpleUploadedFile"""

    @classmethod
    def setUpTestData(cls):
        Project.objects.create(
            title="Project",
            intro="Foo",
            body="Bar",
            site="Somewhere",
            category="ALT",
            type="ALT",
            status="ALT",
            cost="ALT",
        )
        Project.objects.create(date=datetime.strptime("2020-05-09", "%Y-%m-%d"))
        # stat = ProjectStation.objects.create(prog=prog, title='Station')
        # StationImage.objects.create(stat_id=stat.id,
        # image='uploads/images/galleries/image.jpg')

    def test_project_str_method(self):
        prog = Project.objects.get(slug="project")
        self.assertEquals(prog.__str__(), "Project")

    def test_project_str_method_no_title(self):
        prog = Project.objects.get(date="2020-05-09")
        self.assertEquals(prog.__str__(), "Project-09-05-20")

    def test_project_get_full_path(self):
        prog = Project.objects.get(slug="project")
        self.assertEquals(prog.get_full_path(), "/projects/project/")
