OS = $(shell uname)
ifeq ($(OS),Linux)
	CLIP = xclip -sel clip
	PYTHON = python3
else
	CLIP = clip
	PYTHON = python
endif

MAKE = make -s

first: sv_documenter

sv_documenter: clean
	@mkdir -p ___temp
	@$(PYTHON) sv_documenter.py ../../rtl/rv_g_regfile.sv ___temp/

sv_lister: clean
	@$(PYTHON) sv_lister.py ../../rtl/rv_g_regfile.sv

clean:
	@rm -rf $(shell cat .gitignore | sed "s/\n//g")
	@git restore README.md
