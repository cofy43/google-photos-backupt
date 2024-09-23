make run:
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt
	msgfmt locales/en/LC_MESSAGES/messages.po -o locales/en/LC_MESSAGES/messages.mo 
	msgfmt locales/es/LC_MESSAGES/messages.po -o locales/es/LC_MESSAGES/messages.mo 
	python3 main.py