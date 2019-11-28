.EXPORT_ALL_VARIABLES:

PROJECT_NAME=$(shell awk -F '=' '{if (! ($$0 ~ /^;/) && $$0 ~ /^name/) print $$2}' METADATA | tr -d ' ')
VERSION=$(shell awk -F '=' '{if (! ($$0 ~ /^;/) && $$0 ~ /^version/) print $$2}' METADATA | tr -d ' ')
COMPOSE_ENVIRONMENT=$(or $(COMPOSE_ENV),override)
COMPOSE_COMMAND=docker-compose -f docker-compose.yml -f docker-compose.${COMPOSE_ENVIRONMENT}.yml ${DEBUG:+--verbose}

REPORTS_DIR=reports
REPORTS_JUNIT=${REPORTS_DIR}/junit.xml
REPORTS_COVERAGE=${REPORTS_DIR}/coverage.xml

default:
	@echo ""
	@echo "Targets:"
	@echo ""
	@echo "  params                 Print parameters"
	@echo "  compose-build          Build image"
	@echo ""

checkTest:
	@if [ "${COMPOSE_ENVIRONMENT}" != "test" ]; then \
		echo "Not test environment. Exiting"; \
		return 1; \
	fi

params:
	@echo "User: $(whoami)"
	@echo "Project name: ${PROJECT_NAME}"
	@echo "Version: ${VERSION}"
	@echo "Compose environment: ${COMPOSE_ENVIRONMENT}"

compose-ps:
	@${COMPOSE_COMMAND} ps

compose-build-cached:
	@${COMPOSE_COMMAND} build disam-api

compose-build:
	@${COMPOSE_COMMAND} build --no-cache disam-api

compose-prepare: checkTest
	@${COMPOSE_COMMAND} run --rm disam-dep uname -a

compose-logs:
	@${COMPOSE_COMMAND} logs --tail=20 disam-api

compose-test-python: compose-test-dev-requirements
	@${COMPOSE_COMMAND} exec -T disam-api ./test.sh --cov --junitxml ${REPORTS_JUNIT} --cov-report xml:${REPORTS_COVERAGE}

compose-prepare-reports:
	@${COMPOSE_COMMAND} exec -T disam-api mkdir -p reports
	@${COMPOSE_COMMAND} exec -T disam-api chmod 777 reports

compose-up:
	@${COMPOSE_COMMAND} up -d disam-api

compose-down:
	@${COMPOSE_COMMAND} down -v --rmi local --remove-orphans

compose-test-dev-requirements:
	@${COMPOSE_COMMAND} exec -T disam-api pip install -r requirements_dev.txt

compose-test: compose-test-dev-requirements
	@${COMPOSE_COMMAND} exec -T disam-api ./test.sh

compose-test-full: compose-test-dev-requirements
	@${COMPOSE_COMMAND} exec -T disam-api pip install -r requirements_dev.txt
	@${COMPOSE_COMMAND} exec -T disam-api ./test.sh --cov --pylint

clean-image:
	rm -rfv images

clean-reports:
	rm -rfv ${REPORTS_DIR}
