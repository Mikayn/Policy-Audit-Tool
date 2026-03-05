import unittest
import builtins
import main



# Ensures missing policies.json returns an empty dictionary without crashing.
def test_load_policies_missing():
    original_open = builtins.open
    builtins.open = lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError)

    try:
        result = main.load_policies()
        assert result == {}
    finally:
        builtins.open = original_open

# Checks that an admin SIS policy is allowed.
def test_sis_admin_allowed():
    main.policy_schemas = {
        "SIS": {
            "vars": {
                "role": "String",
                "action": "String",
                "owner": "Bool"
            }
        }
    }

    policy = {
        "type": "SIS",
        "role": "admin",
        "action": "delete",
        "owner": False
    }

    assert main.evaluate_policy(policy) is True

# Ensures conflicting exam permissions are denied.
def test_exam_conflict_denied():
    main.policy_schemas = {
        "Exam": {
            "vars": {
                "create": "Bool",
                "grade": "Bool",
                "invigilate": "Bool"
            }
        }
    }

    policy = {
        "type": "Exam",
        "create": True,
        "grade": True,
        "invigilate": True
    }

    assert main.evaluate_policy(policy) is False


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.FunctionTestCase(test_load_policies_missing))
    suite.addTest(unittest.FunctionTestCase(test_sis_admin_allowed))
    suite.addTest(unittest.FunctionTestCase(test_exam_conflict_denied))

    unittest.TextTestRunner(verbosity=2).run(suite)