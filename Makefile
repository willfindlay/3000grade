INSTALL_DIR = /opt/grade3000
PATH_LINK = /usr/bin/grade3000

.phony: install

install:
	mkdir -p $(INSTALL_DIR); rm $(PATH_LINK); cp -r ./* $(INSTALL_DIR) && ln -s $(INSTALL_DIR)/main.py $(PATH_LINK)
