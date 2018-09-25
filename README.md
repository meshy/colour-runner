# colour-runner

Colour formatting for `unittest` test output.

## Installation

    pip install colour-runner

### Django

Mix the `ColourRunnerMixin` into your `unittest` test runner (eg: in `project/runner.py`):

    from django.test.runner import DiscoverRunner  # Django 1.6's default
    from colour_runner.django_runner import ColourRunnerMixin

    class MyTestRunner(ColourRunnerMixin, DiscoverRunner):
        pass

Point django at it in `settings.py`:

    TEST_RUNNER = 'project.runner.MyTestRunner'

You can also disable colour runner for an individual test run with Django's `--no-color` flag:

    manage.py test --no-color

### Other Python

Where you would normally use:

* `unittest.TextTestRunner`, use `colour_runner.runner.ColourTextTestRunner`.
* `unittest.TextTestResult`, use `colour_runner.result.ColourTextTestResult`.
