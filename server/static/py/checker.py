from browser import document as doc, window, alert
import io
import sys
import traceback


def type_name(obj):
    t = type(obj)

    module = t.__module__
    if module == 'builtins':
        if hasattr(t, '__qualname__'):
            return t.__qualname__
        else: # http://bugs.python.org/issue13577
            return t.__name__ # __qualname__ is not present on builtin methods and functions on Python <= 3.2

    return t.__module__ + '.' + t.__qualname__


def parse_exception(exc):
    exception = {}

    if isinstance(exc[1], SyntaxError):
        exception['line'] = exc[1].args[1][1]
        exception['offset'] = exc[1].args[1][2]
    else:
        traceback = exc[2]
        while traceback is not None: # let's walk up to the user code frame
            if traceback.tb_frame.f_code.co_filename == '__main__':
                break
            print(traceback.tb_frame.f_code.__dict__)

            traceback = traceback.tb_next

        assert traceback is not None

        if hasattr(traceback, 'tb_lineno'):
            exception['line'] = traceback.tb_lineno

        if hasattr(traceback, 'tb_offset'):
            exception['offset'] = traceback.tb_offset

    exception['exception_type'] = type_name(exc[1])

    if hasattr(exc[1], 'msg'):
        exception['exception_msg'] = exc[1].msg
    elif hasattr(exc[1], 'args') and len(exc[1].args) > 0:
        exception['exception_msg'] = exc[1].args[0]

    exception['exception_str'] = exception['exception_type'] + ': ' + exception['exception_msg']

    return exception


def execute_python(source, input_data):
    orig_stdin = sys.stdin
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr

    sys.stdin = io.StringIO(input_data)
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    parsed_exception = None

    try:
        exec(source, {'__name__': '__main__'})
    except Exception as exc:
        parsed_exception = parse_exception(sys.exc_info())
        traceback.print_exc(file=sys.stderr)
    finally:
        exec_stdout = sys.stdout
        exec_stderr = sys.stderr

        sys.stdin = orig_stdin
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

    res = {
        'stdout': exec_stdout.getvalue(),
        'stderr': exec_stderr.getvalue(),
    }

    if parsed_exception:
        res['exception'] = parsed_exception

    return res


class TestResult:
    def __init__(self, test, status, stderr, user_answer, is_correct):
        self.status = status
        self.stderr = stderr

        self.test_input = test.test_input
        self.correct_answer = test.correct_answer
        self.output = user_answer

        self.is_correct = is_correct


class Test:
    def __init__(self, test_input, correct_answer):
        self.test_input = test_input
        self.correct_answer = correct_answer

    def _tokens_are_equal(self, x, y):
        res = False

        try:
            res = abs(float(x) - float(y)) < 1e-3
        except ValueError:
            res = (x == y)

        return res

    def _compare_sequences_of_tokens(self, seq1, seq2):
        seq1 = [i for i in seq1.split() if i]
        seq2 = [i for i in seq2.split() if i]
        return len(seq1) == len(seq2) and all(self._tokens_are_equal(x, y) for x, y in zip(seq1, seq2))


    def test_code(self, code):
        res = execute_python(code, self.test_input)
        user_answer = res['stdout'].strip()

        is_correct = self._compare_sequences_of_tokens(user_answer, self.correct_answer)

        if res['stderr'] != '':
            result = 'stderr'
        elif is_correct:
            result = 'ok'
        else:
            result = 'wrong_answer'

        return TestResult(self, result, res['stderr'], user_answer, is_correct)


def run_test(user_code, test_input, test_answer):
    test = Test(test_input, test_answer)
    return test.test_code(user_code)


window.run_test = run_test
window.execute_python = execute_python
