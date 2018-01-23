import cgi, cgitb, os, sys, codecs

cgitb.enable()
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())
import st39.main


#	добавить импорт своего модуля по шаблону
#	import st<номер по журналу>.main


MENU = [
        ["[39] Иванов В.О", st39.main.main],
	]


def menu(selfurl):
	print ("Content-type: text/html; charset=utf-8\n\n")
	print ('<pre>------------------------------');
	for i, item in enumerate(MENU):
		print('<a href="{0}?student={1}">{2}</a>'.format(selfurl, i+1, item[0]))
	print ("------------------------------</pre>");


def main():
	q = cgi.FieldStorage()
	selfurl = os.environ['SCRIPT_NAME']
	st = int(q.getvalue('student', 0))
	if st > 0 and st <= len(MENU):
		MENU[st-1][1](q, selfurl)
	else:
		menu(selfurl)

main()
