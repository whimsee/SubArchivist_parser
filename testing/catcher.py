mode = "default"
import catcher_tests
# from catcher_tests import defaults

if any(s in mode for s in catcher_tests.defaults):
    print("found")
else:
    print("not found")