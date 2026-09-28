PY   ?= python3
KEYS := $(wildcard */*.scad)

.PHONY: all validate drawings clean
all: validate drawings

validate:
	@for k in $(KEYS); do $(PY) tools/build_and_validate.py $$k | tee $$(dirname $$k)/VALIDATION.txt; done

drawings:
	@for k in $(KEYS); do $(PY) tools/make_drawing.py $$k; done

clean:
	rm -f */*._design.off */*._print.off
