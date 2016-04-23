install:
	(\
	virtualenv venv --relocatable;\
	test -d /var/toughwlan/data || mkdir -p /var/toughwlan/data;\
	rm -f /etc/toughwlan.conf && cp etc/toughwlan.conf /etc/toughwlan.conf;\
	test -f /etc/toughwlan.json || cp etc/toughwlan.json /etc/toughwlan.json;\
	rm -f /etc/init.d/toughwlan && cp etc/toughwlan /etc/init.d/toughwlan;\
	chmod +x /etc/init.d/toughwlan && chkconfig toughwlan on;\
	rm -f /usr/lib/systemd/system/toughwlan.service && cp etc/toughwlan.service /usr/lib/systemd/system/toughwlan.service;\
	chmod 754 /usr/lib/systemd/system/toughwlan.service && systemctl enable toughwlan;\
	systemctl daemon-reload;\
	)

install-deps:
	(\
	yum install -y epel-release;\
	yum install -y wget zip python-devel libffi-devel openssl openssl-devel gcc git;\
	yum install -y czmq czmq-devel python-virtualenv supervisor;\
	yum install -y mysql-devel MySQL-python redis;\
	test -f /usr/local/bin/supervisord || ln -s `which supervisord` /usr/local/bin/supervisord;\
	)

venv:
	(\
	test -d venv || virtualenv venv;\
	venv/bin/pip install -U pip;\
	venv/bin/pip install -U wheel;\
	venv/bin/pip install -U -r requirements.txt;\
	)

upgrade-libs:
	(\
	venv/bin/pip install -U --no-deps https://github.com/talkincode/toughlib/archive/master.zip;\
	venv/bin/pip install -U --no-deps https://github.com/talkincode/txportal/archive/master.zip;\
	)

upgrade-dev:
	git pull --rebase --stat origin release-dev

upgrade:
	git pull --rebase --stat origin release-stable

test:
	sh runtests.sh

initdb:
	python wlanctl initdb -f -c /etc/toughwlan.json

inittest:
	python wlanctl inittest -c /etc/toughwlan.json

clean:
	rm -fr venv

all:install-deps venv upgrade-libs install

.PHONY: all install install-deps upgrade-libs upgrade-dev upgrade test initdb inittest clean