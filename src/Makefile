COMPILE_CMD = python3 -m py_compile
TEST_CMD = python3 -m doctest
CHECKSTYLE_CMD = flake8

all: compile test checkstyle

compile:
	$(COMPILE_CMD) *.py
	$(COMPILE_CMD) modules/*.py

test:
	$(TEST_CMD) *.py
	$(TEST_CMD) modules/*.py

checkstyle:
	$(CHECKSTYLE_CMD) *.py
	$(CHECKSTYLE_CMD) modules/*.py

clean:
	rm -f *.pyc
	rm -rf __pycache__
	rm -f modules/*.pyc
	rm -rf modules/__pycache__
