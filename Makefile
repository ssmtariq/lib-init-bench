.PHONY: setup build-all clean $(wildcard deploy-*) $(wildcard invoke-*)

APPS := dnavisualizer csvvalidator versionreporter logformatter \
        statsgen texthasher jsonvalidator textanalyzer \
        jsontransform numprocessor

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements-dev.txt

build-all:
	@for app in $(APPS); do \
		echo "Building $$app..."; \
		cd applications/$$app && sam build; \
	done

deploy-%:
	@app=$*; \
	cd applications/$$app && ./deploy.sh

invoke-%:
	@app=$*; \
	cd applications/$$app && ./invoke.sh

clean:
	find . -name '.aws-sam' -type d -exec rm -rf {} +
	find . -name '__pycache__' -type d -exec rm -rf {} +
	find . -name '.pytest_cache' -type d -exec rm -rf {} +
	find . -name '*.pyc' -delete