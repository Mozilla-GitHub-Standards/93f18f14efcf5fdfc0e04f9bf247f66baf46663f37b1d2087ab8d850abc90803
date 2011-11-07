from django.test import TestCase

from projects.models import Project
from challenges.models import Challenge, Submission, Phase


class EntriesToLive(TestCase):
    
    def setUp(self):
        self.project = Project.objects.create(
            name=u'A project for a test',
            allow_participation=True
        )
        self.challenge = Challenge.objects.create(
            title=u'Testing my submissions',
            end_date=u'2020-11-30 12:23:28',
            project=self.project,
            moderate=True
        )
        self.phase = Phase.objects.create(
            name=u'Phase 1', challenge=self.challenge, order=1
        )
        self.submission = Submission.objects.create(
            title=u'A submission to test',
            description=u'<h3>Testing bleach</h3>',
            is_live=True,
            phase=self.phase
        )

    def test_entry_hidden(self):
        """
        The user wants the entry to go live but it needs moderating first
        """
        self.assertEqual(self.submission.is_live, False)
    
    def test_phase_unicode(self):
        """Test the string representation of a phase."""
        self.assertEqual(unicode(self.phase),
                         u'Phase 1 (Testing my submissions)')
    
    def test_bleach_clearning(self):
        """
        Check that we're stripping out bad content - <h3> isn't in our 
        allowed list
        """
        self.assertEqual(self.submission.description_html,
                         '&lt;h3&gt;Testing bleach&lt;/h3&gt;')