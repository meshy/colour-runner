from .runner import ColourTextTestRunner


class ColourRunnerMixin(object):
    test_runner = ColourTextTestRunner

    def __init__(self, *args, **kwargs):
        self.no_colour = kwargs.get('no_color', False)
        super(ColourRunnerMixin, self).__init__(*args, **kwargs)

    def run_suite(self, suite, **kwargs):
        """This is the version from Django 1.7."""
        return self.test_runner(
            verbosity=self.verbosity,
            failfast=self.failfast,
            no_colour=self.no_colour,
        ).run(suite)
