import unittest

from . import assistant
from . import director
from . import executive


# initialize loader and suite of tests
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# load the tests into the suite
suite.addTests(loader.loadTestsFromModule(assistant))
# suite.addTests(loader.loadTestsFromModule(director))
# suite.addTests(loader.loadTestsFromModule(executive))

# initialize tests runner
runner = unittest.TextTestRunner(verbosity=1)
# pass the suite (built with some test cases) to the runner
result = runner.run(suite)
